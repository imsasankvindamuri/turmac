import sys
from pathlib import Path

if __name__ == "__main__":
    file = Path(sys.argv[1])
    bf_commands : list[str] = [
            "+" , "-" , "." , "," ,
            ">" , "<" , "[" , "]",
            ]
    bf_code : list[str] = [cmd for cmd in file.read_text() if cmd in bf_commands]

    output = Path(f"{file.with_suffix('.turmac')}")
    output.touch()

    turmac_code = []
    data_pointer = 0
    num_loops = 0
    loop_lable_stack = []

    for cmd in bf_code:
        # A naive implementation first.
        # A more optimized implementation will be done when I port this to Rust.
        if cmd == "+":
            turmac_code.append(f"""
            %{data_pointer} 1 + 256 %
            """)
        elif cmd == "-":
            turmac_code.append(f"""
            %{data_pointer} 1 - 256 %
            """)
        elif cmd == ".":
            turmac_code.append("""
            stdout
            // Please note that TURMAC and BF don't map perfectly
            // This prints the raw integer value, rather than the ASCII value
            """)
        elif cmd == ",":
            turmac_code.append(f"""
            stdin\n%{data_pointer} 256 %
            // Please note that TURMAC and BF don't map perfectly
            // This takes input and converts into the ASCII value
            // of a single ASCII character
            """)
        elif cmd == ">":
            data_pointer += 1
            turmac_code.append(f"""
            mv %{data_pointer}
            """)
        elif cmd == "<":
            data_pointer -= 1
            turmac_code.append(f"""
            mv %{data_pointer}
            """)
        elif cmd == "[":
            num_loops += 1
            loop_lable_stack.append(num_loops)
            turmac_code.append(f"""
            is_zero end_{loop_lable_stack[-1]} loop_{loop_lable_stack[-1]}\nflag loop_{loop_lable_stack[-1]}
            """)
        elif cmd == "]":
            turmac_code.append(f"""
            is_zero end_{loop_lable_stack[-1]} loop_{loop_lable_stack[-1]}\nflag end_{loop_lable_stack[-1]}
            """)
            loop_lable_stack.pop()


    with output.open("w") as output_file:
        output_file.write("\n".join([cmd.strip() for cmd in turmac_code]))
