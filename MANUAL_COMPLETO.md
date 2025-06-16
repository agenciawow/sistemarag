# 📚 Manual Completo - Sistema RAG Multimodal

## 🎯 Para Quem é Este Manual

Este manual foi criado para **iniciantes completos** que querem configurar e usar um sistema RAG (Retrieval-Augmented Generation) profissional. Não é necessário ter experiência prévia com programação ou inteligência artificial.

**O que você vai aprender:**
- ✅ Como configurar o sistema do zero
- ✅ Como indexar seus documentos 
- ✅ Como fazer buscas inteligentes
- ✅ Como avaliar a qualidade do sistema
- ✅ Como personalizar para seu negócio

---

## 📋 Índice

1. [Pré-requisitos](#1-pré-requisitos)
2. [Instalação](#2-instalação)
3. [Configuração das APIs](#3-configuração-das-apis)
4. [Configuração do Sistema](#4-configuração-do-sistema)
5. [Primeiro Uso](#5-primeiro-uso)
6. [Indexando Seus Documentos](#6-indexando-seus-documentos)
7. [Fazendo Buscas](#7-fazendo-buscas)
8. [Sistema de Avaliação](#8-sistema-de-avaliação)
9. [Personalização Avançada](#9-personalização-avançada)
10. [Resolução de Problemas](#10-resolução-de-problemas)
11. [Dicas e Melhores Práticas](#11-dicas-e-melhores-práticas)

---

## 1. Pré-requisitos

### 1.1. Conhecimentos Necessários
- ✅ Saber usar o computador básico
- ✅ Saber abrir arquivos e pastas
- ✅ Não precisa saber programar!

### 1.2. O Que Você Precisa Ter

#### Hardware Mínimo
- **Computador**: Windows, Mac ou Linux
- **RAM**: Pelo menos 4GB (recomendado 8GB+)
- **Espaço**: 2GB livres no disco
- **Internet**: Conexão estável

#### Contas Necessárias (gratuitas)
1. **OpenAI** - Para inteligência artificial
2. **Voyage AI** - Para análise de texto
3. **Astra DB** - Para banco de dados
4. **Cloudflare** - Para armazenar imagens
5. **Google Drive** - Para documentos (opcional)

> 💡 **Importante**: Todas essas contas têm versões gratuitas suficientes para começar!

---

## 2. Instalação

### 2.1. Instalando o Python

#### No Windows:
1. Vá para https://python.org
2. Clique em "Download Python" (versão 3.11 ou superior)
3. Execute o arquivo baixado
4. ⚠️ **IMPORTANTE**: Marque "Add Python to PATH"
5. Clique em "Install Now"

#### No Mac:
1. Abra o Terminal (Cmd + Espaço, digite "Terminal")
2. Digite: `python3 --version`
3. Se não tiver Python, instale pelo site python.org

#### No Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2.2. Verificando a Instalação
Abra o terminal/prompt de comando e digite:
```bash
python --version
```
Deve mostrar algo como "Python 3.11.x" ou superior.

### 2.3. Baixando o Sistema RAG

#### Opção 1: Download Direto (Mais Fácil)
1. Baixe o arquivo ZIP do sistema
2. Extraia em uma pasta (ex: `C:\MeuSistemaRAG`)
3. Abra o terminal nesta pasta

#### Opção 2: Git (Para Quem Conhece)
```bash
git clone [URL_DO_REPOSITORIO]
cd sistemarag
```

### 2.4. Instalando as Dependências
No terminal, dentro da pasta do sistema, digite:
```bash
pip install -r requirements.txt
```

⏳ **Aguarde**: Pode levar alguns minutos para instalar tudo.

---

## 3. Configuração das APIs

### 3.1. OpenAI (Obrigatório)

#### Criando Conta:
1. Vá para https://platform.openai.com
2. Clique em "Sign up" 
3. Crie sua conta (email + senha)
4. Confirme o email

#### Obtendo a Chave:
1. Faça login em https://platform.openai.com
2. Clique no seu perfil (canto superior direito)
3. Vá em "API keys"
4. Clique "Create new secret key"
5. **⚠️ COPIE E GUARDE**: A chave começa com `sk-`

#### Adicionando Créditos:
1. Vá em "Billing" no menu
2. Adicione pelo menos $5 (suficiente para muitos testes)
3. Configure limite de gastos para segurança

### 3.2. Voyage AI (Obrigatório)

#### Criando Conta:
1. Vá para https://www.voyageai.com
2. Clique em "Get Started"
3. Crie conta com GitHub ou Google
4. Confirme o email

#### Obtendo a Chave:
1. Vá para o Dashboard
2. Clique em "API Keys"
3. Crie uma nova chave
4. **⚠️ COPIE E GUARDE**: A chave começa com `pa-`

### 3.3. Astra DB (Obrigatório)

#### Criando Conta:
1. Vá para https://astra.datastax.com
2. Clique "Start Free"
3. Registre-se (gratuito até 25GB)

#### Criando Banco:
1. No dashboard, clique "Create Database"
2. Escolha "Serverless"
3. Nome: `sistemarag`
4. Keyspace: `default_keyspace`
5. Região: Escolha a mais próxima
6. Clique "Create Database"

#### Obtendo Credenciais:
1. Na lista de bancos, clique no seu banco
2. Vá em "Connect" → "APIs"
3. Copie o **Database ID** e **Region**
4. Vá em "Settings" → "Application Tokens"
5. Clique "Generate Token"
6. Papel: "Database Administrator"
7. **⚠️ COPIE E GUARDE**: Token + Endpoint

### 3.4. Cloudflare R2 (Obrigatório)

#### Criando Conta:
1. Vá para https://cloudflare.com
2. Clique "Sign up"
3. Crie conta gratuita

#### Configurando R2:
1. No dashboard, vá em "R2 Object Storage"
2. Clique "Create bucket"
3. Nome: `sistemarag-images`
4. Região: Automatic

#### Criando Worker:
1. Vá em "Workers & Pages"
2. Clique "Create Application" → "Create Worker"
3. Nome: `sistemarag-api`
4. Substitua o código pelo código fornecido no README
5. Clique "Save and Deploy"

#### Configurando Variáveis:
1. No Worker, vá em "Settings" → "Variables"
2. Adicione:
   - `AUTH_TOKEN`: Crie uma senha secreta (ex: `minha-senha-123`)
   - `BUCKET`: `sistemarag-images`

### 3.5. Google Drive (Opcional)

Se você quiser indexar documentos do Google Drive:

1. Coloque seu documento no Google Drive
2. Clique com botão direito → "Compartilhar"
3. Altere para "Qualquer pessoa com o link"
4. Copie o link completo

---

## 4. Configuração do Sistema

### 4.1. Arquivo de Configuração (.env)

1. Na pasta do sistema, encontre o arquivo `.env.example`
2. Copie e renomeie para `.env`
3. Abra o arquivo `.env` em um editor de texto
4. Preencha com suas chaves:

```bash
# APIs Externas
OPENAI_API_KEY=sk-sua-chave-openai-aqui
VOYAGE_API_KEY=pa-sua-chave-voyage-aqui
LLAMA_CLOUD_API_KEY=llx-sua-chave-llama-aqui

# Astra DB
ASTRA_DB_APPLICATION_TOKEN=AstraCS:seu-token-aqui
ASTRA_DB_API_ENDPOINT=https://database-id-region.apps.astra.datastax.com
ASTRA_DB_KEYSPACE=default_keyspace
ASTRA_DB_COLLECTION=meu_negocio

# Cloudflare R2
R2_ENDPOINT=https://seu-worker.workers.dev
R2_AUTH_TOKEN=sua-senha-secreta

# Google Drive Document (se estiver usando)
GOOGLE_DRIVE_URL=https://drive.google.com/file/d/SEU_ID/view

# Modelos OpenAI (opcional - deixe como está)
OPENAI_RERANK_MODEL=gpt-4o-mini
OPENAI_QUERY_TRANSFORM_MODEL=gpt-4o-mini
OPENAI_ANSWER_GENERATION_MODEL=gpt-4o
OPENAI_EXTRACTION_MODEL=gpt-4o
```

### 4.2. Configuração das Perguntas de Avaliação

No mesmo arquivo `.env`, configure as perguntas que o sistema usará para se auto-avaliar:

```bash
# Perguntas para seu tipo de negócio (exemplo: restaurante)
EVAL_QUESTIONS=Quais pratos vocês servem?|Qual é o preço do prato mais caro?|Vocês fazem delivery?|Qual o horário de funcionamento?|Vocês têm opções vegetarianas?

# Palavras-chave que devem aparecer nas respostas
EVAL_KEYWORDS=pratos,cardápio,menu,comida|preço,valor,caro,custo|delivery,entrega,domicílio|horário,funcionamento,aberto|vegetariano,vegano,sem carne

# Categorias das perguntas
EVAL_CATEGORIES=menu|pricing|delivery|hours|dietary
```

**Como personalizar para seu negócio:**

- **Loja de roupas**: "Quais tamanhos vocês têm?|Fazem trocas?|Têm desconto?"
- **Consultoria**: "Quais serviços oferecem?|Como funciona o orçamento?|Qual o prazo?"
- **Escola**: "Quais cursos têm?|Como é a mensalidade?|Têm aulas online?"

### 4.3. Testando a Configuração

No terminal, digite:
```bash
python -c "from sistema_rag.config.settings import settings; print('✅ Configuração OK!')"
```

Se aparecer "✅ Configuração OK!", está tudo certo!

---

## 5. Primeiro Uso

### 5.1. Teste Rápido

Vamos fazer um teste simples para ver se tudo está funcionando:

```bash
python -c "
from sistema_rag.search.conversational_rag import ModularConversationalRAG
rag = ModularConversationalRAG()
print('✅ Sistema inicializado com sucesso!')
"
```

### 5.2. Se Deu Erro

**Erro comum**: "Module not found"
```bash
# Instale novamente as dependências
pip install --upgrade -r requirements.txt
```

**Erro de chave API**: Verifique se todas as chaves no `.env` estão corretas.

**Erro de conexão**: Verifique sua internet e se as URLs estão corretas.

---

## 6. Indexando Seus Documentos

### 6.1. Preparando Documentos

O sistema aceita vários formatos:
- ✅ PDF
- ✅ Word (.docx)
- ✅ PowerPoint (.pptx)
- ✅ Excel (.xlsx)
- ✅ Texto (.txt)
- ✅ Markdown (.md)

**Dicas importantes:**
- Máximo 100MB por arquivo
- Textos em português funcionam melhor
- Imagens são processadas automaticamente

### 6.2. Indexação via Google Drive (Mais Fácil)

#### Passo 1: Preparar Documento
1. Coloque seu documento no Google Drive
2. Configure compartilhamento público (como explicado na seção 3.5)
3. Copie o link

#### Passo 2: Atualizar .env
```bash
GOOGLE_DRIVE_URL=https://drive.google.com/file/d/SEU_ID_AQUI/view
```

#### Passo 3: Indexar
```bash
python ingestion.py
```

### 6.3. Indexação via Arquivo Local

#### Passo 1: Copiar Arquivo
Coloque seu documento na pasta `documentos/` (crie se não existir)

#### Passo 2: Indexar
```bash
python -m sistema_rag.ingestion.run_pipeline --file "documentos/meu_documento.pdf"
```

### 6.4. Acompanhando o Progresso

Durante a indexação, você verá:
```
🔄 Baixando documento...
📄 Processando com LlamaParse...
🖼️ Extraindo imagens...
🔤 Gerando embeddings...
💾 Salvando no banco...
✅ Indexação concluída!
```

⏳ **Tempo estimado**: 2-10 minutos dependendo do tamanho do documento.

---

## 7. Fazendo Buscas

### 7.1. Interface Simples

#### Busca por Comando:
```bash
python search.py "Quais produtos vocês têm?"
```

#### Busca Interativa:
```bash
python -m sistema_rag.search.conversational_rag
```

Vai abrir um chat onde você pode fazer perguntas:
```
💬 Você: Quais são os preços?
🤖 Assistente: Baseado no documento, os preços são...

💬 Você: Fazem entrega?
🤖 Assistente: Sim, fazemos entrega...
```

### 7.2. Comandos Especiais no Chat

- `/help` - Mostra ajuda
- `/clear` - Limpa histórico
- `/stats` - Mostra estatísticas
- `/exit` - Sair

### 7.3. Tipos de Perguntas

**✅ Perguntas que funcionam bem:**
- "Quais produtos vocês têm?"
- "Qual é o preço do X?"
- "Como funciona o processo de Y?"
- "Vocês fazem Z?"

**❌ Perguntas que não funcionam:**
- Perguntas sobre informações não no documento
- Cálculos complexos
- Perguntas sobre eventos futuros

---

## 8. Sistema de Avaliação

### 8.1. O Que é a Avaliação

O sistema inclui um avaliador automático que testa a qualidade das respostas usando perguntas que você define. É como ter um "auditor" que verifica se o sistema está funcionando bem.

### 8.2. Configurando Perguntas de Teste

No arquivo `.env`, defina perguntas relevantes para seu negócio:

**Para Restaurante:**
```bash
EVAL_QUESTIONS=Quais pratos vocês servem?|Fazem delivery?|Qual o horário?|Têm opções veganas?|Como fazer reserva?

EVAL_KEYWORDS=pratos,cardápio,comida|delivery,entrega|horário,funcionamento|vegano,vegetariano|reserva,mesa

EVAL_CATEGORIES=menu|delivery|hours|dietary|booking
```

**Para Loja Online:**
```bash
EVAL_QUESTIONS=Quais produtos vendem?|Como é o frete?|Fazem trocas?|Quais formas de pagamento?|Tem garantia?

EVAL_KEYWORDS=produtos,itens,venda|frete,entrega,correios|troca,devolução|pagamento,cartão,pix|garantia,defeito

EVAL_CATEGORIES=catalog|shipping|returns|payment|warranty
```

### 8.3. Executando Avaliação

```bash
python rag_evaluator.py
```

### 8.4. Entendendo os Resultados

O sistema gera dois arquivos:

#### `rag_evaluation_report.json`
Relatório técnico completo com todas as métricas.

#### `rag_evaluation_detailed.txt`
Relatório em português fácil de entender:

```
📊 RESUMO GERAL:
• Total de perguntas: 5
• Avaliações bem-sucedidas: 4
• Taxa de sucesso: 80%

📈 MÉTRICAS:
• Tempo médio de resposta: 6.2s
• Cobertura de palavras-chave: 75%

📋 RESULTADOS:
• Pergunta 1: ✅ Respondeu corretamente
• Pergunta 2: ✅ Respondeu corretamente  
• Pergunta 3: ❌ Não encontrou informação
```

### 8.5. Interpretando Métricas

- **Taxa de sucesso**: % de perguntas respondidas sem erro
- **Tempo de resposta**: Velocidade do sistema
- **Cobertura de palavras-chave**: % de palavras esperadas nas respostas

**O que é considerado bom:**
- ✅ Taxa de sucesso > 70%
- ✅ Tempo < 10 segundos
- ✅ Cobertura > 60%

---

## 9. Personalização Avançada

### 9.1. Ajustando Modelos OpenAI

No `.env`, você pode escolher diferentes modelos para economizar ou ter mais qualidade:

**Configuração Econômica:**
```bash
OPENAI_RERANK_MODEL=gpt-4o-mini
OPENAI_QUERY_TRANSFORM_MODEL=gpt-4o-mini
OPENAI_ANSWER_GENERATION_MODEL=gpt-4o-mini
OPENAI_EXTRACTION_MODEL=gpt-4o-mini
```

**Configuração Alta Qualidade:**
```bash
OPENAI_RERANK_MODEL=gpt-4o
OPENAI_QUERY_TRANSFORM_MODEL=gpt-4o
OPENAI_ANSWER_GENERATION_MODEL=gpt-4o
OPENAI_EXTRACTION_MODEL=gpt-4o
```

### 9.2. Configurando Temperatura

A temperatura controla a "criatividade" das respostas:

```bash
# Respostas mais conservadoras/precisas
OPENAI_ANSWER_GENERATION_TEMPERATURE=0.1

# Respostas mais criativas/variadas  
OPENAI_ANSWER_GENERATION_TEMPERATURE=0.9
```

**Recomendado**: Entre 0.3 e 0.7

### 9.3. Personalizando Nome da Coleção

Para organizar diferentes projetos:

```bash
# Para cada projeto/cliente
ASTRA_DB_COLLECTION=cliente_abc
ASTRA_DB_COLLECTION=projeto_xyz
ASTRA_DB_COLLECTION=loja_moda
```

---

## 10. Resolução de Problemas

### 10.1. Problemas Comuns e Soluções

#### ❌ "Module not found"
**Causa**: Dependências não instaladas
**Solução**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### ❌ "Authentication failed"
**Causa**: Chave de API incorreta
**Solução**: 
1. Verifique se a chave no `.env` está correta
2. Confirme se a chave não expirou
3. Teste a chave na plataforma original

#### ❌ "Connection timeout"
**Causa**: Problema de internet ou firewall
**Solução**:
1. Verifique conexão com internet
2. Teste: `ping google.com`
3. Verifique firewall corporativo

#### ❌ "Quota exceeded"
**Causa**: Limite de uso da API atingido
**Solução**:
1. Verifique saldo nas plataformas
2. Aumente limite de gastos se necessário
3. Aguarde renovação do limite gratuito

#### ❌ Sistema muito lento
**Causas e soluções**:
- **Documento muito grande**: Divida em partes menores
- **Muitas imagens**: Use documentos com menos imagens
- **Modelo muito avançado**: Use `gpt-4o-mini` em vez de `gpt-4o`

#### ❌ Respostas ruins
**Causas e soluções**:
- **Documento mal estruturado**: Melhore formatação
- **Perguntas muito vagas**: Seja mais específico
- **Temperatura muito alta**: Diminua para 0.3

### 10.2. Comandos de Diagnóstico

#### Teste de Conexões:
```bash
python -c "
from sistema_rag.search.retrieval import VectorSearcher
searcher = VectorSearcher()
result = searcher.test_connection()
print(result.message)
"
```

#### Verificar Documentos Indexados:
```bash
python -c "
from sistema_rag.search.retrieval import VectorSearcher
searcher = VectorSearcher()
print(f'Documentos: {searcher.collection.estimated_document_count()}')
"
```

#### Teste de APIs:
```bash
python -c "
from openai import OpenAI
client = OpenAI()
response = client.models.list()
print('✅ OpenAI OK')
"
```

### 10.3. Logs e Depuração

#### Ativando Logs Detalhados:
```bash
export PYTHONPATH=.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
# Execute seu comando aqui
"
```

#### Arquivo de Log:
Os logs são salvos automaticamente. Procure por arquivos `.log` na pasta do sistema.

---

## 11. Dicas e Melhores Práticas

### 11.1. Preparação de Documentos

#### ✅ Faça:
- **Use títulos claros**: "Preços", "Serviços", "Contato"
- **Organize por seções**: Agrupe informações relacionadas
- **Inclua contexto**: "Nossos preços são:" em vez de só "Preços:"
- **Use listas e tabelas**: Facilitam a extração de informação
- **Mantenha atualizado**: Remova informações obsoletas

#### ❌ Evite:
- Textos muito longos sem pausas
- Formatação excessiva que confunde
- Informações contraditórias
- Documentos com muitos tipos de letra
- Imagens com texto importante (use texto real)

### 11.2. Criando Boas Perguntas de Avaliação

#### ✅ Perguntas Efetivas:
- **Específicas**: "Qual o preço do hambúrguer?" vs "Quais são os preços?"
- **Naturais**: Como um cliente real perguntaria
- **Testáveis**: Que têm resposta clara no documento
- **Variadas**: Cubra diferentes aspectos do negócio

#### Exemplos por Setor:

**Restaurante:**
```
- Quais pratos têm no cardápio?
- Fazem entrega em domicílio?
- Qual o horário de funcionamento?
- Têm opções para celíacos?
- Como fazer reserva?
```

**Consultoria:**
```
- Quais serviços vocês oferecem?
- Como funciona o orçamento?
- Qual o tempo de projeto?
- Têm experiência no setor X?
- Como é o acompanhamento?
```

**E-commerce:**
```
- Quais produtos vocês vendem?
- Como é calculado o frete?
- Qual o prazo de entrega?
- Fazem trocas e devoluções?
- Quais formas de pagamento?
```

### 11.3. Otimização de Performance

#### Para Economizar na API:
1. **Use modelos menores**: `gpt-4o-mini` em vez de `gpt-4o`
2. **Documente bem**: Menos re-processamento
3. **Perguntas diretas**: Evite conversas muito longas
4. **Limpe dados**: Remova informações desnecessárias

#### Para Melhor Qualidade:
1. **Use modelos maiores**: `gpt-4o` para respostas críticas
2. **Ajuste temperatura**: 0.3-0.5 para precisão
3. **Mais contexto**: Documentos bem estruturados
4. **Teste regularmente**: Use o avaliador com frequência

### 11.4. Monitoramento e Manutenção

#### Monitore Semanalmente:
- Execute `python rag_evaluator.py`
- Verifique taxa de sucesso > 70%
- Monitore tempo de resposta < 10s
- Revise custos das APIs

#### Atualize Mensalmente:
- Revisar documentos indexados
- Atualizar perguntas de avaliação
- Verificar novas versões do sistema
- Backup das configurações

#### Sinais de Problemas:
- ❌ Taxa de sucesso < 50%
- ❌ Tempo > 15 segundos
- ❌ Muitas respostas "não encontrado"
- ❌ Custos muito altos

### 11.5. Segurança e Privacidade

#### Proteja Suas Chaves:
- ✅ Nunca compartilhe o arquivo `.env`
- ✅ Use senhas fortes para contas
- ✅ Configure limites de gastos
- ✅ Monitore uso regularmente

#### Dados Sensíveis:
- ❌ Não indexe documentos com dados pessoais
- ❌ Evite informações financeiras sensíveis
- ❌ Não inclua senhas ou tokens em documentos
- ✅ Use apenas informações públicas ou autorizadas

---

## 🎓 Conclusão

Parabéns! Agora você tem um sistema RAG completo funcionando. 

**O que você consegue fazer agora:**
- ✅ Indexar qualquer documento
- ✅ Fazer buscas inteligentes
- ✅ Avaliar qualidade automaticamente
- ✅ Personalizar para seu negócio
- ✅ Monitorar e manter o sistema

**Próximos Passos:**
1. Teste com documentos reais do seu negócio
2. Configure perguntas específicas da sua área
3. Execute avaliações regulares
4. Otimize baseado nos resultados
5. Expanda para mais documentos

**Precisa de Ajuda?**
- 📖 Releia as seções relevantes deste manual
- 🔍 Use os comandos de diagnóstico
- 📧 Verifique logs de erro
- 🌐 Consulte documentação das APIs

**Lembre-se**: Este é um sistema profissional, mas começar simples é sempre a melhor estratégia. Vá incrementando aos poucos conforme ganha experiência!

---

*Manual criado para iniciantes - Sistema RAG Multimodal v2.0*