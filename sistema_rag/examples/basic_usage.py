"""
Exemplo básico de uso do Sistema RAG Multimodal

Este exemplo demonstra como usar os componentes principais para:
1. Baixar documento do Google Drive
2. Processar com LlamaParse
3. Gerar chunks multimodais
4. Criar embeddings
5. Armazenar no Cloudflare R2
"""
import os
import asyncio
from typing import List

# Importar componentes do sistema
from ..components.ingestion.google_drive_downloader import GoogleDriveDownloader
from ..components.ingestion.file_selector import FileSelector
from ..components.processing.llamaparse_processor import LlamaParseProcessor
from ..components.processing.multimodal_merger import MultimodalMerger
from ..components.embeddings.voyage_embedder import VoyageEmbedder
from ..components.storage.cloudflare_r2 import CloudflareR2Uploader
from ..components.storage.astra_db import AstraDBInserter
from ..config.settings import settings


async def basic_rag_pipeline():
    """
    Pipeline básico do sistema RAG
    """
    print("🚀 Iniciando Sistema RAG Multimodal")
    
    # =====================================
    # 1. CONFIGURAÇÃO DAS APIs
    # =====================================
    
    # Verificar se as chaves estão configuradas
    required_keys = [
        'LLAMA_CLOUD_API_KEY',
        'VOYAGE_API_KEY', 
        'R2_ENDPOINT',
        'R2_AUTH_TOKEN',
        'ASTRA_DB_APPLICATION_TOKEN',
        'ASTRA_DB_API_ENDPOINT',
        'ASTRA_DB_KEYSPACE',
        'ASTRA_DB_COLLECTION',
        'GOOGLE_DRIVE_URL'
    ]
    
    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Chaves de API ausentes: {', '.join(missing_keys)}")
        print("Por favor, configure as variáveis de ambiente ou .env")
        return
    
    print("✅ Chaves de API configuradas")
    
    # =====================================
    # 2. DOWNLOAD DO GOOGLE DRIVE
    # =====================================
    
    print("\n📥 Baixando documento do Google Drive...")
    
    # URL configurada via variável de ambiente
    google_drive_url = os.getenv('GOOGLE_DRIVE_URL')
    urls = [google_drive_url]
    
    print(f"📄 URL configurada: {google_drive_url}")
    
    downloader = GoogleDriveDownloader(
        timeout=30,
        max_file_size_mb=50
    )
    
    try:
        downloaded_files = downloader.download_files(urls)
        print(f"✅ Baixados {len(downloaded_files)} arquivos")
        
        # Mostrar resumo dos downloads
        for file_info in downloaded_files:
            if file_info.download_success:
                print(f"  📄 {file_info.filename} ({file_info.size_mb} MB)")
            else:
                print(f"  ❌ Erro: {file_info.error_message}")
        
    except Exception as e:
        print(f"❌ Erro no download: {e}")
        return
    
    # =====================================
    # 3. SELEÇÃO DE ARQUIVO
    # =====================================
    
    print("\n🔎 Selecionando arquivo...")
    
    selector = FileSelector()
    
    try:
        # Selecionar primeiro arquivo válido
        selected_file = selector.select_file(downloaded_files, file_index=0)
        print(f"✅ Selecionado: {selected_file.filename}")
        print(f"  Método: {selected_file.selection_info.selection_method}")
        print(f"  De: {selected_file.selection_info.valid_files_count} arquivos válidos")
        
    except Exception as e:
        print(f"❌ Erro na seleção: {e}")
        return
    
    # =====================================
    # 4. PROCESSAMENTO COM LLAMAPARSE
    # =====================================
    
    print("\n🖼️ Processando com LlamaParse...")
    
    processor = LlamaParseProcessor(
        api_key=os.getenv('LLAMA_CLOUD_API_KEY'),
        take_screenshot=True,
        parse_mode="parse_page_with_agent"  # Modo Premium que suporta screenshots
    )
    
    try:
        # Processar documento
        parsed_doc = processor.process_document(selected_file)
        
        if parsed_doc.success:
            print(f"✅ Documento processado")
            print(f"  Job ID: {parsed_doc.job_id}")
            print(f"  Caracteres: {parsed_doc.char_count}")
            print(f"  Screenshots: {parsed_doc.screenshots_count}")
        else:
            print(f"❌ Erro no processamento: {parsed_doc.error_message}")
            return
        
        # Obter screenshots
        screenshots = processor.get_screenshots(parsed_doc.job_id)
        print(f"📸 Obtidas {screenshots.total_screenshots} screenshots")
        
        if screenshots.total_screenshots == 0:
            print("⚠️  Nenhuma screenshot encontrada - pode ser um PDF simples sem elementos visuais")
        
    except Exception as e:
        print(f"❌ Erro no LlamaParse: {e}")
        return
    
    # =====================================
    # 5. MERGE MULTIMODAL
    # =====================================
    
    print("\n🧩 Criando chunks multimodais...")
    
    merger = MultimodalMerger(
        merge_strategy="page_based",
        max_chunk_size=1500,
        include_metadata=True
    )
    
    try:
        chunk_collection = merger.merge_content(
            parsed_doc, 
            screenshots, 
            document_name="exemplo_documento"
        )
        
        print(f"✅ Criados {chunk_collection.total_chunks} chunks")
        print(f"  Multimodais (texto+imagem): {chunk_collection.multimodal_chunks}")
        print(f"  Texto apenas (sem screenshots): {chunk_collection.text_only_chunks}")
        
        if chunk_collection.multimodal_chunks == 0 and screenshots.total_screenshots == 0:
            print("⚠️  Todos os chunks são text-only porque não há screenshots disponíveis")
            print("💡 Para embeddings verdadeiramente multimodais, screenshots são necessárias")
        
    except Exception as e:
        print(f"❌ Erro no merge: {e}")
        return
    
    # =====================================
    # 6. GERAÇÃO DE EMBEDDINGS
    # =====================================
    
    print("\n🧬 Gerando embeddings...")
    
    embedder = VoyageEmbedder(
        api_key=os.getenv('VOYAGE_API_KEY'),
        batch_size=5  # Lotes menores para exemplo
    )
    
    try:
        embedded_chunks = embedder.embed_chunks(chunk_collection)
        print(f"✅ Embeddings gerados para {len(embedded_chunks)} chunks")
        
        # Mostrar estatísticas
        if embedded_chunks:
            first_embedding = embedded_chunks[0].embedding
            print(f"  Dimensão: {len(first_embedding)}")
            print(f"  Modelo: {embedded_chunks[0].model}")
        
    except Exception as e:
        print(f"❌ Erro nos embeddings: {e}")
        return
    
    # =====================================
    # 7. UPLOAD PARA CLOUDFLARE R2
    # =====================================
    
    print("\n☁️ Fazendo upload para Cloudflare R2...")
    
    uploader = CloudflareR2Uploader(
        r2_endpoint=os.getenv('R2_ENDPOINT'),
        auth_token=os.getenv('R2_AUTH_TOKEN'),
        replace_existing=True
    )
    
    try:
        # Testar conexão primeiro
        connection_test = uploader.test_connection()
        if not connection_test["success"]:
            print(f"❌ Erro na conexão R2: {connection_test['message']}")
            return
        
        # Fazer upload das imagens
        upload_result = uploader.upload_chunk_images(embedded_chunks)
        
        summary = upload_result["summary"]
        print(f"✅ Upload concluído")
        print(f"  Imagens encontradas: {summary['total_images_found']}")
        print(f"  Imagens enviadas: {summary['total_images_uploaded']}")
        print(f"  Taxa de sucesso: {summary['success_rate']}")
        
        # Atualizar chunks com URLs
        final_chunks = upload_result["documents"]
        
    except Exception as e:
        print(f"❌ Erro no upload R2: {e}")
        return
    
    # =====================================
    # 8. INSERÇÃO NO ASTRA DB
    # =====================================
    
    print("\n🗄️ Inserindo no Astra DB...")
    
    astra_inserter = AstraDBInserter(
        api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT'),
        auth_token=os.getenv('ASTRA_DB_APPLICATION_TOKEN'),
        keyspace=os.getenv('ASTRA_DB_KEYSPACE'),
        collection_name=os.getenv('ASTRA_DB_COLLECTION'),
        replace_existing=True,
        batch_size=20
    )
    
    try:
        # Testar conexão primeiro
        connection_test = astra_inserter.test_connection()
        if not connection_test["success"]:
            print(f"❌ Erro na conexão Astra DB: {connection_test['message']}")
            return
        
        # Inserir documentos
        astra_result = astra_inserter.insert_chunks(final_chunks)
        
        insertion_summary = astra_result.get("summary", {})
        print(f"✅ Inserção no Astra DB concluída")
        print(f"  Documentos inseridos: {insertion_summary.get('total_documents_inserted', 0)}")
        print(f"  Taxa de sucesso: {insertion_summary.get('success_rate', '0%')}")
        print(f"  Tamanho total: {insertion_summary.get('total_data_size_kb', 0)} KB")
        
        # Estatísticas da coleção
        stats = astra_inserter.get_collection_stats()
        print(f"  Total na coleção: {stats.get('total_documents', 0)} documentos")
        
    except Exception as e:
        print(f"❌ Erro no Astra DB: {e}")
        return
    
    # =====================================
    # 9. RESULTADO FINAL
    # =====================================
    
    print(f"\n🎉 Pipeline completo de ingestão concluído com sucesso!")
    print(f"  📊 {len(final_chunks)} chunks processados")
    print(f"  🧬 Embeddings de {len(final_chunks[0].embedding)} dimensões")
    print(f"  ☁️ Imagens armazenadas no R2")
    print(f"  🗄️ Documentos indexados no Astra DB")
    
    # Mostrar exemplo de chunk final
    if final_chunks:
        example_chunk = final_chunks[0]
        print(f"\n📄 Exemplo de chunk processado:")
        print(f"  ID: {example_chunk.chunk_id}")
        print(f"  Conteúdo: {example_chunk.content[:100]}...")
        print(f"  Página: {example_chunk.page_number}")
        print(f"  Tem imagem: {bool(getattr(example_chunk, 'image_url', None))}")
        if hasattr(example_chunk, 'image_url') and example_chunk.image_url:
            print(f"  URL da imagem: {example_chunk.image_url}")
    
    return final_chunks


def quick_test():
    """
    Teste rápido dos componentes
    """
    print("🧪 Teste rápido dos componentes")
    
    # Teste Google Drive Downloader
    print("\n1. Testando Google Drive Downloader...")
    downloader = GoogleDriveDownloader()
    test_url = os.getenv('GOOGLE_DRIVE_URL', "https://drive.google.com/file/d/1EDArLh4yTTf43UP9ilmeKN02Yyl6rVyQ/view")
    validation = downloader.validate_urls([test_url])
    print(f"   URLs válidas: {validation['valid_count']}")
    if validation['valid_count'] > 0:
        print(f"   File ID: {validation['valid_urls'][0]['file_id']}")
    
    # Teste Voyage API (se chave disponível)
    if os.getenv('VOYAGE_API_KEY'):
        print("\n2. Testando Voyage API...")
        embedder = VoyageEmbedder(api_key=os.getenv('VOYAGE_API_KEY'))
        connection_test = embedder.validate_api_connection()
        print(f"   Status: {connection_test['status']}")
        if connection_test['status'] == 'success':
            print(f"   Dimensões: {connection_test['test_embedding_dimension']}")
    
    # Teste Cloudflare R2 (se configurado)
    if os.getenv('R2_ENDPOINT') and os.getenv('R2_AUTH_TOKEN'):
        print("\n3. Testando Cloudflare R2...")
        uploader = CloudflareR2Uploader(
            r2_endpoint=os.getenv('R2_ENDPOINT'),
            auth_token=os.getenv('R2_AUTH_TOKEN')
        )
        connection_test = uploader.test_connection()
        print(f"   Status: {'✅' if connection_test['success'] else '❌'}")
    
    # Teste Astra DB (se configurado)
    if os.getenv('ASTRA_DB_API_ENDPOINT') and os.getenv('ASTRA_DB_APPLICATION_TOKEN'):
        print("\n4. Testando Astra DB...")
        inserter = AstraDBInserter(
            api_endpoint=os.getenv('ASTRA_DB_API_ENDPOINT'),
            auth_token=os.getenv('ASTRA_DB_APPLICATION_TOKEN'),
            keyspace=os.getenv('ASTRA_DB_KEYSPACE', 'default_keyspace'),
            collection_name=os.getenv('ASTRA_DB_COLLECTION', 'test_collection')
        )
        connection_test = inserter.test_connection()
        print(f"   Status: {'✅' if connection_test['success'] else '❌'}")
        if connection_test['success']:
            stats = inserter.get_collection_stats()
            print(f"   Documentos: {stats['total_documents']}")
    
    print("\n✅ Testes concluídos")


if __name__ == "__main__":
    # Carregar variáveis de ambiente
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv não instalado. Configure as variáveis manualmente.")
    
    # Executar teste rápido ou pipeline completo
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        quick_test()
    else:
        print("Para executar o pipeline completo:")
        print("  python -m sistema_rag.examples.basic_usage")
        print("\nPara teste rápido:")
        print("  python -m sistema_rag.examples.basic_usage test")
        
        # asyncio.run(basic_rag_pipeline())