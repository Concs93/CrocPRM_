#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar um CSV melhorado com informações dos itens de drop
"""

import csv
import re

def load_item_names():
    """Carrega nomes dos itens dos arquivos YAML"""
    item_names = {}
    
    # Procurar em todos os arquivos YAML
    yaml_files = [
        'db/re/item_db_etc.yml',
        'db/re/item_db_equip.yml', 
        'db/pre-re/item_db_etc.yml',
        'db/pre-re/item_db_equip.yml'
    ]
    
    for file_path in yaml_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair nomes dos itens
            pattern = r'Id:\s*(\d+).*?AegisName:\s*(.+?)\n.*?Name:\s*(.+?)\n'
            matches = re.findall(pattern, content, re.DOTALL)
            
            for item_id, aegis_name, display_name in matches:
                item_names[item_id.strip()] = {
                    'aegis_name': aegis_name.strip(),
                    'display_name': display_name.strip()
                }
                
        except Exception as e:
            print(f"Erro ao carregar {file_path}: {e}")
            continue
    
    return item_names

def create_enhanced_csv():
    """Cria CSV melhorado com informações dos itens alvo"""
    
    # Carregar nomes dos itens
    print("📚 Carregando nomes dos itens...")
    item_names = load_item_names()
    
    # Ler CSV original
    with open('drop_items.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Criar CSV melhorado
    with open('drop_items_enhanced.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'Item_ID', 'Item_Aegis_Name', 'Item_Display_Name',
            'Drop_Type', 'Target_Item_ID', 'Target_Item_Name', 'Target_Item_Aegis',
            'Rate', 'Race', 'Script_Example', 'Notes'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in rows:
            target_id = row['Target_Item_ID']
            target_info = item_names.get(target_id, {})
            
            # Determinar notas baseadas no tipo de drop
            notes = ""
            if row['Drop_Type'] == 'item':
                if row['Race'] == 'All':
                    notes = "Aumenta drop de item específico de todos os monstros"
                else:
                    notes = f"Aumenta drop de item específico de monstros da raça {row['Race']}"
            elif row['Drop_Type'] == 'item_group':
                notes = f"Aumenta drop de itens do grupo {row['Target_Item_ID']}"
            elif row['Drop_Type'] == 'card':
                notes = "Aumenta drop de cartas"
            elif row['Drop_Type'] == 'card_rate':
                notes = "Aumenta taxa de drop de cartas"
            elif row['Drop_Type'] == 'item_rate':
                notes = "Aumenta taxa de drop de itens"
            
            writer.writerow({
                'Item_ID': row['Item_ID'],
                'Item_Aegis_Name': row['Aegis_Name'],
                'Item_Display_Name': row['Display_Name'],
                'Drop_Type': row['Drop_Type'],
                'Target_Item_ID': target_id,
                'Target_Item_Name': target_info.get('display_name', 'Unknown Item'),
                'Target_Item_Aegis': target_info.get('aegis_name', 'Unknown_Aegis'),
                'Rate': row['Rate'],
                'Race': row['Race'],
                'Script_Example': row['Script_Example'],
                'Notes': notes
            })
    
    print("✅ CSV melhorado criado: drop_items_enhanced.csv")

def create_summary_csv():
    """Cria um resumo dos itens por categoria"""
    
    with open('drop_items.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Agrupar por tipo de drop
    summary = {}
    for row in rows:
        drop_type = row['Drop_Type']
        if drop_type not in summary:
            summary[drop_type] = {
                'count': 0,
                'items': set(),
                'total_rates': 0
            }
        
        summary[drop_type]['count'] += 1
        summary[drop_type]['items'].add(row['Item_ID'])
        try:
            summary[drop_type]['total_rates'] += int(row['Rate'])
        except:
            pass
    
    # Criar CSV de resumo
    with open('drop_items_summary.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Drop_Type', 'Item_Count', 'Unique_Items', 'Avg_Rate', 'Description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for drop_type, data in summary.items():
            avg_rate = data['total_rates'] / data['count'] if data['count'] > 0 else 0
            
            description = ""
            if drop_type == 'item':
                description = "Aumenta drop de itens específicos"
            elif drop_type == 'item_group':
                description = "Aumenta drop de grupos de itens"
            elif drop_type == 'card':
                description = "Aumenta drop de cartas"
            elif drop_type == 'card_rate':
                description = "Aumenta taxa de drop de cartas"
            elif drop_type == 'item_rate':
                description = "Aumenta taxa de drop de itens"
            
            writer.writerow({
                'Drop_Type': drop_type,
                'Item_Count': data['count'],
                'Unique_Items': len(data['items']),
                'Avg_Rate': round(avg_rate, 2),
                'Description': description
            })
    
    print("📊 Resumo criado: drop_items_summary.csv")

def main():
    """Função principal"""
    print("🔧 Criando CSV melhorado dos itens de drop...")
    
    create_enhanced_csv()
    create_summary_csv()
    
    print("\n📋 Arquivos gerados:")
    print("  - drop_items.csv (original)")
    print("  - drop_items_enhanced.csv (com nomes dos itens alvo)")
    print("  - drop_items_summary.csv (resumo por categoria)")

if __name__ == "__main__":
    main()
