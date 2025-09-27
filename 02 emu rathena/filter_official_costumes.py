#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para filtrar apenas costumes oficiais (C_ e CH_)
"""

import csv

def filter_official_costumes():
    """Filtra costumes que começam com C_ ou CH_"""
    
    official_costumes = []
    filtered_out = []
    
    try:
        with open('costumes_complete.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                aegis_name = row['Aegis_Name']
                
                # Filtrar apenas costumes que começam com C_ ou CH_
                if aegis_name.startswith('C_') or aegis_name.startswith('CH_'):
                    official_costumes.append(row)
                else:
                    filtered_out.append(row)
        
        print(f"✅ Filtrados {len(official_costumes)} costumes oficiais")
        print(f"❌ Removidos {len(filtered_out)} costumes não oficiais")
        
    except Exception as e:
        print(f"❌ Erro ao processar CSV: {e}")
        return
    
    return official_costumes, filtered_out

def create_filtered_csv(official_costumes, filtered_out):
    """Cria CSVs com costumes filtrados"""
    
    # CSV com costumes oficiais
    with open('costumes_official.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Item_ID', 'Aegis_Name', 'Display_Name', 'View_Sprite', 'Costume_Type', 'Status'])
        
        for costume in official_costumes:
            writer.writerow([
                costume['Item_ID'],
                costume['Aegis_Name'],
                costume['Display_Name'],
                costume['View_Sprite'],
                costume['Costume_Type'],
                'Official'
            ])
    
    # CSV com costumes removidos
    with open('costumes_removed.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Item_ID', 'Aegis_Name', 'Display_Name', 'View_Sprite', 'Costume_Type', 'Status'])
        
        for costume in filtered_out:
            writer.writerow([
                costume['Item_ID'],
                costume['Aegis_Name'],
                costume['Display_Name'],
                costume['View_Sprite'],
                costume['Costume_Type'],
                'Removed'
            ])

def create_official_script(official_costumes):
    """Cria script com costumes oficiais"""
    
    with open('costume_official_script.txt', 'w', encoding='utf-8') as f:
        f.write("// Script para drop especial de costumes oficiais\n")
        f.write("// Apenas costumes que começam com C_ ou CH_\n\n")
        
        f.write("// Array com IDs dos costumes oficiais\n")
        f.write("setarray .@costume_ids[0], ")
        
        for i, costume in enumerate(official_costumes):
            f.write(costume['Item_ID'])
            if i < len(official_costumes) - 1:
                f.write(", ")
            if (i + 1) % 15 == 0:
                f.write("\n\t")
        
        f.write(";\n\n")
        
        f.write("// Função para dropar costume oficial aleatório\n")
        f.write("function script DropOfficialCostume {\n")
        f.write("\t.@random = rand(getarraysize(.@costume_ids));\n")
        f.write("\t.@costume_id = .@costume_ids[.@random];\n")
        f.write("\tgetitem .@costume_id, 1;\n")
        f.write("\treturn .@costume_id;\n")
        f.write("}\n\n")
        
        f.write("// Exemplo de uso (substituir bDropAddRace)\n")
        f.write("// bonus_script \"{ if(rand(100) < 3) callfunc('DropOfficialCostume'); }\", 100, 1, 0;\n")
        f.write("// Chance de 3% de dropar costume oficial aleatório\n\n")
        
        f.write(f"// Total: {len(official_costumes)} costumes oficiais\n")
        
        # Estatísticas por tipo
        types = {}
        for costume in official_costumes:
            t = costume['Costume_Type']
            types[t] = types.get(t, 0) + 1
        
        f.write("// Tipos de costume oficial:\n")
        for t, count in types.items():
            f.write(f"// - {t}: {count} itens\n")

def show_statistics(official_costumes, filtered_out):
    """Mostra estatísticas dos costumes"""
    
    print(f"\n📊 Estatísticas dos Costumes Oficiais:")
    
    # Por tipo
    types = {}
    for costume in official_costumes:
        t = costume['Costume_Type']
        types[t] = types.get(t, 0) + 1
    
    for t, count in types.items():
        print(f"   - {t}: {count} itens")
    
    print(f"\n👗 Primeiros 15 costumes oficiais:")
    for i, costume in enumerate(official_costumes[:15]):
        print(f"   {i+1:2d}. {costume['Display_Name']} (ID: {costume['Item_ID']}) - {costume['Costume_Type']}")
    
    print(f"\n❌ Exemplos de costumes removidos:")
    for i, costume in enumerate(filtered_out[:10]):
        print(f"   {i+1:2d}. {costume['Display_Name']} (ID: {costume['Item_ID']}) - {costume['Aegis_Name']}")

def main():
    print("🎯 Filtrando costumes oficiais (C_ e CH_)...")
    
    official_costumes, filtered_out = filter_official_costumes()
    
    if official_costumes:
        create_filtered_csv(official_costumes, filtered_out)
        create_official_script(official_costumes)
        show_statistics(official_costumes, filtered_out)
        
        print(f"\n📁 Arquivos gerados:")
        print(f"   - costumes_official.csv ({len(official_costumes)} itens)")
        print(f"   - costumes_removed.csv ({len(filtered_out)} itens)")
        print(f"   - costume_official_script.txt (script pronto)")
    else:
        print("❌ Nenhum costume oficial encontrado!")

if __name__ == "__main__":
    main()
