"""
Testes do Core dos Agentes

Testa a funcionalidade principal dos agentes, descoberta automática e ferramentas.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Adicionar path do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from agents.core.operator import agent_operator, get_agent, list_agents, agent_exists
from agents.core.rag_search_agent import RAGSearchAgent
from agents.tools.retrieval_tool import RetrievalTool, test_retrieval_tool


class TestAgentOperator:
    """Testes do operador de descoberta de agentes"""
    
    def test_list_agents(self):
        """Testa se agentes são descobertos"""
        agents = list_agents()
        assert isinstance(agents, list)
        assert len(agents) > 0
        
        # Verificar se agente RAG está presente
        agent_ids = [agent['agent_id'] for agent in agents]
        assert 'rag-search' in agent_ids
    
    def test_agent_exists(self):
        """Testa verificação de existência de agente"""
        assert agent_exists('rag-search') == True
        assert agent_exists('agente-inexistente') == False
    
    def test_get_agent(self):
        """Testa obtenção de instância de agente"""
        agent = get_agent('rag-search')
        assert agent is not None
        assert hasattr(agent, 'ask')
        assert hasattr(agent, 'clear_history')
        assert hasattr(agent, 'get_chat_history')
    
    def test_get_nonexistent_agent(self):
        """Testa erro ao obter agente inexistente"""
        with pytest.raises(ValueError, match="não encontrado"):
            get_agent('agente-inexistente')


class TestRAGSearchAgent:
    """Testes do agente de busca RAG"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.agent = RAGSearchAgent()
    
    def test_agent_initialization(self):
        """Testa inicialização do agente"""
        assert self.agent.name == "RAG Search Agent"
        assert self.agent.agent_id == "rag-search"
        assert hasattr(self.agent, 'retrieval_tool')
        assert isinstance(self.agent.retrieval_tool, RetrievalTool)
    
    def test_simple_response(self):
        """Testa resposta simples (sem RAG)"""
        response = self.agent.ask("Olá")
        assert isinstance(response, str)
        assert len(response) > 0
        assert "assistente" in response.lower() or "olá" in response.lower()
    
    def test_chat_history(self):
        """Testa gerenciamento de histórico"""
        # Histórico inicial vazio
        assert len(self.agent.get_chat_history()) == 0
        
        # Fazer pergunta
        self.agent.ask("Teste")
        
        # Verificar histórico
        history = self.agent.get_chat_history()
        assert len(history) == 2  # user + assistant
        assert history[0]['role'] == 'user'
        assert history[1]['role'] == 'assistant'
        
        # Limpar histórico
        self.agent.clear_history()
        assert len(self.agent.get_chat_history()) == 0
    
    def test_agent_stats(self):
        """Testa obtenção de estatísticas do agente"""
        stats = self.agent.get_agent_stats()
        assert isinstance(stats, dict)
        assert 'agent_info' in stats
        assert 'chat_history_length' in stats
        assert 'config' in stats
    
    def test_agent_test_function(self):
        """Testa função de teste do agente"""
        test_result = self.agent.test_agent()
        assert isinstance(test_result, dict)
        assert 'agent_status' in test_result
        assert 'timestamp' in test_result


class TestRetrievalTool:
    """Testes da ferramenta de retrieval"""
    
    def test_tool_connection(self):
        """Testa conexão da ferramenta"""
        test_result = test_retrieval_tool()
        assert isinstance(test_result, dict)
        assert 'success' in test_result
        
        # Se a tool estiver configurada corretamente, deve passar
        if test_result['success']:
            assert test_result['message'] == 'Pipeline testado com sucesso'
            assert 'details' in test_result
    
    def test_tool_initialization(self):
        """Testa inicialização da ferramenta"""
        try:
            tool = RetrievalTool()
            assert hasattr(tool, 'rag_pipeline')
            assert hasattr(tool, 'search_documents')
        except Exception as e:
            # Pode falhar se não estiver configurado
            pytest.skip(f"Tool não configurada: {e}")
    
    @patch('agentes.tools.retrieval_tool.RetrievalTool')
    def test_search_documents_mock(self, mock_tool):
        """Testa busca de documentos com mock"""
        # Configurar mock
        mock_instance = Mock()
        mock_tool.return_value = mock_instance
        
        # Simular resultado de busca
        mock_result = {
            'success': True,
            'documents': [
                {
                    'document_name': 'test.pdf',
                    'page_number': 1,
                    'content': 'Conteúdo de teste',
                    'similarity_score': 0.9
                }
            ],
            'query_info': {
                'original_query': 'teste',
                'needs_rag': True
            }
        }
        mock_instance.search_documents.return_value = mock_result
        
        # Testar
        tool = RetrievalTool()
        result = tool.search_documents("teste")
        
        assert result['success'] == True
        assert len(result['documents']) == 1


@pytest.fixture
def sample_agent():
    """Fixture para agente de teste"""
    return RAGSearchAgent()


def test_integration_agent_with_tool(sample_agent):
    """Teste de integração agente + ferramenta"""
    # Verificar se agente tem ferramenta
    assert hasattr(sample_agent, 'retrieval_tool')
    
    # Testar resposta simples
    response = sample_agent.ask("Olá")
    assert isinstance(response, str)
    assert len(response) > 0


if __name__ == "__main__":
    # Executar testes se rodado diretamente
    pytest.main([__file__, "-v"])