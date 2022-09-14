"""
Hello!
This is a [WIP] emulator of Trident, a simple ternary computer
inspired by the (binary) CHIP-8 and z80.
It should have a set of instructions when finished, 6813 trytes of memory,
9 six-trit registers, and one flag register.
"""

#hides the annoying pygame welcome message
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

#imports go here.
#We use pygame to simulate the screen and handle the keyboard.
#logic_and_base_conversion contains a useful module, baseconvert,
#as well as some functions that make ternary base conversion easy.
#The pkg_resources is needed for building to exe with pyinstaller
from logic_and_base_conversion import *
from pygame.locals import *
import pygame
import sys
#import pkg_resources.py2_warn

#Initialize the pygame screen
#Make the background color black, set it to the
#right dimensions (243x243), all that
pygame.init()
background_colour = (0,0,0)
screen = pygame.display.set_mode((243,243),pygame.NOFRAME)
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
    #9 six-trit (1 Tryte) registers
    registers = [0,0,0,0,0,0,0,0,0,[0,0,0]]
    #program counter
    pc = 0
    #The keys of the keyboard that Trident can recognize
    pygame_keys = ["backspace","return","space","0","1","2",
                   "3","4","5","6","7","8","9","a",
                   "b","c","d","e","f","g","h","i","j","k","l","m",
                   "n","o","p","q","r","s","t","u","v",
                   "w","x","y","z"]
    

    #Loads the .tri file. Prints debug message if
    #debug is on.
    def load_file(filename,debug_status):
        print("File Loading")
        ternary = open(filename, "r").read()
        i = 0
        #reads the file a tryte at a time
        for k in range(0,len(ternary),6):
            tryte = ternary[k:k+6]
            Trident.memory[i+13] = tryte
            if debug_status.upper() == "DEBUG":
                print("Loaded tryte " + str(tryte) + " into memory location " + str(i+13))
            i = i + 1
        return i

    #This handles drawing to the screen.
    #Is used by the DRW command.
    #Where can_draw is a boolean and x,y are coordinates.
    #value is the trit of memory at the location.
    def pygame_draw(can_draw,value,x,y):
        #print("Drawing...")
        if can_draw:
            #Ternary XORs the value from the DRW command
            #with the value of the pixel on the screen.
            #0 = white, 1 = grey, 2 = black
            if value == 0:
                screen.set_at((x,y),(255,255,255))
            elif value == 1:
                screen.set_at((x,y),(128,128,128))
            else:
                screen.set_at((x,y),(0,0,0))
            #update the screen
            pygame.display.flip()

    #Deals with the keyboard and keys used by Trident
    #What this does is, it gets the name of the key
    #which is pressed and returns it. 
    def handle_keys():
        c = 0
        x = True
        try:
            while x == True:
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
        #Trident.pc = 729  #Trytes here, not trits
        Trident.pc = 13 #program counter starts at tryte 13
        #opcode = "0"
        Trident.registers = [0,0,0,0,0,0,0,0,0,[0,0,0]]
        Trident.sp = 0 #stack pointer
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

        #make it easier to use flags by assigning them to variable
        flags = Trident.registers[9]
        
        #And now, the long if-else chain!

        cmds_dict = {"JP":"000","AND":"001","OR":"002","XOR":"003",
                     "NOT":"011","PTI":"012","NTI":"020","SUM":"021",
                     "LDR":"022","LD":"100",
                     "ADD":"101","SUB":"102","CP":"110","INC":"111",
                     "DEC":"112","NOP":"120","CLS":"121",
                     "SNE":"122","SE":"200",
                     "PUSH":"201","POP":"202","RET":"210",
                     "DRW":"211","LDM":"212","LDS":"220","KEY":"221","JC":"222"
                     }
        print(list(cmds_dict.keys())[list(cmds_dict.values()).index(tribble)])
        #print(tribble) 

        #000 = JP, or "Jump".
        #See opcode documentation for more details
        if tribble == "000":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            str2 = convert(operand2,3,10)
            op2 = int(str2)
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
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            unary_op("NOT",Trident.registers[op1])
            Trident.pc = Trident.pc + 2
        #PTI
        elif tribble == "012":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            unary_op("PTI",registers[op1])
            Trident.pc = Trident.pc + 2
        #NTI
        elif tribble == "020":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            unary_op("NTI",registers[op1])
            Trident.pc = Trident.pc + 2
        #SUM
        elif tribble == "021":
            registers[0] = logic("SUM",opcode,registers[0])
            Trident.pc = Trident.pc + 2
        #LDR
        elif tribble == "022":
            str1 = convert(operand1,3,10)
            str2 = convert(operand2,3,10)
            op1 = int(str1)
            op2 = int(str2)
            Trident.registers[op1] = Trident.registers[op2]
            Trident.pc = Trident.pc + 3
        #LD
        elif tribble == "100":
            str1 = convert(str(operand1),3,10)
            str2 = convert(str(operand2),3,10)
            op1 = int(str1)
            op2 = int(str2)
            Trident.registers[op1] = op2
            Trident.pc = Trident.pc + 3
        #ADD
        elif tribble == "101":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            #if there's no overflow
            if Trident.registers[0] + Trident.registers[op1] <=728:
                Trident.registers[0] = Trident.registers[0] + Trident.registers[op1]
                flags[2] = 0
            #if there's overflow
            else:
                Trident.registers[0] = (Trident.registers[0] + Trident.registers[op1]) - 729
                flags[2] = 2
            Trident.pc = Trident.pc + 2
        #SUB
        elif tribble == "102":
            tup1 = convert(operand1,3,10)
            op1 = int(''.join(map(str, tup1)))
            Trident.registers[0] = Trident.registers[0] - Trident.registers[op1]
            if Trident.registers[0] < Trident.registers[op1]:
                flags[2] = 2
            else:
                flags[2] = 0
            Trident.pc = Trident.pc + 2
        #CP
        elif tribble == "110":
            if int(convert(operand1,3,10)) == Trident.registers[0]:
                flags[1] = 2
            else:
                flags[1] = 0
            Trident.pc = Trident.pc + 2
        #INC
        elif tribble == "111":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            Trident.registers[op1] = Trident.registers[op1] + 1
            Trident.pc = Trident.pc + 2
        #DEC
        elif tribble == "112":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            Trident.registers[op1] = Trident.registers[op1] - 1
            Trident.pc = Trident.pc + 2
        #NOP
        elif tribble == "120":
            pass
            Trident.pc = Trident.pc + 2
        #CLS
        elif tribble == "121":
            screen.fill(background_colour)
            pygame.display.flip()
            Trident.pc = Trident.pc + 1
        #SNE
        elif tribble == "122":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            str2 = convert(operand2,3,10)
            op2 = int(str2)
            if Trident.registers[op1] != op2:
                pass
            Trident.pc = Trident.pc + 3
        #SE
        elif tribble == "200":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            str2 = convert(operand2,3,10)
            op2 = int(str2)
            if Trident.registers[op1] == Trident.registers[op2]:
                """try:
                    Trident.cycle()
                except RecursionError:
                    print("Infinite Loop Error")"""
                Trident.pc = Trident.pc + 7
            else:
                Trident.pc = Trident.pc + 3
        #PUSH
        elif tribble == "201":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            #Trident.memory[Trident.sp] = Trident.registers[op1]
            Trident.stack[Trident.sp] = Trident.registers[op1]
            Trident.sp = Trident.sp - 1
            Trident.pc = Trident.pc + 2
        #POP
        elif tribble == "202":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            #Trident.registers[op1] = Trident.memory[Trident.sp]
            Trident.registers[op1] = Trident.stack[Trident.sp]
            Trident.sp = Trident.sp + 1
            Trident.pc = Trident.pc + 2
        #RET
        elif tribble == "210":
            Trident.pc = Trident.memory[Trident.sp]
            Trident.sp = Trident.sp -1
        #DRW
        elif tribble == "211":
            can_draw = True 
            xstr = convert(operand1,3,10)
            x = int(xstr) 
            ystr = convert(operand2,3,10)
            y = int(ystr) 
            rows_high_str = convert(operand3,3,10)
            rows_high = int(rows_high_str)
            start_addr = Trident.registers[8] + Trident.registers[7]
            row = 0
            pixel_offset = 0
            xloc = x + row
            yloc = y + pixel_offset
            while row < rows_high:
                yloc = yloc - 1
                cur_row = Trident.memory[row + start_addr]
                str_row = convert(str(cur_row),10,3)
                while len(str_row) < 6:
                    str_row = ''.join(("0",str_row))
                while pixel_offset < 6:
                    xloc = xloc + 1
                    color = str_row[pixel_offset]
                    if color == "0":
                        value = 0
                    elif color == "2":
                        value = 2
                    elif color == "1":
                        value = 1
                    pixel_offset = pixel_offset + 1
                    Trident.pygame_draw(can_draw,value,xloc,yloc)
                row = row + 1
                xloc = xloc - 6
                pixel_offset = pixel_offset - 6
            can_draw = False
            Trident.pc = Trident.pc + 4
        #LDM
        elif tribble == "212":
            strlocation1 = convert(operand1,3,10)
            strlocation2 = convert(operand2,3,10)
            strendreg = convert(operand3,3,10)
            location1 = int(strlocation1)
            location2 = int(strlocation2)
            loc = location1 + location2
            endreg = int(strendreg)
            if endreg!= 0:
                for j in range(endreg):
                    converted = convert(str(Trident.registers[j]),10,3)
                    for n in range(7):
                        if len(converted) < n:
                            converted = "0" + converted
                    Trident.memory[loc + j] = converted
                    print("LDM-Loaded " + converted + " into " + str(loc+j))
            else:
                converted = convert(str(Trident.registers[0]),10,3)
                for n in range(7):
                    if len(converted) < n:
                        converted = "0" + converted
                Trident.memory[loc] = converted
                print("Loaded (using LDM)- " + converted + " into " + str(loc))
                #print("mem[loc+j] = " + str(Trident.memory[loc+j]))
            Trident.pc = Trident.pc + 4
        #LDS
        elif tribble == "220":
            str1 = convert(operand1,3,10)
            str2 = convert(operand2,3,10)
            op1 = int(str1)
            op2 = int(str2)
            addr = op1+op2
            Trident.sp = addr
            Trident.pc = Trident.pc + 3
        #KEY
        elif tribble == "221":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            keynum = Trident.handle_keys()
            Trident.registers[op1] = keynum
            Trident.pc = Trident.pc + 2
        #JC
        elif tribble == "222":
            str1 = convert(operand1,3,10)
            op1 = int(str1)
            str2 = convert(operand2,3,10)
            op2 = int(str2)
            str3 = convert(operand3,3,10)
            op3 = int(str3)
            if flags[op1] == 2:
                addr = op2 + op3
                Trident.pc = addr
            else:
                Trident.pc = Trident.pc + 4
                
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
