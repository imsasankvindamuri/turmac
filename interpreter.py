import sys
import re

"""
I gotta thank King Varuna for giving me the insight for my language in a dream.

TURMAC : TURing MAChine ---- A ASM and BrainFuck inspired minimal esoteric programming language,
meant to simulate a Turning Machine using ASM-style syntax.
"""

class TURMAC:
    
    def __init__(self, raw_code : str) -> None:
        self.tape_length : int = 2**10
        self.memory_tape : list[int] = [0 for i in range(self.tape_length)]
        """
        Tape length is set to 15 for the sake of simple debugging for now...
        I don't want my terminal spitting out 1024 0s every time I try to debug
        using print(self.memory_tape)
        """
        self.data_pointer : int = 0
        self.program_counter : int = 0

        self.raw_code = raw_code
        self.tokenized_code = self.tokenize()

        # self.stdlib will have a command - regex pairing so that eval() can easily verify if the command is valid.
        self.stdlib_syntax_verify = {
            "stdout" : r"^stdout$",
            "mv" : r"^mv (%\d+)$",
            "inc" : r"^inc (\d+)$",
            "stdin" : r"^stdin$",
            "end" : r"^end$",
            "flag" : r"^flag ([a-zA-Z_][a-zA-Z0-9_]+)$",
            "is_zero" :r"^is_zero ([a-zA-Z_][a-zA-Z0-9_]+) ([a-zA-Z_][a-zA-Z0-9_]+)$"
        }

        self.flag_registry = {}


        self.stdlib_execute = {
            "stdout" : self._stdout,
            "mv" : self._mv,
            "inc" : self._inc,
            "stdin" : self._stdin,
            "end" : self._end,
            "flag" : self._flag,
            "is_zero" : self._is_zero,
        }

    def execute(self) -> None:
        """
        Every line in my language is either:
        - Whitespace/comments (ignore)
        - RPN (evaluate and push to *data_pointer)
        - A command (evaluate syntax via regex, then execute)

        I hope this is easy... I keep failing at everything I do.
        If I keep this up, my future wife will leave me for a Rust dev,
        and I'll be sad and alone.
        """

        # Create a universal registry of flags to allow for jumping
        self.set_flag_registry()

        while self.program_counter < len(self.tokenized_code):
            cmd = self.tokenized_code[self.program_counter].split()

            if cmd[0] in list(self.stdlib_syntax_verify.keys()):
                """
                Do something for syntax checking, probably using regex
                Seems legit? Execute. No? Panic.
                """

                full_line = " ".join(cmd)
                match = re.fullmatch(self.stdlib_syntax_verify[cmd[0]], full_line)

                if match:
                    captured_args = list(match.groups())

                    proper_args : list[int] = []
                    if cmd[0] not in ["flag","is_zero"]:
                        for arg in captured_args:
                            if re.fullmatch(r"^%\d+$", arg):
                                proper_args.append(int(arg[1:]))
                            else:
                                proper_args.append(int(arg))
                        if not proper_args:
                            self.stdlib_execute[cmd[0]]()
                        else:
                            self.stdlib_execute[cmd[0]](proper_args)

                    else:
                        self.stdlib_execute[cmd[0]]([arg for arg in captured_args])

                else:
                    raise SyntaxError(f"Uh Oh... Expected syntax '{self.stdlib_syntax_verify[cmd[0]]}', received syntax '{" ".join(cmd)}'")
            else:
                self.eval_rpn(cmd)

            self.program_counter += 1
        ...
        print(self.flag_registry)
        # print(self.memory_tape)

    def eval_rpn(self, toks : list[str] = [""]) -> None:
        valid_ops = {
            "+" : lambda a , b : int(a) + int(b),
            "-" : lambda a , b : int(a) - int(b),
            "*" : lambda a , b : int(a) * int(b),
            "/" : lambda a , b : int(a) // int(b),
            "^" : lambda a , b : int(a) ** int(b),
            "%" : lambda a , b : int(a) % int(b),
            "==" : lambda a , b : 1 if (int(a) == int(b)) else 0,
            ">=" : lambda a , b : 1 if (int(a) >= int(b)) else 0,
            "<=" : lambda a , b : 1 if (int(a) <= int(b)) else 0,
            ">" : lambda a , b : 1 if (int(a) > int(b)) else 0,
            "<" : lambda a , b : 1 if (int(a) < int(b)) else 0,
        }

        stack = []
        for tok in toks:
            if tok.isdigit(): stack.append(int(tok))
            elif tok in list(valid_ops.keys()):
                rhs = stack.pop() ; lhs = stack.pop()
                stack.append(valid_ops[tok](lhs , rhs))
            else:
                if re.fullmatch(r"^%\d+$", tok):
                    stack.append(self.memory_tape[int(tok[1:])])


        if len(stack) != 1: raise Exception(f"""Uh Oh... Something went wrong at Program Counter = {self.program_counter} :
            '{self.tokenized_code[self.program_counter]}'""")
        
        self.memory_tape[self.data_pointer] = stack[0]
    
    def tokenize(self) -> list[str]:
        code_lines = [
            line.strip() for line in self.raw_code.split("\n") if line.strip() != "" and not line.strip().startswith("//")
        ]
        # Will add more tokenization features later
        return code_lines

    def state(self) -> None:
        print(f"/// Memory Tape = {self.memory_tape} | Program Counter = {self.program_counter} | Data Pointer = {self.data_pointer} ///")
    
    def set_flag_registry(self) -> None:
        line_number = 0
        while line_number < len(self.tokenized_code):
            command = self.tokenized_code[line_number]
            cmd = command.split()
            if cmd[0] == "flag":
                match = re.fullmatch(self.stdlib_syntax_verify[cmd[0]], command)
                if not match:
                    raise SyntaxError(f"Uh Oh... Expected syntax '{self.stdlib_syntax_verify[cmd[0]]}', received syntax '{command}'")
                else:
                    flag_name = list(match.groups())[0]
                    self.flag_registry[flag_name] = line_number
            line_number += 1

    def _stdout(self) -> None:
        print(self.memory_tape[self.data_pointer])
        print()

    def _mv(self, move_location : list[int]) -> None:
        self.data_pointer = move_location[0]

    def _inc(self, amt : list[int]) -> None:
        self.memory_tape[self.data_pointer] += amt[0]

    def _stdin(self) -> None:
        try:
            val = int(input(f"Please provide input for Memory Location {self.data_pointer}:\n"))
            self.memory_tape[self.data_pointer] = val
        except ValueError:
            raise ValueError("TURMAC is a mono-typed language and only accepts integers.")

    def _end(self) -> None:
        self.program_counter = len(self.tokenized_code)

    def _flag(self, args : list[str]) -> None:
        print(f"At flag '{args[0]}'.\n")

    def _is_zero(self, args : list[str]) -> None:
        # Verify if both flags exist
        flag1 , flag2 = args[0], args[1]
        chosen : str

        if flag1 not in list(self.flag_registry.keys()):
            raise Exception(f"Nonexistent flag called '{flag1}'")
        if flag2 not in list(self.flag_registry.keys()):
            raise Exception(f"Nonexistent flag called '{flag1}'")
        
        if self.memory_tape[self.data_pointer] == 0:
            chosen = flag1
        else:
            chosen = flag2

        self.program_counter = self.flag_registry[chosen]


if __name__ == "__main__":
    code = open(sys.argv[1]).read()
    
    TURMAC(code).execute()
    ...