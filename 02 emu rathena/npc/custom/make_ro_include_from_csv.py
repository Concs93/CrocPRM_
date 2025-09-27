# -*- coding: utf-8 -*-
"""
Lê randomopt_groups_semicolon.csv (delimitador ';') e produz
npc/custom/include/ro_data_from_csv.txt COM VARIÁVEIS GLOBAIS ($, $@).
"""
from pathlib import Path
import csv, re

# === CONFIG ===
CSV_PATH = Path(r"E:\PRM\test\randomopt_groups_semicolon.csv")
OUT_PATH = Path(r"E:\PRM\test\02 emu rathena\npc\custom\include\ro_data_from_csv.txt")
DELIM = ';'
# ==============

def safe_name(s: str) -> str:
    # só letras/números/_ para virar parte do nome da variável
    return re.sub(r'[^A-Za-z0-9_]+', '_', s)

# ---- carrega CSV ----
rows = []
with open(CSV_PATH, 'r', encoding='utf-8') as f:
    rdr = csv.DictReader(f, delimiter=DELIM)
    for r in rdr:
        g = (r['group'] or '').strip()
        if not g:
            continue
        rows.append({
            'group': g,
            'slot': int(r['slot']) if r['slot'] else 0,
            'pick_type': (r['pick_type'] or '').strip(),
            'key': (r['option_key'] or '').strip(),
            'min': int(r['min']) if r['min'] else 0,
            'max': int(r['max']) if r['max'] else 0,
            'chance': int(r['chance']) if r['chance'] else 0,
            'param': int(r['param']) if r['param'] else 0,
        })

# ---- organiza por grupo ----
groups = {}  # g -> { fixed: {slot:[...]}, random:[...], maxrand:int }
for r in rows:
    g = r['group']
    groups.setdefault(g, {'fixed': {}, 'random': [], 'maxrand': 0})
    if r['pick_type'] == 'FixedSlot':
        groups[g]['fixed'].setdefault(r['slot'], []).append(r)
    else:  # RandomPool (usa 'slot' como MaxRandom)
        groups[g]['random'].append(r)
        if r['slot'] > groups[g]['maxrand']:
            groups[g]['maxrand'] = r['slot']

# ---- gera include (variáveis GLOBAIS) ----
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8', newline='\n') as out:
    w = out.write
    w("// AUTO-GERADO a partir de randomopt_groups_semicolon.csv\n")
    w("// NÃO EDITE À MÃO — rode o script Python para atualizar.\n")
    w("-\tscript\tRO_Data_From_CSV\t-1,{\n\nOnInit:\n")

    # lista de grupos
    group_names = sorted(groups.keys(), key=lambda s: s.lower())
    glist = ','.join(f'"{g}"' for g in group_names)
    w(f"\t// grupos disponíveis\n\tsetarray $@ro_groups$[0], {glist};\n")
    w(f"\tset $ro_groups_count, {len(group_names)};\n")
    w('\tdebugmes "[RO CSV] include OK. grupos="+$ro_groups_count;\n\n')

    for g in group_names:
        gs = groups[g]
        gsafe = safe_name(g)

        # ----- fixed slots -----
        slotnums = sorted(gs['fixed'].keys())
        if slotnums:
            w(f"\t// ===== group: {g} — fixed slots =====\n")
            w(f"\tsetarray $@ro_slotnums_{gsafe}[0], {','.join(str(s) for s in slotnums)};\n")
            w(f"\tset $ro_slotcount_{gsafe}, {len(slotnums)};\n")
            for s in slotnums:
                arr = gs['fixed'][s]
                keys = ','.join(f'"{r["key"]}"' for r in arr)
                mins = ','.join(str(r['min']) for r in arr)
                maxs = ','.join(str(r['max']) for r in arr)
                chs  = ','.join(str(r['chance']) for r in arr)
                prs  = ','.join(str(r['param']) for r in arr)
                w(f"\t// slot {s}\n")
                w(f"\tset $rok_size_{gsafe}_{s}, {len(arr)};\n")
                w(f"\tsetarray $@rok_{gsafe}_{s}$[0], {keys};\n")
                w(f"\tsetarray $@romin_{gsafe}_{s}[0], {mins};\n")
                w(f"\tsetarray $@romax_{gsafe}_{s}[0], {maxs};\n")
                w(f"\tsetarray $@roch_{gsafe}_{s}[0], {chs};\n")
                w(f"\tsetarray $@roparam_{gsafe}_{s}[0], {prs};\n")
            w("\n")
        else:
            w(f"\t// ===== group: {g} — sem fixed slots =====\n")
            w(f"\tset $ro_slotcount_{gsafe}, 0;\n")
            w(f"\tdeletearray $@ro_slotnums_{gsafe}[0], getarraysize($@ro_slotnums_{gsafe});\n\n")

        # ----- random pool -----
        if gs['random']:
            arr = gs['random']
            keys = ','.join(f'"{r["key"]}"' for r in arr)
            mins = ','.join(str(r['min']) for r in arr)
            maxs = ','.join(str(r['max']) for r in arr)
            chs  = ','.join(str(r['chance']) for r in arr)
            prs  = ','.join(str(r['param']) for r in arr)
            w(f"\t// random pool\n")
            w(f"\tset $rorand_slots_{gsafe}, {gs['maxrand']};\n")
            w(f"\tset $rorand_size_{gsafe}, {len(arr)};\n")
            w(f"\tsetarray $@rorand_k_{gsafe}$[0], {keys};\n")
            w(f"\tsetarray $@rorand_min_{gsafe}[0], {mins};\n")
            w(f"\tsetarray $@rorand_max_{gsafe}[0], {maxs};\n")
            w(f"\tsetarray $@rorand_ch_{gsafe}[0], {chs};\n")
            w(f"\tsetarray $@rorand_param_{gsafe}[0], {prs};\n\n")
        else:
            w(f"\tset $rorand_slots_{gsafe}, 0;\n")
            w(f"\tset $rorand_size_{gsafe}, 0;\n\n")

    w("\tend;\n}\n")

print(f"OK: gerado {OUT_PATH}")
