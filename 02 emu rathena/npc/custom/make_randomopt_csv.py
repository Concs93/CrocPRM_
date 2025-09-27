# -*- coding: utf-8 -*-
import os, csv, re, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    print("Instale:  pip install pyyaml"); sys.exit(1)

DB_ROOT = Path(r"E:\PRM\test\02 emu rathena\db")
GROUP_FILES = [DB_ROOT/"re"/"item_randomopt_group.yml",
               DB_ROOT/"import"/"item_randomopt_group.yml"]
OPTDB_FILES = [DB_ROOT/"re"/"item_randomopt_db.yml",
               DB_ROOT/"import"/"item_randomopt_db.yml"]
OUT_COMMA = Path("randomopt_groups_comma.csv")
OUT_SC    = Path("randomopt_groups_semicolon.csv")

def load_yaml(p: Path):
    return yaml.safe_load(p.read_text(encoding="utf-8")) if p.exists() else None

def one_line(s): 
    return re.sub(r"\s+"," ",str(s)).strip() if s is not None else ""

def index_optdb(datas):
    idx={}
    for d in datas:
        if not d or "Body" not in d: continue
        for row in d["Body"]:
            key=row.get("Option")
            if key: idx[key]=one_line(row.get("Script"))
    return idx

def merge_groups(datas):
    m={}
    for d in datas:
        if not d or "Body" not in d: continue
        for row in d["Body"]:
            g=row.get("Group")
            if g: m[g]=row  # import sobrescreve re
    return m

def rows_from_group(name, g, idx):
    rows=[]
    # Slots fixos
    for sl in (g.get("Slots") or []):
        slot=sl.get("Slot")
        opts=sl.get("Options") or []
        total=sum((o.get("Chance") or 0) for o in opts) or 0
        for o in opts:
            ch=o.get("Chance"); pct=(ch/total*100.0 if ch and total else None)
            rows.append(dict(
                group=name, slot=slot, pick_type="FixedSlot",
                option_key=o.get("Option"), min=o.get("MinValue"),
                max=o.get("MaxValue"), chance=ch,
                chance_pct_slot=(round(pct,4) if pct is not None else None),
                param=o.get("Param"), script_one_line=idx.get(o.get("Option"),"")
            ))
    # Pool Random (quando existir)
    rnd=g.get("Random") or []
    if rnd:
        total=sum((o.get("Chance") or 0) for o in rnd) or 0
        for o in rnd:
            ch=o.get("Chance"); pct=(ch/total*100.0 if ch and total else None)
            rows.append(dict(
                group=name, slot=g.get("MaxRandom"), pick_type="RandomPool",
                option_key=o.get("Option"), min=o.get("MinValue"),
                max=o.get("MaxValue"), chance=ch,
                chance_pct_slot=(round(pct,4) if pct is not None else None),
                param=o.get("Param"), script_one_line=idx.get(o.get("Option"),"")
            ))
    return rows

def write_csv(path, rows, delimiter):
    path.write_text("", encoding="utf-8")  # garante novo
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "group","slot","pick_type","option_key","min","max",
            "chance","chance_pct_slot","param","script_one_line"
        ], delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows: w.writerow(r)

def main():
    groups = merge_groups([load_yaml(p) for p in GROUP_FILES])
    optidx = index_optdb([load_yaml(p) for p in OPTDB_FILES])

    rows=[]
    for name,g in sorted(groups.items(), key=lambda kv: kv[0].lower()):
        rows.extend(rows_from_group(name,g,optidx))

    write_csv(OUT_COMMA, rows, delimiter=",")
    write_csv(OUT_SC,    rows, delimiter=";")
    print(f"OK: {len(rows)} linhas.")
    print(f"- {OUT_COMMA.resolve()}")
    print(f"- {OUT_SC.resolve()}")

if __name__=="__main__": main()
