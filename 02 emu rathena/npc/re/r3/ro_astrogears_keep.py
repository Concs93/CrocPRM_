import re
from pathlib import Path

p = Path(r"E:\PRM\test\02 emu rAthena\npc\re\r3\astroheadgears.txt")  # ajuste se necessário
txt = p.read_text(encoding="utf-8")

# 1) Injeta a função F_UpgradeHatKeepOpts se não existir
if "function\tscript\tF_UpgradeHatKeepOpts" not in txt:
    helper = r"""
//============================================================
// F_UpgradeHatKeepOpts(src_id, dst_id)
//============================================================
function	script	F_UpgradeHatKeepOpts	{
	.@SRC = getarg(0);
	.@DST = getarg(1);
	getinventorylist;
	.@pick = -1;
	for (.@i = 0; .@i < @inventorylist_count; .@i++) {
		if (@inventorylist_id[.@i] == .@SRC && @inventorylist_refine[.@i] == 9) { .@pick = .@i; break; }
	}
	if (.@pick < 0) end;
	.@base = .@pick * 5;
	for (.@s = 0; .@s < 5; .@s++) {
		.@opt_id[.@s]  = @inventorylist_option_id[.@base + .@s];
		.@opt_val[.@s] = @inventorylist_option_value[.@base + .@s];
		.@opt_par[.@s] = @inventorylist_option_param[.@base + .@s];
	}
	delitem2 .@SRC, 1, 9, 0, 0, 0, 0, 0;
	getitem2 .@DST, 1, 1, 0, 0, 0, 0, 0, 0;
	getinventorylist;
	.@new_idx = -1;
	for (.@i = 0; .@i < @inventorylist_count; .@i++) if (@inventorylist_id[.@i] == .@DST) .@new_idx = .@i;
	if (.@new_idx >= 0) {
		for (.@s = 0; .@s < 5; .@s++) if (.@opt_id[.@s] > 0)
			setitemoption @inventorylist_idx[.@new_idx], .@s, .@opt_id[.@s], .@opt_val[.@s], .@opt_par[.@s];
	}
	end;
}
""".strip()
    # Insere a função antes do primeiro "script" do arquivo
    txt = helper + "\n\n" + txt

# 2) Dentro de cada bloco "case 1:", troca delitem2 SRC... + getitem DST,1 por callfunc
def repl_block(m):
    block = m.group(0)
    # acha SRC no delitem2
    del_m = re.search(r"delitem2\s+(\d+)\s*,\s*1\s*,\s*9\s*,\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*;", block)
    # acha DST no getitem
    get_m = re.search(r"getitem\s+(\d+)\s*,\s*1\s*;", block)
    if not del_m or not get_m:
        return block  # não toca
    src = del_m.group(1)
    dst = get_m.group(1)
    # remove a linha do delitem2 e do getitem, insere callfunc no lugar do getitem
    block = re.sub(r"delitem2\s+\d+\s*,\s*1\s*,\s*9\s*,\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*,\s*0\s*;\s*\n", "", block)
    block = re.sub(r"getitem\s+\d+\s*,\s*1\s*;\s*", f'callfunc "F_UpgradeHatKeepOpts", {src}, {dst};\n', block)
    return block

pattern = re.compile(r"(case\s+1:\s*.*?break;)", re.DOTALL | re.IGNORECASE)
txt2 = pattern.sub(repl_block, txt)

backup = p.with_suffix(".txt.bak")
backup.write_text(txt, encoding="utf-8")
p.write_text(txt2, encoding="utf-8")
print("OK: backup salvo em", backup)
