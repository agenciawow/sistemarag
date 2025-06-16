"""
Teste do sistema de agentes

Script para testar a implementação do agente RAG e a descoberta automática.
"""

import sys
import os
# Adicionar diretório raiz ao path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from agents.core.operator import agent_operator
from agents.core.rag_search_agent import RAGSearchAgent
from agents.tools.retrieval_tool import test_retrieval_tool


def test_agent_discovery():
    """Testa a descoberta automática de agentes"""
    print("=== TESTE DE DESCOBERTA DE AGENTES ===")
    
    try:
        # Listar agentes descobertos
        agents = agent_operator.list_agents()
        print(f"Agentes descobertos: {len(agents)}")
        
        for agent in agents:
            print(f"  - {agent['name']} (ID: {agent['agent_id']})")
            print(f"    Descrição: {agent['description']}")
            print(f"    Módulo: {agent['module']}")
            print()
        
        return len(agents) > 0
        
    except Exception as e:
        print(f"❌ Erro na descoberta: {e}")
        return False


def test_retrieval_tool_directly():
    """Testa a tool de retrieval diretamente"""
    print("=== TESTE DA TOOL DE RETRIEVAL ===")
    
    try:
        # Testar conexão
        test_result = test_retrieval_tool()
        print(f"Teste de conexão: {test_result}")
        
        if not test_result.get("success", False):
            print("❌ Tool de retrieval não está funcionando")
            return False
        
        print("✅ Tool de retrieval funcionando")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar tool: {e}")
        return False


def test_agent_instantiation():
    """Testa a criação de instância do agente"""
    print("=== TESTE DE INSTANCIAÇÃO DO AGENTE ===")
    
    try:
        # Testar se agente RAG existe
        if not agent_operator.agent_exists("rag-search"):
            print("❌ Agente rag-search não foi descoberto")
            return False
        
        # Obter instância do agente
        agent = agent_operator.get_agent("rag-search")
        print(f"✅ Agente criado: {agent.name}")
        
        # Testar se tem métodos necessários
        required_methods = ['ask', 'clear_history', 'get_chat_history', 'test_agent']
        for method in required_methods:
            if hasattr(agent, method):
                print(f"  ✅ Método {method} disponível")
            else:
                print(f"  ❌ Método {method} ausente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na instanciação: {e}")
        return False


def test_agent_functionality():
    """Testa funcionalidade básica do agente"""
    print("=== TESTE DE FUNCIONALIDADE DO AGENTE ===")
    
    try:
        # Obter agente
        agent = agent_operator.get_agent("rag-search")
        
        # Testar pergunta simples
        print("Testando pergunta simples...")
        response = agent.ask("Olá!")
        print(f"Resposta: {response[:100]}...")
        
        # Testar histórico
        history = agent.get_chat_history()
        print(f"Histórico tem {len(history)} mensagens")
        
        # Testar limpeza
        agent.clear_history()
        history_after = agent.get_chat_history()
        print(f"Após limpeza: {len(history_after)} mensagens")
        
        print("✅ Funcionalidade básica ok")
        return True
        
    except Exception as e:
        print(f"❌ Erro na funcionalidade: {e}")
        return False


def run_all_tests():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO SISTEMA DE AGENTES\n")
    
    tests = [
        ("Descoberta de Agentes", test_agent_discovery),
        ("Tool de Retrieval", test_retrieval_tool_directly),
        ("Instanciação do Agente", test_agent_instantiation),
        ("Funcionalidade do Agente", test_agent_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        success = test_func()
        results.append((test_name, success))
        if success:
            print(f"✅ {test_name}: PASSOU")
        else:
            print(f"❌ {test_name}: FALHOU")
    
    print(f"\n{'='*50}")
    print("RESUMO DOS TESTES")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name}: {status}")
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\nSistema de agentes pronto para uso!")
        print("\nPara usar:")
        print("1. API atual: http://localhost:8000 (mantida intacta)")
        print("2. API de agentes: http://localhost:8001")
        print("3. Documentação: http://localhost:8001/docs")
    else:
        print("⚠️  Alguns testes falharam. Verifique as configurações.")


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n❌ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro geral nos testes: {e}")
        import traceback
        traceback.print_exc()