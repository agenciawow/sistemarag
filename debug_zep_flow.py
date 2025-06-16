#!/usr/bin/env python3
"""
Debug do fluxo Zep - identificar onde está falhando

Teste com user_id="123" e session_id="123" sempre
"""

import logging
from agents.core.zep_client import get_zep_client, ZepMessage

# Configurar logging detalhado
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_zep_basic_flow():
    """Testa fluxo básico do Zep passo a passo"""
    print("🔍 DEBUG: Testando Fluxo Básico do Zep")
    print("=" * 50)
    
    try:
        # Obter cliente
        zep_client = get_zep_client()
        print(f"✅ Cliente Zep conectado")
        
        user_id = "123"
        session_id = "123"
        
        print(f"\n📋 Usando sempre: user_id='{user_id}', session_id='{session_id}'")
        
        # PASSO 1: Verificar/criar usuário
        print(f"\n🔴 PASSO 1: Verificar usuário {user_id}")
        user = zep_client.get_user(user_id)
        if user:
            print(f"✅ Usuário {user_id} já existe: {user}")
        else:
            print(f"⚠️  Usuário {user_id} não existe, criando...")
            user = zep_client.create_user(user_id)
            print(f"✅ Usuário {user_id} criado: {user}")
        
        # PASSO 2: Verificar sessão (via mensagens)
        print(f"\n🔴 PASSO 2: Verificar sessão {session_id}")
        messages = zep_client.get_session_messages(session_id, limit=10)
        print(f"📊 Sessão {session_id} tem {len(messages)} mensagens")
        
        for i, msg in enumerate(messages, 1):
            role = msg.get('role_type', 'unknown')
            content = msg.get('content', '')[:50]
            print(f"  {i}. [{role}] {content}...")
        
        # PASSO 3: Adicionar mensagem do usuário
        print(f"\n🔴 PASSO 3: Adicionar mensagem do usuário")
        user_message = f"Mensagem de teste {len(messages) + 1}"
        user_messages = [ZepMessage(content=user_message, role_type="user")]
        
        result = zep_client.add_memory_to_session(session_id, user_messages)
        print(f"✅ Mensagem do usuário adicionada: {result}")
        
        # PASSO 4: Verificar se foi salva
        print(f"\n🔴 PASSO 4: Verificar se mensagem foi salva")
        messages_after = zep_client.get_session_messages(session_id, limit=10)
        print(f"📊 Sessão {session_id} agora tem {len(messages_after)} mensagens")
        
        if len(messages_after) > len(messages):
            print("✅ Mensagem do usuário foi salva com sucesso!")
            # Mostrar última mensagem
            last_msg = messages_after[-1]
            print(f"📝 Última mensagem: [{last_msg.get('role_type')}] {last_msg.get('content')}")
        else:
            print("❌ ERRO: Mensagem do usuário NÃO foi salva!")
            return False
        
        # PASSO 5: Adicionar resposta do assistente
        print(f"\n🔴 PASSO 5: Adicionar resposta do assistente")
        assistant_message = f"Resposta do assistente para mensagem {len(messages) + 1}"
        assistant_messages = [ZepMessage(content=assistant_message, role_type="assistant")]
        
        result = zep_client.add_memory_to_session(session_id, assistant_messages)
        print(f"✅ Resposta do assistente adicionada: {result}")
        
        # PASSO 6: Verificar resultado final
        print(f"\n🔴 PASSO 6: Verificar resultado final")
        final_messages = zep_client.get_session_messages(session_id, limit=10)
        print(f"📊 Sessão {session_id} finalmente tem {len(final_messages)} mensagens")
        
        expected_messages = len(messages) + 2  # user + assistant
        if len(final_messages) == expected_messages:
            print("✅ SUCESSO: Ambas mensagens foram salvas!")
        else:
            print(f"❌ ERRO: Esperado {expected_messages} mensagens, encontrado {len(final_messages)}")
            return False
        
        # Mostrar todas as mensagens finais
        print(f"\n📋 MENSAGENS FINAIS NA SESSÃO {session_id}:")
        for i, msg in enumerate(final_messages, 1):
            role = msg.get('role_type', 'unknown')
            content = msg.get('content', '')
            created = msg.get('created_at', 'N/A')
            print(f"  {i}. [{role:9}] {content} ({created})")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_agent_integration():
    """Testa integração com agente"""
    print(f"\n🔍 DEBUG: Testando Integração com Agente")
    print("=" * 50)
    
    try:
        from agents.core.operator import agent_operator
        
        agent = agent_operator.get_agent("rag-search")
        user_id = "123"
        session_id = "123"
        
        print(f"🤖 Testando agente com user_id='{user_id}', session_id='{session_id}'")
        
        # Contar mensagens antes
        zep_client = get_zep_client()
        messages_before = zep_client.get_session_messages(session_id, limit=50)
        print(f"📊 Mensagens antes: {len(messages_before)}")
        
        # Fazer pergunta ao agente
        test_message = "Teste do agente - quais hambúrgueres vocês têm?"
        print(f"📤 Enviando: {test_message}")
        
        response = agent.ask(test_message, user_id=user_id, session_id=session_id)
        print(f"💬 Resposta: {response[:100]}...")
        
        # Contar mensagens depois
        messages_after = zep_client.get_session_messages(session_id, limit=50)
        print(f"📊 Mensagens depois: {len(messages_after)}")
        
        expected_new = 2  # user + assistant
        actual_new = len(messages_after) - len(messages_before)
        
        if actual_new == expected_new:
            print(f"✅ SUCESSO: Agente salvou {actual_new} mensagens corretamente!")
        else:
            print(f"❌ ERRO: Esperado +{expected_new} mensagens, encontrado +{actual_new}")
        
        # Mostrar últimas mensagens
        print(f"\n📋 ÚLTIMAS 5 MENSAGENS:")
        for i, msg in enumerate(messages_after[-5:], len(messages_after)-4):
            role = msg.get('role_type', 'unknown')
            content = msg.get('content', '')[:60]
            print(f"  {i}. [{role:9}] {content}...")
        
        return actual_new == expected_new
        
    except Exception as e:
        print(f"❌ ERRO no teste do agente: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes de debug"""
    print("🚀 DEBUG COMPLETO DO FLUXO ZEP")
    print("=" * 60)
    
    # Teste 1: Fluxo básico do Zep
    success1 = test_zep_basic_flow()
    
    # Teste 2: Integração com agente
    success2 = test_agent_integration()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DO DEBUG")
    print("=" * 60)
    print(f"🔧 Fluxo Básico Zep: {'✅ OK' if success1 else '❌ FALHOU'}")
    print(f"🤖 Integração Agente: {'✅ OK' if success2 else '❌ FALHOU'}")
    
    if success1 and success2:
        print("\n🎉 TUDO FUNCIONANDO! O problema pode estar na API.")
    elif success1 and not success2:
        print("\n⚠️  Zep funciona, mas agente tem problemas.")
    else:
        print("\n❌ Problema fundamental no Zep.")

if __name__ == "__main__":
    main()