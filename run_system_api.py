#!/usr/bin/env python3
"""
Script de conveniência para executar a API do Sistema RAG

Executa: python -m system_rag.api.api
"""

import subprocess
import sys
import os

def main():
    """Executa a API do Sistema RAG"""
    try:
        print("🚀 Iniciando API do Sistema RAG...")
        print("📍 Porta: 8000")
        print("📚 Docs: http://localhost:8000/docs")
        print("🔐 Auth: Bearer Token required")
        print("=" * 50)
        
        # Executar API do sistema RAG
        result = subprocess.run([
            sys.executable, "-m", "system_rag.api.api"
        ], cwd=os.path.dirname(os.path.abspath(__file__)))
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n🛑 API interrompida pelo usuário")
        return 0
    except Exception as e:
        print(f"❌ Erro ao executar API: {e}")
        return 1

if __name__ == "__main__":
    exit(main())