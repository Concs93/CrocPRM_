#!/usr/bin/env python3
"""
Script para analisar diferenças entre itens nos arquivos item_db_etc.yml
"""

import yaml
from pathlib import Path
from collections import defaultdict

def load_yaml_file(file_path):
    """Carrega um arquivo YAML e retorna o conteúdo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ERRO ao carregar {file_path}: {e}")
        return None

def analyze_items():
    """Analisa as diferenças entre os itens dos dois arquivos"""
    print("Analisando diferencas entre itens...")
    
    # Caminhos dos arquivos
    local_path = Path("E:/PRM/test/02 emu rathena/db/re/item_db_etc.yml")
    zets_path = Path("c:/Users/User/Downloads/item_db_etc_zets.yml")
    
    # Carrega os arquivos
    print("Carregando arquivo local...")
    local_data = load_yaml_file(local_path)
    if not local_data:
        return
    
    print("Carregando arquivo zets...")
    zets_data = load_yaml_file(zets_path)
    if not zets_data:
        return
    
    # Cria dicionários para facilitar a busca
    local_items = {}
    zets_items = {}
    
    # Processa itens locais
    if 'Body' in local_data:
        for item in local_data['Body']:
            if 'Id' in item:
                local_items[item['Id']] = item
    
    # Processa itens zets
    if 'Body' in zets_data:
        for item in zets_data['Body']:
            if 'Id' in item:
                zets_items[item['Id']] = item
    
    print(f"Local: {len(local_items)} itens")
    print(f"Zets:  {len(zets_items)} itens")
    
    # Encontra diferenças
    only_in_local = []
    only_in_zets = []
    different_items = []
    
    # Itens que existem apenas no local
    for item_id in local_items:
        if item_id not in zets_items:
            only_in_local.append(item_id)
    
    # Itens que existem apenas no zets
    for item_id in zets_items:
        if item_id not in local_items:
            only_in_zets.append(item_id)
    
    # Itens que existem em ambos mas são diferentes
    for item_id in local_items:
        if item_id in zets_items:
            local_item = local_items[item_id]
            zets_item = zets_items[item_id]
            
            # Compara os itens (ignora ordem das chaves)
            if local_item != zets_item:
                different_items.append(item_id)
    
    # Gera relatório
    with open("item_analysis_report.txt", "w", encoding="utf-8") as f:
        f.write("RELATORIO DE ANALISE DE ITENS\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"RESUMO:\n")
        f.write(f"- Itens apenas no LOCAL: {len(only_in_local)}\n")
        f.write(f"- Itens apenas no ZETS: {len(only_in_zets)}\n")
        f.write(f"- Itens diferentes: {len(different_items)}\n")
        f.write(f"- Total de diferencas: {len(only_in_local) + len(only_in_zets) + len(different_items)}\n\n")
        
        # Itens apenas no local
        if only_in_local:
            f.write("ITENS APENAS NO LOCAL:\n")
            f.write("-" * 30 + "\n")
            for item_id in sorted(only_in_local):
                item = local_items[item_id]
                name = item.get('AegisName', 'N/A')
                f.write(f"ID: {item_id} - {name}\n")
            f.write("\n")
        
        # Itens apenas no zets
        if only_in_zets:
            f.write("ITENS APENAS NO ZETS:\n")
            f.write("-" * 30 + "\n")
            for item_id in sorted(only_in_zets):
                item = zets_items[item_id]
                name = item.get('AegisName', 'N/A')
                f.write(f"ID: {item_id} - {name}\n")
            f.write("\n")
        
        # Itens diferentes
        if different_items:
            f.write("ITENS DIFERENTES:\n")
            f.write("-" * 30 + "\n")
            for item_id in sorted(different_items):
                local_item = local_items[item_id]
                zets_item = zets_items[item_id]
                name = local_item.get('AegisName', 'N/A')
                f.write(f"ID: {item_id} - {name}\n")
                
                # Mostra as diferenças específicas
                local_keys = set(local_item.keys())
                zets_keys = set(zets_item.keys())
                
                # Chaves que existem apenas no local
                only_local_keys = local_keys - zets_keys
                if only_local_keys:
                    f.write(f"  Chaves apenas no LOCAL: {', '.join(sorted(only_local_keys))}\n")
                
                # Chaves que existem apenas no zets
                only_zets_keys = zets_keys - local_keys
                if only_zets_keys:
                    f.write(f"  Chaves apenas no ZETS: {', '.join(sorted(only_zets_keys))}\n")
                
                # Chaves com valores diferentes
                common_keys = local_keys & zets_keys
                for key in sorted(common_keys):
                    if local_item[key] != zets_item[key]:
                        f.write(f"  {key}:\n")
                        f.write(f"    LOCAL: {local_item[key]}\n")
                        f.write(f"    ZETS:  {zets_item[key]}\n")
                
                f.write("\n")
    
    print(f"\nRelatorio salvo como: item_analysis_report.txt")
    print(f"\nRESUMO:")
    print(f"- Itens apenas no LOCAL: {len(only_in_local)}")
    print(f"- Itens apenas no ZETS: {len(only_in_zets)}")
    print(f"- Itens diferentes: {len(different_items)}")
    print(f"- Total de diferencas: {len(only_in_local) + len(only_in_zets) + len(different_items)}")
    
    # Mostra alguns exemplos
    if only_in_zets:
        print(f"\nExemplos de itens apenas no ZETS:")
        for item_id in sorted(only_in_zets)[:5]:
            item = zets_items[item_id]
            name = item.get('AegisName', 'N/A')
            print(f"  ID: {item_id} - {name}")
        if len(only_in_zets) > 5:
            print(f"  ... e mais {len(only_in_zets) - 5} itens")

if __name__ == "__main__":
    analyze_items()
