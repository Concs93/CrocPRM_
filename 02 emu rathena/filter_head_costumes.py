#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para filtrar apenas costumes de cabeça (remover garments)
"""

import csv

def filter_head_costumes():
    """Filtra apenas costumes de cabeça (Head_Top, Head_Mid, Head_Low)"""
    
    head_costumes = []
    garments_removed = []
    
    try:
        with open('costumes_official.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                costume_type = row['Costume_Type']
                
                # Manter apenas costumes de cabeça
                if costume_type in ['Head_Top', 'Head_Mid', 'Head_Low']:
                    head_costumes.append(row)
                else:
                    garments_removed.append(row)
        
        print(f"✅ Mantidos {len(head_costumes)} costumes de cabeça")
        print(f"❌ Removidos {len(garments_removed)} garments")
        
    except Exception as e:
        print(f"❌ Erro ao processar CSV: {e}")
        return
    
    return head_costumes, garments_removed

def create_filtered_csv(head_costumes, garments_removed):
    """Cria CSVs com costumes filtrados"""
    
    # CSV com costumes de cabeça
    with open('costumes_head_only.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Item_ID', 'Aegis_Name', 'Display_Name', 'View_Sprite', 'Costume_Type', 'Status'])
        
        for costume in head_costumes:
            writer.writerow([
                costume['Item_ID'],
                costume['Aegis_Name'],
                costume['Display_Name'],
                costume['View_Sprite'],
                costume['Costume_Type'],
                'Head_Only'
            ])
    
    # CSV com garments removidos
    with open('costumes_garments_removed.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Item_ID', 'Aegis_Name', 'Display_Name', 'View_Sprite', 'Costume_Type', 'Status'])
        
        for costume in garments_removed:
            writer.writerow([
                costume['Item_ID'],
                costume['Aegis_Name'],
                costume['Display_Name'],
                costume['View_Sprite'],
                costume['Costume_Type'],
                'Garment_Removed'
            ])

def create_head_script(head_costumes):
    """Cria script com costumes de cabeça"""
    
    with open('costume_head_script.txt', 'w', encoding='utf-8') as f:
        f.write("// Script para drop especial de costumes de cabeça\n")
        f.write("// Apenas Head_Top, Head_Mid, Head_Low (sem garments)\n\n")
        
        f.write("// Array com IDs dos costumes de cabeça\n")
        f.write("setarray .@costume_ids[0], ")
        
        for i, costume in enumerate(head_costumes):
            f.write(costume['Item_ID'])
            if i < len(head_costumes) - 1:
                f.write(", ")
            if (i + 1) % 15 == 0:
                f.write("\n\t")
        
        f.write(";\n\n")
        
        f.write("// Função para dropar costume de cabeça aleatório\n")
        f.write("function script DropHeadCostume {\n")
        f.write("\t.@random = rand(getarraysize(.@costume_ids));\n")
        f.write("\t.@costume_id = .@costume_ids[.@random];\n")
        f.write("\tgetitem .@costume_id, 1;\n")
        f.write("\treturn .@costume_id;\n")
        f.write("}\n\n")
        
        f.write("// Exemplo de uso (substituir bDropAddRace)\n")
        f.write("// bonus_script \"{ if(rand(100) < 3) callfunc('DropHeadCostume'); }\", 100, 1, 0;\n")
        f.write("// Chance de 3% de dropar costume de cabeça aleatório\n\n")
        
        f.write(f"// Total: {len(head_costumes)} costumes de cabeça\n")
        
        # Estatísticas por tipo
        types = {}
        for costume in head_costumes:
            t = costume['Costume_Type']
            types[t] = types.get(t, 0) + 1
        
        f.write("// Tipos de costume de cabeça:\n")
        for t, count in types.items():
            f.write(f"// - {t}: {count} itens\n")

def show_statistics(head_costumes, garments_removed):
    """Mostra estatísticas dos costumes"""
    
    print(f"\n📊 Estatísticas dos Costumes de Cabeça:")
    
    # Por tipo
    types = {}
    for costume in head_costumes:
        t = costume['Costume_Type']
        types[t] = types.get(t, 0) + 1
    
    for t, count in types.items():
        print(f"   - {t}: {count} itens")
    
    print(f"\n👗 Primeiros 15 costumes de cabeça:")
    for i, costume in enumerate(head_costumes[:15]):
        print(f"   {i+1:2d}. {costume['Display_Name']} (ID: {costume['Item_ID']}) - {costume['Costume_Type']}")
    
    print(f"\n❌ Garments removidos:")
    for i, costume in enumerate(garments_removed):
        print(f"   {i+1:2d}. {costume['Display_Name']} (ID: {costume['Item_ID']}) - {costume['Costume_Type']}")

def main():
    print("🎯 Filtrando costumes de cabeça (removendo garments)...")
    
    head_costumes, garments_removed = filter_head_costumes()
    
    if head_costumes:
        create_filtered_csv(head_costumes, garments_removed)
        create_head_script(head_costumes)
        show_statistics(head_costumes, garments_removed)
        
        print(f"\n📁 Arquivos gerados:")
        print(f"   - costumes_head_only.csv ({len(head_costumes)} itens)")
        print(f"   - costumes_garments_removed.csv ({len(garments_removed)} itens)")
        print(f"   - costume_head_script.txt (script pronto)")
    else:
        print("❌ Nenhum costume de cabeça encontrado!")

if __name__ == "__main__":
    main()
