#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir TODOS os bDropAddRace restantes
"""

import re

def fix_all_remaining():
    """Corrige todos os bDropAddRace restantes"""
    
    files = ['db/re/item_db_etc.yml', 'db/re/item_db_equip.yml']
    
    for file_path in files:
        print(f"🔧 Processando: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Padrões restantes
            patterns = [
                # bonus2 bDropAddRace,RC_All,-50;
                (r'(\s+)bonus2\s+bDropAddRace,RC_All,-(\d+);', r'\1// bonus2 bDropAddRace,RC_All,-\2; // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;'),
                
                # bonus2 bDropAddRace,RC_All,.@r/2;
                (r'(\s+)bonus2\s+bDropAddRace,RC_All,\.@(\w+)/2;', r'\1// bonus2 bDropAddRace,RC_All,.\2/2; // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;'),
                
                # bonus2 bDropAddRace,RC_All,3*.@r;
                (r'(\s+)bonus2\s+bDropAddRace,RC_All,(\d+)\*\.@(\w+);', r'\1// bonus2 bDropAddRace,RC_All,\2*.\3; // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;'),
            ]
            
            replacements_made = 0
            
            for pattern, replacement in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, replacement, content)
                    replacements_made += len(matches)
                    print(f"   ✅ {len(matches)} substituições com padrão: {pattern}")
            
            if content != original_content:
                # Salvar arquivo modificado
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ {file_path}: {replacements_made} substituições feitas")
            else:
                print(f"ℹ️  {file_path}: Nenhuma substituição necessária")
                
        except Exception as e:
            print(f"❌ Erro ao processar {file_path}: {e}")

if __name__ == "__main__":
    fix_all_remaining()
    print("\n🎯 Verificação final...")
    
    # Verificar se ainda há bDropAddRace ativos
    import subprocess
    result1 = subprocess.run(['grep', '-c', 'bonus[23] bDropAddRace', 'db/re/item_db_etc.yml'], capture_output=True, text=True)
    result2 = subprocess.run(['grep', '-c', 'bonus[23] bDropAddRace', 'db/re/item_db_equip.yml'], capture_output=True, text=True)
    
    total_remaining = int(result1.stdout.strip()) + int(result2.stdout.strip())
    print(f"📊 Total de bDropAddRace restantes: {total_remaining}")
    
    if total_remaining == 0:
        print("🎉 Todos os bDropAddRace foram substituídos!")
    else:
        print("⚠️  Ainda há bDropAddRace restantes - verificar manualmente")
