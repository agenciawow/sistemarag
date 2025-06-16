#!/usr/bin/env python3
"""
Teste com query mais genérica
"""
from sistema_rag.search.conversational_rag import ModularConversationalRAG

def test_rag():
    """Teste com query genérica"""
    print("Inicializando sistema RAG...")
    
    try:
        rag = ModularConversationalRAG()
        print("✅ Sistema inicializado")
        
        # Teste com query genérica
        query = "Quais serviços a agência oferece?"
        print(f"\n🔍 Pergunta: {query}")
        
        response = rag.ask(query)
        print(f"\n🤖 Resposta: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_rag()