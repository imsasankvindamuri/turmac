import sys

if __name__ == "__main__":
    bf_code = open(sys.argv[1]).read()
    turmac_code = []
    loop_counter = 0
    loop_stack = []
    exit_stack = []
    jump_stack = []
    data_pointer = 0

    for tok in bf_code:
        if tok == "+": turmac_code.append(f"%{data_pointer} 1 + 256 %")
        elif tok == "-": turmac_code.append(f"%{data_pointer} 1 - 256 %")
        elif tok == ">": data_pointer += 1 ; turmac_code.append(f"mv %{data_pointer}")
        elif tok == "<": data_pointer -= 1 ; turmac_code.append(f"mv %{data_pointer}")
        elif tok == ".": turmac_code.append("stdout")
        elif tok == ",": turmac_code.append("stdin") ; turmac_code.append(f"%{data_pointer} 256 %")
        elif tok == "[":
            loop_counter += 1
            loop_stack.append(f"loop_{loop_counter}")
            exit_stack.append(f"exit_{loop_counter}")
            jump_stack.append(f"jump_{loop_counter}")
            turmac_code.append(f"flag {jump_stack[-1]}")
            turmac_code.append(f"is_zero {exit_stack[-1]} {loop_stack[-1]}")
            turmac_code.append(f"flag {loop_stack[-1]}")
        elif tok == "]":
            turmac_code.append(f"is_zero {jump_stack[-1]} {jump_stack[-1]}")
            turmac_code.append(f"flag {exit_stack[-1]}")
            loop_stack.pop() ; exit_stack.pop()
        else:
            continue

    open(sys.argv[2],"w").write("\n".join(turmac_code))