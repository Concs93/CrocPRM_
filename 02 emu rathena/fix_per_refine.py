#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corrigir textos com "per refine" que foram alterados incorretamente
"""

import re
import shutil
import os
from datetime import datetime

def create_backup(file_path):
    """Cria backup do arquivo original"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"Backup criado: {backup_path}")
    return backup_path

def fix_per_refine_texts(file_path):
    """Corrige textos com 'per refine' que foram alterados incorretamente"""
    
    # Criar backup primeiro
    backup_path = create_backup(file_path)
    
    try:
        # Tentar diferentes encodings
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
        content = None
        detected_encoding = None
        
        for encoding in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                detected_encoding = encoding
                print(f"Encoding detectado: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            raise Exception("Nao foi possivel detectar o encoding do arquivo")
        
        print(f"Arquivo lido: {len(content)} caracteres")
        
        # Padrões para corrigir textos com "per refine"
        replacements = [
            # Corrigir textos que foram alterados incorretamente
            (r'\^00c000Visual item drop chance \+0\.1% per refine\^000000', r'^00c000Visual item drop chance +0.1%^000000'),
            (r'\^00c000\^00c000Visual item drop chance \+0\.1%\^000000 per refine', r'^00c000Visual item drop chance +0.1%^000000'),
            (r'\^00c000Visual item drop chance \+0\.1% per refine\^000000\.', r'^00c000Visual item drop chance +0.1%^000000.'),
        ]
        
        # Contadores
        total_replacements = 0
        replacement_stats = {}
        
        # Aplicar substituições
        for pattern, replacement in replacements:
            matches = re.findall(pattern, content)
            if matches:
                count = len(matches)
                replacement_stats[pattern] = count
                total_replacements += count
                content = re.sub(pattern, replacement, content)
                print(f"Correcao: {pattern[:50]}... -> {count} vezes")
        
        # Salvar arquivo atualizado
        with open(file_path, 'w', encoding=detected_encoding) as f:
            f.write(content)
        
        print(f"\nArquivo atualizado com sucesso!")
        print(f"Total de correcoes: {total_replacements}")
        print(f"Backup salvo em: {backup_path}")
        
        # Estatísticas detalhadas
        if replacement_stats:
            print(f"\nEstatisticas por padrao:")
            for pattern, count in replacement_stats.items():
                print(f"   {pattern[:60]}... -> {count} vezes")
        
        return True
        
    except Exception as e:
        print(f"ERRO durante a correcao: {e}")
        print(f"Restaurando backup...")
        
        # Restaurar backup em caso de erro
        try:
            shutil.copy2(backup_path, file_path)
            print(f"Backup restaurado com sucesso!")
        except Exception as restore_error:
            print(f"ERRO ao restaurar backup: {restore_error}")
        
        return False

def main():
    """Função principal"""
    file_path = r"E:\PRM\test\Return to Morroc Client\System\itemInfo_EN.lua"
    
    print("Iniciando correcao de textos com 'per refine'...")
    print(f"Arquivo: {file_path}")
    
    # Verificar se arquivo existe
    if not os.path.exists(file_path):
        print(f"ERRO: Arquivo nao encontrado: {file_path}")
        return
    
    # Confirmar operação
    print(f"\nATENCAO: Este script ira modificar o arquivo original!")
    print(f"Será criado um backup automatico antes da modificacao.")
    response = input("Deseja continuar? (s/N): ").lower().strip()
    
    if response not in ['s', 'sim', 'y', 'yes']:
        print("Operacao cancelada pelo usuario.")
        return
    
    # Executar correção
    success = fix_per_refine_texts(file_path)
    
    if success:
        print(f"\nCorrecao concluida com sucesso!")
        print(f"Dica: Verifique o arquivo antes de usar no jogo.")
    else:
        print(f"\nCorrecao falhou. Verifique os erros acima.")

if __name__ == "__main__":
    main()
