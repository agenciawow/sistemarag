#!/usr/bin/env python3
"""
Teste com sessão corrigida - user_id="5678" e session_id="5678"
"""

import logging
from agents.core.operator import agent_operator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_fixed_session():
    """Testa a sessão corrigida com user_id vinculado"""
    print("🔧 Testando sessão corrigida com user_id vinculado")
    print("=" * 55)
    
    try:
        # Obter agente
        agent = agent_operator.get_agent("rag-search")
        
        user_id = "5678"
        session_id = "5678"
        
        print(f"👤 User ID: {user_id}")
        print(f"💬 Session ID: {session_id}")
        print(f"🔧 CORREÇÃO: Agora a sessão será criada com add_session(session_id, user_id)")
        
        # Mensagem de teste
        message = "Olá! Meu nome é João Pedro e sou desenvolvedor. Vocês fazem entrega?"
        
        print(f"\n📤 Enviando mensagem:")
        print(f"   {message}")
        
        # Executar agente (deve criar sessão corretamente agora)
        response = agent.ask(message, user_id=user_id, session_id=session_id)
        
        print(f"\n💬 Resposta recebida:")
        print(f"   {response}")
        
        print(f"\n✅ Execução concluída!")
        print(f"🔍 Agora verifique no painel Zep:")
        print(f"   - User ID: {user_id}")
        print(f"   - Session ID: {session_id}")
        print(f"   - A sessão deve estar vinculada ao usuário {user_id}")
        print(f"   - Deve haver 2 mensagens: user + assistant")
        print(f"   - Memória deve conter: João Pedro, desenvolvedor")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fixed_session()
    print(f"\n{'='*55}")
    print(f"Status: {'✅ SUCESSO' if success else '❌ ERRO'}")