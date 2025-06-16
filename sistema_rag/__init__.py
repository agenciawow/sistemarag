"""
Sistema RAG Multimodal - Arquitetura Modular

Este sistema implementa um pipeline completo de RAG (Retrieval-Augmented Generation)
com suporte a documentos multimodais, incluindo texto e imagens.

Componentes principais:
- Ingestion: Download e processamento de documentos
- Processing: Parsing e chunking multimodal
- Embeddings: Geração de embeddings multimodais
- Storage: Armazenamento em Astra DB e Cloudflare R2
- Retrieval: Busca vetorial e reranking
- Generation: Resposta final com contexto multimodal
"""

__version__ = "1.0.0"
__author__ = "Sistema RAG Team"