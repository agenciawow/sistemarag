#!/usr/bin/env python3
"""
Debug da criação de sessão para identificar onde está falhando
"""

import logging
from agents.core.zep_client import get_zep_client

# Configurar logging detalhado
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_session_creation():
    """Debug passo a passo da criação de sessão"""
    print("🐛 DEBUG: Criação de Sessão Zep")
    print("=" * 50)
    
    try:
        zep_client = get_zep_client()
        
        user_id = "debug_user_123"
        session_id = "debug_session_123"
        
        print(f"👤 User ID: {user_id}")
        print(f"💬 Session ID: {session_id}")
        
        # PASSO 1: Criar usuário
        print(f"\n🔄 PASSO 1: Criando usuário {user_id}")
        try:
            user = zep_client.create_user(user_id)
            print(f"✅ Usuário criado: {user.user_id}")
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"ℹ️  Usuário já existe")
                user = zep_client.get_user(user_id)
            else:
                raise e
        
        # PASSO 2: Verificar se sessão existe
        print(f"\n🔄 PASSO 2: Verificando sessão {session_id}")
        try:
            session = zep_client.client.memory.get_session(session_id=session_id)
            print(f"✅ Sessão já existe: {session.session_id} para usuário {session.user_id}")
        except Exception as e:
            print(f"ℹ️  Sessão não existe: {e}")
            
            # PASSO 3: Criar sessão explicitamente
            print(f"\n🔄 PASSO 3: Criando sessão {session_id} para usuário {user_id}")
            try:
                result = zep_client.client.memory.add_session(
                    session_id=session_id,
                    user_id=user_id
                )
                print(f"✅ Sessão criada com sucesso!")
                print(f"   - Session ID: {result.session_id}")
                print(f"   - User ID: {result.user_id}")
                print(f"   - Created At: {result.created_at}")
            except Exception as e:
                print(f"❌ ERRO ao criar sessão: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        # PASSO 4: Verificar se sessão foi criada corretamente
        print(f"\n🔄 PASSO 4: Verificando sessão criada")
        try:
            session = zep_client.client.memory.get_session(session_id=session_id)
            print(f"✅ Sessão verificada:")
            print(f"   - Session ID: {session.session_id}")
            print(f"   - User ID: {session.user_id}")
            print(f"   - Usuário correto: {'✅' if session.user_id == user_id else '❌'}")
        except Exception as e:
            print(f"❌ ERRO ao verificar sessão: {e}")
            return False
        
        # PASSO 5: Testar adição de mensagem
        print(f"\n🔄 PASSO 5: Testando adição de mensagem")
        try:
            from agents.core.zep_client import ZepMessage
            from zep_cloud.types import Message
            
            # Criar mensagem
            test_message = Message(
                content="Mensagem de teste para debug",
                role_type="user"
            )
            
            # Adicionar à sessão
            result = zep_client.client.memory.add(
                session_id=session_id,
                messages=[test_message]
            )
            print(f"✅ Mensagem adicionada: {result}")
            
            # Verificar se foi salva
            messages = zep_client.client.memory.get_session_messages(
                session_id=session_id,
                limit=10
            )
            print(f"📊 Mensagens na sessão: {len(messages.messages)}")
            if len(messages.messages) > 0:
                last_msg = messages.messages[-1]
                print(f"📝 Última mensagem: {last_msg.content}")
            
        except Exception as e:
            print(f"❌ ERRO ao adicionar mensagem: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print(f"\n🎉 DEBUG concluído com sucesso!")
        print(f"🔍 Verifique no painel Zep:")
        print(f"   - User ID: {user_id}")
        print(f"   - Session ID: {session_id}")
        print(f"   - A sessão deve estar vinculada ao usuário correto")
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO no debug: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_session_creation()
    print(f"\n{'='*50}")
    print(f"Status: {'✅ SUCESSO' if success else '❌ ERRO'}")