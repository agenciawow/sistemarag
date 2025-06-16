#!/usr/bin/env python3
"""Script dedicado para busca - equivale ao antigo buscador.py"""

import os
from dotenv import load_dotenv

def main():
    print("🔍 Iniciando Buscador RAG Modular...")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Verificar se temos as variáveis necessárias
    if not os.getenv('VOYAGE_API_KEY'):
        print("❌ VOYAGE_API_KEY não encontrada no .env")
        return
    
    if not os.getenv('ASTRA_DB_API_ENDPOINT'):
        print("❌ ASTRA_DB_API_ENDPOINT não encontrada no .env")
        return
    
    try:
        # Importar e usar o sistema de busca
        from sistema_rag.components.embeddings.voyage_embedder import VoyageEmbedder
        from sistema_rag.components.retrieval import VectorSearcher
        
        print("✅ Sistema RAG carregado com sucesso!")
        print("=" * 50)
        
        # Testar conexões
        searcher = VectorSearcher()
        test = searcher.test_connection()
        print(f"🔗 Conexão Astra DB: {'✅' if test.success else '❌'}")
        
        if not test.success:
            print(f"❌ Erro: {test.message}")
            return
        
        # Listar documentos disponíveis
        docs = searcher.list_documents()
        print(f"📄 Documentos na base: {len(docs)}")
        
        if not docs:
            print("⚠️  Nenhum documento encontrado. Execute primeiro: python ingestao.py")
            return
        
        for doc in docs:
            print(f"   - {doc['document_name']} (página {doc['page_number']})")
        
        print("\n" + "=" * 50)
        print("💬 Faça suas perguntas (digite 'sair' para encerrar):")
        
        # Interface de busca simples
        embedder = VoyageEmbedder(api_key=os.getenv('VOYAGE_API_KEY'))
        
        while True:
            try:
                pergunta = input("\n🙋 Você: ").strip()
                
                if pergunta.lower() in ['sair', 'exit', 'quit']:
                    print("👋 Até logo!")
                    break
                
                if not pergunta:
                    continue
                
                print("🔍 Buscando...")
                
                # Gerar embedding
                query_embedding = embedder.embed_query(pergunta)
                
                # Buscar documentos similares
                results = searcher.search_by_text(pergunta, query_embedding.embedding, limit=2)
                
                if results.documents:
                    print(f"\n🤖 Encontrei {len(results.documents)} resultados relevantes:")
                    
                    for i, doc in enumerate(results.documents):
                        print(f"\n📄 Resultado {i+1}:")
                        print(f"   📋 Documento: {doc.document_name} (página {doc.page_number})")
                        print(f"   🎯 Similaridade: {doc.similarity:.3f}")
                        
                        # Mostrar um trecho do conteúdo
                        content = doc.content
                        if content.startswith('{"markdown":'):
                            # Extrair markdown do JSON
                            import json
                            try:
                                data = json.loads(content)
                                content = data.get('markdown', content)
                            except:
                                pass
                        
                        # Limitar o conteúdo mostrado
                        if len(content) > 200:
                            content = content[:200] + "..."
                        
                        print(f"   📝 Conteúdo: {content}")
                        
                        if doc.image_url:
                            print(f"   🖼️  Imagem: {doc.image_url}")
                else:
                    print("❌ Nenhum resultado encontrado para sua pergunta.")
                
            except KeyboardInterrupt:
                print("\n👋 Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
    
    except Exception as e:
        print(f"❌ Erro ao inicializar o sistema: {e}")
        print("💡 Dica: Verifique se o arquivo .env está configurado corretamente")

if __name__ == "__main__":
    main()