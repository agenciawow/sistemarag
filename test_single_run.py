#!/usr/bin/env python3
"""
Teste único com user_id="1234" e session_id="1234" para verificar no painel Zep
"""

import logging
from agents.core.operator import agent_operator

# Configurar logging para ver detalhes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def single_run_test():
    """Executa uma única interação para verificar no painel Zep"""
    print("🚀 Executando teste único para painel Zep")
    print("=" * 50)
    
    try:
        # Obter agente
        agent = agent_operator.get_agent("rag-search")
        
        user_id = "1234"
        session_id = "1234"
        
        print(f"👤 User ID: {user_id}")
        print(f"💬 Session ID: {session_id}")
        print(f"🔗 Verifique no painel Zep: https://cloud.getzep.com")
        
        # Mensagem de teste
        message = "Olá! Meu nome é Maria Silva e sou gerente de marketing. Quais hambúrgueres vocês têm disponíveis?"
        
        print(f"\n📤 Enviando mensagem:")
        print(f"   {message}")
        
        # Executar agente
        response = agent.ask(message, user_id=user_id, session_id=session_id)
        
        print(f"\n💬 Resposta recebida:")
        print(f"   {response}")
        
        print(f"\n✅ Execução concluída!")
        print(f"🔍 Agora verifique no painel Zep:")
        print(f"   - User ID: {user_id}")
        print(f"   - Session ID: {session_id}")
        print(f"   - Deve haver 2 mensagens: user + assistant")
        print(f"   - Memória deve conter: Maria Silva, gerente de marketing")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = single_run_test()
    print(f"\n{'='*50}")
    print(f"Status: {'✅ SUCESSO' if success else '❌ ERRO'}")