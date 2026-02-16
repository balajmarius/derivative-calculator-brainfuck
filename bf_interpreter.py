#!/usr/bin/env python3
"""Brainfuck interpreter for testing."""


def run_bf(code, input_str="", cell_size=256, max_steps=1_000_000):
    """
    Run a Brainfuck program.

    Args:
        code: BF source code (only ><+-.,[] are significant)
        input_str: Input string (converted to bytes)
        cell_size: Cell value range (256 for 8-bit)
        max_steps: Maximum instructions before timeout

    Returns:
        Output string

    Raises:
        RuntimeError on timeout or unmatched brackets
    """
    # Strip non-BF characters
    ops = [c for c in code if c in "><+-.,[]"]

    # Pre-compute bracket matching
    brackets = {}
    stack = []
    for i, op in enumerate(ops):
        if op == "[":
            stack.append(i)
        elif op == "]":
            if not stack:
                raise RuntimeError(f"Unmatched ] at position {i}")
            j = stack.pop()
            brackets[j] = i
            brackets[i] = j
    if stack:
        raise RuntimeError(f"Unmatched [ at position {stack[-1]}")

    # Execute
    tape = [0] * 30000
    ptr = 0
    ip = 0
    input_bytes = input_str.encode("latin-1") if isinstance(input_str, str) else input_str
    input_pos = 0
    output = []
    steps = 0

    while ip < len(ops):
        steps += 1
        if steps > max_steps:
            raise RuntimeError(
                f"Exceeded {max_steps} steps. Output so far: {''.join(output)}"
            )

        op = ops[ip]
        if op == ">":
            ptr += 1
            if ptr >= len(tape):
                tape.extend([0] * 1000)
        elif op == "<":
            ptr -= 1
            if ptr < 0:
                raise RuntimeError(f"Pointer moved below 0 at step {steps}")
        elif op == "+":
            tape[ptr] = (tape[ptr] + 1) % cell_size
        elif op == "-":
            tape[ptr] = (tape[ptr] - 1) % cell_size
        elif op == ".":
            output.append(chr(tape[ptr]))
        elif op == ",":
            if input_pos < len(input_bytes):
                tape[ptr] = input_bytes[input_pos]
                input_pos += 1
            else:
                tape[ptr] = 0  # EOF = 0
        elif op == "[":
            if tape[ptr] == 0:
                ip = brackets[ip]
        elif op == "]":
            if tape[ptr] != 0:
                ip = brackets[ip]
        ip += 1

    return "".join(output)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python bf_interpreter.py <file.bf> [input]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        code = f.read()

    input_str = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        result = run_bf(code, input_str)
        print(result, end="")
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
