#!/usr/bin/env python3
"""
Teste final com a correção - user_id="final123" e session_id="final123"
"""

import logging
from agents.core.operator import agent_operator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_final_fix():
    """Teste final com correção aplicada"""
    print("🔧 Teste Final - Correção de Sessão Zep")
    print("=" * 50)
    
    try:
        # Obter agente
        agent = agent_operator.get_agent("rag-search")
        
        user_id = "final123"
        session_id = "final123"
        
        print(f"👤 User ID: {user_id}")
        print(f"💬 Session ID: {session_id}")
        print(f"🔧 CORREÇÃO APLICADA: Usar add_session() com user_id")
        
        # Mensagem de teste
        message = "Olá! Meu nome é Carlos Mendes e sou chef. Quais são os ingredientes do Classic Burger?"
        
        print(f"\n📤 Enviando mensagem:")
        print(f"   {message}")
        
        # Executar agente
        response = agent.ask(message, user_id=user_id, session_id=session_id)
        
        print(f"\n💬 Resposta recebida:")
        print(f"   {response}")
        
        print(f"\n✅ Execução concluída!")
        print(f"🔍 VERIFICAR NO PAINEL ZEP:")
        print(f"   - User ID: {user_id}")
        print(f"   - Session ID: {session_id}")
        print(f"   - Sessão deve estar vinculada ao usuário {user_id}")
        print(f"   - NÃO deve haver usuários com hash automático")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_final_fix()
    print(f"\n{'='*50}")
    print(f"Status: {'✅ SUCESSO' if success else '❌ ERRO'}")