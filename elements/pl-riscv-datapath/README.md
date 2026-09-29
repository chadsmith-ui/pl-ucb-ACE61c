# pl-riscv-datapath

Interactive single-cycle RISC-V datapath (from the CS61C reference card). Students click wire segments and can be asked to type hex values on chosen wires. Wrong or missing segments are dashed in the graded submission.

Install: put this folder in your course's `elements/` directory (`elements/pl-riscv-datapath/`), sync, and use the tag in any `question.html`. The controller is one self-contained file (JS and CSS are embedded), so no `clientFiles` are needed.

## Quick start

```html
<pl-riscv-datapath answers-name="dp" instruction="andi x5, x6, 0x1" value-boxes="pcsel, regwen, memrw, wbsel"></pl-riscv-datapath>
```

Put your question text in a `<pl-question-panel>`. Place the tag once, outside the panels. To build a tag by clicking, add `<pl-riscv-datapath answers-name="builder" mode="builder">` to a scratch question (the `riscv-datapath-author` question does this).

## Two ways to ask

**Every wire (default).** All wires start thin black. Students turn wires ON (thick red). Scoring modes below.

**Only certain wires (bold wires).** Set `bold-wires`. Only those wires matter:

- Bold wires start bold grey ("not set yet"). The first click makes one bold red; after that each click flips it between bold red and bold black. It cannot go back to grey.
- Every other wire is thin, cannot be clicked and is not graded. It is thin black unless you list it in `initial-wires`, which shows it thin red (fixed context the student cannot change).
- Each bold wire is one item and must match the key: red where the key says ON, black where it says OFF. A wire left grey is wrong.
- Bold wires can start red or black (possibly wrong) so students must correct them: `initial-wires` starts wires red, `initial-off-wires` starts them black. Bold wires in neither list start grey.
- Thin wires: `initial-wires` makes a thin wire red, otherwise it is black. `initial-off-wires` has no effect on thin wires (they are already black).

```html
<pl-riscv-datapath answers-name="dp" instruction="lw x5, 0(x6)"
    bold-wires="to:wbmux" initial-wires="j_alu2__wbmux_1" initial-off-wires="wbsel__wbmux_sel"></pl-riscv-datapath>
```

## Attributes

| Attribute | Meaning |
|---|---|
| `answers-name` | Required. Unique within the question. |
| `instruction` | Fills the answer key from a preset (see below). Operands are ignored. |
| `branch-taken` | `true` / `false`. Required for branch instructions. |
| `answer-wires` | Wires that are ON in the key. Replaces the preset's wires (or builds a key with no preset). `answer-wires=""` means none. |
| `bold-wires` | Turns on bold-wire mode; only these wires are interactive and graded. |
| `initial-wires` | Wires that start ON (red). In bold-wire mode, a listed thin wire shows thin red and cannot be changed. Default: all off. |
| `initial-off-wires` | Bold-wire mode only: wires that start bold black. |
| `locked-wires` | Wires students cannot change. |
| `value-boxes` | `none` (default), `control`, or a list from `pcsel, regwen, bsel, asel, memrw, wbsel, brun`. Adds a gray hex box with the preset's value. |
| `scoring-mode` | Every-wire mode only: `on_items` (default), `subtract`, `all_segments`. |
| `wire-points`, `value-points` | Points per wire / per box. Default 1. |
| `weight` | PrairieLearn weight of this diagram within the question. Default 1. |
| `mode` | `builder` shows the question builder instead. |

Every wire-list attribute (`answer-wires`, `bold-wires`, `initial-wires`, `initial-off-wires`, `locked-wires`) takes wire names and/or these groups, separated by commas: `all`, `control` (the 11 control-signal wires), `to:<component>` and `from:<component>`. Wire names are `origin__destination`, so `to:wbmux` means every wire into the write-back mux (its three data inputs and its select line). Components: `pc pcmux plus4 imem reg immgen amux bmux alu dmem wbmux brcomp ctrl`. Example: `bold-wires="to:wbmux, to:pcmux"`.

Child tags adjust individual wires (write the closing tag): `<pl-wire name="alu__j_alu1" state="on|off" value="0x1" bold="true|false" initial="on|off|unset" locked="true|false"></pl-wire>`. `value` adds a gray box on any wire (data wires included), so it can hold a value you computed in `server.py`.

Every attribute accepts Mustache, so randomizing is ordinary PrairieLearn: compute `params.instr` in `generate()` and write `instruction="{{params.instr}}"` (see `riscv-datapath-random`).

## Scoring

Every-wire mode:

- `on_items`: every wire that should be ON, plus every wire the student turned ON by mistake, is an item. Correct ON wires earn points; mistaken ones earn none.
- `subtract`: items are the wires that should be ON; each mistaken wire also takes a point away.
- `all_segments`: every segment is an item; ON/OFF must match.

Bold-wire mode: each bold wire is one item worth `wire-points`; it must match the key, and grey counts as wrong.

In both modes each value box is one more item worth `value-points`. Hex is compared numerically (`1`, `01`, `0x1` match).

## Presets: conventions to review

Control signals (`*` = don't care):

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

Wire rules (a segment is ON when it carries a value the instruction uses):

1. Only the selected input of each mux is ON.
2. A control-signal wire is ON whenever its signal has a defined value (not `*`). ImmSel and ALUSel are ON but have no numeric preset box (their encodings vary by course).
3. ALU output to DMEM `addr` is always ON.
4. The instruction bus is ON down to control decode; the `rd`, `rs1`, `rs2` and Imm Gen branches are ON only when the instruction uses them.
5. The branch comparator's inputs and its BrEq/BrLT outputs are ON only for branches.
6. PC+4 is ON only where used (PCSel = 0 or WBSel = 2); ALU to PC mux is ON only when PCSel = 1.

Pseudo-instructions map to: `mv li nop` to addi, `neg` to sub, `not` to xori, `j` to jal, `jr ret` to jalr, `beqz` to beq, `bnez` to bne. Any preset can be adjusted with `<pl-wire state="on|off">`.

## Troubleshooting

- "Loading datapath diagram..." stays: JavaScript is not running. Press F12 and check the Console.
- An error naming an attribute, wire or instruction is shown at preview time; it lists the allowed values.
