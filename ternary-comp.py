"""
Hello!
This is a [WIP] emulator of Trident, a simple ternary computer
inspired by the (binary) CHIP-8 and z80.
It should have a set of instructions when finished, 6813 trytes of memory,
9 six-trit registers, and one flag register.

Trytes 0-729 are reserved for important things like a possible
future fontset and/or simple OS.
"""

#hides the annoying pygame welcome message
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from logic_and_base_conversion import *
from pygame.locals import *
import pygame
import sys

pygame.init()
background_colour = (0,0,0)
screen = pygame.display.set_mode((243,243))
screen.fill(background_colour)
#The main class for the emulator
class Trident():
    #memory, in trits
    memory = [0]*6813  #That's 6813 trytes
    stack = [0]*243
    #stack pointer
    sp = 0
    #We use strings for opcodes because Python doesn't have native ternary or
    #base 27 support. 
    opcode = "0"
    #flag register
    flag = [0,0,0]
    #9 six-trit (1 Tryte) registers
    registers = [0,0,0,0,0,0,0,0,0]
    #program counter
    pc = 0
    pygame_keys = ["backspace","return","space","0","1","2",
                   "3","4","5","6","7","8","9","a",
                   "b","c","d","e","f","g","h","i","l","m",
                   "n","o","p","q","r","s","t","u","v",
                   "w","x","y","z"]
    

    def load_file(filename,debug_status):
        print("File Loading")
        ternary = open(filename, "r").read()
        i = 0
        for k in range(0,len(ternary),6):
            tryte = ternary[k:k+6]
            Trident.memory[i+729] = tryte
            if debug_status.upper() == "DEBUG":
                print("Loaded " + str(tryte) + " into " + str(i+729))
            i = i + 1
        return i
    
    def pygame_draw(can_draw,value,x,y):
        print("Drawing...")
        if can_draw:
            if value == 0:
                screen.set_at((x,y),(255,255,255))
            elif value == 1:
                screen.set_at((x,y),(128,128,128))
            else:
                screen.set_at((x,y),(0,0,0))
            pygame.display.flip()
            #return
        
    def handle_keys():
        c = 0
        x = True
        try:
            while x == True:
                #screen = pygame.display.set_mode((243,243))
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == KEYDOWN:
                            if str(pygame.key.name(event.key)) in Trident.pygame_keys:
                                x = False
                                kn = str(pygame.key.name(event.key))
                                for c,i in enumerate(Trident.pygame_keys):
                                    if kn == i:
                                        return c
        except pygame.error:
            sys.exit()
        
        
    #initialize registers and memory
    def initialize():
        print("Initialize")
        #program starts here
        Trident.pc = 729  #Trytes here, not trits
        #opcode = "0"
        Trident.flag = [0,0,0]
        Trident.sp = 0
        Trident.memory = [0]*6813
        #Initialize fonts and/or OS, whatever the system should have built in
        #here
        return

    #Emulates one cycle of the CPU
    def cycle():
        #fetches the opcode at the program counter
        opcode = Trident.memory[Trident.pc]
        #print("pc is " + str(Trident.pc))
        opcode = str(opcode)
        #Gets the first tribble for decoding
        tribble = opcode[-3:]
        #Gets just the operand, or parameter, or whatever you want to call it
        operand1 = Trident.memory[Trident.pc + 1]
        operand2 = Trident.memory[Trident.pc + 2]
        operand3 = Trident.memory[Trident.pc + 3]
        #And now, the long if-else chain!

        #000 = JP, or "Jump". Operand xxxxxx is loaded to the program counter.
        #See opcode documentation for more details
        if tribble == "000":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            tup2 = convert(operand2,3,10)
            op2 = int(''.join(map(str, tup2)))
            addr = op1 + op2
            Trident.pc = addr
        #001- Logical AND 
        elif tribble == "001":
            Trident.registers[0] = logic("AND",operand1,Trident.registers[0])
            Trident.pc = Trident.pc + 2
        #ternary OR
        elif tribble == "002":
            Trident.registers[0] = logic("OR",operand1,Trident.registers[0])
            Trident.pc = Trident.pc + 2
        #XOR
        elif tribble == "010":
            Trident.registers[0] = logic("XOR",operand1,Trident.registers[0])
            Trident.pc = Trident.pc + 2
        #NOT
        elif tribble == "011":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            unary_op("NOT",Trident.registers[op1])
            Trident.pc = Trident.pc + 2
        #PTI
        elif tribble == "012":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            unary_op("PTI",registers[op1])
            Trident.pc = Trident.pc + 2
        #NTI
        elif tribble == "020":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            unary_op("NTI",registers[op1])
            Trident.pc = Trident.pc + 2
        #SUM
        elif tribble == "021":
            registers[0] = logic("SUM",opcode,registers[0])
            Trident.pc = Trident.pc + 2
        #LDR
        elif tribble == "022":
            tup1 = convert(operand1,3,10)
            tup2 = convert(operand2,3,10)
            op1 = int(''.join(map(str, tup1)))
            op2 = int(''.join(map(str, tup2)))
            Trident.registers[op1] = Trident.registers[op2]
            Trident.pc = Trident.pc + 3
        #LD
        elif tribble == "100":
            tup1 = convert(operand1,3,10)
            tup2 = convert(operand2,3,10)
            op1 = int(''.join(map(str, tup1)))
            op2 = int(''.join(map(str, tup2)))
            Trident.registers[op1] = op2
            Trident.pc = Trident.pc + 3
        #ADD
        elif tribble == "101":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            if Trident.registers[0] + Trident.registers[op1] <= 728:
                Trident.registers[0] = Trident.registers[0] + Trident.registers[op1]
            else:
                last_tryte3 = int(str(operand1)[-6:])
                last_tryte_tup = convert(last_tryte3,3,10)
                last_tryte = int(''.join(map(str, last_tryte_tup)))
                Trident.registers[0] = last_tryte
                flag[0] = 2
            Trident.pc = Trident.pc + 2
        #SUB
        elif tribble == "102":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            Trident.registers[0] = Trident.registers[0] - Trident.registers[op1]
            Trident.pc = Trident.pc + 2
        #CP
        elif tribble == "110":
            if int(convert(operand1)) == Trident.registers[0]:
                flag[1] = 1
            Trident.pc = Trident.pc + 2
        #INC
        elif tribble == "111":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            Trident.registers[op1] = Trident.registers[op1] + 1
            Trident.pc = Trident.pc + 2
        #DEC
        elif tribble == "112":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            Trident.registers[op1] = Trident.registers[op1] - 1
            Trident.pc = Trident.pc + 2
        #NOP
        elif tribble == "120":
            pass
            Trident.pc = Trident.pc + 2
        #CLS
        elif tribble == "121":
            screen.fill(background_colour)
            Trident.pc = Trident.pc + 2
        #SNE
        elif tribble == "122":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            tup2 = convert(operand2,3,10)
            op2 = int(''.join(map(str, tup2)))
            if registers[op1] != op2:
                pass
            Trident.pc = Trident.pc + 3
        #SE
        elif tribble == "200":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            tup2 = convert(operand2,3,10)
            op2 = int(''.join(map(str, tup2)))
            if Trident.registers[op1] == Trident.registers[op2]:
                pass
            Trident.pc = Trident.pc + 3
        #PUSH
        elif tribble == "201":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            Trident.memory[Trident.sp] = Trident.registers[op1]
            Trident.sp = Trident.sp - 1
            Trident.pc = Trident.pc + 2
        #POP
        elif tribble == "202":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            Trident.registers[op1] = Trident.memory[Trident.sp]
            Trident.sp = Trident.sp + 1
            Trident.pc = Trident.pc + 2
        #RET
        elif tribble == "210":
            Trident.pc = Trident.memory[Trident.sp]
            Trident.sp = Trident.sp -1
        #DRW
        elif tribble == "211":
            can_draw = True 
            xtup = convert(operand1,3,10)
            x = int(''.join(map(str, xtup))) 
            ytup = convert(operand2,3,10)
            y = int(''.join(map(str, ytup))) 
            rows_high_tup = convert(operand3,3,10)
            rows_high = int(''.join(map(str, rows_high_tup)))
            start_addr = Trident.registers[8] + Trident.registers[7]
            row = 0
            pixel_offset = 0
            xloc = x + row
            yloc = y + pixel_offset
            while row < rows_high:
                yloc = yloc - 1
                while pixel_offset < 9:
                    xloc = xloc + 1
                    color = screen.get_at((xloc,yloc))[:3]
                    if color == (0,0,0):
                        value = 0
                    elif color == (255,255,255):
                        value = 2
                    elif color == (128,128,128):
                        value = 1
                    pixel_offset = pixel_offset + 1
                    Trident.pygame_draw(can_draw,value,xloc,yloc)
                row = row + 1
                xloc = xloc - 9
                pixel_offset = pixel_offset - 9
            can_draw = False
            Trident.pc = Trident.pc + 4
        #LDM
        elif tribble == "212":
            tuplocation1 = convert(operand1,3,10)
            tuplocation2 = convert(operand2,3,10)
            tupendreg = convert(operand3,3,10)
            location1 = int(''.join(map(str, tuplocation1)))
            location2 = int(''.join(map(str, tuplocation2)))
            loc = location1 + location2
            endreg = int(''.join(map(str, tupendreg)))
            for j in range(endreg):
                Trident.memory[loc + j] = Trident.registers[j]
                #print("mem[loc+j] = " + str(Trident.memory[loc+j]))
            Trident.pc = Trident.pc + 4
        #LDS
        elif tribble == "220":
            tup1 = convert(operand1,3,10)
            tup2 = convert(operand2,3,10)
            op1 = int(''.join(map(str, tup1)))
            op2 = int(''.join(map(str, tup2)))
            addr = op1+op2
            Trident.sp = addr
            Trident.pc = Trident.pc + 3
        #KEY
        elif tribble == "221":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            keynum = Trident.handle_keys()
            Trident.registers[op1] = keynum
            print(Trident.registers[op1])
            Trident.pc = Trident.pc + 2
                
        else:
            print("Unknown opcode")
            
    def main():
        done = False
        try:
            filename = sys.argv[1]
        except IndexError:
            print("Required argument [filename].")
            print("Syntax: python ternary-comp.py [filename] [debug status]")
            print("Where 'debug status' optional, use DEBUG to show where the file is loaded.")
        try:
            debug_status = sys.argv[2]
        except IndexError:
            debug_status = "don't debug"
        Trident.initialize()
        Trident.load_file(filename,debug_status)
        print("Cycling")
        while done == False:
            Trident.cycle()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            if Trident.pc == 0:
                done = True
        print("done.")


TriEmu = Trident
TriEmu.main()
