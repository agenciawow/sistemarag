# 🚀 Sistema RAG Multimodal - Python Puro

Sistema completo de RAG (Retrieval-Augmented Generation) multimodal implementado em Python puro, seguindo arquitetura modular e componente por componente.

## 📋 Visão Geral

Este sistema implementa um pipeline completo para processamento de documentos multimodais (texto + imagens) com capacidades de busca vetorial e geração de respostas contextualizadas.

### 🏗️ Arquitetura

```
📁 sistemarag/
├── 📄 ingestao.py       # 🚀 Comando de ingestão
├── 📄 busca.py          # 🔍 Comando de busca
└── 📁 sistema_rag/      # 🏗️ Sistema centralizado
    ├── 📄 run_pipeline.py    # Pipeline interno
    ├── 📁 config/            # Configurações globais
    ├── 📁 models/            # Modelos de dados
    ├── 📁 utils/             # Utilitários e helpers
    ├── 📁 components/        # Componentes modulares
    │   ├── 📁 ingestion/     # Ingestão de documentos
    │   ├── 📁 processing/    # Processamento de documentos
    │   ├── 📁 embeddings/    # Geração de embeddings
    │   ├── 📁 storage/       # Armazenamento (R2 + Astra DB)
    │   ├── 📁 retrieval/     # Busca e recuperação
    │   └── 📁 generation/    # Geração de respostas
    └── 📁 examples/          # Exemplos de uso
```

## 🔧 Componentes Implementados

### ✅ Ingestão de Documentos
- **Google Drive Downloader** - Download automático de arquivos do Google Drive
- **File Selector** - Seleção inteligente de arquivos com múltiplos critérios

### ✅ Processamento de Documentos  
- **LlamaParse Processor** - Processamento com LlamaParse + screenshots
- **Multimodal Merger** - Combinação de texto e imagens em chunks

### ✅ Sistema de Embeddings
- **Voyage Embedder** - Embeddings multimodais com Voyage AI

### ✅ Armazenamento
- **Cloudflare R2 Uploader** - Upload otimizado de imagens
- **Astra DB Inserter** - Inserção otimizada no Astra DB

### ✅ Sistema de Busca Modular
- **RAG Pipeline** - Pipeline completo de busca e resposta
- **Query Transformer** - Transformação inteligente de queries conversacionais
- **Vector Searcher** - Busca vetorial otimizada no Astra DB
- **Image Fetcher** - Busca de imagens do Cloudflare R2
- **Reranker** - Reordenação inteligente com GPT-4

## 📦 Dependências

```bash
pip install -r requirements.txt
```

### APIs Necessárias

1. **LlamaParse** - Processamento de documentos
2. **Voyage AI** - Embeddings multimodais  
3. **Cloudflare R2** - Armazenamento de imagens
4. **Astra DB** - Banco vetorial
5. **OpenAI** (opcional) - Para reranking e geração

## ⚙️ Configuração

### 1. Variáveis de Ambiente

Copie `.env.example` para `.env` e configure:

```bash
# APIs Externas
OPENAI_API_KEY=sk-your-openai-key-here
VOYAGE_API_KEY=pa-your-voyage-key-here
LLAMA_CLOUD_API_KEY=llx-your-llama-key-here

# APIs para Modo Multimodal LlamaParse (opcional, reduz custo)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_API_KEY=your-google-api-key-here

# Astra DB
ASTRA_DB_APPLICATION_TOKEN=AstraCS:your-token-here
ASTRA_DB_API_ENDPOINT=https://your-db.apps.astra.datastax.com
ASTRA_DB_KEYSPACE=default_keyspace
ASTRA_DB_COLLECTION=sistema_rag_docs

# Cloudflare R2
R2_ENDPOINT=https://your-worker.workers.dev
R2_AUTH_TOKEN=your-r2-token-here

# Google Drive Document
GOOGLE_DRIVE_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
```

### 2. Configuração do Astra DB

1. Crie um banco Astra DB
2. Crie uma coleção com dimensão **1024** (para Voyage AI)
3. Obtenha o token de aplicação e endpoint

### 3. Configuração do Cloudflare R2

#### 3.1. Criar o Worker

1. Acesse o [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Vá para **Workers & Pages** → **Create Application** → **Create Worker**
3. Substitua o código padrão pelo código abaixo:

```javascript
function isAuthorized(request, env) {
  const authHeader = request.headers.get("Authorization");
  return authHeader === `Bearer ${env.AUTH_TOKEN}`;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // Verificação de autenticação
    if (!isAuthorized(request, env)) {
      return new Response("Não autorizado", { status: 401 });
    }

    // Upload de imagem: /upload/<key>
    if (request.method === "PUT" && pathname.startsWith("/upload/")) {
      const key = decodeURIComponent(pathname.replace("/upload/", ""));
      const body = await request.arrayBuffer();
      await env.BUCKET.put(key, body);
      return new Response(`Upload feito: ${key}`, { status: 200 });
    }

    // Download de arquivo: /file/<key>
    if (request.method === "GET" && pathname.startsWith("/file/")) {
      const key = decodeURIComponent(pathname.replace("/file/", ""));
      try {
        const object = await env.BUCKET.get(key);
        if (!object) {
          return new Response("Arquivo não encontrado", { status: 404 });
        }
        // Detecta o content-type se possível
        const contentType = object.httpMetadata?.contentType || "image/jpeg";
        return new Response(object.body, {
          status: 200,
          headers: {
            "Content-Type": contentType,
            "Cache-Control": "public, max-age=31536000",
          }
        });
      } catch (e) {
        return new Response("Erro ao buscar arquivo", { status: 500 });
      }
    }

    // Delete por documento: /delete-doc/<docId>
    if (request.method === "DELETE" && pathname.startsWith("/delete-doc/")) {
      const docId = decodeURIComponent(pathname.replace("/delete-doc/", ""));
      const prefix = `${docId}_`;
      const list = await env.BUCKET.list({ prefix });

      const deletions = list.objects.map(obj => env.BUCKET.delete(obj.key));
      await Promise.all(deletions);

      return new Response(`Deletados ${list.objects.length} arquivos com prefixo: ${prefix}`, {
        status: 200,
      });
    }

    // Delete TODOS os arquivos: /delete-all
    if (request.method === "DELETE" && pathname === "/delete-all") {
      let totalDeleted = 0;
      let cursor = undefined;

      // Lista e deleta em batches (R2 retorna max 1000 por vez)
      do {
        const listResponse = await env.BUCKET.list({ cursor });

        if (listResponse.objects.length > 0) {
          const deletions = listResponse.objects.map(obj => env.BUCKET.delete(obj.key));
          await Promise.all(deletions);
          totalDeleted += listResponse.objects.length;
        }

        cursor = listResponse.truncated ? listResponse.cursor : undefined;
      } while (cursor);

      return new Response(`Deletados ${totalDeleted} arquivos do bucket`, {
        status: 200,
      });
    }

    // Listar arquivos por prefixo: /list/<prefix> (para dry run)
    if (request.method === "GET" && pathname.startsWith("/list/")) {
      const prefix = decodeURIComponent(pathname.replace("/list/", ""));
      const list = await env.BUCKET.list({ prefix: `${prefix}_` });

      const files = list.objects.map(obj => ({
        name: obj.key,
        size: obj.size,
        modified: obj.uploaded
      }));

      return new Response(JSON.stringify({
        files: files,
        count: files.length,
        total_size: files.reduce((sum, file) => sum + file.size, 0)
      }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    // Stats do bucket: /stats (para dry run delete-all)
    if (request.method === "GET" && pathname === "/stats") {
      let totalFiles = 0;
      let totalSize = 0;
      let cursor = undefined;

      // Lista todos os arquivos para contar
      do {
        const listResponse = await env.BUCKET.list({ cursor });
        totalFiles += listResponse.objects.length;
        totalSize += listResponse.objects.reduce((sum, obj) => sum + obj.size, 0);
        cursor = listResponse.truncated ? listResponse.cursor : undefined;
      } while (cursor);

      return new Response(JSON.stringify({
        total_files: totalFiles,
        total_size: totalSize
      }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });
    }

    return new Response(
      "Use PUT /upload/<nome>, DELETE /delete-doc/<docId>, DELETE /delete-all, GET /list/<prefix>, GET /stats, ou GET /file/<key>",
      { status: 400 }
    );
  }
}
```

#### 3.2. Configurar Variáveis de Ambiente

1. No painel do Worker, vá para **Settings** → **Variables**
2. Adicione a variável:
   - **Nome**: `AUTH_TOKEN`
   - **Valor**: Um token seguro (ex: `your-secret-token-123`)

#### 3.3. Criar Bucket R2

1. No Cloudflare Dashboard, vá para **R2 Object Storage**
2. Clique em **Create bucket**
3. Nomeie seu bucket (ex: `sistema-rag-images`)

#### 3.4. Associar Worker ao Bucket

1. No painel do Worker, vá para **Settings** → **Variables**
2. Na seção **R2 Bucket Bindings**, clique em **Add binding**
3. Configure:
   - **Variable name**: `BUCKET`
   - **R2 bucket**: Selecione o bucket criado

#### 3.5. Atualizar .env

No seu arquivo `.env`, configure:
```bash
R2_ENDPOINT=https://seu-worker.seu-subdominio.workers.dev
R2_AUTH_TOKEN=your-secret-token-123
```

### 4. Configuração do Google Drive

1. **Faça upload do seu documento** para o Google Drive
2. **Torne o documento público**:
   - Clique com o botão direito > "Compartilhar"
   - Clique em "Alterar para qualquer pessoa com o link"
   - Defina permissão como "Visualizador"
3. **Copie o link** e extraia o FILE_ID:
   ```
   https://drive.google.com/file/d/1EDArLh4yTTf43UP9ilmeKN02Yyl6rVyQ/view
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                            Este é o FILE_ID
   ```
4. **Configure no .env**:
   ```bash
   GOOGLE_DRIVE_URL=https://drive.google.com/file/d/SEU_FILE_ID/view
   ```

## 🚀 Uso Básico

### 📋 Comandos Principais

```bash
# 🚀 Ingestão de documentos
python ingestao.py

# 🔍 Busca/consulta
python busca.py
```

### 🧪 Comandos de Teste

```bash
# Teste rápido das APIs
python -m sistema_rag.run_pipeline test

# Pipeline completo de ingestão (alternativo)
python -m sistema_rag.run_pipeline

# Sistema de busca conversacional (avançado)
python -m sistema_rag.examples.conversational_rag
```

### 🔍 Sistema de Busca - Interface Simples

```python
from sistema_rag import SimpleRAG

# Criar interface
rag = SimpleRAG()

# Fazer perguntas
resposta = rag.search("Como funciona o Zep?")
print(resposta)

# Conversa com contexto
resposta = rag.search("E sobre sua performance?")
print(resposta)

# Extração de dados estruturados
template = {"title": "", "authors": [], "concepts": []}
dados = rag.extract(template)
print(dados)
```

### 🔧 Pipeline RAG Personalizado

```python
from sistema_rag import RAGPipeline

# Criar pipeline personalizado
pipeline = RAGPipeline(
    max_candidates=10,
    max_selected=2,
    enable_reranking=True,
    enable_image_fetching=True  # Cloudflare R2
)

# Buscar com histórico de conversa
chat_history = [
    {"role": "user", "content": "O que é o Zep?"},
    {"role": "assistant", "content": "O Zep é um sistema..."}
]

result = pipeline.search_and_answer(
    query="Como ele funciona?",
    chat_history=chat_history
)

print(result["answer"])
print(f"Documentos: {result['selected_pages']}")
print(f"Justificativa: {result['justification']}")
```

### 📱 Interface CLI Conversacional

```bash
python -m sistema_rag.examples.conversational_rag
```

**Comandos disponíveis:**
- `/help` - Ajuda
- `/clear` - Limpar histórico
- `/stats` - Estatísticas do sistema
- `/extract {"campo": ""}` - Extração de dados

## 🎯 Exemplo Prático

### Ingestão do Cardápio

```bash
# Processa cardápio American Burger
python ingestao.py
```

**Resultado:**
- ✅ 2 páginas processadas
- 🖼️ Imagens no Cloudflare R2
- 🧬 Embeddings no Astra DB

### Busca no Cardápio

```bash
# Busca itens do menu
python busca.py
```

**Exemplos de perguntas testadas:**
- 🍔 "hambúrguer de frango" → Score: 0.724
- 🍰 "sobremesas" → Score: 0.686
- 💰 "preços" → Score: 0.609
- 🥤 "bebidas" → Score: 0.628

### Modo Multimodal LlamaParse

O sistema suporta o novo modo multimodal do LlamaParse que gera screenshots automaticamente:

#### Configuração Básica (usando créditos LlamaParse)
```python
from sistema_rag.components.processing import LlamaParseProcessor

processor = LlamaParseProcessor.create_multimodal(
    api_key="llx-...",
    model_name="anthropic-sonnet-3.5"
)
```

#### Configuração Econômica (usando sua própria chave)
```python
processor = LlamaParseProcessor.create_multimodal(
    api_key="llx-...",
    model_name="anthropic-sonnet-3.5", 
    model_api_key="sk-ant-..."  # Reduz custo para ~$0.003/página
)
```

#### Modelos Disponíveis
- **Anthropic**: `anthropic-sonnet-3.5`, `anthropic-sonnet-3.7`, `anthropic-sonnet-4.0`
- **OpenAI**: `openai-gpt4o`, `openai-gpt-4o-mini`, `openai-gpt-4-1`
- **Google**: `gemini-2.0-flash-001`, `gemini-2.5-pro`, `gemini-1.5-pro`

Ou usando o módulo diretamente:

```python
from sistema_rag.examples.basic_usage import basic_rag_pipeline
import asyncio

# Executar pipeline completo
asyncio.run(basic_rag_pipeline())
```

### Uso por Componentes

#### Pipeline de Ingestão
```python
# 1. Download do Google Drive
from sistema_rag.components.ingestion import GoogleDriveDownloader

downloader = GoogleDriveDownloader()
files = downloader.download_files(["sua_url_aqui"])

# 2. Seleção de arquivo
from sistema_rag.components.ingestion import FileSelector

selector = FileSelector()
selected = selector.select_file(files, file_index=0)

# 3. Processamento com LlamaParse
from sistema_rag.components.processing import LlamaParseProcessor

processor = LlamaParseProcessor(api_key="sua_chave")
parsed_doc = processor.process_document(selected)
screenshots = processor.get_screenshots(parsed_doc.job_id)

# 4. Merge multimodal
from sistema_rag.components.processing import MultimodalMerger

merger = MultimodalMerger(merge_strategy="page_based")
chunks = merger.merge_content(parsed_doc, screenshots)

# 5. Embeddings
from sistema_rag.components.embeddings import VoyageEmbedder

embedder = VoyageEmbedder(api_key="sua_chave")
embedded_chunks = embedder.embed_chunks(chunks)

# 6. Upload para R2
from sistema_rag.components.storage import CloudflareR2Uploader

uploader = CloudflareR2Uploader(r2_endpoint="...", auth_token="...")
upload_result = uploader.upload_chunk_images(embedded_chunks)

# 7. Inserção no Astra DB
from sistema_rag.components.storage import AstraDBInserter

inserter = AstraDBInserter(api_endpoint="...", auth_token="...", collection_name="docs")
final_result = inserter.insert_chunks(upload_result["documents"])
```

#### Componentes de Busca
```python
# 1. Transformador de queries
from sistema_rag.components.retrieval import QueryTransformer

transformer = QueryTransformer()
chat_history = [{"role": "user", "content": "O que é isso?"}]
transformed = transformer.transform_query(chat_history)

# 2. Busca vetorial
from sistema_rag.components.retrieval import VectorSearcher

searcher = VectorSearcher()
search_results = searcher.search_by_text("query", embedding)

# 3. Busca de imagens R2
from sistema_rag.components.retrieval import ImageFetcher

fetcher = ImageFetcher()
enriched_results = fetcher.enrich_search_results(search_results)

# 4. Re-ranking
from sistema_rag.components.retrieval import SearchReranker

reranker = SearchReranker()
reranked = reranker.rerank_results("query", search_results)
```

## 🧪 Testes

### Teste Rápido das APIs

```bash
# Teste completo do sistema
python -m sistema_rag.run_pipeline test
```

### Diagnóstico de Problemas

```bash
# Verificar variáveis de ambiente
cat .env | grep -E "(VOYAGE|ASTRA|R2)"

# Testar componentes individualmente
python -c "
from dotenv import load_dotenv; load_dotenv()
from sistema_rag.components.retrieval import VectorSearcher
searcher = VectorSearcher()
print(searcher.test_connection().message)
"
```

## 📊 Estratégias de Chunking

### Page-based (Padrão)
- Um chunk por página
- Associação direta texto-imagem
- Ideal para documentos estruturados

### Section-based
- Chunks por cabeçalhos
- Estimativa de página por posição
- Ideal para documentos longos

### Smart Chunks
- Respeita limite de caracteres
- Divisão inteligente por parágrafos
- Distribuição proporcional de imagens

### Text-only / Image-only
- Processamento separado
- Para casos específicos

## 🔍 Características Técnicas

### Otimizações Implementadas

1. **Limpeza de Base64** - Remove campos base64 antes do Astra DB
2. **Truncamento Inteligente** - Limita texto preservando integridade
3. **Processamento em Lotes** - Otimiza chamadas de API
4. **URLs vs Base64** - Usa URLs para reduzir tamanho no DB
5. **Retry Logic** - Tratamento de erros e tentativas

### Limites e Considerações

- **Voyage AI**: 10 chunks por lote, 5000 chars por texto
- **Astra DB**: 100 docs por inserção, 7000 chars por campo texto
- **LlamaParse**: 100MB por arquivo, 300s timeout
- **Cloudflare R2**: Dependente da configuração do Worker

## 📝 Exemplos de Dados

### Chunk Multimodal Final

```json
{
  "_id": "documento_page_1",
  "content": "Conteúdo da página 1...",
  "$vector": [0.1, -0.2, 0.3, ...],
  "document_name": "documento",
  "page_number": 1,
  "image_url": "https://r2.example.com/file/documento_page_1.jpg",
  "metadata": {
    "document_name": "documento",
    "parse_mode": "parse_page_with_agent",
    "job_id": "abc123"
  }
}
```

## 📊 Performance e Melhorias

### ⚡ Otimizações Implementadas

| **Componente** | **Melhoria** | **Benefício** |
|----------------|--------------|---------------|
| **Arquitetura** | Modular | Escalabilidade e manutenibilidade |
| **Imagens** | Cloudflare R2 | URLs diretas vs base64 |
| **Cache** | Inteligente | Reduz chamadas de API |
| **Fallbacks** | Robustos | Alta disponibilidade |
| **Busca** | Vetorial + IA | Precisão otimizada |

### 🚀 Comandos Simplificados

**Sistema atual:**
```bash
# Ingestão
python ingestao.py

# Busca
python busca.py
```

### 📈 Resultados de Performance
- **Cache de Queries**: Reduz chamadas à IA em 60-80%
- **Classificação Determinística**: Evita IA para queries simples
- **Cache de Imagens**: Reduz downloads do R2
- **Re-ranking Otimizado**: Seleção mais precisa

## 🗺️ Status do Projeto

### ✅ Componentes Completos
- [x] **Sistema de Ingestão** - Pipeline completo com LlamaParse
- [x] **Sistema de Busca** - Busca vetorial multimodal
- [x] **Armazenamento** - Astra DB + Cloudflare R2
- [x] **Embeddings** - Voyage AI multimodal
- [x] **Cache Inteligente** - Otimizações de performance
- [x] **Arquitetura Modular** - Componentes independentes

### 🚧 Roadmap Futuro
- [ ] **Interface Web** - Dashboard para interação
- [ ] **Métricas Avançadas** - Monitoring e analytics
- [ ] **Multi-idioma** - Suporte a múltiplos idiomas
- [ ] **Embeddings Locais** - Opção open-source

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente seguindo a arquitetura modular
4. Adicione testes apropriados
5. Submeta um Pull Request

## 📄 Licença

MIT License - veja LICENSE para detalhes.

## 🆘 Suporte

### 🔧 Comandos de Diagnóstico

```bash
# Teste geral do sistema
python -m sistema_rag.run_pipeline test

# Verificar variáveis de ambiente
cat .env | grep -E "(VOYAGE|ASTRA|R2)"

# Testar busca específica
python busca.py
```

### 📞 Para Dúvidas

- **APIs**: Consulte documentação oficial de cada serviço
- **Configuração**: Verifique `.env.example` e variáveis
- **Erros**: Execute `python -m sistema_rag.run_pipeline test`
- **Performance**: Ajuste configurações no `sistema_rag/config/`

---

🔥 **Sistema RAG Multimodal - Arquitetura Modular Completa**
