# Trident
Ternary computer emulator written in Python

May be bugs, please let me know if any are found.

# Usage

Run .\ternary-comp.exe FILENAME.tri
Or drag the filename.tri over the .exe. Optional argument DEBUG for..debugging .tri programs.
Like this: .\ternary-comp.exe FILENAME.tri DEBUG

# Documentation
See "opcodes.txt" for documentation on the machine instruction Trident uses.

Any file you give Trident which contains machine code must have the code all on one line, no spaces.

The included .tri files are tests. draw-test.tri should draw a block sprite. 
keyboard-test.tri ends the program when a key is pressed.

# Assembler

Will convert valid instructions into machine code, and put the machine code in a seperate file all on one line no spaces, as is needed.

It also ignores (most) comments. Single-line comments are allowed by using a semicolon (";").

Command line syntax to use it is "python Assembler.py input-file-name.txt output-file-name.tri"
