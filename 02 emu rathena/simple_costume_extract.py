#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para extrair costumes
"""

import re

def extract_costumes():
    """Extrai costumes de forma simples"""
    
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
        
        print(f"✅ Encontrados {len(costumes)} costumes")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return costumes

def main():
    print("👗 Extraindo costumes...")
    
    costumes = extract_costumes()
    
    if costumes:
        print(f"\n👗 Primeiros 20 costumes:")
        for i, costume in enumerate(costumes[:20]):
            print(f"   {i+1:2d}. {costume['display_name']} (ID: {costume['id']}) - {costume['type']}")
        
        # Salvar em arquivo simples
        with open('costumes_simple.txt', 'w', encoding='utf-8') as f:
            f.write("// Lista de costumes para drop especial\n")
            f.write("setarray .@costume_ids[0], ")
            
            for i, costume in enumerate(costumes):
                f.write(costume['id'])
                if i < len(costumes) - 1:
                    f.write(", ")
                if (i + 1) % 15 == 0:
                    f.write("\n\t")
            
            f.write(";\n\n")
            f.write(f"// Total: {len(costumes)} costumes\n")
        
        print(f"\n📝 Arquivo gerado: costumes_simple.txt")
        print(f"📊 Total: {len(costumes)} costumes encontrados")
    else:
        print("❌ Nenhum costume encontrado!")

if __name__ == "__main__":
    main()
