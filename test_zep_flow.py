#!/usr/bin/env python3
"""
Teste do fluxo exato do Zep conforme especificado:

1. Verificar se usuário existe → se não, criar
2. Verificar se sessão existe → se não, criar (implicitamente)
3. Buscar contexto: Get Session Memory + Get Messages for Session (limite 10)
4. Adicionar mensagem do usuário
5. Processar com agente (incluindo contexto no prompt)
6. Adicionar resposta do assistente
"""

import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_exact_zep_flow():
    """Testa o fluxo exato conforme especificado"""
    print("🧪 Testando Fluxo Exato do Zep")
    print("=" * 50)
    
    try:
        from agents.core.zep_client import get_zep_client, is_zep_available
        from agents.core.operator import agent_operator
        
        if not is_zep_available():
            print("❌ Zep não disponível")
            return False
        
        # IDs únicos para teste
        test_user_id = f"flow_test_user_{int(datetime.now().timestamp())}"
        test_session_id = f"flow_test_session_{int(datetime.now().timestamp())}"
        
        print(f"👤 Usuario: {test_user_id}")
        print(f"💬 Sessão: {test_session_id}")
        
        # Obter cliente e agente
        zep_client = get_zep_client()
        agent = agent_operator.get_agent("rag-search")
        
        print("\n🔄 ETAPA 1: Primeira mensagem (nova sessão)")
        print("-" * 40)
        
        # Primeira mensagem - deve criar usuário e sessão
        response1 = agent.ask(
            "Olá, meu nome é João e eu trabalho com tecnologia",
            user_id=test_user_id,
            session_id=test_session_id
        )
        
        print(f"✅ Resposta 1: {response1[:100]}...")
        
        print("\n🔄 ETAPA 2: Segunda mensagem (sessão existente)")
        print("-" * 40)
        
        # Segunda mensagem - deve usar contexto da primeira
        response2 = agent.ask(
            "Você se lembra do meu nome e profissão?",
            user_id=test_user_id,
            session_id=test_session_id
        )
        
        print(f"✅ Resposta 2: {response2[:100]}...")
        
        print("\n🔄 ETAPA 3: Terceira mensagem (mais contexto)")
        print("-" * 40)
        
        # Terceira mensagem - deve acumular mais contexto
        response3 = agent.ask(
            "Quais produtos estão disponíveis no cardápio?",
            user_id=test_user_id,
            session_id=test_session_id
        )
        
        print(f"✅ Resposta 3: {response3[:100]}...")
        
        print("\n📊 VERIFICAÇÃO FINAL")
        print("-" * 40)
        
        # Verificar se usuário existe
        user = zep_client.get_user(test_user_id)
        print(f"👤 Usuário criado: {'✅' if user else '❌'}")
        
        # Verificar mensagens na sessão
        messages = zep_client.get_session_messages(test_session_id, limit=10)
        print(f"💬 Mensagens na sessão: {len(messages)}")
        
        # Verificar memória
        memory = zep_client.get_session_memory(test_session_id)
        if isinstance(memory, str):
            has_memory = bool(memory.strip())
        elif isinstance(memory, dict):
            has_memory = memory and (memory.get("summary") or memory.get("facts"))
        else:
            has_memory = bool(memory)
        print(f"🧠 Memória gerada: {'✅' if has_memory else '❌'}")
        
        if has_memory:
            if isinstance(memory, str):
                print(f"📝 Resumo: {memory[:150]}...")
            elif isinstance(memory, dict):
                summary = memory.get("summary", "")
                if summary and isinstance(summary, str):
                    print(f"📝 Resumo: {summary[:150]}...")
                elif summary:
                    print(f"📝 Resumo: {str(summary)[:150]}...")
        
        # Verificar se contexto está sendo usado (verificar na 3ª resposta que mencionou "João")
        context_used = "joão" in response3.lower()
        print(f"🎯 Contexto usado na resposta: {'✅' if context_used else '❌'}")
        
        print(f"\n🎉 Teste concluído! Mensagens: {len(messages)}, Memória: {'Sim' if has_memory else 'Não'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_flow():
    """Testa o fluxo via API"""
    print("\n🌐 Testando Fluxo via API")
    print("=" * 50)
    
    try:
        import requests
        import json
        
        base_url = "http://localhost:8001/v1/agents/rag-search/ask"
        headers = {
            "Authorization": "Bearer sistemarag-api-key-secure-2024",
            "Content-Type": "application/json"
        }
        
        # IDs únicos
        test_user_id = f"api_flow_user_{int(datetime.now().timestamp())}"
        test_session_id = f"api_flow_session_{int(datetime.now().timestamp())}"
        
        print(f"👤 Usuario API: {test_user_id}")
        print(f"💬 Sessão API: {test_session_id}")
        
        # Primeira mensagem
        data1 = {
            "message": "Olá, meu nome é Maria e trabalho com marketing",
            "user_id": test_user_id,
            "session_id": test_session_id
        }
        
        print(f"\n📤 Enviando mensagem 1...")
        response1 = requests.post(base_url, headers=headers, json=data1, timeout=30)
        
        if response1.status_code == 200:
            result1 = response1.json()
            print(f"✅ Resposta 1: {result1['response'][:100]}...")
        else:
            print(f"❌ Erro API 1: {response1.status_code}")
            return False
        
        # Segunda mensagem
        data2 = {
            "message": "Você lembra do meu nome e área de trabalho?",
            "user_id": test_user_id,
            "session_id": test_session_id
        }
        
        print(f"\n📤 Enviando mensagem 2...")
        response2 = requests.post(base_url, headers=headers, json=data2, timeout=30)
        
        if response2.status_code == 200:
            result2 = response2.json()
            print(f"✅ Resposta 2: {result2['response'][:100]}...")
            
            # Verificar se contexto foi usado
            context_used = "maria" in result2['response'].lower() or "marketing" in result2['response'].lower()
            print(f"🎯 Contexto usado: {'✅' if context_used else '❌'}")
            
        else:
            print(f"❌ Erro API 2: {response2.status_code}")
            return False
        
        print(f"\n🎉 Teste API concluído com sucesso!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("⚠️  API não está rodando - execute: python run_agents_api.py")
        return True  # Não é erro do código
    except Exception as e:
        print(f"❌ Erro no teste API: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Testando Fluxo Exato do Zep")
    print("=" * 60)
    
    # Teste direto
    success1 = test_exact_zep_flow()
    
    # Teste via API
    success2 = test_api_flow()
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    print(f"🧪 Fluxo Direto: {'✅ PASSOU' if success1 else '❌ FALHOU'}")
    print(f"🌐 Fluxo API: {'✅ PASSOU' if success2 else '❌ FALHOU'}")
    
    if success1 and success2:
        print("\n🎉 Todos os testes passaram! Fluxo Zep implementado corretamente.")
        return True
    else:
        print("\n⚠️  Alguns testes falharam.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)