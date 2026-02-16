#!/usr/bin/env python3
"""
Brainfuck code generator for a polynomial derivative calculator.

Input format:  Coefficients from constant term to highest degree,
               single digits (0-9), space-separated, newline-terminated.
               Example: "1 5 0 3" means 1 + 5x + 0x^2 + 3x^3

Output format: Derivative coefficients in same format.
               Example: "5 0 9" means 5 + 0x + 9x^2
"""


class BF:
    """BF code generator with automatic pointer tracking."""

    def __init__(self):
        self.code = []
        self.pos = 0

    def _goto(self, cell):
        diff = cell - self.pos
        if diff > 0:
            self.code.append(">" * diff)
        elif diff < 0:
            self.code.append("<" * (-diff))
        self.pos = cell

    def inc(self, cell, n=1):
        self._goto(cell)
        self.code.append("+" * n)

    def dec(self, cell, n=1):
        self._goto(cell)
        self.code.append("-" * n)

    def clear(self, cell):
        self._goto(cell)
        self.code.append("[-]")

    def read(self, cell):
        self._goto(cell)
        self.code.append(",")

    def write(self, cell):
        self._goto(cell)
        self.code.append(".")

    def loop_open(self, cell):
        self._goto(cell)
        self.code.append("[")

    def loop_close(self, cell):
        self._goto(cell)
        self.code.append("]")

    def move(self, src, dst):
        """Move src to dst. src -> 0, dst must be 0."""
        self._goto(src)
        self.code.append("[-")
        self._goto(dst)
        self.code.append("+")
        self._goto(src)
        self.code.append("]")

    def copy(self, src, dst, tmp):
        """Copy src to dst via tmp. dst and tmp must be 0. src preserved."""
        self._goto(src)
        self.code.append("[-")
        self._goto(dst)
        self.code.append("+")
        self._goto(tmp)
        self.code.append("+")
        self._goto(src)
        self.code.append("]")
        self.move(tmp, src)

    def multiply(self, a, b, result, tmp):
        """result = a * b. a consumed (->0). b preserved. result,tmp must be 0."""
        self._goto(a)
        self.code.append("[-")  # while a > 0: a--
        self._goto(b)
        self.code.append("[-")  # while b > 0: b--
        self._goto(result)
        self.code.append("+")  # result++
        self._goto(tmp)
        self.code.append("+")  # tmp++
        self._goto(b)
        self.code.append("]")  # end b loop
        self.move(tmp, b)  # restore b from tmp
        self._goto(a)
        self.code.append("]")  # end a loop

    def divmod_10(self, base):
        """
        Divmod by 10 using esolangs algorithm.

        Uses 6 consecutive cells: base through base+5.
        Input:  base+1 = dividend (n), others = 0.
        Sets base+2 = 10 (divisor) internally.

        Output: base+3 = n%10 (remainder), base+4 = n/10 (quotient).
        Side effect: base+2 gets junk (d - remainder). Cleaned up here.
        """
        self.inc(base + 2, 10)  # set divisor = 10
        # Esolangs divmod: >[->-[>+>>]>[+[-<+>]>+>>]<<<<<]
        # Pointer starts at base, moves to base+1, loop exits at base+1
        self._goto(base)
        self.code.append(">")
        self.pos = base + 1
        self.code.append("[->-[>+>>]>[+[-<+>]>+>>]<<<<<]")
        self.pos = base + 1  # algorithm exits with pointer at base+1 (the n cell)
        # Clean up junk in base+2
        self.clear(base + 2)

    def print_number(self, val_cell, ws):
        """
        Print number in val_cell as decimal ASCII (0-255).
        val_cell is consumed (becomes 0).
        Uses cells ws through ws+13 as workspace (must all be 0).

        Layout after divmods:
          ones     = ws+3
          tens     = ws+9
          hundreds = ws+10
          flag_h   = ws+12
          flag_t   = ws+13
        """
        # Move value to ws+1 for first divmod
        self.move(val_cell, ws + 1)

        # First divmod: (value) / 10
        # Input:  ws+1 = value
        # Output: ws+3 = ones (value%10), ws+4 = quotient (value/10)
        self.divmod_10(ws)

        # Move quotient to ws+7 for second divmod
        self.move(ws + 4, ws + 7)

        # Second divmod: (value/10) / 10
        # Input:  ws+7 = value/10
        # Output: ws+9 = tens, ws+10 = hundreds
        self.divmod_10(ws + 6)

        # Now: ones=ws+3, tens=ws+9, hundreds=ws+10

        # Set flags for leading zero suppression
        self.inc(ws + 12)  # flag_h = 1
        self.inc(ws + 13)  # flag_t = 1

        # --- Branch 1: hundreds > 0 -> print all three digits ---
        self.loop_open(ws + 10)
        self.dec(ws + 12)  # flag_h = 0
        self.dec(ws + 13)  # flag_t = 0
        # Print hundreds
        self.inc(ws + 10, 48)
        self.write(ws + 10)
        self.clear(ws + 10)
        # Print tens
        self.inc(ws + 9, 48)
        self.write(ws + 9)
        self.clear(ws + 9)
        # Print ones
        self.inc(ws + 3, 48)
        self.write(ws + 3)
        self.clear(ws + 3)
        self.loop_close(ws + 10)

        # --- Branch 2: hundreds == 0 (flag_h still 1) ---
        self.loop_open(ws + 12)
        self.dec(ws + 12)  # consume flag_h

        # Sub-branch 2a: tens > 0 -> print tens and ones
        self.loop_open(ws + 9)
        self.dec(ws + 13)  # flag_t = 0
        self.inc(ws + 9, 48)
        self.write(ws + 9)
        self.clear(ws + 9)
        self.inc(ws + 3, 48)
        self.write(ws + 3)
        self.clear(ws + 3)
        self.loop_close(ws + 9)

        # Sub-branch 2b: tens == 0 (flag_t still 1) -> print just ones
        self.loop_open(ws + 13)
        self.dec(ws + 13)  # consume flag_t
        self.inc(ws + 3, 48)
        self.write(ws + 3)
        self.clear(ws + 3)
        self.loop_close(ws + 13)

        self.loop_close(ws + 12)

    def output(self):
        raw = "".join(self.code)
        return "".join(c for c in raw if c in "><+-.,[]")


def generate():
    """Generate the complete BF derivative calculator."""
    bf = BF()

    # =========================================================
    # Memory layout:
    #   Cell 0:  loop_flag (1 = continue main loop)
    #   Cell 1:  separator temp / output temp
    #   Cell 2:  value (current coefficient, consumed by multiply)
    #   Cell 3:  multiplier (preserved across iterations)
    #   Cell 4:  result (multiply output)
    #   Cell 5:  temp (multiply scratch)
    #   Cell 6:  separator flag
    #   Cells 7-20: print_number workspace
    # =========================================================

    # --- Phase 0: Read and discard constant term ---
    bf.read(0)  # read constant digit
    bf.clear(0)  # discard it
    bf.read(0)  # read separator after constant

    # Check if separator is space (ASCII 32)
    bf.dec(0, 32)  # cell0 = 0 if space, non-zero otherwise

    # Set flag: cell1 = 1 (means "was space")
    bf.inc(1)

    # If cell0 != 0 (not space): clear cell1
    bf.loop_open(0)
    bf.dec(1)  # cell1 = 0
    bf.clear(0)  # cell0 = 0
    bf.loop_close(0)

    # Now: cell1 = 1 if space (has more coefficients)
    #      cell1 = 0 if not space (constant polynomial)

    # Set cell6 = 1 (flag for "was NOT space" / constant case)
    bf.inc(6)

    # If cell1 != 0 (was space): clear cell6, set cell0 = 1 for main loop
    bf.loop_open(1)
    bf.dec(6)  # cell6 = 0
    bf.dec(1)  # consume cell1
    bf.inc(0)  # cell0 = 1 (enter main loop)
    bf.loop_close(1)

    # If cell6 != 0 (constant polynomial): output "0\n"
    bf.loop_open(6)
    bf.dec(6)  # consume flag
    bf.inc(1, 48)  # cell1 = '0'
    bf.write(1)
    bf.clear(1)
    bf.inc(1, 10)  # cell1 = '\n'
    bf.write(1)
    bf.clear(1)
    bf.loop_close(6)

    # --- Phase 1: Main derivative loop ---

    # Set multiplier = 1
    bf.inc(3)

    # Main loop (while cell0 != 0)
    bf.loop_open(0)

    # Clear loop flag (will set back to 1 if continuing)
    bf.dec(0)

    # Read digit, convert to value
    bf.read(2)  # cell2 = digit char
    bf.dec(2, 48)  # cell2 = digit value (0-9)

    # Multiply: cell4 = cell2 * cell3
    # cell2 consumed, cell3 preserved
    bf.multiply(2, 3, 4, 5)

    # Print result (cell4) as decimal. Uses cells 7-20.
    bf.print_number(4, 7)

    # Increment multiplier
    bf.inc(3)

    # Read separator
    bf.read(1)  # cell1 = separator char
    bf.dec(1, 32)  # cell1 = 0 if space, non-zero if newline/EOF

    # Set cell6 = 1 (flag for "was space")
    bf.inc(6)

    # If cell1 != 0 (not space): clear cell6, print newline (end of output)
    bf.loop_open(1)
    bf.dec(6)  # cell6 = 0 (not space -> stop)
    bf.clear(1)  # cell1 = 0
    # Print newline here (last coefficient done)
    bf.inc(1, 10)
    bf.write(1)
    bf.clear(1)
    bf.loop_close(1)

    # If cell6 != 0 (was space): set loop flag, print space
    bf.loop_open(6)
    bf.dec(6)  # consume flag
    bf.inc(0)  # cell0 = 1 (continue loop)
    bf.inc(1, 32)  # cell1 = ' '
    bf.write(1)
    bf.clear(1)
    bf.loop_close(6)

    # Back to cell0 for loop check
    bf.loop_close(0)

    return bf.output()


if __name__ == "__main__":
    code = generate()
    print(f"Generated BF code ({len(code)} characters):")
    print(code)

    # Also write to file
    with open("derivative.bf", "w") as f:
        f.write(code)
    print(f"\nWritten to derivative.bf")
