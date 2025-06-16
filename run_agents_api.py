#!/usr/bin/env python3
"""
Script de conveniência para executar a API de agents

Executa: python -m agents.api.main
"""

import subprocess
import sys
import os

def main():
    """Executa a API de agents"""
    try:
        print("🚀 Iniciando API de Agents...")
        print("📍 Porta: 8001")
        print("📚 Docs: http://localhost:8001/docs")
        print("🔐 Auth: Bearer Token required")
        print("=" * 50)
        
        # Executar API de agents
        result = subprocess.run([
            sys.executable, "-m", "agents.api.main"
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