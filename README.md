# Trident
Ternary computer emulator written in Python, with its own machine language!

May be bugs, please let me know if any are found.

# Usage

To use, you must have created or use an existing .tri file containing machine code instructions to tell Trident what to do.
(See "opcodes.txt")

Run ```.\ternary-comp.exe FILENAME.tri```

Or drag the ```filename.tri``` over the .exe. 

Optional argument DEBUG for debugging .tri programs.

Like this: ```.\ternary-comp.exe FILENAME.tri DEBUG```

If you choose to run the ```ternary-comp.py``` file instead of the ```.exe```, make sure ```logic-and-base-conversion.py``` is in the same directory.

The ```.exe``` was compiled using PyInstaller. Therefore, some systems may flag it as a false positive for virus. It is not.

# Documentation
See ```opcodes.txt``` for documentation on the machine instruction Trident uses.

The ```Assembler.py``` file can convert a ```.txt``` file of valid Trident assembly instructions into a ```.tri``` file, which will contain ternary machine code on one line, no spaces. Ternary machine code uses 0's, 1's and 2's, similar to Binary which uses only 0's and 1's. 

The included ```.tri``` files are tests. draw-test.tri should draw a block sprite. 

```keyboard-test.tri``` ends the program when a key is pressed.

# Assembler

Will convert valid instructions into machine code, and put the machine code in a seperate file all on one line no spaces, as is needed.

It takes a text file containing the instructions in ternary Assembly, and outputs a .tri file which should be able to work with Trident.

It also ignores (most) comments. Single-line comments are allowed by using a semicolon (";").

Command line syntax to use it is:

```python Assembler.py input-file-name.txt output-file-name.tri```

Where ```input-file-name``` and ```output-file-name``` are replaced by the actual names of your files.

There may be bugs in this also. Please let me know if any are found so I can fix them.


# Purpose

"Why create such a thing?"
 
 1. To learn more about how computers and low level operations work
 
 2. To improve Python skills/abilities
 
 3. Gain a better understanding of machine language and how it works
 
 4. As a form of art - This project's main purpose of using Ternary rather than Binary is to demonstrate that computers and programming can be creative as well as technical, and to show that thinking outside the box is always possible.


# How would such a computer be implemented using real-life hardware?

It is the idea that:

0 - negative voltage

1- no voltage

2 - positive voltage

Ternary logic gates can be implemented using existing technologies such as standard transistors.


# Further Reading

[Ternary Computer From Scratch - Hackaday](https://hackaday.io/project/1043-base-3-ternary-computer-from-scratch)

[Mathematics behind Ternary Logic and Troolean Algebra - Prof. Douglas Jones](https://homepage.divms.uiowa.edu/~jones/ternary/logic.shtml)
