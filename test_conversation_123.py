#!/usr/bin/env python3
"""
Teste de conversa simulada para verificar duplicidade no Zep

Simula conversa com:
- user_id: "123"
- session_id: "123"
- 10 mensagens alternadas (user -> assistant -> user -> assistant...)
"""

import requests
import json
import time
from datetime import datetime

def test_conversation():
    """Simula conversa completa"""
    print("🗣️ Simulando Conversa com 10 Mensagens")
    print("=" * 50)
    print("👤 User ID: 123")
    print("💬 Session ID: 123")
    print()
    
    base_url = "http://localhost:8001/v1/agents/rag-search/ask"
    headers = {
        "Authorization": "Bearer sistemarag-api-key-secure-2024",
        "Content-Type": "application/json"
    }
    
    # 10 mensagens de teste
    messages = [
        "Olá, meu nome é João da Silva",
        "Trabalho como gerente de vendas há 5 anos",
        "Quais produtos vocês oferecem?",
        "Qual é o preço do Classic Burger?",
        "Vocês têm opções vegetarianas?",
        "Qual o horário de funcionamento?",
        "Posso fazer pedido para entrega?",
        "Quais formas de pagamento vocês aceitam?",
        "Vocês têm promoções especiais?",
        "Obrigado pelas informações! Até logo."
    ]
    
    responses = []
    
    for i, message in enumerate(messages, 1):
        print(f"📤 Mensagem {i}/10: {message}")
        
        data = {
            "message": message,
            "user_id": "123",
            "session_id": "123"
        }
        
        try:
            start_time = time.time()
            response = requests.post(base_url, headers=headers, json=data, timeout=60)
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                agent_response = result['response']
                responses.append({
                    'user_message': message,
                    'agent_response': agent_response,
                    'timestamp': result['timestamp'],
                    'metadata': result['metadata'],
                    'elapsed': elapsed
                })
                
                print(f"💬 Resposta {i}: {agent_response[:100]}...")
                print(f"⏱️  Tempo: {elapsed:.2f}s")
                print(f"📊 Metadata: {result['metadata']}")
                print("-" * 40)
                
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                break
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            break
        
        # Pequena pausa entre mensagens
        time.sleep(1)
    
    return responses

def check_zep_messages():
    """Verifica mensagens no Zep"""
    print("\n🔍 Verificando Mensagens no Zep")
    print("=" * 50)
    
    try:
        from agents.core.zep_client import get_zep_client
        
        zep_client = get_zep_client()
        
        # Verificar usuário
        user = zep_client.get_user("123")
        print(f"👤 Usuário 123: {'✅ Existe' if user else '❌ Não existe'}")
        
        # Verificar mensagens na sessão
        messages = zep_client.get_session_messages("123", limit=50)  # Buscar até 50 para ver tudo
        print(f"💬 Total de mensagens na sessão: {len(messages)}")
        
        # Analisar padrão das mensagens
        user_messages = [msg for msg in messages if msg.get('role_type') == 'user']
        assistant_messages = [msg for msg in messages if msg.get('role_type') == 'assistant']
        
        print(f"👤 Mensagens do usuário: {len(user_messages)}")
        print(f"🤖 Mensagens do assistente: {len(assistant_messages)}")
        
        # Verificar se há duplicatas
        print(f"\n📋 Análise de Duplicatas:")
        
        user_contents = [msg.get('content', '') for msg in user_messages]
        assistant_contents = [msg.get('content', '') for msg in assistant_messages]
        
        user_duplicates = len(user_contents) - len(set(user_contents))
        assistant_duplicates = len(assistant_contents) - len(set(assistant_contents))
        
        print(f"👤 Duplicatas do usuário: {user_duplicates}")
        print(f"🤖 Duplicatas do assistente: {assistant_duplicates}")
        
        if user_duplicates > 0 or assistant_duplicates > 0:
            print("⚠️  DUPLICATAS DETECTADAS!")
        else:
            print("✅ Nenhuma duplicata detectada")
        
        # Mostrar últimas 10 mensagens para análise
        print(f"\n📝 Últimas 10 mensagens:")
        for i, msg in enumerate(messages[-10:], 1):
            role = msg.get('role_type', 'unknown')
            content = msg.get('content', '')[:60]
            timestamp = msg.get('created_at', 'N/A')
            print(f"{i:2}. [{role:9}] {content}... ({timestamp})")
        
        # Verificar memória
        memory = zep_client.get_session_memory("123")
        has_memory = bool(memory)
        print(f"\n🧠 Memória da sessão: {'✅ Existe' if has_memory else '❌ Não existe'}")
        
        if has_memory and isinstance(memory, str):
            print(f"📝 Resumo: {memory[:200]}...")
        elif has_memory and isinstance(memory, dict):
            summary = memory.get('summary', '')
            if summary:
                print(f"📝 Resumo: {summary[:200]}...")
        
        return {
            'total_messages': len(messages),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'user_duplicates': user_duplicates,
            'assistant_duplicates': assistant_duplicates,
            'has_memory': has_memory
        }
        
    except Exception as e:
        print(f"❌ Erro ao verificar Zep: {e}")
        return None

def main():
    """Executa teste completo"""
    print("🧪 Teste de Duplicidade no Zep")
    print("=" * 60)
    
    # 1. Executar conversa
    responses = test_conversation()
    
    print(f"\n✅ Conversa concluída: {len(responses)} trocas de mensagens")
    
    # 2. Verificar no Zep
    zep_analysis = check_zep_messages()
    
    # 3. Análise final
    print("\n" + "=" * 60)
    print("📊 ANÁLISE FINAL")
    print("=" * 60)
    
    if zep_analysis:
        expected_messages = len(responses) * 2  # user + assistant para cada troca
        actual_messages = zep_analysis['total_messages']
        
        print(f"🔢 Mensagens esperadas: {expected_messages}")
        print(f"🔢 Mensagens no Zep: {actual_messages}")
        print(f"📊 Diferença: {actual_messages - expected_messages}")
        
        if actual_messages > expected_messages:
            print("⚠️  POSSÍVEL DUPLICAÇÃO DETECTADA!")
            print(f"   Esperado: {expected_messages} mensagens")
            print(f"   Encontrado: {actual_messages} mensagens")
            print(f"   Excesso: {actual_messages - expected_messages} mensagens")
        elif actual_messages == expected_messages:
            print("✅ Número de mensagens correto - SEM DUPLICAÇÃO")
        else:
            print("⚠️  Menos mensagens que esperado")
        
        # Duplicatas por conteúdo
        total_duplicates = zep_analysis['user_duplicates'] + zep_analysis['assistant_duplicates']
        if total_duplicates > 0:
            print(f"🔁 Duplicatas por conteúdo: {total_duplicates}")
        else:
            print("✅ Sem duplicatas por conteúdo")
        
    else:
        print("❌ Não foi possível analisar dados do Zep")
    
    print(f"\n🎯 Status: {'✅ SUCESSO' if zep_analysis and zep_analysis['total_messages'] == len(responses) * 2 and zep_analysis['user_duplicates'] == 0 and zep_analysis['assistant_duplicates'] == 0 else '⚠️ VERIFICAR'}")

if __name__ == "__main__":
    main()