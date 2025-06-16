#!/usr/bin/env python3
"""
Teste de criação correta de sessão - user_id="9999" e session_id="9999"
"""

import logging
from agents.core.operator import agent_operator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_session_creation():
    """Testa a criação correta de sessão com user_id vinculado"""
    print("🎯 Testando criação correta de sessão com user_id vinculado")
    print("=" * 60)
    
    try:
        # Obter agente
        agent = agent_operator.get_agent("rag-search")
        
        user_id = "9999"
        session_id = "9999"
        
        print(f"👤 User ID: {user_id}")
        print(f"💬 Session ID: {session_id}")
        print(f"🎯 OBJETIVO: Criar sessão EXPLICITAMENTE com add_session(session_id, user_id)")
        
        # Mensagem de teste
        message = "Olá! Meu nome é Ana Silva e sou nutricionista. Vocês têm opções saudáveis?"
        
        print(f"\n📤 Enviando mensagem:")
        print(f"   {message}")
        
        # Executar agente (deve criar sessão explicitamente)
        response = agent.ask(message, user_id=user_id, session_id=session_id)
        
        print(f"\n💬 Resposta recebida:")
        print(f"   {response}")
        
        print(f"\n✅ Execução concluída!")
        print(f"🔍 VERIFICAR NO PAINEL ZEP:")
        print(f"   - User ID: {user_id}")
        print(f"   - Session ID: {session_id}")
        print(f"   - A sessão deve estar vinculada corretamente ao usuário {user_id}")
        print(f"   - Não deve haver usuários automáticos com IDs aleatórios")
        print(f"   - Deve haver 2 mensagens: user + assistant")
        print(f"   - Memória deve conter: Ana Silva, nutricionista")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_session_creation()
    print(f"\n{'='*60}")
    print(f"Status: {'✅ SUCESSO' if success else '❌ ERRO'}")