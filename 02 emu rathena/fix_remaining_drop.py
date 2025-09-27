#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir o último bDropAddRace restante
"""

import re

def fix_remaining_drop():
    """Corrige o último bDropAddRace restante"""
    
    file_path = 'db/re/item_db_equip.yml'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Padrão específico para o caso restante
        pattern = r'(\s+)bonus2\s+bDropAddRace,RC_All,2\*\(\.@r\);\s*\n'
        replacement = r'\1// bonus2 bDropAddRace,RC_All,2*(.@r); // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;\n'
        
        # Fazer a substituição
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            # Salvar arquivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Último bDropAddRace corrigido!")
            return True
        else:
            print("ℹ️  Nenhuma correção necessária")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    fix_remaining_drop()
