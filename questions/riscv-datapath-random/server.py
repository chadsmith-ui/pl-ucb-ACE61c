import random

R_TYPE = ["add", "sub", "and", "or", "xor", "slt"]
I_TYPE = ["addi", "andi", "ori", "xori", "slti"]
LOADS = ["lw", "lh", "lb"]
STORES = ["sw", "sh", "sb"]
BRANCHES = ["beq", "bne", "blt", "bge"]

# Every control-signal wire is a thick wire in this question.
CONTROL_WIRES = ["pcsel__pcmux_sel", "regwen__reg_wen", "immsel__immgen", "brun__brcomp", "brcomp_breq__ctrl",
                 "brcomp_brlt__ctrl", "bsel__bmux_sel", "asel__amux_sel", "alusel__alu", "memrw__dmem", "wbsel__wbmux_sel"]
# y = 4 possible box places (always defined for every instruction); each variant turns on x of them.
BOX_PLACES = ["pcsel__pcmux_sel", "regwen__reg_wen", "bsel__bmux_sel", "memrw__dmem"]


def generate(data):
    reg = lambda: "x%d" % random.randint(1, 31)
    kind = random.choice(["r", "i", "load", "store", "branch", "lui", "auipc", "jal", "jalr"])
    taken = ""
    if kind == "r":
        instr = "%s %s, %s, %s" % (random.choice(R_TYPE), reg(), reg(), reg())
    elif kind == "i":
        instr = "%s %s, %s, %d" % (random.choice(I_TYPE), reg(), reg(), random.randint(-64, 64))
    elif kind == "load":
        instr = "%s %s, %d(%s)" % (random.choice(LOADS), reg(), 4 * random.randint(0, 16), reg())
    elif kind == "store":
        instr = "%s %s, %d(%s)" % (random.choice(STORES), reg(), 4 * random.randint(0, 16), reg())
    elif kind == "branch":
        instr = "%s %s, %s, label" % (random.choice(BRANCHES), reg(), reg())
        taken = random.choice(["true", "false"])
    elif kind == "lui" or kind == "auipc":
        instr = "%s %s, 0x%x" % (kind, reg(), random.randint(1, 0xFFFFF))
    elif kind == "jal":
        instr = "jal %s, label" % random.choice(["x1", reg()])
    else:
        instr = "jalr %s, %d(%s)" % (random.choice(["x1", reg()]), 4 * random.randint(0, 8), reg())
    data["params"]["instr"] = instr
    data["params"]["taken"] = taken
    data["params"]["branch_note"] = ("Assume the branch is taken." if taken == "true" else "Assume the branch is not taken.") if taken else ""
    data["params"]["wires"] = [{"name": w} for w in CONTROL_WIRES]
    # x boxes out of y places
    chosen = random.sample(BOX_PLACES, random.randint(1, 3))
    data["params"]["boxes"] = [{"loc": w} for w in BOX_PLACES if w in chosen]
