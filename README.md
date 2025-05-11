# TURMAC

**TURMAC** (TURing MAChine) is a brutalist, minimalist esoteric programming language focused on expressiveness through constraint. It is designed to investigate the boundaries of Turing completeness, symbolic computation, and the implementation of low-level logic using minimal syntax.

> TURMAC is not intended to be practical—its value lies in what it reveals about computation, not what it replaces.

## What is an Esoteric Language?

An **esoteric programming language** (or *esolang*) is a language created primarily for experimentation, fun, or exploration of theoretical ideas in computer science. They are typically not meant for general-purpose development but rather to challenge norms, express art, or probe the definition of "programming."

TURMAC is an esolang inspired by languages like [Brainfuck](https://esolangs.org/wiki/Brainfuck), [Befunge](https://esolangs.org/wiki/Befunge), and minimalist assembly languages.

---

## Key Features

- **Monotyped Language**: Only integer types are supported.
- **RPN-Style Evaluation**: Most expressions use Reverse Polish Notation.
- **Fixed Memory Model**: Uses direct memory locations (e.g., `%0`, `%1`, ...) with no dynamic resizing.
- **Control Flow via Flags**: Conditional jumps based on the value at the data pointer.
- **Turing Complete**: A one-to-one mapping from Brainfuck to TURMAC exists (via transpilation), which implies TURMAC’s Turing completeness.

---

## Language Syntax

| Command      | Description |
|--------------|-------------|
| `stdin`      | Takes integer input and stores it at the current data pointer location. |
| `stdout`     | Prints the value at the current data pointer. |
| `mv %n`      | Moves the data pointer to memory cell `%n`. |
| `inc n`      | Increments the value at the data pointer by `n`. |
| `flag <label>` | Marks a location in the code that `is_zero` can jump to. |
| `is_zero a b` | If the current value is 0, jump to label `a`; else, jump to `b`. |
| `end`        | Immediately halts execution. |
| _RPN expression_ | Any other statement is interpreted as an RPN expression and evaluated. |

---

## Example: Fibonacci Sequence

```turmac
stdin           

mv %2
%2 1 +          

flag condition
mv %0
is_zero yes no

flag yes
end

flag no
mv %1
stdout          

mv %3
%2 0 +          

mv %2
%2 %1 +         

mv %1
%3 0 +          

mv %0
%0 1 -

is_zero condition condition
````

---

## Paradigm Programs

Below is a list of classic esolang benchmarks that test various aspects of Turing completeness, looping, arithmetic, and memory control. These are ideal candidates to showcase TURMAC’s expressiveness:

### 1. **Truth Machine**

* **Goal**: Print the input forever if it is `1`; otherwise, print it once.
* **Demonstrates**: Conditional branching, infinite looping, and input/output.
* **Brainfuck**: `,.[-->>+[<]<]<[.]`

### 2. **Cat Program**

* **Goal**: Echo any input back to the user.
* **Demonstrates**: Character I/O loop.
* **Brainfuck**: `,[.,]`

### 3. **Adder**

* **Goal**: Read two integers and output their sum.
* **Demonstrates**: Arithmetic, input parsing.
* **Note**: May require building a tokenizer if not assuming newline-separated input.

### 4. **Factorial**

* **Goal**: Compute `n!` for a given input `n`.
* **Demonstrates**: Arithmetic loops and multiplicative state.

### 5. **Mandelbrot Set (ASCII Rendered)**

* **Goal**: Renders the Mandelbrot fractal using ASCII characters.
* **Demonstrates**: High-complexity computation, nested loops, RPN stack usage.
* **Note**: Very few esolangs can run this fully due to complexity.

---

## Development Roadmap

### ✅ Version 0.1.0 (Current)

* RPN Evaluation
* Core commands (`stdin`, `stdout`, `mv`, `inc`, `flag`, `is_zero`, `end`)
* Brainfuck transpiler

### ⏳ Version 0.1.1 (Planned)

* `set n`: Initializes tape length statically at program start.
* Improved input sanitization
* Debug mode

### 🚧 Version 0.2.0 (Rewrite in Rust)

* Learn Rust through systems programming
* Implement a proper lexer + parser
* Performance-focused VM

---

## Why This Project?

TURMAC explores:

* **Language minimalism**: What is the minimum structure needed to achieve universality?
* **Systems thinking**: How can a simple rule set simulate arbitrary computation?
* **Self-education**: Designed as a vehicle for exploring language design, parsing theory, and Rust.

This language is not intended to be practical but is a serious intellectual project grounded in theory and expressive constraint.

---

## Contributing

TURMAC is currently a solo project. However, bug reports, suggestions, or curious questions are welcome. You can fork it, play with the transpiler, or try writing a program in it!

---

## License

MIT License.

---

## Author

Built by [V Sai Sasank (aka NotAUniquePerson)](https://github.com/imsasankvindamuri), CSE student, Python enthusiast, and esolang explorer.
