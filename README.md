My working files and solutions to [rootme](https://www.root-me.org/en) puzzles, with an emphasis on reverse engineering ("cracking") and static analysis.

## Software Used

- [Python 3.12](https://www.python.org/)
- [Hex-Rays IDA Free](https://hex-rays.com/ida-free/)
- [ILSpy](https://github.com/icsharpcode/ILSpy)

## Cracking

The `cracking/` folder contains solutions to the cracking puzzles on [rootme.org](https://www.root-me.org/en). These puzzles generally involve static analysis of an executable, deobfuscation, and other reverse engineering.

In general:

- `flag.dat` is the final flag used to complete the challenge
- `note.md`, if present, may contain notes about how the flag was obtained (such as specific commands used)
- `*.i64`, if present, contains the final state of the [IDA Free](https://hex-rays.com/ida-free/) disassembly of the input
- Additional scripts, if present, are usually written in Python 3 and would have been derived from IDA pseudocode or assembly
