#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para extrair costumes do item_db_equip.yml
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
        
        # Procurar por itens com Location: Costume
        pattern = r'Id:\s*(\d+).*?AegisName:\s*(.+?)\n.*?Name:\s*(.+?)\n.*?Location:\s*Costume.*?View:\s*(.+?)\n'
        
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            item_id, aegis_name, display_name, view = match
            
            # Verificar se tem sprite válido
            view_clean = view.strip()
            if view_clean and view_clean != 'None' and view_clean != '':
                costumes.append({
                    'id': item_id.strip(),
                    'aegis_name': aegis_name.strip(),
                    'display_name': display_name.strip(),
                    'view': view_clean
                })
        
        print(f"✅ Encontrados {len(costumes)} costumes")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return costumes

def generate_csv(costumes):
    """Gera CSV com os costumes"""
    
    with open('costumes_simple.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Item_ID', 'Aegis_Name', 'Display_Name', 'View_Sprite'])
        
        for costume in costumes:
            writer.writerow([
                costume['id'],
                costume['aegis_name'],
                costume['display_name'],
                costume['view']
            ])

def generate_script(costumes):
    """Gera script de drop de costumes"""
    
    with open('costume_drop_script.txt', 'w', encoding='utf-8') as f:
        f.write("// Script para drop especial de costumes\n\n")
        
        f.write("// Array com IDs dos costumes\n")
        f.write("setarray .@costume_ids[0], ")
        
        for i, costume in enumerate(costumes):
            f.write(costume['id'])
            if i < len(costumes) - 1:
                f.write(", ")
            if (i + 1) % 10 == 0:
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
        f.write("// bonus_script \"{ if(rand(100) < 3) callfunc('DropRandomCostume'); }\", 100, 1, 0;\n")
        f.write("// Chance de 3% de dropar costume aleatório\n\n")
        
        f.write(f"// Total: {len(costumes)} costumes disponíveis\n")

def main():
    print("👗 Extraindo costumes...")
    
    costumes = extract_costumes()
    
    if costumes:
        generate_csv(costumes)
        generate_script(costumes)
        print("📊 Arquivos gerados: costumes_simple.csv, costume_drop_script.txt")
        
        print(f"\n👗 Primeiros 10 costumes:")
        for i, costume in enumerate(costumes[:10]):
            print(f"   {i+1}. {costume['display_name']} (ID: {costume['id']})")
    else:
        print("❌ Nenhum costume encontrado!")

if __name__ == "__main__":
    main()
