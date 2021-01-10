import sys
import re

words_list = ["JP","AND","OR","XOR","NOT","PTI","NTI","SUM","LDR","LD",
              "ADD","SUB","CP","INC","DEC","NOP","CLS","CALL","SNE","SE",
              "PUSH","POP","RET","DRW","LDM"]

opcodes_list = ["000","001","002","010","011","012","020","021","022","100",
                "101","102","110","111","112","120","121","122","200","201",
                "202","210","211","212"]

def replace_str(file_name, stext, rtext):
    with open(file_name,"r+") as file:
        lines = file.readlines()
    with open(file_name,"w") as file1:
        for l in lines:
            file1.write(l.replace(stext,rtext))

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
   replace_str(outfile," ","")
   print("Ok! Done!")
   
def main():
    program_file = sys.argv[1]
    outfile = program_file+".tri"
    assemble(program_file,outfile)


main()
