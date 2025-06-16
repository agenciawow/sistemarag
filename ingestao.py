#!/usr/bin/env python3
"""Script dedicado para ingestão - equivale ao antigo ingestao.py"""

import asyncio
from sistema_rag.examples.basic_usage import basic_rag_pipeline

if __name__ == "__main__":
    print("🚀 Iniciando Ingestão RAG Modular...")
    asyncio.run(basic_rag_pipeline())