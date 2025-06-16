#!/usr/bin/env python3
"""
Teste simples da nova implementação do Zep SDK
"""

import logging
from datetime import datetime
import random

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_zep_sdk():
    """Testa o Zep SDK com usuário e sessão únicos"""
    print("🧪 Testando Zep SDK Oficial")
    print("=" * 50)
    
    try:
        from agents.core.zep_client import get_zep_client, is_zep_available, ZepMessage
        
        if not is_zep_available():
            print("❌ Zep não disponível")
            return False
        
        # IDs únicos para evitar conflito
        timestamp = int(datetime.now().timestamp())
        user_id = f"test_user_{timestamp}_{random.randint(1000, 9999)}"
        session_id = f"test_session_{timestamp}_{random.randint(1000, 9999)}"
        
        print(f"👤 Usuário de teste: {user_id}")
        print(f"💬 Sessão de teste: {session_id}")
        
        zep_client = get_zep_client()
        
        # 1. Criar usuário
        print(f"\n🔄 1. Criando usuário...")
        user = zep_client.create_user(user_id)
        print(f"✅ Usuário criado: {user.user_id}")
        
        # 2. Verificar sessão (deve estar vazia)
        print(f"\n🔄 2. Verificando sessão vazia...")
        messages = zep_client.get_session_messages(session_id, limit=10)
        print(f"📊 Mensagens iniciais: {len(messages)}")
        
        # 3. Adicionar primeira mensagem
        print(f"\n🔄 3. Adicionando primeira mensagem...")
        msg1 = ZepMessage(content="Olá, meu nome é João", role_type="user")
        result1 = zep_client.add_memory_to_session(session_id, [msg1])
        print(f"✅ Primeira mensagem adicionada: {result1}")
        
        # 4. Verificar se foi salva
        print(f"\n🔄 4. Verificando se primeira mensagem foi salva...")
        messages_after_1 = zep_client.get_session_messages(session_id, limit=10)
        print(f"📊 Mensagens após primeira: {len(messages_after_1)}")
        
        if len(messages_after_1) > 0:
            print(f"📝 Última mensagem: {messages_after_1[-1]['content']}")
        
        # 5. Adicionar resposta do assistente
        print(f"\n🔄 5. Adicionando resposta do assistente...")
        msg2 = ZepMessage(content="Olá João! Como posso ajudar?", role_type="assistant")
        result2 = zep_client.add_memory_to_session(session_id, [msg2])
        print(f"✅ Resposta do assistente adicionada: {result2}")
        
        # 6. Verificar resultado final
        print(f"\n🔄 6. Verificando resultado final...")
        final_messages = zep_client.get_session_messages(session_id, limit=10)
        print(f"📊 Mensagens finais: {len(final_messages)}")
        
        # 7. Exibir todas as mensagens
        print(f"\n📋 Todas as mensagens:")
        for i, msg in enumerate(final_messages, 1):
            role = msg.get('role_type', 'unknown')
            content = msg.get('content', '')
            print(f"  {i}. [{role:9}] {content}")
        
        # 8. Verificar memória
        print(f"\n🔄 7. Verificando memória da sessão...")
        memory = zep_client.get_session_memory(session_id)
        print(f"🧠 Memória: {memory}")
        
        # 9. Testar contexto completo
        print(f"\n🔄 8. Testando contexto completo...")
        context, messages, is_new = zep_client.ensure_session_context(session_id, user_id)
        print(f"📊 Contexto: {len(context)} chars")
        print(f"📊 Mensagens: {len(messages)}")
        print(f"🆕 Nova sessão: {is_new}")
        
        success = len(final_messages) >= 2
        print(f"\n🎯 Status: {'✅ SUCESSO' if success else '⚠️ VERIFICAR'}")
        
        return success
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_zep_sdk()
    print(f"\n{'='*50}")
    print(f"Resultado: {'PASSOU' if success else 'FALHOU'}")