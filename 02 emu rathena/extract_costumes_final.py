#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script final para extrair costumes do item_db_equip.yml
"""

import re
import csv

def extract_costumes():
    """Extrai costumes do item_db_equip.yml"""
    
    costumes = []
    file_path = 'db/re/item_db_equip.yml'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Procurar por itens que têm Costume_*: true
        pattern = r'Id:\s*(\d+).*?AegisName:\s*(.+?)\n.*?Name:\s*(.+?)\n.*?View:\s*(.+?)\n.*?Costume_(Head_Top|Head_Mid|Head_Low|Garment):\s*true'
        
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            item_id, aegis_name, display_name, view, costume_type = match
            
            # Verificar se tem sprite válido
            view_clean = view.strip()
            if view_clean and view_clean != 'None' and view_clean != '':
                costumes.append({
                    'id': item_id.strip(),
                    'aegis_name': aegis_name.strip(),
                    'display_name': display_name.strip(),
                    'view': view_clean,
                    'type': costume_type.strip()
                })
        
        print(f"✅ Encontrados {len(costumes)} costumes")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return costumes

def generate_csv(costumes):
    """Gera CSV com os costumes"""
    
    with open('costumes_final.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Item_ID', 'Aegis_Name', 'Display_Name', 'View_Sprite', 'Costume_Type'])
        
        for costume in costumes:
            writer.writerow([
                costume['id'],
                costume['aegis_name'],
                costume['display_name'],
                costume['view'],
                costume['type']
            ])

def generate_script(costumes):
    """Gera script de drop de costumes"""
    
    with open('costume_drop_script.txt', 'w', encoding='utf-8') as f:
        f.write("// Script para drop especial de costumes\n")
        f.write("// Substitui bDropAddRace por chance de drop de costume\n\n")
        
        f.write("// Array com IDs dos costumes\n")
        f.write("setarray .@costume_ids[0], ")
        
        for i, costume in enumerate(costumes):
            f.write(costume['id'])
            if i < len(costumes) - 1:
                f.write(", ")
            if (i + 1) % 15 == 0:
                f.write("\n\t")
        
        f.write(";\n\n")
        
        f.write("// Função para dropar costume aleatório\n")
        f.write("function script DropRandomCostume {\n")
        f.write("\t.@random = rand(getarraysize(.@costume_ids));\n")
        f.write("\t.@costume_id = .@costume_ids[.@random];\n")
        f.write("\tgetitem .@costume_id, 1;\n")
        f.write("\treturn .@costume_id;\n")
        f.write("}\n\n")
        
        f.write("// Exemplo de uso (substituir bDropAddRace)\n")
        f.write("// bonus_script \"{ if(rand(100) < 2) callfunc('DropRandomCostume'); }\", 100, 1, 0;\n")
        f.write("// Chance de 2% de dropar costume aleatório\n\n")
        
        f.write(f"// Total: {len(costumes)} costumes disponíveis\n")
        
        # Estatísticas por tipo
        types = {}
        for costume in costumes:
            t = costume['type']
            types[t] = types.get(t, 0) + 1
        
        f.write("// Tipos de costume:\n")
        for t, count in types.items():
            f.write(f"// - {t}: {count} itens\n")

def main():
    print("👗 Extraindo costumes do item_db_equip.yml...")
    
    costumes = extract_costumes()
    
    if costumes:
        generate_csv(costumes)
        generate_script(costumes)
        print("📊 Arquivos gerados: costumes_final.csv, costume_drop_script.txt")
        
        print(f"\n👗 Primeiros 15 costumes:")
        for i, costume in enumerate(costumes[:15]):
            print(f"   {i+1:2d}. {costume['display_name']} (ID: {costume['id']}) - {costume['type']}")
        
        # Estatísticas
        types = {}
        for costume in costumes:
            t = costume['type']
            types[t] = types.get(t, 0) + 1
        
        print(f"\n📊 Estatísticas por tipo:")
        for t, count in types.items():
            print(f"   - {t}: {count} itens")
    else:
        print("❌ Nenhum costume encontrado!")

if __name__ == "__main__":
    main()
