#!/usr/bin/env python3
"""
Teste final com user_id="123" e session_id="123" conforme solicitado
"""

import logging
from agents.core.operator import agent_operator

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_123_session():
    """Testa o fluxo com usuário 123 e sessão 123"""
    print("🧪 Testando com user_id='123' e session_id='123'")
    print("=" * 60)
    
    try:
        # Obter agente
        agent = agent_operator.get_agent("rag-search")
        
        user_id = "123"
        session_id = "123"
        
        print(f"👤 Usuário: {user_id}")
        print(f"💬 Sessão: {session_id}")
        
        # Primeira mensagem - presentação
        print(f"\n🔄 1. Primeira interação...")
        msg1 = "Olá, meu nome é Carlos e trabalho como chef de cozinha"
        response1 = agent.ask(msg1, user_id=user_id, session_id=session_id)
        print(f"📤 Enviado: {msg1}")
        print(f"💬 Resposta: {response1[:100]}...")
        
        # Segunda mensagem - teste de memória
        print(f"\n🔄 2. Teste de memória...")
        msg2 = "Você se lembra do meu nome e profissão?"
        response2 = agent.ask(msg2, user_id=user_id, session_id=session_id)
        print(f"📤 Enviado: {msg2}")
        print(f"💬 Resposta: {response2[:100]}...")
        
        # Verificar se usou contexto
        context_used = "carlos" in response2.lower() or "chef" in response2.lower()
        print(f"🎯 Contexto usado: {'✅' if context_used else '❌'}")
        
        # Terceira mensagem - pergunta sobre produto
        print(f"\n🔄 3. Pergunta sobre produtos...")
        msg3 = "Quais hambúrgueres estão no cardápio?"
        response3 = agent.ask(msg3, user_id=user_id, session_id=session_id)
        print(f"📤 Enviado: {msg3}")
        print(f"💬 Resposta: {response3[:150]}...")
        
        # Verificar se usou nome do contexto anterior
        name_context = "carlos" in response3.lower()
        print(f"🎯 Nome mencionado na resposta: {'✅' if name_context else '❌'}")
        
        print(f"\n🎉 Teste finalizado!")
        print(f"✅ Memória funcionando: {context_used}")
        print(f"✅ Contexto persistente: {name_context}")
        
        return context_used and name_context
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_123_session()
    print(f"\n{'='*60}")
    print(f"Status: {'✅ SUCESSO' if success else '⚠️ VERIFICAR'}")