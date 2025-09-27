#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para substituir bDropAddRace pela nova função de drop visual
"""

import re
import os

def replace_drop_bonuses_in_file(file_path):
    """Substitui bDropAddRace pela nova função em um arquivo"""
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Padrões para encontrar bDropAddRace
        patterns = [
            # bonus2 bDropAddRace,RC_All,50;
            (r'(\s+)bonus2\s+bDropAddRace,RC_All,(\d+);', r'\1// bonus2 bDropAddRace,RC_All,\2; // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;'),
            
            # bonus3 bDropAddRace,RC_All,50;
            (r'(\s+)bonus3\s+bDropAddRace,RC_All,(\d+);', r'\1// bonus3 bDropAddRace,RC_All,\2; // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;'),
            
            # bonus2 bDropAddRace,RC_All,50,100;
            (r'(\s+)bonus2\s+bDropAddRace,RC_All,(\d+),(\d+);', r'\1// bonus2 bDropAddRace,RC_All,\2,\3; // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;'),
            
            # bonus3 bDropAddRace,RC_All,50,100;
            (r'(\s+)bonus3\s+bDropAddRace,RC_All,(\d+),(\d+);', r'\1// bonus3 bDropAddRace,RC_All,\2,\3; // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;'),
        ]
        
        replacements_made = 0
        
        for pattern, replacement in patterns:
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, replacement, content)
                replacements_made += len(matches)
                print(f"   ✅ {len(matches)} substituições com padrão: {pattern}")
        
        # Verificar se houve mudanças
        if content != original_content:
            # Fazer backup
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Salvar arquivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {file_path}: {replacements_made} substituições feitas")
            print(f"   📁 Backup salvo em: {backup_path}")
            return True
        else:
            print(f"ℹ️  {file_path}: Nenhuma substituição necessária")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False

def main():
    print("🔄 Substituindo bDropAddRace pela nova função de drop visual...")
    
    files_to_process = [
        'db/re/item_db_etc.yml',
        'db/re/item_db_equip.yml'
    ]
    
    total_replacements = 0
    
    for file_path in files_to_process:
        print(f"\n📁 Processando: {file_path}")
        if replace_drop_bonuses_in_file(file_path):
            total_replacements += 1
    
    print(f"\n📊 Resumo:")
    print(f"   ✅ Arquivos processados: {len(files_to_process)}")
    print(f"   ✅ Arquivos modificados: {total_replacements}")
    print(f"   📁 Backups criados para segurança")
    
    print(f"\n🎯 Próximos passos:")
    print(f"   1. Verificar os arquivos modificados")
    print(f"   2. Testar o sistema de drop visual")
    print(f"   3. Ajustar chances conforme necessário")

if __name__ == "__main__":
    main()
