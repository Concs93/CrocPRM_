#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair itens com bonus bDropAddRace do rAthena
e gerar um arquivo CSV com as informações
"""

import re
import csv
import os

def extract_drop_race_items():
    """Extrai itens com bonus bDropAddRace dos arquivos YAML do rAthena"""
    
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
                
                # Procurar por itens com bonus bDropAddRace usando regex
                # Padrão para encontrar blocos de item
                item_pattern = r'- Id:\s*(\d+).*?AegisName:\s*(.+?)\n.*?Name:\s*(.+?)\n.*?Script:\s*(.+?)(?=\n\s*- Id:|\n\s*$|\Z)'
                
                items = re.findall(item_pattern, content, re.DOTALL)
                
                for item_match in items:
                    item_id, aegis_name, display_name, script_content = item_match
                    
                    # Procurar por bonus bDropAddRace no script
                    drop_bonuses = []
                    
                    # Padrões para diferentes tipos de bonus de drop
                    patterns = [
                        (r'bDropAddRace,(\d+),(\d+)', 'drop_rate', 2),
                        (r'bDropAddRace,(\d+),(\d+),(\d+)', 'drop_rate_race', 3),
                        (r'bDropAddRace,(\d+),(\d+),(\d+),(\d+)', 'drop_rate_race_level', 4),
                        (r'bDropAddRace,(\d+),(\d+),(\d+),(\d+),(\d+)', 'drop_rate_race_level_type', 5),
                        (r'bDropAddRace,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', 'drop_rate_race_level_type_item', 6)
                    ]
                    
                    for pattern, bonus_type, num_groups in patterns:
                        matches = re.findall(pattern, script_content)
                        for match in matches:
                            if num_groups == 2:
                                drop_bonuses.append({
                                    'type': bonus_type,
                                    'race_id': match[0],
                                    'rate': match[1],
                                    'level': 'All',
                                    'type_id': 'All',
                                    'item_id': 'All'
                                })
                            elif num_groups == 3:
                                drop_bonuses.append({
                                    'type': bonus_type,
                                    'race_id': match[0],
                                    'rate': match[1],
                                    'level': match[2],
                                    'type_id': 'All',
                                    'item_id': 'All'
                                })
                            elif num_groups == 4:
                                drop_bonuses.append({
                                    'type': bonus_type,
                                    'race_id': match[0],
                                    'rate': match[1],
                                    'level': match[2],
                                    'type_id': match[3],
                                    'item_id': 'All'
                                })
                            elif num_groups == 5:
                                drop_bonuses.append({
                                    'type': bonus_type,
                                    'race_id': match[0],
                                    'rate': match[1],
                                    'level': match[2],
                                    'type_id': match[3],
                                    'item_id': match[4]
                                })
                            elif num_groups == 6:
                                drop_bonuses.append({
                                    'type': bonus_type,
                                    'race_id': match[0],
                                    'rate': match[1],
                                    'level': match[2],
                                    'type_id': match[3],
                                    'item_id': match[4]
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

def get_race_name(race_id):
    """Converte ID da raça para nome"""
    race_names = {
        '0': 'Formless',
        '1': 'Undead', 
        '2': 'Brute',
        '3': 'Plant',
        '4': 'Insect',
        '5': 'Fish',
        '6': 'Demon',
        '7': 'DemiHuman',
        '8': 'Angel',
        '9': 'Dragon',
        '10': 'All'
    }
    return race_names.get(race_id, f'Race_{race_id}')

def get_type_name(type_id):
    """Converte ID do tipo para nome"""
    type_names = {
        '0': 'Normal',
        '1': 'Boss',
        '2': 'Guardian',
        '3': 'All'
    }
    return type_names.get(type_id, f'Type_{type_id}')

def generate_csv(drop_items, filename='drop_race_items.csv'):
    """Gera arquivo CSV com os itens de drop encontrados"""
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Item_ID', 'Aegis_Name', 'Display_Name', 
            'Bonus_Type', 'Race_ID', 'Race_Name', 'Rate', 'Level', 'Type_ID', 'Type_Name', 'Item_ID_Target', 'Script_Example'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in drop_items:
            for bonus in item.get('drop_bonuses', []):
                race_name = get_race_name(bonus['race_id'])
                type_name = get_type_name(bonus['type_id'])
                
                # Gerar exemplo de script baseado no tipo
                if bonus['type'] == 'drop_rate':
                    script_example = f"bonus2 bDropAddRace,{bonus['race_id']},{bonus['rate']}"
                elif bonus['type'] == 'drop_rate_race':
                    script_example = f"bonus3 bDropAddRace,{bonus['race_id']},{bonus['rate']},{bonus['level']}"
                elif bonus['type'] == 'drop_rate_race_level':
                    script_example = f"bonus4 bDropAddRace,{bonus['race_id']},{bonus['rate']},{bonus['level']},{bonus['type_id']}"
                elif bonus['type'] == 'drop_rate_race_level_type':
                    script_example = f"bonus5 bDropAddRace,{bonus['race_id']},{bonus['rate']},{bonus['level']},{bonus['type_id']},{bonus['item_id']}"
                elif bonus['type'] == 'drop_rate_race_level_type_item':
                    script_example = f"bonus6 bDropAddRace,{bonus['race_id']},{bonus['rate']},{bonus['level']},{bonus['type_id']},{bonus['item_id']}"
                else:
                    script_example = "Unknown"
                
                writer.writerow({
                    'Item_ID': item.get('id', ''),
                    'Aegis_Name': item.get('aegis_name', ''),
                    'Display_Name': item.get('display_name', ''),
                    'Bonus_Type': bonus.get('type', ''),
                    'Race_ID': bonus.get('race_id', ''),
                    'Race_Name': race_name,
                    'Rate': bonus.get('rate', ''),
                    'Level': bonus.get('level', ''),
                    'Type_ID': bonus.get('type_id', ''),
                    'Type_Name': type_name,
                    'Item_ID_Target': bonus.get('item_id', ''),
                    'Script_Example': script_example
                })

def create_summary_csv(drop_items, filename='drop_race_summary.csv'):
    """Cria um resumo dos itens por categoria"""
    
    # Agrupar por tipo de bonus
    summary = {}
    for item in drop_items:
        for bonus in item.get('drop_bonuses', []):
            bonus_type = bonus['type']
            if bonus_type not in summary:
                summary[bonus_type] = {
                    'count': 0,
                    'items': set(),
                    'total_rates': 0,
                    'races': set()
                }
            
            summary[bonus_type]['count'] += 1
            summary[bonus_type]['items'].add(item['id'])
            summary[bonus_type]['races'].add(bonus['race_id'])
            try:
                summary[bonus_type]['total_rates'] += int(bonus['rate'])
            except:
                pass
    
    # Criar CSV de resumo
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Bonus_Type', 'Item_Count', 'Unique_Items', 'Avg_Rate', 'Races_Affected', 'Description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for bonus_type, data in summary.items():
            avg_rate = data['total_rates'] / data['count'] if data['count'] > 0 else 0
            
            description = ""
            if bonus_type == 'drop_rate':
                description = "Aumenta taxa de drop geral"
            elif bonus_type == 'drop_rate_race':
                description = "Aumenta taxa de drop por raça e nível"
            elif bonus_type == 'drop_rate_race_level':
                description = "Aumenta taxa de drop por raça, nível e tipo"
            elif bonus_type == 'drop_rate_race_level_type':
                description = "Aumenta taxa de drop por raça, nível, tipo e item"
            elif bonus_type == 'drop_rate_race_level_type_item':
                description = "Aumenta taxa de drop específica por todos os parâmetros"
            
            writer.writerow({
                'Bonus_Type': bonus_type,
                'Item_Count': data['count'],
                'Unique_Items': len(data['items']),
                'Avg_Rate': round(avg_rate, 2),
                'Races_Affected': len(data['races']),
                'Description': description
            })
    
    print(f"📊 Resumo criado: {filename}")

def main():
    """Função principal"""
    print("🔍 Procurando itens com bonus bDropAddRace no rAthena...")
    
    drop_items = extract_drop_race_items()
    
    print(f"✅ Encontrados {len(drop_items)} itens com bonus bDropAddRace")
    
    # Gerar CSV
    generate_csv(drop_items)
    print("📊 Arquivo CSV gerado: drop_race_items.csv")
    
    # Criar resumo
    create_summary_csv(drop_items)
    
    # Mostrar alguns exemplos
    print("\n📋 Exemplos encontrados:")
    for i, item in enumerate(drop_items[:10]):
        print(f"{i+1}. ID: {item.get('id', 'N/A')} - {item.get('display_name', 'N/A')}")
        for bonus in item.get('drop_bonuses', []):
            race_name = get_race_name(bonus['race_id'])
            print(f"   - {bonus['type']}: Raça {race_name} (Rate: {bonus['rate']}, Level: {bonus['level']})")

if __name__ == "__main__":
    main()
