#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para implementar sistema de drop visual configurável
"""

import csv
import re

def create_visual_drop_system():
    """Cria sistema completo de drop visual"""
    
    with open('visual_drop_system_complete.txt', 'w', encoding='utf-8') as f:
        f.write("// ===== SISTEMA DE DROP VISUAL CONFIGURÁVEL =====\n")
        f.write("// Base: 0.05% + Refino: +0.01% por nível (ajustável por item)\n\n")
        
        f.write("// ===== CONFIGURAÇÕES GLOBAIS =====\n")
        f.write("// Chance base de drop visual (0.05% = 5 em 10000)\n")
        f.write("set .@base_chance, 5;\n\n")
        
        f.write("// Incremento por refino (0.01% = 1 em 10000)\n")
        f.write("set .@refine_bonus, 1;\n\n")
        
        f.write("// ===== FUNÇÃO PRINCIPAL =====\n")
        f.write("function script CalculateVisualDropChance {\n")
        f.write("\t.@total_chance = 0;\n\n")
        
        f.write("\t// Verificar cada slot de equipamento\n")
        f.write("\tfor (.@i = 0; .@i < 10; .@i++) {\n")
        f.write("\t\t.@item_id = getequipid(.@i);\n")
        f.write("\t\tif (.@item_id <= 0) continue;\n\n")
        
        f.write("\t\t// Verificar se o item tem configuração de drop visual\n")
        f.write("\t\t.@item_config = getiteminfo(.@item_id, 1000); // Campo customizado\n")
        f.write("\t\tif (.@item_config <= 0) continue;\n\n")
        
        f.write("\t\t// Extrair chance base e bônus de refino\n")
        f.write("\t\t.@base_chance = .@item_config / 10000;\n")
        f.write("\t\t.@refine_multiplier = .@item_config % 100;\n\n")
        
        f.write("\t\t// Calcular bônus de refino\n")
        f.write("\t\t.@refine = getequiprefinerycnt(.@i);\n")
        f.write("\t\t.@refine_bonus = .@refine_multiplier * .@refine;\n\n")
        
        f.write("\t\t// Somar à chance total\n")
        f.write("\t\t.@total_chance += .@base_chance + .@refine_bonus;\n")
        f.write("\t}\n\n")
        
        f.write("\treturn .@total_chance;\n")
        f.write("}\n\n")
        
        f.write("// ===== FUNÇÃO DE DROP =====\n")
        f.write("function script TryVisualDrop {\n")
        f.write("\t.@chance = callfunc('CalculateVisualDropChance');\n\n")
        
        f.write("\tif (rand(10000) < .@chance) {\n")
        f.write("\t\t// Dropar costume aleatório\n")
        f.write("\t\tcallfunc('DropHeadCostume');\n")
        f.write("\t\treturn 1;\n")
        f.write("\t}\n\n")
        
        f.write("\treturn 0;\n")
        f.write("}\n\n")
        
        f.write("// ===== IMPLEMENTAÇÃO =====\n")
        f.write("// Substituir bDropAddRace por:\n")
        f.write("// bonus_script \"{ callfunc('TryVisualDrop'); }\", 100, 1, 0;\n\n")
        
        f.write("// ===== CONFIGURAÇÃO POR ITEM =====\n")
        f.write("// Formato: (base_chance * 10000) + refine_multiplier\n")
        f.write("// Exemplo: 500 = 0.05% base + 0.01% por refino\n")
        f.write("// Exemplo: 1000 = 0.10% base + 0.01% por refino\n")
        f.write("// Exemplo: 2005 = 0.20% base + 0.05% por refino\n\n")
        
        f.write("// ===== EXEMPLOS DE CONFIGURAÇÃO =====\n")
        f.write("// Item básico: 500 (0.05% + 0.01% por refino)\n")
        f.write("// Item raro: 1000 (0.10% + 0.01% por refino)\n")
        f.write("// Item épico: 2005 (0.20% + 0.05% por refino)\n")
        f.write("// Item lendário: 5000 (0.50% + 0.01% por refino)\n")

def create_item_config_examples():
    """Cria exemplos de configuração para itens"""
    
    with open('item_visual_drop_config.txt', 'w', encoding='utf-8') as f:
        f.write("// ===== CONFIGURAÇÕES DE DROP VISUAL POR ITEM =====\n\n")
        
        f.write("// ===== ITENS BÁSICOS (0.05% base + 0.01% por refino) =====\n")
        f.write("// Configuração: 500\n")
        f.write("// Exemplos:\n")
        f.write("// - Anel de Drop +1: 0.05% + 0.01% = 0.06%\n")
        f.write("// - Anel de Drop +5: 0.05% + 0.05% = 0.10%\n")
        f.write("// - Anel de Drop +10: 0.05% + 0.10% = 0.15%\n\n")
        
        f.write("// ===== ITENS RAROS (0.10% base + 0.01% por refino) =====\n")
        f.write("// Configuração: 1000\n")
        f.write("// Exemplos:\n")
        f.write("// - Anel de Drop Raro +1: 0.10% + 0.01% = 0.11%\n")
        f.write("// - Anel de Drop Raro +5: 0.10% + 0.05% = 0.15%\n")
        f.write("// - Anel de Drop Raro +10: 0.10% + 0.10% = 0.20%\n\n")
        
        f.write("// ===== ITENS ÉPICOS (0.20% base + 0.05% por refino) =====\n")
        f.write("// Configuração: 2005\n")
        f.write("// Exemplos:\n")
        f.write("// - Anel de Drop Épico +1: 0.20% + 0.05% = 0.25%\n")
        f.write("// - Anel de Drop Épico +5: 0.20% + 0.25% = 0.45%\n")
        f.write("// - Anel de Drop Épico +10: 0.20% + 0.50% = 0.70%\n\n")
        
        f.write("// ===== ITENS LENDÁRIOS (0.50% base + 0.01% por refino) =====\n")
        f.write("// Configuração: 5000\n")
        f.write("// Exemplos:\n")
        f.write("// - Anel de Drop Lendário +1: 0.50% + 0.01% = 0.51%\n")
        f.write("// - Anel de Drop Lendário +5: 0.50% + 0.05% = 0.55%\n")
        f.write("// - Anel de Drop Lendário +10: 0.50% + 0.10% = 0.60%\n\n")
        
        f.write("// ===== COMO IMPLEMENTAR =====\n")
        f.write("// 1. Adicionar campo customizado no item_db\n")
        f.write("// 2. Usar getiteminfo(item_id, 1000) para ler configuração\n")
        f.write("// 3. Substituir bDropAddRace por bonus_script\n")
        f.write("// 4. Configurar valores conforme tabela acima\n")

def create_implementation_guide():
    """Cria guia de implementação"""
    
    with open('visual_drop_implementation_guide.txt', 'w', encoding='utf-8') as f:
        f.write("// ===== GUIA DE IMPLEMENTAÇÃO =====\n\n")
        
        f.write("// ===== PASSO 1: CONFIGURAR ITENS =====\n")
        f.write("// No item_db, adicionar campo customizado:\n")
        f.write("// CustomField: visual_drop_config\n")
        f.write("// Valores: 500, 1000, 2005, 5000, etc.\n\n")
        
        f.write("// ===== PASSO 2: SUBSTITUIR bDropAddRace =====\n")
        f.write("// Trocar:\n")
        f.write("// bonus2 bDropAddRace,RC_All,50;\n")
        f.write("// Por:\n")
        f.write("// bonus_script \"{ callfunc('TryVisualDrop'); }\", 100, 1, 0;\n\n")
        
        f.write("// ===== PASSO 3: TESTAR SISTEMA =====\n")
        f.write("// 1. Equipar item com configuração\n")
        f.write("// 2. Atacar mobs\n")
        f.write("// 3. Verificar se costumes são dropados\n")
        f.write("// 4. Ajustar chances conforme necessário\n\n")
        
        f.write("// ===== PASSO 4: BALANCEAR =====\n")
        f.write("// - Ajustar valores base conforme necessário\n")
        f.write("// - Modificar bônus de refino\n")
        f.write("// - Testar com diferentes combinações\n\n")
        
        f.write("// ===== VANTAGENS DO SISTEMA =====\n")
        f.write("// ✅ Configurável por item\n")
        f.write("// ✅ Acumulativo entre itens\n")
        f.write("// ✅ Bônus de refino\n")
        f.write("// ✅ Fácil de balancear\n")
        f.write("// ✅ Substitui bDropAddRace\n")

def main():
    print("🎯 Criando sistema de drop visual configurável...")
    
    create_visual_drop_system()
    create_item_config_examples()
    create_implementation_guide()
    
    print("✅ Arquivos gerados:")
    print("   - visual_drop_system_complete.txt")
    print("   - item_visual_drop_config.txt")
    print("   - visual_drop_implementation_guide.txt")
    
    print("\n📊 Sistema criado com sucesso!")
    print("   - Base: 0.05% + Refino: +0.01% por nível")
    print("   - Acumulativo entre itens")
    print("   - Configurável por item")
    print("   - Substitui bDropAddRace")

if __name__ == "__main__":
    main()
