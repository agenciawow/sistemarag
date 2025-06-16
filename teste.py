#!/usr/bin/env python3
"""Script para testar o sistema RAG"""

import os
from dotenv import load_dotenv

def main():
    print("🧪 Testando Sistema RAG...")
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    print("\n1. 📋 Verificando variáveis de ambiente...")
    required_vars = {
        'VOYAGE_API_KEY': 'Voyage AI (embeddings)',
        'ASTRA_DB_API_ENDPOINT': 'Astra DB (banco vetorial)',
        'ASTRA_DB_APPLICATION_TOKEN': 'Astra DB (autenticação)',
        'R2_ENDPOINT': 'Cloudflare R2 (imagens)',
        'R2_AUTH_TOKEN': 'Cloudflare R2 (autenticação)'
    }
    
    missing = []
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value and value != 'sk-your-openai-key-here':
            print(f"   ✅ {var}: {desc}")
        else:
            print(f"   ❌ {var}: {desc} - AUSENTE")
            missing.append(var)
    
    if missing:
        print(f"\n❌ Configure as variáveis ausentes no arquivo .env")
        return
    
    print("\n2. 🔗 Testando conexões...")
    
    try:
        # Teste Voyage AI
        from sistema_rag.components.embeddings.voyage_embedder import VoyageEmbedder
        embedder = VoyageEmbedder(api_key=os.getenv('VOYAGE_API_KEY'))
        test_embedding = embedder.embed_query("teste")
        print(f"   ✅ Voyage AI: Embedding gerado ({len(test_embedding.embedding)} dimensões)")
    except Exception as e:
        print(f"   ❌ Voyage AI: {e}")
        return
    
    try:
        # Teste Astra DB
        from sistema_rag.components.retrieval import VectorSearcher
        searcher = VectorSearcher()
        test = searcher.test_connection()
        print(f"   {'✅' if test.success else '❌'} Astra DB: {test.message}")
        
        if test.success:
            docs = searcher.list_documents()
            print(f"      📄 Documentos na base: {len(docs)}")
    except Exception as e:
        print(f"   ❌ Astra DB: {e}")
        return
    
    try:
        # Teste Cloudflare R2
        from sistema_rag.components.retrieval import ImageFetcher
        fetcher = ImageFetcher()
        test = fetcher.test_connection()
        print(f"   {'✅' if test.success else '❌'} Cloudflare R2: {test.message}")
    except Exception as e:
        print(f"   ❌ Cloudflare R2: {e}")
    
    print("\n3. 🔍 Testando busca...")
    
    try:
        # Teste de busca
        query = "teste de busca"
        embedding = embedder.embed_query(query)
        results = searcher.search_by_text(query, embedding.embedding, limit=1)
        
        if results.documents:
            doc = results.documents[0]
            print(f"   ✅ Busca funcionando:")
            print(f"      📋 Documento: {doc.document_name}")
            print(f"      📄 Página: {doc.page_number}")
            print(f"      🎯 Similaridade: {doc.similarity:.3f}")
        else:
            print("   ⚠️  Busca funcionando, mas nenhum documento encontrado")
            print("      💡 Execute: python ingestao.py")
    
    except Exception as e:
        print(f"   ❌ Erro na busca: {e}")
    
    print("\n✅ Teste concluído!")
    print("\n📋 Próximos passos:")
    print("   - Para ingestão: python ingestao.py")
    print("   - Para busca: python buscador.py")

if __name__ == "__main__":
    main()