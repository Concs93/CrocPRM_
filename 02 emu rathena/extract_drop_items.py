#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair itens com bonus de drop do rAthena
e gerar um arquivo CSV com as informações
"""

import re
import yaml
import csv
import os

def extract_drop_items():
    """Extrai itens com bonus de drop dos arquivos YAML do rAthena"""
    
    # Padrões para identificar bonus de drop
    drop_patterns = [
        r'bAddMonsterDropItem,(\d+),(\d+)',
        r'bAddMonsterDropItem,(\d+),(\d+),(\d+)',
        r'bAddMonsterDropItem,(\d+),RC_(\w+),(\d+)',
        r'bAddMonsterDropItemGroup,IG_(\w+),(\d+)',
        r'bAddMonsterDropCard,(\d+),(\d+)',
        r'bAddMonsterDropCardRate,(\d+),(\d+)',
        r'bAddMonsterDropItemRate,(\d+),(\d+)'
    ]
    
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
                    
                # Procurar por itens com bonus de drop
                lines = content.split('\n')
                current_item = None
                
                for i, line in enumerate(lines):
                    # Detectar início de um item
                    if line.strip().startswith('- Id:') or line.strip().startswith('Id:'):
                        current_item = {}
                        # Extrair ID do item
                        id_match = re.search(r'Id:\s*(\d+)', line)
                        if id_match:
                            current_item['id'] = id_match.group(1)
                    
                    # Detectar nome do item
                    elif line.strip().startswith('AegisName:') and current_item:
                        name_match = re.search(r'AegisName:\s*(.+)', line)
                        if name_match:
                            current_item['aegis_name'] = name_match.group(1).strip()
                    
                    # Detectar nome display
                    elif line.strip().startswith('Name:') and current_item:
                        display_match = re.search(r'Name:\s*(.+)', line)
                        if display_match:
                            current_item['display_name'] = display_match.group(1).strip()
                    
                    # Procurar por bonus de drop
                    elif 'Script:' in line and current_item:
                        script_content = line
                        # Continuar lendo se a linha Script: não termina
                        j = i + 1
                        while j < len(lines) and not lines[j].strip().startswith('- ') and not lines[j].strip().startswith('Id:') and lines[j].strip():
                            script_content += ' ' + lines[j].strip()
                            j += 1
                        
                        # Verificar se contém bonus de drop
                        for pattern in drop_patterns:
                            matches = re.findall(pattern, script_content)
                            if matches:
                                if 'drop_bonuses' not in current_item:
                                    current_item['drop_bonuses'] = []
                                
                                for match in matches:
                                    if len(match) == 2:
                                        current_item['drop_bonuses'].append({
                                            'type': 'item',
                                            'item_id': match[0],
                                            'rate': match[1],
                                            'race': 'All'
                                        })
                                    elif len(match) == 3:
                                        if match[1].startswith('RC_'):
                                            current_item['drop_bonuses'].append({
                                                'type': 'item',
                                                'item_id': match[0],
                                                'rate': match[2],
                                                'race': match[1]
                                            })
                                        else:
                                            current_item['drop_bonuses'].append({
                                                'type': 'item',
                                                'item_id': match[0],
                                                'rate': match[1],
                                                'race': 'All'
                                            })
                                    elif len(match) == 4:
                                        current_item['drop_bonuses'].append({
                                            'type': 'item',
                                            'item_id': match[0],
                                            'rate': match[2],
                                            'race': match[1]
                                        })
                
                # Adicionar itens encontrados à lista
                if current_item and 'drop_bonuses' in current_item:
                    drop_items.append(current_item)
                    
            except Exception as e:
                print(f"Erro ao processar {file_path}: {e}")
                continue
    
    return drop_items

def generate_csv(drop_items, filename='drop_items.csv'):
    """Gera arquivo CSV com os itens de drop encontrados"""
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Item_ID', 'Aegis_Name', 'Display_Name', 
            'Drop_Type', 'Target_Item_ID', 'Rate', 'Race', 'Script_Line'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in drop_items:
            for bonus in item.get('drop_bonuses', []):
                writer.writerow({
                    'Item_ID': item.get('id', ''),
                    'Aegis_Name': item.get('aegis_name', ''),
                    'Display_Name': item.get('display_name', ''),
                    'Drop_Type': bonus.get('type', ''),
                    'Target_Item_ID': bonus.get('item_id', ''),
                    'Rate': bonus.get('rate', ''),
                    'Race': bonus.get('race', ''),
                    'Script_Line': f"bonus2 bAddMonsterDropItem,{bonus.get('item_id', '')},{bonus.get('rate', '')}"
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
    for i, item in enumerate(drop_items[:5]):
        print(f"{i+1}. ID: {item.get('id', 'N/A')} - {item.get('display_name', 'N/A')}")
        for bonus in item.get('drop_bonuses', []):
            print(f"   - {bonus['type']}: Item {bonus['item_id']} (Rate: {bonus['rate']}, Race: {bonus['race']})")

if __name__ == "__main__":
    main()
