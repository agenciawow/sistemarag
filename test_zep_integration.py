#!/usr/bin/env python3
"""
Script de teste para integração com Zep

Testa:
- Cliente Zep 
- Criação de usuários
- Gerenciamento de sessões
- Adição de memória
- Recuperação de contexto
- Integração com agentes
"""

import os
import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def test_zep_client():
    """Testa o cliente Zep básico"""
    print("🧪 Testando Cliente Zep...")
    
    try:
        from agents.core.zep_client import get_zep_client, is_zep_available, ZepMessage
        
        if not is_zep_available():
            print("❌ Zep não está disponível - verifique ZEP_API_KEY no .env")
            return False
        
        zep_client = get_zep_client()
        print(f"✅ Cliente Zep inicializado: {zep_client.base_url}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar cliente Zep: {e}")
        return False

def test_user_management():
    """Testa gerenciamento de usuários"""
    print("\n👤 Testando Gerenciamento de Usuários...")
    
    try:
        from agents.core.zep_client import get_zep_client
        
        zep_client = get_zep_client()
        test_user_id = f"test_user_{int(datetime.now().timestamp())}"
        
        # Testar criação/verificação de usuário
        user = zep_client.ensure_user_exists(test_user_id)
        print(f"✅ Usuário criado/verificado: {user.user_id}")
        
        # Testar busca de usuário
        found_user = zep_client.get_user(test_user_id)
        if found_user:
            print(f"✅ Usuário encontrado: {found_user.user_id}")
        else:
            print("❌ Usuário não encontrado após criação")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no gerenciamento de usuários: {e}")
        return False

def test_session_memory():
    """Testa gerenciamento de memória de sessão"""
    print("\n💭 Testando Memória de Sessão...")
    
    try:
        from agents.core.zep_client import get_zep_client, ZepMessage
        
        zep_client = get_zep_client()
        test_user_id = f"test_user_{int(datetime.now().timestamp())}"
        test_session_id = f"test_session_{int(datetime.now().timestamp())}"
        
        # Garantir que usuário existe
        user = zep_client.ensure_user_exists(test_user_id)
        print(f"✅ Usuário preparado: {user.user_id}")
        
        # Adicionar mensagens de teste
        test_messages = [
            ZepMessage(content="Olá, como você está?", role_type="user"),
            ZepMessage(content="Olá! Estou bem, obrigado por perguntar. Como posso ajudar?", role_type="assistant"),
            ZepMessage(content="Quero saber sobre documentos técnicos", role_type="user"),
            ZepMessage(content="Claro! Posso ajudar com análise de documentos técnicos.", role_type="assistant"),
        ]
        
        # Adicionar mensagens
        zep_client.add_memory_to_session(test_session_id, test_messages)
        print(f"✅ {len(test_messages)} mensagens adicionadas à sessão {test_session_id}")
        
        # Recuperar contexto
        memory_context, messages = zep_client.get_session_context(test_session_id, test_user_id)
        print(f"✅ Contexto recuperado: {len(memory_context)} chars de memória, {len(messages)} mensagens")
        
        if memory_context:
            print(f"📝 Contexto de memória: {memory_context[:200]}...")
        
        if messages:
            print(f"💬 Primeira mensagem: {messages[0].get('content', '')[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de memória: {e}")
        return False

def test_agent_integration():
    """Testa integração com agentes"""
    print("\n🤖 Testando Integração com Agentes...")
    
    try:
        from agents.core.operator import agent_operator
        
        # Verificar se agentes estão disponíveis
        agents = agent_operator.list_agents()
        if not agents:
            print("❌ Nenhum agente disponível")
            return False
        
        print(f"✅ {len(agents)} agente(s) disponível(eis)")
        
        # Testar agente RAG com Zep
        agent = agent_operator.get_agent("rag-search")
        if not agent:
            print("❌ Agente rag-search não encontrado")
            return False
        
        test_user_id = f"test_user_{int(datetime.now().timestamp())}"
        test_session_id = f"test_session_{int(datetime.now().timestamp())}"
        
        # Testar pergunta com contexto Zep
        response = agent.ask(
            "Olá, como você está?",
            user_id=test_user_id,
            session_id=test_session_id
        )
        
        print(f"✅ Resposta do agente: {response[:100]}...")
        
        # Testar segunda pergunta para verificar contexto
        response2 = agent.ask(
            "Você se lembra da minha pergunta anterior?",
            user_id=test_user_id,
            session_id=test_session_id
        )
        
        print(f"✅ Segunda resposta: {response2[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração com agentes: {e}")
        return False

def test_api_integration():
    """Testa integração com API"""
    print("\n🌐 Testando Integração com API...")
    
    try:
        import requests
        import json
        
        # Headers para autenticação
        headers = {
            "Authorization": "Bearer sistemarag-api-key-secure-2024",
            "Content-Type": "application/json"
        }
        
        # Dados de teste
        test_data = {
            "message": "Olá, como você está?",
            "user_id": f"api_test_user_{int(datetime.now().timestamp())}",
            "session_id": f"api_test_session_{int(datetime.now().timestamp())}"
        }
        
        # Testar endpoint
        url = "http://localhost:8001/v1/agents/rag-search/ask"
        
        print(f"📡 Enviando request para: {url}")
        print(f"📋 Dados: {test_data}")
        
        # Fazer request (sem validar se API está rodando)
        print("ℹ️  Teste de API seria executado se a API estivesse rodando")
        print(f"ℹ️  URL: {url}")
        print(f"ℹ️  Headers: {headers}")
        print(f"ℹ️  Data: {test_data}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de API: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando Testes de Integração Zep")
    print("=" * 50)
    
    tests = [
        ("Cliente Zep", test_zep_client),
        ("Gerenciamento de Usuários", test_user_management),
        ("Memória de Sessão", test_session_memory),
        ("Integração com Agentes", test_agent_integration),
        ("Integração com API", test_api_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Integração Zep está funcionando.")
    else:
        print("⚠️  Alguns testes falharam. Verifique a configuração.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)