# Derivative Calculator in Brainfuck

> This project was brainstormed and implemented in a single Claude Code session: https://claudebin.com/threads/OFl5KE5_6n

A **938-character Brainfuck program** that computes symbolic derivatives of polynomials.

```brainfuck
,[-],-------------------------------->+<[>-<[-]]>>>>>>+<<<<<[>>>>>-<<<<<-<+>]>>>>>
[-<<<<<++++++++++++++++++++++++++++++++++++++++++++++++.[-]++++++++++.[-]>>>>>]<<<+
<<<[->>,------------------------------------------------[->[->+>+<<]>>[-<<+>>]<<<]
>>[->>>>+<<<<]>>>>>++++++++++<<>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]>[-]>>[->>>+<<<]>>>>
++++++++++<<>[->-[>+>>]>[+[-<+>]>+>>]<<<<<]>[-]>>>>+>+<<<[>>->-<<<++++++++++++++++
++++++++++++++++++++++++++++++++.[-]<++++++++++++++++++++++++++++++++++++++++++++++++
.[-]<<<<<<++++++++++++++++++++++++++++++++++++++++++++++++.[-]>>>>>>>]>>[-<<<[>>>>-
<<<<++++++++++++++++++++++++++++++++++++++++++++++++.[-]<<<<<<+++++++++++++++++++++
+++++++++++++++++++++++++++.[-]>>>>>>]>>>>[-<<<<<<<<<<+++++++++++++++++++++++++++++
+++++++++++++++++++.[-]>>>>>>>>>>]<]<<<<<<<<<<<<<<<<+<<,--------------------------------
>>>>>+<<<<<[>>>>>-<<<<<[-]++++++++++.[-]]>>>>>[-<<<<<<+>++++++++++++++++++++++++++
++++++.[-]>>>>>]<<<<<<]
```

## Usage

**Input:** Coefficients from constant term to highest degree, single digits (`0`-`9`), space-separated, newline-terminated.

**Output:** Derivative coefficients in the same format.

### Examples

| Polynomial | Input | Output | Derivative |
|---|---|---|---|
| `3x³ + 5x + 1` | `1 5 0 3` | `5 0 9` | `9x² + 5` |
| `x²` | `0 0 1` | `0 2` | `2x` |
| `9x⁹` | `0 0 0 0 0 0 0 0 0 9` | `0 0 0 0 0 0 0 0 81` | `81x⁸` |
| `7` (constant) | `7` | `0` | `0` |
| `9x²⁸` | `0 0 ... 0 9` (29 terms) | `0 0 ... 0 252` | `252x²⁷` |

### Run with the included interpreter

```bash
echo "1 5 0 3" | python3 bf_interpreter.py derivative.bf
# Output: 5 0 9
```

### Run tests

```bash
python3 test.py
# 17 passed, 0 failed out of 17 tests
```

## How it works

The program applies the **power rule** (`d/dx[axⁿ] = n·a·xⁿ⁻¹`) by streaming coefficients left-to-right:

1. **Read and discard** the constant term (degree 0)
2. **For each remaining coefficient**, multiply it by its degree (1, 2, 3, ...)
3. **Output** each result as decimal ASCII with leading zero suppression

### BF building blocks used

| Operation | Technique |
|---|---|
| Multiplication | Standard nested-loop multiply with temp cell restoration |
| Division by 10 | [Esolangs divmod algorithm](https://esolangs.org/wiki/brainfuck_algorithms#Divmod_algorithm) |
| Decimal output | Two rounds of divmod (hundreds, tens, ones) with flag-based leading zero suppression |
| Input parsing | ASCII subtraction (`char - 48` for digits, `char - 32` to detect spaces) |
| Conditional logic | Cell-zeroing with flag inversion pattern |

### Memory layout

```
Cell 0:  loop flag        Cell 4:  multiply result
Cell 1:  separator temp   Cell 5:  multiply scratch
Cell 2:  coefficient      Cell 6:  separator flag
Cell 3:  multiplier       Cells 7-20: decimal output workspace
```

### Constraints

- Input coefficients must be single digits (`0`-`9`)
- Maximum result per coefficient is `255` (8-bit cell limit), so `coefficient × degree ≤ 255`
- Practically supports polynomials up to degree ~28 with coefficient 9

## Project structure

| File | Description |
|---|---|
| `derivative.bf` | The 938-character Brainfuck program |
| `bf_codegen.py` | Python generator with pointer tracking and high-level BF operations |
| `bf_interpreter.py` | Python Brainfuck interpreter |
| `test.py` | 17 test cases |

