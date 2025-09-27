#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair itens com bonus de drop do rAthena
e gerar um arquivo CSV com as informações
"""

import re
import csv
import os

def extract_drop_items():
    """Extrai itens com bonus de drop dos arquivos YAML do rAthena"""
    
    # Lista para armazenar os itens encontrados
    drop_items = []
    
    # Diretórios para procurar
    db_dirs = ['db/re', 'db/pre-re', 'db/import']
    
    for db_dir in db_dirs:
        if not os.path.exists(db_dir):
            continue
            
        # Arquivos YAML para processar
        yaml_files = [
            'item_db_etc.yml',
            'item_db_equip.yml',
            'item_db.yml'
        ]
        
        for yaml_file in yaml_files:
            file_path = os.path.join(db_dir, yaml_file)
            if not os.path.exists(file_path):
                continue
                
            print(f"Processando: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Procurar por itens com bonus de drop usando regex
                # Padrão para encontrar blocos de item
                item_pattern = r'- Id:\s*(\d+).*?AegisName:\s*(.+?)\n.*?Name:\s*(.+?)\n.*?Script:\s*(.+?)(?=\n\s*- Id:|\n\s*$|\Z)'
                
                items = re.findall(item_pattern, content, re.DOTALL)
                
                for item_match in items:
                    item_id, aegis_name, display_name, script_content = item_match
                    
                    # Procurar por bonus de drop no script
                    drop_bonuses = []
                    
                    # Padrões para diferentes tipos de bonus de drop
                    patterns = [
                        (r'bAddMonsterDropItem,(\d+),(\d+)', 'item', 2),
                        (r'bAddMonsterDropItem,(\d+),(\d+),(\d+)', 'item', 3),
                        (r'bAddMonsterDropItem,(\d+),RC_(\w+),(\d+)', 'item_race', 3),
                        (r'bAddMonsterDropItemGroup,IG_(\w+),(\d+)', 'item_group', 2),
                        (r'bAddMonsterDropCard,(\d+),(\d+)', 'card', 2),
                        (r'bAddMonsterDropCardRate,(\d+),(\d+)', 'card_rate', 2),
                        (r'bAddMonsterDropItemRate,(\d+),(\d+)', 'item_rate', 2)
                    ]
                    
                    for pattern, bonus_type, num_groups in patterns:
                        matches = re.findall(pattern, script_content)
                        for match in matches:
                            if num_groups == 2:
                                drop_bonuses.append({
                                    'type': bonus_type,
                                    'target_id': match[0],
                                    'rate': match[1],
                                    'race': 'All'
                                })
                            elif num_groups == 3:
                                if bonus_type == 'item_race':
                                    drop_bonuses.append({
                                        'type': 'item',
                                        'target_id': match[0],
                                        'rate': match[2],
                                        'race': f"RC_{match[1]}"
                                    })
                                else:
                                    drop_bonuses.append({
                                        'type': bonus_type,
                                        'target_id': match[0],
                                        'rate': match[1],
                                        'race': 'All'
                                    })
                    
                    if drop_bonuses:
                        drop_items.append({
                            'id': item_id.strip(),
                            'aegis_name': aegis_name.strip(),
                            'display_name': display_name.strip(),
                            'drop_bonuses': drop_bonuses
                        })
                        
            except Exception as e:
                print(f"Erro ao processar {file_path}: {e}")
                continue
    
    return drop_items

def generate_csv(drop_items, filename='drop_items.csv'):
    """Gera arquivo CSV com os itens de drop encontrados"""
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Item_ID', 'Aegis_Name', 'Display_Name', 
            'Drop_Type', 'Target_Item_ID', 'Rate', 'Race', 'Script_Example'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in drop_items:
            for bonus in item.get('drop_bonuses', []):
                # Gerar exemplo de script baseado no tipo
                if bonus['type'] == 'item':
                    script_example = f"bonus2 bAddMonsterDropItem,{bonus['target_id']},{bonus['rate']}"
                elif bonus['type'] == 'item_race':
                    script_example = f"bonus3 bAddMonsterDropItem,{bonus['target_id']},{bonus['race']},{bonus['rate']}"
                elif bonus['type'] == 'item_group':
                    script_example = f"bonus2 bAddMonsterDropItemGroup,IG_{bonus['target_id']},{bonus['rate']}"
                elif bonus['type'] == 'card':
                    script_example = f"bonus2 bAddMonsterDropCard,{bonus['target_id']},{bonus['rate']}"
                elif bonus['type'] == 'card_rate':
                    script_example = f"bonus2 bAddMonsterDropCardRate,{bonus['target_id']},{bonus['rate']}"
                elif bonus['type'] == 'item_rate':
                    script_example = f"bonus2 bAddMonsterDropItemRate,{bonus['target_id']},{bonus['rate']}"
                else:
                    script_example = "Unknown"
                
                writer.writerow({
                    'Item_ID': item.get('id', ''),
                    'Aegis_Name': item.get('aegis_name', ''),
                    'Display_Name': item.get('display_name', ''),
                    'Drop_Type': bonus.get('type', ''),
                    'Target_Item_ID': bonus.get('target_id', ''),
                    'Rate': bonus.get('rate', ''),
                    'Race': bonus.get('race', ''),
                    'Script_Example': script_example
                })

def main():
    """Função principal"""
    print("🔍 Procurando itens com bonus de drop no rAthena...")
    
    drop_items = extract_drop_items()
    
    print(f"✅ Encontrados {len(drop_items)} itens com bonus de drop")
    
    # Gerar CSV
    generate_csv(drop_items)
    print("📊 Arquivo CSV gerado: drop_items.csv")
    
    # Mostrar alguns exemplos
    print("\n📋 Exemplos encontrados:")
    for i, item in enumerate(drop_items[:10]):
        print(f"{i+1}. ID: {item.get('id', 'N/A')} - {item.get('display_name', 'N/A')}")
        for bonus in item.get('drop_bonuses', []):
            print(f"   - {bonus['type']}: Item {bonus['target_id']} (Rate: {bonus['rate']}, Race: {bonus['race']})")

if __name__ == "__main__":
    main()
