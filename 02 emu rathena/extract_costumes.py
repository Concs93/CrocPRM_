#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para extrair todos os costumes do item_db_equip.yml
e gerar uma lista para drop especial
"""

import re
import csv
import os

def extract_costumes():
    """Extrai todos os costumes do item_db_equip.yml"""
    
    costumes = []
    file_path = 'db/re/item_db_equip.yml'
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return costumes
    
    print(f"🔍 Processando: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Procurar por itens de equipamento
        item_pattern = r'- Id:\s*(\d+).*?AegisName:\s*(.+?)\n.*?Name:\s*(.+?)\n.*?Type:\s*(.+?)\n.*?SubType:\s*(.+?)\n.*?Location:\s*(.+?)\n.*?Buy:\s*(.+?)\n.*?Sell:\s*(.+?)\n.*?Weight:\s*(.+?)\n.*?Attack:\s*(.+?)\n.*?Defense:\s*(.+?)\n.*?Range:\s*(.+?)\n.*?Slots:\s*(.+?)\n.*?Job:\s*(.+?)\n.*?Upper:\s*(.+?)\n.*?Gender:\s*(.+?)\n.*?Locations:\s*(.+?)\n.*?WeaponLevel:\s*(.+?)\n.*?ArmorLevel:\s*(.+?)\n.*?EquipLevelMin:\s*(.+?)\n.*?EquipLevelMax:\s*(.+?)\n.*?Refineable:\s*(.+?)\n.*?Gradable:\s*(.+?)\n.*?View:\s*(.+?)\n.*?Script:\s*(.+?)(?=\n\s*- Id:|\n\s*$|\Z)'
        
        items = re.findall(item_pattern, content, re.DOTALL)
        
        for item_match in items:
            item_id, aegis_name, display_name, item_type, sub_type, location, buy, sell, weight, attack, defense, range, slots, job, upper, gender, locations, weapon_level, armor_level, equip_level_min, equip_level_max, refineable, gradable, view, script = item_match
            
            # Filtrar apenas costumes (Location: Costume)
            if 'Costume' in location or 'costume' in location.lower():
                # Extrair informações do View (sprite)
                view_info = view.strip()
                
                # Verificar se tem sprite válido (não vazio e não "None")
                if view_info and view_info != 'None' and view_info != '':
                    costumes.append({
                        'id': item_id.strip(),
                        'aegis_name': aegis_name.strip(),
                        'display_name': display_name.strip(),
                        'type': item_type.strip(),
                        'sub_type': sub_type.strip(),
                        'location': location.strip(),
                        'view': view_info,
                        'gender': gender.strip(),
                        'job': job.strip(),
                        'buy_price': buy.strip(),
                        'sell_price': sell.strip(),
                        'weight': weight.strip(),
                        'script': script.strip()[:200] + '...' if len(script.strip()) > 200 else script.strip()
                    })
        
        print(f"✅ Encontrados {len(costumes)} costumes com sprites válidos")
        
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
    
    return costumes

def categorize_costumes(costumes):
    """Categoriza os costumes por tipo"""
    categories = {
        'Head_Top': [],
        'Head_Mid': [],
        'Head_Low': [],
        'Armor': [],
        'Shield': [],
        'Garment': [],
        'Shoes': [],
        'Accessory': [],
        'Other': []
    }
    
    for costume in costumes:
        location = costume['location'].lower()
        
        if 'head' in location and 'top' in location:
            categories['Head_Top'].append(costume)
        elif 'head' in location and 'mid' in location:
            categories['Head_Mid'].append(costume)
        elif 'head' in location and 'low' in location:
            categories['Head_Low'].append(costume)
        elif 'armor' in location:
            categories['Armor'].append(costume)
        elif 'shield' in location:
            categories['Shield'].append(costume)
        elif 'garment' in location:
            categories['Garment'].append(costume)
        elif 'shoes' in location or 'foot' in location:
            categories['Shoes'].append(costume)
        elif 'accessory' in location:
            categories['Accessory'].append(costume)
        else:
            categories['Other'].append(costume)
    
    return categories

def generate_csv(costumes, filename='costumes_list.csv'):
    """Gera arquivo CSV com os costumes encontrados"""
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Item_ID', 'Aegis_Name', 'Display_Name', 'Type', 'SubType', 
            'Location', 'View_Sprite', 'Gender', 'Job', 'Buy_Price', 
            'Sell_Price', 'Weight', 'Script_Preview'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for costume in costumes:
            writer.writerow({
                'Item_ID': costume['id'],
                'Aegis_Name': costume['aegis_name'],
                'Display_Name': costume['display_name'],
                'Type': costume['type'],
                'SubType': costume['sub_type'],
                'Location': costume['location'],
                'View_Sprite': costume['view'],
                'Gender': costume['gender'],
                'Job': costume['job'],
                'Buy_Price': costume['buy_price'],
                'Sell_Price': costume['sell_price'],
                'Weight': costume['weight'],
                'Script_Preview': costume['script']
            })

def generate_categorized_csv(categories, filename='costumes_categorized.csv'):
    """Gera CSV categorizado por tipo de equipamento"""
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Category', 'Item_ID', 'Aegis_Name', 'Display_Name', 'View_Sprite', 'Gender', 'Job']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for category, items in categories.items():
            for item in items:
                writer.writerow({
                    'Category': category,
                    'Item_ID': item['id'],
                    'Aegis_Name': item['aegis_name'],
                    'Display_Name': item['display_name'],
                    'View_Sprite': item['view'],
                    'Gender': item['gender'],
                    'Job': item['job']
                })

def generate_drop_script(costumes, filename='costume_drop_script.txt'):
    """Gera script de exemplo para drop de costumes"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("// Script de exemplo para drop especial de costumes\n")
        f.write("// Substitui bDropAddRace por chance de drop de costume\n\n")
        
        f.write("// Lista de costumes disponíveis para drop\n")
        f.write("setarray .@costume_list[0], ")
        
        costume_ids = [costume['id'] for costume in costumes]
        for i, costume_id in enumerate(costume_ids):
            if i % 10 == 0 and i > 0:
                f.write("\n\t")
            f.write(f"{costume_id}")
            if i < len(costume_ids) - 1:
                f.write(", ")
        
        f.write(";\n\n")
        
        f.write("// Função para dropar costume aleatório\n")
        f.write("function script DropRandomCostume {\n")
        f.write("\t.@random = rand(getarraysize(.@costume_list));\n")
        f.write("\t.@costume_id = .@costume_list[.@random];\n")
        f.write("\tgetitem .@costume_id, 1;\n")
        f.write("\treturn .@costume_id;\n")
        f.write("}\n\n")
        
        f.write("// Exemplo de uso em item (substituir bDropAddRace)\n")
        f.write("// bonus_script \"{ if(rand(100) < 5) callfunc('DropRandomCostume'); }\", 100, 1, 0;\n")
        f.write("// Chance de 5% de dropar um costume aleatório\n\n")
        
        f.write(f"// Total de costumes disponíveis: {len(costumes)}\n")
        f.write("// Categorias:\n")
        
        categories = categorize_costumes(costumes)
        for category, items in categories.items():
            if items:
                f.write(f"// - {category}: {len(items)} itens\n")

def main():
    """Função principal"""
    print("👗 Procurando costumes no item_db_equip.yml...")
    
    costumes = extract_costumes()
    
    if not costumes:
        print("❌ Nenhum costume encontrado!")
        return
    
    # Categorizar costumes
    categories = categorize_costumes(costumes)
    
    # Gerar CSVs
    generate_csv(costumes)
    print("📊 Lista completa: costumes_list.csv")
    
    generate_categorized_csv(categories)
    print("📊 Lista categorizada: costumes_categorized.csv")
    
    # Gerar script de exemplo
    generate_drop_script(costumes)
    print("📝 Script de exemplo: costume_drop_script.txt")
    
    # Mostrar estatísticas
    print(f"\n📊 Estatísticas:")
    print(f"   Total de costumes: {len(costumes)}")
    for category, items in categories.items():
        if items:
            print(f"   - {category}: {len(items)} itens")
    
    # Mostrar alguns exemplos
    print(f"\n👗 Exemplos de costumes:")
    for i, costume in enumerate(costumes[:10]):
        print(f"   {i+1}. {costume['display_name']} (ID: {costume['id']}) - {costume['location']}")

if __name__ == "__main__":
    main()
