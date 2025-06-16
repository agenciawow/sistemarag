#!/usr/bin/env python3
"""Script para testar busca sem interface interativa"""

import os
from dotenv import load_dotenv

def main():
    print("🔍 Sistema de Busca RAG")
    print("=" * 40)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    try:
        # Importar componentes
        from sistema_rag.search.embeddings.voyage_embedder import VoyageEmbedder
        from sistema_rag.search.retrieval import VectorSearcher
        
        print("✅ Sistema carregado!")
        
        # Inicializar componentes
        embedder = VoyageEmbedder(api_key=os.getenv('VOYAGE_API_KEY'))
        searcher = VectorSearcher()
        
        # Testar conexão
        test = searcher.test_connection()
        print(f"🔗 Astra DB: {'✅' if test.success else '❌'}")
        
        # Listar documentos
        docs = searcher.list_documents()
        print(f"📄 Documentos: {len(docs)}")
        for doc in docs:
            print(f"   - {doc['document_name']} (página {doc['page_number']})")
        
        print("\n💡 Digite sua pergunta (ou 'sair' para encerrar)")
        print("   Exemplos: 'hambúrguer de frango', 'sobremesas', 'preços'")
        
        while True:
            try:
                # Receber pergunta do usuário
                pergunta = input("\n🔍 Sua pergunta: ").strip()
                
                if not pergunta:
                    continue
                    
                if pergunta.lower() in ['sair', 'exit', 'quit']:
                    print("👋 Até logo!")
                    break
                
                print(f"🔎 Buscando por: '{pergunta}'")
                
                # Gerar embedding
                embedding = embedder.embed_query(pergunta)
                
                # Buscar
                results = searcher.search_by_text(pergunta, embedding.embedding, limit=3)
                
                if results.documents:
                    print(f"✅ {len(results.documents)} resultados encontrados:")
                    
                    for j, doc in enumerate(results.documents, 1):
                        print(f"\n{j}. 📄 {doc.document_name} - página {doc.page_number}")
                        print(f"   📊 Score: {doc.similarity:.3f}")
                        
                        # Mostrar conteúdo
                        content = doc.content
                        if content.startswith('{"markdown":'):
                            import json
                            try:
                                data = json.loads(content)
                                content = data.get('markdown', content)[:200]
                            except:
                                content = content[:200]
                        else:
                            content = content[:200]
                        
                        print(f"   📝 {content}...")
                        
                        if doc.image_url:
                            print(f"   🖼️  Imagem: {doc.image_url}")
                else:
                    print("❌ Nenhum resultado encontrado")
                    
            except KeyboardInterrupt:
                print("\n👋 Até logo!")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
        
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        print("\n💡 Para busca avançada com IA, use:")
        print("   python -m sistema_rag.search.conversational_rag")

if __name__ == "__main__":
    main()