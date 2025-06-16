#!/usr/bin/env python3
"""Script para testar busca sem interface interativa"""

import os
from dotenv import load_dotenv

def main():
    print("🔍 Testando Sistema de Busca...")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    try:
        # Importar componentes
        from sistema_rag.components.embeddings.voyage_embedder import VoyageEmbedder
        from sistema_rag.components.retrieval import VectorSearcher
        
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
        
        # Perguntas de teste sobre o cardápio
        perguntas = [
            "hambúrguer de frango",
            "sobremesas",
            "preços",
            "bebidas",
            "American Burger"
        ]
        
        print(f"\n🧪 Testando {len(perguntas)} perguntas:")
        
        for i, pergunta in enumerate(perguntas, 1):
            print(f"\n{i}. 🔍 '{pergunta}'")
            
            try:
                # Gerar embedding
                embedding = embedder.embed_query(pergunta)
                
                # Buscar
                results = searcher.search_by_text(pergunta, embedding.embedding, limit=2)
                
                if results.documents:
                    print(f"   ✅ {len(results.documents)} resultados:")
                    
                    for j, doc in enumerate(results.documents):
                        print(f"      {j+1}. {doc.document_name} p.{doc.page_number} (score: {doc.similarity:.3f})")
                        
                        # Mostrar um trecho
                        content = doc.content
                        if content.startswith('{"markdown":'):
                            import json
                            try:
                                data = json.loads(content)
                                content = data.get('markdown', content)[:150]
                            except:
                                content = content[:150]
                        else:
                            content = content[:150]
                        
                        print(f"         📝 {content}...")
                        
                        if doc.image_url:
                            print(f"         🖼️  {doc.image_url}")
                else:
                    print("   ❌ Nenhum resultado")
                    
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        
        print(f"\n✅ Teste de busca concluído!")
        print(f"\n💡 Para busca interativa, use: python buscador.py")
        print(f"   (Funciona melhor em terminal local)")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()