#!/usr/bin/env python3
"""
Script para comparar item_db_etc.yml local com o do repositório PRM-EMULATOR
"""

import requests
import yaml
import difflib
from pathlib import Path

def download_prm_file():
    """Baixa o arquivo item_db_etc.yml do repositório PRM-EMULATOR"""
    url = "https://raw.githubusercontent.com/zetsbr/PRM-EMULATOR/main/db/re/item_db_etc.yml"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Erro ao baixar arquivo: {e}")
        return None

def load_local_file():
    """Carrega o arquivo local item_db_etc.yml"""
    local_path = Path("db/re/item_db_etc.yml")
    if not local_path.exists():
        print(f"Arquivo local não encontrado: {local_path}")
        return None
    
    try:
        with open(local_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Erro ao ler arquivo local: {e}")
        return None

def compare_files():
    """Compara os dois arquivos e gera um diff"""
    print("🔍 Baixando arquivo do repositório PRM-EMULATOR...")
    prm_content = download_prm_file()
    
    if not prm_content:
        print("❌ Falha ao baixar arquivo do repositório")
        return
    
    print("📁 Carregando arquivo local...")
    local_content = load_local_file()
    
    if not local_content:
        print("❌ Falha ao carregar arquivo local")
        return
    
    print("🔍 Comparando arquivos...")
    
    # Salva o arquivo PRM para referência
    with open("item_db_etc_prm.yml", "w", encoding="utf-8") as f:
        f.write(prm_content)
    print("💾 Arquivo PRM salvo como: item_db_etc_prm.yml")
    
    # Gera diff
    local_lines = local_content.splitlines(keepends=True)
    prm_lines = prm_content.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        local_lines,
        prm_lines,
        fromfile="local/db/re/item_db_etc.yml",
        tofile="prm/db/re/item_db_etc.yml",
        lineterm=""
    )
    
    # Salva o diff
    diff_content = list(diff)
    if diff_content:
        with open("item_db_etc_diff.txt", "w", encoding="utf-8") as f:
            f.writelines(diff_content)
        print("📊 Diff salvo como: item_db_etc_diff.txt")
        print(f"📈 Total de linhas diferentes: {len([line for line in diff_content if line.startswith(('+', '-'))])}")
    else:
        print("✅ Arquivos são idênticos!")
    
    # Estatísticas básicas
    print(f"\n📊 Estatísticas:")
    print(f"   Local: {len(local_lines)} linhas")
    print(f"   PRM:   {len(prm_lines)} linhas")

if __name__ == "__main__":
    compare_files()
