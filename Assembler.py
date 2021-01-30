import sys
import re

words_list = ["JP","AND","OR","XOR","NOT","PTI","NTI","SUM","LDR","LD",
              "ADD","SUB","CP","INC","DEC","NOP","CLS","SNE","SE",
              "PUSH","POP","RET","DRW","LDM","LDS","KEY","JC"]

opcodes_list = ["000000","000001","000002","000010","000011","000012",
                "000020","000021","000022","000100",
                "000101","000102","000110","000111","000112","000120",
                "000121","000122","000200","000201",
                "000202","000210","000211","000212","000220","000221","000222"]


def check_file(outfile):
    with open(outfile,"r") as file_boi:
        data = file_boi.read()
        numchars = len(data)
        if numchars % 6 == 0:
            print("Assemble was successful :)")
        else:
            print("Assemble failed :(")
            print("Try removing comments that contain keywords or weird characters.")
            print("Make sure you use correct syntax.")

def replace_str(file_name, stext, rtext):
    with open(file_name,"r") as file:
        lines = file.readlines()
    with open(file_name,"w") as file1:
        for l in lines:
            file1.write(l.replace(stext,rtext))

def remove_newline(outfile):
    string_without_line_breaks = ""
    with open(outfile,"r") as ff:
        for the_line in ff:
            stripped_line = the_line.rstrip()
            string_without_line_breaks += stripped_line
    with open(outfile,"w") as fff:
        fff.write(string_without_line_breaks)
            
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
        
def assemble(program_file,outfile):
   with open(program_file,"r") as f:
       with open(outfile,"w") as f1:
            lines = f.readlines()
            for l in lines:
                for c,item in enumerate(words_list):
                    if findWholeWord(item)(l):
                        f1.write(l.replace(words_list[c],opcodes_list[c]))
            for x,m in enumerate(lines):
                if ";" in m:
                    replace_str(outfile,";","")
                else:
                    continue
   replace_str(outfile," ","")
   remove_newline(outfile)
   print("Ok! Done!")
   
def main():
    #print("Arguments: [program-file] [output file]")
    program_file = sys.argv[1]
    outfile = sys.argv[2]
    assemble(program_file,outfile)
    check_file(outfile)


main()
