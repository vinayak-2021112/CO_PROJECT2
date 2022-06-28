#dictionaries
instruction = {"add":"10000","sub":"10001","movi":"10010","movr":"10011","ld":"10100","st":"10101","mul":"10110","div":"10111","rs":"11000","ls":"11001","xor":"11010","or":"11011","and":"11100","not":"11101","cmp":"11110","jmp":"11111","jlt":"01100","jgt":"01101","je":"01111","hlt":"01010"}
register = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"};


#variables
arr=[]
line_counter = 0
#reading from file
f=open("Myfile.txt","r")

#extracting individual lines from file
s=f.read().split("\n")
def function(s):
    for i in s:
        # will pass only the part of the string after a valid label
        lab_len = check_labels(str(i))
        if(lab_len>=0):
            apply(str(i)[lab_len::])
        else:
            # ERROR HANDLING
            print("error")
# saumil make convert to binary (8 bit)
def makehere(y):
    return "X"

# checking for labels if any
def check_labels(i):
    k = i.split(" ")
    if(k[0] not in instruction.keys()):
        # format for a label should be label: instruction.
        if(k[0][-1]==":"):
            label_len = len(k[0])
            if(i[label_len]==" "):
                return label_len+1
            # if the syntax is not in in instruction and is not a label returning -1
            else:
                return -1
        else:
            return -1
    else:
        # returning 0 if there is no label
        return 0

def apply(i):
    k=i.split(" ")
    string=""
    #seperate conditions for miv immediate and mov register
    if k[0] == "mov" and k[2] not in register.keys():
        string+=instruction["movi"]+register[k[1]]+makehere(int(k[2]))
    if k[0] == "mov" and k[2] in register.keys():
        string+=instruction[k[0]]+"00000"+register[k[1]]+register[k[2]]
    if k[0] in ["add","sub","mul","xor","or","and"]:
        string+=instruction[k[0]]+"00"+register[k[1]]+register[k[2]]+register[k[3]]
    if k[0] in ["mov","ls","rs"] and k[2] not in register.keys():
        string+=instruction[k[0]]+register[k[1]]+makehere(int(k[2]))
    if k[0] in ["mov","div","not","cmp"]:
        string+=instruction[k[0]]+"00000"+register[k[1]]+register[k[2]]
    if k[0] in ["ld","st"]:
        string+=instruction[k[0]]+register[k[1]]+k[2]
    if k[0] in ["jmp","jlt","jgt","je"]:
        string+=instruction[k[0]]+"000"+k[2]
    if k[0]=="hlt":
        string+=instruction[k[0]]+"00000000000"
    arr.append(string)

function(s)
