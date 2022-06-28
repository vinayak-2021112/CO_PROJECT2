#dictionaries
instruction = {"add":"10000","sub":"10001","movi":"10010","movr":"10011","ld":"10100","st":"10101","mul":"10110","div":"10111","rs":"11000","ls":"11001","xor":"11010","or":"11011","and":"11100","not":"11101","cmp":"11110","jmp":"11111","jlt":"01100","jgt":"01101","je":"01111","hlt":"01010"}
register = {"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"};


#variables
arr=[]
#reading from file
f=open("Myfile.txt","r")

#extracting individual lines from file
s=f.read().split("\n")
def function(s):
    for i in s:
        apply(str(i))
# saumil make convert to binary (8 bit)
def makehere(y):
    return "X"

def apply(i):
    k=i.split(" ")
    string=""
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
