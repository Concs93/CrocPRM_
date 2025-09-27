#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para substituir bDropAddRace de forma limpa, evitando duplicatas
"""

import re
import os

def clean_replace_drop_bonuses(file_path):
    """Substitui bDropAddRace de forma limpa, evitando duplicatas"""
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Padrão mais específico para evitar duplicatas
        # Procura por linhas que NÃO estão comentadas e contêm bDropAddRace
        patterns = [
            # Padrão principal: bonus2/3 bDropAddRace que não está comentado
            (r'^(\s+)bonus([23])\s+bDropAddRace,RC_All,([^;]+);\s*$', 
             r'\1// bonus\2 bDropAddRace,RC_All,\3; // Comentado - substituído por drop visual\n\1bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;'),
        ]
        
        replacements_made = 0
        
        for pattern, replacement in patterns:
            # Usar re.MULTILINE para ^ e $ funcionarem corretamente
            matches = re.findall(pattern, content, re.MULTILINE)
            if matches:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                replacements_made += len(matches)
                print(f"   ✅ {len(matches)} substituições com padrão: {pattern}")
        
        # Verificar se houve mudanças
        if content != original_content:
            # Fazer backup
            backup_path = file_path + '.clean_backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Salvar arquivo modificado
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {file_path}: {replacements_made} substituições feitas")
            print(f"   📁 Backup limpo salvo em: {backup_path}")
            return True
        else:
            print(f"ℹ️  {file_path}: Nenhuma substituição necessária")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao processar {file_path}: {e}")
        return False

def verify_no_duplicates(file_path):
    """Verifica se não há duplicatas de bonus_script"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Contar linhas com bonus_script TryVisualDrop
        count = content.count('bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;')
        
        # Verificar se há linhas duplicadas consecutivas
        lines = content.split('\n')
        consecutive_duplicates = 0
        
        for i in range(len(lines) - 1):
            if ('bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;' in lines[i] and 
                'bonus_script "{ callfunc(\'TryVisualDrop\'); }", 100, 1, 0;' in lines[i + 1]):
                consecutive_duplicates += 1
        
        print(f"   📊 Total de bonus_script: {count}")
        print(f"   ⚠️  Duplicatas consecutivas: {consecutive_duplicates}")
        
        return consecutive_duplicates == 0
        
    except Exception as e:
        print(f"❌ Erro ao verificar {file_path}: {e}")
        return False

def main():
    print("🔄 Substituindo bDropAddRace de forma limpa...")
    
    files_to_process = [
        'db/re/item_db_etc.yml',
        'db/re/item_db_equip.yml'
    ]
    
    total_replacements = 0
    
    for file_path in files_to_process:
        print(f"\n📁 Processando: {file_path}")
        if clean_replace_drop_bonuses(file_path):
            total_replacements += 1
            
            # Verificar duplicatas
            print(f"🔍 Verificando duplicatas em {file_path}...")
            if verify_no_duplicates(file_path):
                print(f"   ✅ Sem duplicatas encontradas")
            else:
                print(f"   ⚠️  Duplicatas encontradas - verificar manualmente")
    
    print(f"\n📊 Resumo:")
    print(f"   ✅ Arquivos processados: {len(files_to_process)}")
    print(f"   ✅ Arquivos modificados: {total_replacements}")
    print(f"   📁 Backups limpos criados")
    
    print(f"\n🎯 Próximos passos:")
    print(f"   1. Verificar se não há duplicatas")
    print(f"   2. Testar o sistema de drop visual")
    print(f"   3. Ajustar chances conforme necessário")

if __name__ == "__main__":
    main()
