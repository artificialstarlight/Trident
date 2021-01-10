#import module for easier base conversion
from baseconvert import *

#function to convert bases using BaseConvert module
def convert(num,x,y):
    b = BaseConverter(input_base=x, output_base=y)
    return b(num)


def simple_logic(Type,t1,t2):
    if Type.upper == "AND":
        if t1 <= t2:
            out = t1
        else:
            out = t2
        return out

    if Type.upper == "OR":
        if t1 >= t2:
            out = t1
        else:
            out = t2
        return out

def simple_unary(Type,t1):
    if Type.upper == "NOT":
        if t1 == 0:
            out = 2
        elif t1 == 2:
            out = 0
        else:
            out = 1
        return out

"""
Ternary AND/OR. Works on multiple-trit numbers, as well as numbers in
decimal or base 27. Parameters are named as such because param 1 will
usually be an opcode, and param 2 will usually be some other value.
Parameters should be strings.
"""
def logic(Type,op,num2):
    op = str(op)
    num2 = str(num2)
    #Convert param 2 from DEC to TERNARY. Param 2 should always be base 10
    s2 = convert(int(num2),10,3)
    #Check to see what base param 1 is in.
    if op[0] == "D":
        #Slice off the letters of th string which specify the base
        op = op[2:]
        s1 = convert(int(op),10,3)
    if op[0] == "S":
        op = op[2:]
        s1 = convert(int(op),27,3)
    if op[0] == "T":
        s1 = op[2:]
        #Fill with leading zeroes when needed
    else:
        s1 = op
    """while len(s1) < 9:
        s1 = ''.join(('0',s1))"""
    """#slice off the "instruction" tribble and leave the tryte result
    s1 = s1[3:]"""
    #temporary list
    out = []
    #does the AND comparison
    if Type.upper() == "AND":
        for i,j in zip(s1,s2):
            if int(s1[int(i)]) <= int(s2[int(j)]):
                out.append(i)
            else:
                out.append(j)
    #OR comparison
    elif Type.upper() == "OR":
        for i,j in zip(s1,s2):
            if int(s1[int(i)]) >= int(s2[int(j)]):
                out.append(i)
            else:
                out.append(j)
    #XOR
    elif Type.upper() == "XOR":
        for i,j in zip(s1,s2):
            u1 = simple_logic("AND",i,j)
            u2 = simple_unary("NOT",u1)
            u3 = simple_logic("OR",j,i)
            out.append(simple_logic("AND",u2,u3))
    elif Type.upper() == "SUM":
        for i,j in zip(s1,s2):
            out.append((i+j)%3)
    #converts the temp list to string for returning
    out_str = ''.join([str(elem) for elem in out])
    return out_str

#Logic with unary operators such as inversion
def unary_op(Type,num):
    #Fill with leading zeroes when needed
    while len(s1) < 9:
        s1 = ''.join(('0',s1))
    #temporary list
    out = []
    #does NOT operation
    if Type.upper() == "NOT":
        for i in s1:
            if int(i) == 0:
                out.append("2")
            elif int(i) == 2:
                out.append("0")
            else:
                out.append("1")
    elif Type.upper() == "PTI":
        for i in s1:
            if int(i) == 2:
                out.append("0")
            else:
                out.append("2")
    elif Type.upper() == "NTI":
        for i in s1:
            if int(i) == 0:
                out.append("2")
            else:
                out.append("0")
    out_str = ''.join([str(elem) for elem in out])
    return out_str 
