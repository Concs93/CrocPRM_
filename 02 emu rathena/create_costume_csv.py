#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar CSV organizado dos costumes
"""

import csv

def create_costume_csv():
    """Cria CSV organizado dos costumes"""
    
    # Ler o arquivo de costumes
    costumes = []
    file_path = 'db/re/item_db_equip.yml'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_item = {}
        in_costume = False
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Detectar início de item
            if line.startswith('- Id:'):
                current_item = {'id': line.split(':')[1].strip()}
                in_costume = False
            
            # Detectar nome
            elif line.startswith('AegisName:') and current_item:
                current_item['aegis_name'] = line.split(':', 1)[1].strip()
            
            elif line.startswith('Name:') and current_item:
                current_item['display_name'] = line.split(':', 1)[1].strip()
            
            elif line.startswith('View:') and current_item:
                current_item['view'] = line.split(':', 1)[1].strip()
            
            # Detectar se é costume
            elif 'Costume_Head_Top: true' in line or 'Costume_Head_Mid: true' in line or 'Costume_Head_Low: true' in line or 'Costume_Garment: true' in line:
                in_costume = True
                if 'Head_Top' in line:
                    current_item['type'] = 'Head_Top'
                elif 'Head_Mid' in line:
                    current_item['type'] = 'Head_Mid'
                elif 'Head_Low' in line:
                    current_item['type'] = 'Head_Low'
                elif 'Garment' in line:
                    current_item['type'] = 'Garment'
            
            # Se é costume e tem view válido, adicionar
            elif in_costume and current_item and 'view' in current_item:
                view = current_item['view']
                if view and view != 'None' and view != '':
                    costumes.append(current_item.copy())
                current_item = {}
                in_costume = False
        
        print(f"✅ Processados {len(costumes)} costumes")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    # Criar CSV
    with open('costumes_complete.csv', 'w', newline='', encoding='utf-8') as f:
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
    
    # Criar script de drop
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
    
    # Estatísticas
    types = {}
    for costume in costumes:
        t = costume['type']
        types[t] = types.get(t, 0) + 1
    
    print(f"\n📊 Estatísticas:")
    print(f"   Total de costumes: {len(costumes)}")
    for t, count in types.items():
        print(f"   - {t}: {count} itens")
    
    print(f"\n📁 Arquivos gerados:")
    print(f"   - costumes_complete.csv")
    print(f"   - costume_drop_script.txt")

if __name__ == "__main__":
    create_costume_csv()
