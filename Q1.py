# dictionaries
instruction = {"add": "10000", "sub": "10001", "movi": "10010", "movr": "10011", "ld": "10100", "st": "10101",
               "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011",
               "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101",
               "je": "01111", "hlt": "01010"}
register = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"};

# variables
arr = []
line_counter = 0
# reading from file
f = open("Myfile.txt", "r")

# extracting individual lines from file
s = f.read().split("\n")
pcNo=len(s)
x=0
for i in s:
    k=i.split(" ")
    if k[0]=="var":
        x+=1
pcNo-=x
def function(s):
    for i in s:
        # will pass only the part of the string after a valid label
        lab_len = check_labels(str(i))
        if lab_len >= 0:
            apply(str(i)[lab_len:])
        else:
            # ERROR HANDLING
            print("error",i)



# saumil make convert to binary (8 bit)   ->>>>>>>>>>>>>>> DONE AUR BATAO
def binary(n):
    s = ''
    b = 0
    while n >= 1:
        s += str(n % 2)
        n = n // 2
    return "0" * (8 - len(s)) + s[::-1]


# checking for labels if any
count=0 #change made for resolution of X problem
def check_labels(i):
    global count
    k = i.split(" ")
    if k[0] =="mov" or k[0]=="var":
        return 0
    elif k[0] not in instruction.keys():
        # format for a label should be label: instruction.
        if k[0][-1] == ":":
            label_len = len(k[0])
            if i[label_len] == " ":
                count=count+1  # for X
                return label_len + 1
            # if the syntax is not in in instruction and is not a label returning -1
            else:
                count=count+1   #for X
                return -1
        else:
            count=count+1    #for X
            return -1
    else:
        # returning 0 if there is no label
        count=count+1       #for X
        return 0


def apply(i):
    global pcNo
    k = i.split(" ")
    string = ""
    # seperate conditions for miv immediate and mov register
    if k[0] == "mov" and k[2] not in register.keys():
        string += instruction["movi"] + register[k[1]] + binary(int(k[2][1:]))
    if k[0] == "mov" and k[2] in register.keys():
        string += instruction["movr"] + "00000" + register[k[1]] + register[k[2]]
    if k[0] in ["add", "sub", "mul", "xor", "or", "and"]:
        string += instruction[k[0]] + "00" + register[k[1]] + register[k[2]] + register[k[3]]
    if k[0] in ["ls", "rs"]:
        string += instruction[k[0]] + register[k[1]] + binary(int(k[2][1:]))
    if k[0] in ["div", "not", "cmp"]:
        string += instruction[k[0]] + "00000" + register[k[1]] + register[k[2]]
    if k[0] in ["ld", "st"]:
        string += instruction[k[0]] + register[k[1]] + binary(pcNo)
        pcNo+=1
    if k[0] in ["jmp", "jlt", "jgt", "je"]:
        string += instruction[k[0]] + "000" + k[2]
    if k[0] == "hlt":
        string += instruction[k[0]] + "00000000000"
    arr.append(string)


function(s)
if(x>0):
    print(arr[x:])
else:
    print(arr)
"""
1001000100001010
1001001001100100
1011000011001010
1010101100000101
0101000000000000"""
