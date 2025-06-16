# 🚀 Sistema RAG Multimodal - Python Puro

Sistema completo de RAG (Retrieval-Augmented Generation) multimodal implementado em Python puro, seguindo arquitetura modular e componente por componente.

## 📋 Visão Geral

Este sistema implementa um pipeline completo para processamento de documentos multimodais (texto + imagens) com capacidades de busca vetorial e geração de respostas contextualizadas.

### 🏗️ Arquitetura

```
📁 sistema_rag/
├── 📁 config/           # Configurações globais
├── 📁 models/           # Modelos de dados
├── 📁 utils/            # Utilitários e helpers
├── 📁 components/       # Componentes modulares
│   ├── 📁 ingestion/    # Ingestão de documentos
│   ├── 📁 processing/   # Processamento de documentos
│   ├── 📁 embeddings/   # Geração de embeddings
│   ├── 📁 storage/      # Armazenamento (R2 + Astra DB)
│   ├── 📁 retrieval/    # Busca e recuperação
│   └── 📁 generation/   # Geração de respostas
└── 📁 examples/         # Exemplos de uso
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

### 🚧 Em Desenvolvimento
- **Sistema de Busca** - Busca vetorial multimodal
- **Reranking** - Reordenação inteligente de resultados
- **Geração de Respostas** - Resposta final com contexto multimodal

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

# Astra DB
ASTRA_DB_APPLICATION_TOKEN=AstraCS:your-token-here
ASTRA_DB_API_ENDPOINT=https://your-db.apps.astra.datastax.com

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

1. Configure um Worker para R2
2. Implemente endpoints para upload/download/delete
3. Configure autenticação Bearer

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

### Pipeline Completo de Ingestão

```bash
# Executar pipeline completo
python run_pipeline.py

# Teste rápido das APIs
python run_pipeline.py test
```

Ou usando o módulo diretamente:

```python
from sistema_rag.examples.basic_usage import basic_rag_pipeline
import asyncio

# Executar pipeline completo
asyncio.run(basic_rag_pipeline())
```

### Uso por Componentes

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

## 🧪 Testes

### Teste Rápido das APIs

```bash
python -m sistema_rag.examples.basic_usage test
```

### Teste de Componente Individual

```python
# Testar conexões
from sistema_rag.components.storage import test_astra_connection, test_r2_connection

# Teste Astra DB
astra_test = test_astra_connection(endpoint, token, collection)
print(astra_test)

# Teste R2
r2_test = test_r2_connection(endpoint, token)
print(r2_test)
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

## 🗺️ Roadmap

- [ ] **Sistema de Busca Vetorial** - Busca multimodal no Astra DB
- [ ] **GPT Reranker** - Reordenação com GPT-4o
- [ ] **Enhanced Agent** - Geração de respostas contextualizadas
- [ ] **Interface Web** - Dashboard para interação
- [ ] **Cache Inteligente** - Cache de embeddings e resultados
- [ ] **Métricas** - Monitoring e analytics

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente seguindo a arquitetura modular
4. Adicione testes apropriados
5. Submeta um Pull Request

## 📄 Licença

MIT License - veja LICENSE para detalhes.

## 🆘 Suporte

Para dúvidas sobre:
- **APIs**: Consulte documentação oficial de cada serviço
- **Configuração**: Verifique `.env.example` e variáveis
- **Erros**: Execute teste rápido para diagnosticar conexões
- **Performance**: Ajuste batch_size e timeouts conforme necessário

---

🔥 **Sistema RAG Multimodal - Estado da Arte em Python Puro**