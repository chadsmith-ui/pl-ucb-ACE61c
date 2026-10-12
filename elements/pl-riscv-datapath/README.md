# pl-riscv-datapath

Interactive single-cycle RISC-V datapath (from the CS61C reference card). The diagram is described by one `<pl-wire>` element per wire segment and one `<pl-box>` element per value box. Every setting is a visible attribute, so an instructor can edit anything by hand.

Install: put this folder in your course's `elements/` directory (`elements/pl-riscv-datapath/`), sync, and use the tag in any `question.html`. The controller is one self-contained file (JS and CSS are embedded), so no `clientFiles` are needed.

## What students see

| Look | Meaning |
|---|---|
| Thick grey (dotted in colorblind mode) | A wire the student must set; not set yet. Click to set it. |
| Thick red (blue in colorblind mode) | Carries data (ON). Click to change. |
| Thick black | No data (OFF). Click to change. |
| Thin red / thin black | Fixed. The student cannot change it (it is context). |
| Dashed (with an x in colorblind mode) | Incorrect, shown in the graded submission. |
| Gray box | A place to type a value: `0x` = hex, `0b` = binary, no prefix = decimal. |

A legend with these entries is drawn under the diagram. A thick wire starts grey ("not set"), then each click flips it between red and black; it can never go back to grey. It can also start red or black (possibly wrong) so students must correct it.

## Quick start

```html
<pl-riscv-datapath answers-name="dp" instruction="lw x5, 0(x6)">
  <pl-wire name="wbsel__wbmux_sel"    mutable="true" initial-state="off"   weight="1"></pl-wire>
  <pl-wire name="j_alu2__wbmux_1"     mutable="true" initial-state="on"    weight="1"></pl-wire>
  <pl-wire name="dmem_rdata__wbmux_0" mutable="true" initial-state="unset" weight="1"></pl-wire>
  <pl-wire name="alu__j_alu1"         mutable="false" initial-state="on"></pl-wire>
  <pl-box location="wbsel__wbmux_sel" base="hex" solution="auto" weight="1"></pl-box>
</pl-riscv-datapath>
```

Put your question text in a `<pl-question-panel>` and place the tag once, outside the panels. To build a tag by clicking, add `<pl-riscv-datapath answers-name="builder" mode="builder">` to a scratch question (the `riscv-datapath-author` question does this). The builder writes every wire with all its attributes.

## `<pl-riscv-datapath>` attributes

| Attribute | Meaning |
|---|---|
| `answers-name` | Required. Unique within the question. |
| `instruction` | Sets every wire's default `solution-state` from the instruction (see the preset table). Operands are ignored. |
| `branch-taken` | `true` / `false`. Required for branch instructions. |
| `legend` | `true` (default) or `false`. |
| `tooltips` | `true` shows each wire's plain-English name when hovering (for authors; it can give hints). Default `false`. The builder always shows them. |
| `weight` | PrairieLearn weight of this whole diagram within the question. Default 1. |
| `mode` | `builder` shows the question builder instead. |

## `<pl-wire>` (one per wire; wires you leave out use the defaults)

| Attribute | Values | Default |
|---|---|---|
| `name` | A wire name (list below). Required. | |
| `mutable` | `true` = thick, students can set it. `false` = thin, fixed. | `false` |
| `initial-state` | `unset` (grey), `on` (red) or `off` (black) at the start. Thin wires must be `on` or `off`. | `unset` if mutable, else `off` |
| `solution-state` | `on` or `off`: the correct answer. | from `instruction`, else `off` |
| `weight` | Points for getting this wire right. Only mutable wires can have a weight. | `0` |

A thin wire shows its `initial-state` to students (that is how you give "context" wires). Write the closing tag: `<pl-wire ...></pl-wire>`.

## `<pl-box>` (one per value box)

Each wire has one fixed place for a box (its capacity is in the wire list below), so boxes never overlap wires. To randomize, turn on x boxes out of the y places you want, for example with a Mustache loop (see `riscv-datapath-random`).

| Attribute | Values | Default |
|---|---|---|
| `location` | The wire whose place is used. Required; one box per place. | |
| `name` | Unique name of the box. | the `location` |
| `base` | `hex`, `binary` or `decimal`. | `hex` |
| `size` | Characters the box accepts (at most the place's capacity). | the capacity |
| `solution` | The correct value, e.g. `0x1f`, `0b101`, `42`. `auto` takes the value from the instruction for control-signal places (PCSel, RegWEn, BSel, ASel, MemRW, WBSel, BrUn). | none |
| `initial-value` | Text shown at the start (required if `mutable="false"`). | empty |
| `mutable` | `false` shows a fixed value that students cannot change. | `true` |
| `weight` | Points for a correct value. | `0` |

Binary and decimal boxes hold up to 8 characters on data wires and 2 on control signals (the boxes are sized to fit the diagram). Values are compared numerically, so `0x1`, `1` and `01` all match.

## Scoring

Points come only from `weight`: each wire or box with a weight above 0 is one item. A wire is correct when its final state equals `solution-state`; a wire the student never touches keeps its `initial-state` (so `unset` always counts as wrong). Score = points earned / total weight. If nothing has a weight, the element reports an error. The builder sets weights for you (1 by default; any value can be edited by hand).

## Colorblind mode

Every diagram has a "Colorblind mode" checkbox. It remembers the choice in the browser and applies to all diagrams on the page. It changes:

- ON wires are blue (instead of red) and thick ON wires get a white center line, so they differ from black by shape as well as colour.
- "Not set" wires are dotted (instead of grey).
- Incorrect wires are dashed with an x mark; correct and incorrect boxes get a check mark or cross.
- The legend shows the matching swatches and wording. Every wire also has a text label for screen readers (on, off, not set, fixed).

## Instruction presets

The control-signal and wire rules the presets use:

| Class | PCSel | RegWEn | ImmSel | BrUn | BSel | ASel | ALUSel | MemRW | WBSel |
|---|---|---|---|---|---|---|---|---|---|
| R-type (add sub and or xor sll srl sra slt sltu mul) | 0 | 1 | * | * | 0 | 0 | op | 0 | 1 |
| I-type arithmetic (addi andi ori xori slli srli srai slti sltiu) | 0 | 1 | I | * | 1 | 0 | op | 0 | 1 |
| Loads (lb lbu lh lhu lw) | 0 | 1 | I | * | 1 | 0 | ADD | 0 | 0 |
| Stores (sb sh sw) | 0 | 0 | S | * | 1 | 0 | ADD | 1 | * |
| Branches (beq bne blt bltu bge bgeu) | 1 if taken, else 0 | 0 | B | 1 for bltu/bgeu, else 0 | 1 | 1 | ADD | 0 | * |
| jal | 1 | 1 | J | * | 1 | 1 | ADD | 0 | 2 |
| jalr | 1 | 1 | I | * | 1 | 0 | ADD | 0 | 2 |
| lui | 0 | 1 | U | * | 1 | * | B | 0 | 1 |
| auipc | 0 | 1 | U | * | 1 | 1 | ADD | 0 | 1 |

(`*` = don't care.) A wire's default solution is ON when it carries a value the instruction uses: only the selected input of each mux; a control wire whenever its signal is defined; ALU output to DMEM `addr` always; the instruction bus down to control decode, with `rd`, `rs1`, `rs2` and Imm Gen branches only when used; the branch comparator only for branches; PC+4 only where used and ALU to PC mux only when PCSel = 1. Pseudo-instructions: `mv li nop` to addi, `neg` to sub, `not` to xori, `j` to jal, `jr ret` to jalr, `beqz` to beq, `bnez` to bne.

## Older compact tags still work

Tags that use `answer-wires`, `bold-wires`, `initial-wires`, `initial-off-wires`, `locked-wires`, `value-boxes`, `wire-points`, `value-points`, or `<pl-wire state=... value=... bold=... initial=... locked=...>` are converted into the same model, so there is one grader. Two things differ from before: a tag without `bold-wires` now has every wire thick (every wire is graded, 1 point each), and `scoring-mode` is no longer accepted (an error says so). Do not mix old and new styles in one tag.

## Wire names

**PC and instruction fetch**

| Wire name | What it is | Box capacity |
|---|---|---|
| `pcmux_out__pc` | PC mux output to the PC register | 8 |
| `pc__j_pc1` | PC register output (start of the PC bus) | 8 |
| `j_pc1__imem_addr` | PC to instruction memory address | 8 |
| `j_pc1__j_pc2` | PC bus, continuing toward +4 and the A mux | 8 |
| `j_pc2__plus4` | PC to the +4 adder | 8 |
| `j_pc2__amux_1` | PC to A mux, input 1 | 8 |
| `plus4__j_pc4` | +4 adder output (PC+4) | 8 |
| `j_pc4__pcmux_0` | PC+4 to PC mux, input 0 | 8 |
| `j_pc4__wbmux_2` | PC+4 to write-back mux, input 2 | 8 |

**Instruction bus**

| Wire name | What it is | Box capacity |
|---|---|---|
| `imem_inst__j_i1` | Instruction memory output (inst[31:0]) | 8 |
| `j_i1__reg_rd` | inst[11:7] to register file rd | 2 |
| `j_i1__j_i2` | Instruction bus, continuing down (after rd) | 8 |
| `j_i2__reg_rs1` | inst[19:15] to register file rs1 | 2 |
| `j_i2__j_i3` | Instruction bus, continuing down (after rs1) | 8 |
| `j_i3__reg_rs2` | inst[24:20] to register file rs2 | 2 |
| `j_i3__j_i4` | Instruction bus, continuing down (after rs2) | 8 |
| `j_i4__immgen_inst` | inst[31:7] to Imm Gen | 8 |
| `j_i4__ctrl_inst` | inst[31:0] to the control logic | 8 |

**Register file reads**

| Wire name | What it is | Box capacity |
|---|---|---|
| `reg_rdata1__j_r1` | Register file output rdata1 | 8 |
| `j_r1__amux_0` | rdata1 to A mux, input 0 | 8 |
| `j_r1__brcomp_a` | rdata1 to Branch Comp, input A | 8 |
| `reg_rdata2__j_r2` | Register file output rdata2 | 8 |
| `j_r2__brcomp_b` | rdata2 to Branch Comp, input B | 8 |
| `j_r2__j_r3` | rdata2 bus, continuing toward the B mux and DMEM | 8 |
| `j_r3__bmux_0` | rdata2 to B mux, input 0 | 8 |
| `j_r3__dmem_wdata` | rdata2 to DMEM write data | 8 |

**Imm Gen, muxes and ALU**

| Wire name | What it is | Box capacity |
|---|---|---|
| `immgen__bmux_1` | Imm Gen output to B mux, input 1 | 8 |
| `amux__alu_a` | A mux output to ALU input A | 8 |
| `bmux__alu_b` | B mux output to ALU input B | 8 |
| `alu__j_alu1` | ALU output | 8 |
| `j_alu1__dmem_addr` | ALU output to DMEM address | 8 |
| `j_alu1__j_alu2` | ALU output bus, continuing up toward the PC mux and write-back mux | 8 |
| `j_alu2__pcmux_1` | ALU output to PC mux, input 1 | 8 |
| `j_alu2__wbmux_1` | ALU output to write-back mux, input 1 | 8 |

**Memory and write-back**

| Wire name | What it is | Box capacity |
|---|---|---|
| `dmem_rdata__wbmux_0` | DMEM read data to write-back mux, input 0 | 8 |
| `wbmux_out__reg_wdata` | Write-back mux output to register file write data | 8 |

**Control signals**

| Wire name | What it is | Box capacity |
|---|---|---|
| `pcsel__pcmux_sel` | PCSel control to PC mux select | 2 |
| `regwen__reg_wen` | RegWEn control to register file write enable | 2 |
| `immsel__immgen` | ImmSel control to Imm Gen | 2 |
| `brun__brcomp` | BrUn control to Branch Comp | 2 |
| `brcomp_breq__ctrl` | Branch Comp BrEq output to control | 2 |
| `brcomp_brlt__ctrl` | Branch Comp BrLT output to control | 2 |
| `bsel__bmux_sel` | BSel control to B mux select | 2 |
| `asel__amux_sel` | ASel control to A mux select | 2 |
| `alusel__alu` | ALUSel control to ALU | 2 |
| `memrw__dmem` | MemRW control to DMEM | 2 |
| `wbsel__wbmux_sel` | WBSel control to write-back mux select | 2 |

## Troubleshooting

- "Loading datapath diagram..." stays: JavaScript is not running. Press F12 and check the Console.
- An error naming an attribute, wire or instruction is shown at preview time and lists the allowed values.
