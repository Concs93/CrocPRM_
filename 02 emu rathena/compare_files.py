#!/usr/bin/env python3
"""
Script para comparar item_db_etc.yml local com o baixado do zetsbr
"""

import difflib
from pathlib import Path

def compare_files():
    """Compara os dois arquivos e gera um diff"""
    print("Comparando arquivos...")
    
    # Caminhos dos arquivos
    local_path = Path("E:/PRM/test/02 emu rathena/db/re/item_db_etc.yml")
    zets_path = Path("c:/Users/User/Downloads/item_db_etc_zets.yml")
    
    # Verifica se os arquivos existem
    if not local_path.exists():
        print(f"ERRO: Arquivo local nao encontrado: {local_path}")
        return
    
    if not zets_path.exists():
        print(f"ERRO: Arquivo zets nao encontrado: {zets_path}")
        return
    
    # Carrega os arquivos
    try:
        with open(local_path, 'r', encoding='utf-8') as f:
            local_content = f.read()
        print(f"OK: Arquivo local carregado: {len(local_content.splitlines())} linhas")
    except Exception as e:
        print(f"ERRO: Erro ao ler arquivo local: {e}")
        return
    
    try:
        with open(zets_path, 'r', encoding='utf-8') as f:
            zets_content = f.read()
        print(f"OK: Arquivo zets carregado: {len(zets_content.splitlines())} linhas")
    except Exception as e:
        print(f"ERRO: Erro ao ler arquivo zets: {e}")
        return
    
    # Gera diff
    local_lines = local_content.splitlines(keepends=True)
    zets_lines = zets_content.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        local_lines,
        zets_lines,
        fromfile="local/db/re/item_db_etc.yml",
        tofile="zets/db/re/item_db_etc.yml",
        lineterm=""
    )
    
    # Salva o diff
    diff_content = list(diff)
    if diff_content:
        with open("item_db_etc_diff.txt", "w", encoding="utf-8") as f:
            f.writelines(diff_content)
        print("Diff salvo como: item_db_etc_diff.txt")
        
        # Conta diferenças
        additions = len([line for line in diff_content if line.startswith('+') and not line.startswith('+++')])
        deletions = len([line for line in diff_content if line.startswith('-') and not line.startswith('---')])
        
        print(f"Estatisticas do diff:")
        print(f"   + Adicoes: {additions} linhas")
        print(f"   - Remocoes: {deletions} linhas")
        print(f"   = Total de mudancas: {additions + deletions} linhas")
        
        # Mostra as primeiras 20 linhas do diff
        print(f"\nPrimeiras 20 linhas do diff:")
        for i, line in enumerate(diff_content[:20]):
            print(f"{i+1:2d}: {line.rstrip()}")
        
        if len(diff_content) > 20:
            print(f"   ... e mais {len(diff_content) - 20} linhas")
            
    else:
        print("Arquivos sao identicos!")
    
    # Estatísticas básicas
    print(f"\nEstatisticas dos arquivos:")
    print(f"   Local: {len(local_lines)} linhas")
    print(f"   Zets:  {len(zets_lines)} linhas")

if __name__ == "__main__":
    compare_files()
