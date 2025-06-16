#!/usr/bin/env python3
"""
Teste simples do sistema RAG
"""
from sistema_rag.search.conversational_rag import ModularConversationalRAG

def test_rag():
    """Teste básico do sistema RAG"""
    print("Inicializando sistema RAG...")
    
    try:
        # Inicializar sistema
        rag = ModularConversationalRAG()
        print("✅ Sistema inicializado com sucesso")
        
        # Teste de query
        query = "Qual é o modelo de negócio da agência?"
        print(f"\n🔍 Pergunta: {query}")
        
        response = rag.ask(query)
        print(f"\n🤖 Resposta: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_rag()
    exit(0 if success else 1)