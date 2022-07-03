# dictionaries
instruction = {"add": "10000", "sub": "10001", "movi": "10010", "movr": "10011", "ld": "10100", "st": "10101",
               "mul": "10110", "div": "10111", "rs": "11000", "ls": "11001", "xor": "11010", "or": "11011",
               "and": "11100", "not": "11101", "cmp": "11110", "jmp": "11111", "jlt": "01100", "jgt": "01101",
               "je": "01111", "hlt": "01010", "var": "00000"}
register = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}

flag = "0000000000000000"
dictreg = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0}
ErrorArray=[]
# variables
arr = []
line_counter = 0

label = {}
variables = {}
# reading from file
f = open("Myfile.txt", "w")
# f.write(str(input().split()))
while True:
    try:
        s = input()
        f.write(s+"\n")

    except EOFError:
        break
f.close()
f = open("Myfile.txt", "r")

# extracting individual lines from file
s = f.read().split("\n")
s=s[:len(s)-1]

pcNo = len(s)
x = 0
for i in s:
    k = i.split(" ")
    if k[0] == "var":
        x += 1

pcNo -= x
ErrorFlag = 0
addtoLabel=True

# checking if the immediate value is > 8bit


def function(s):
    global line_counter, ErrorFlag
    for i in s:
        # check for illegal immediate value
        # immediate_check(i.split(" "))
        # will pass only the part of the string after a valid label

        try:
            assert i.split(" ") != ['']
        except AssertionError:
            ErrorArray.append("Error,Blank Line")
            ErrorFlag += 1

        lab_len = check_labels(str(i))
        if lab_len > 0:
            d = []
            line_counter += 1
            d.append(binary(line_counter - x))
            apply(str(i)[lab_len:])
            if addtoLabel:
                d.append(arr[-1])
                label[i[0:lab_len - 2]] = d
        elif lab_len == 0:
            line_counter += 1
            apply(str(i)[lab_len:])

        else:
            # ERROR HANDLING

            return


# saumil make convert to binary (8 bit)   ->>>>>>>>>>>>>>> DONE AUR BATAO
def binary(n):
    s = ''
    b = 0
    while n >= 1:
        s += str(n % 2)
        n = n // 2
    return "0" * (8 - len(s)) + s[::-1]


def xor_or_and(s, a, b):
    if s == "or":
        return a | b
    if s == "xor":
        return a ^ b
    if s == "and":
        return a & b
    return (f)


# function for flag
def flagfunc(a, b, flag):
    if a == b:
        flag[-1] = 1
        return flag
    if (a > b):
        flag[-2] = 1
        return flag
    elif (a < b):
        flag[-3] = 1
        return flag


def add_sub_mul_xor_or_and(s, a, b):
    if s == "mul":
        if a * b < 255:
            return a * b  # check krna hai
        else:
            #ErrorArray.append("Underflow")
            return -1
    if s == "add":
        if a + b < 255:
            return (a + b)
        else:
            #ErrorArray.append("Overflow")
            return -1
    if s == "sub":
        if a - b > 0:
            return (a - b)
        else:
            #ErrorArray.append("Underflow")
            return -1
    if s == ("xor" or "or"):
        return xor_or_and(s, a, b)


# checking for labels if any
count = 0  # change made for resolution of X problem


def check_labels(i):
    global count, ErrorFlag
    k = i.split(" ")

    #multiple spaces
    # while True:
    #     if list(k[0]) == []:
    #         k=k[1:]
    #     else:
    #         break
    if k[0] == "mov" or k[0] == "var":
        return 0
    elif k[0] not in instruction.keys():
        if k[0][-1] == ":":
            if len(k)==1:
                ErrorFlag+=1
                ErrorArray.append("No instruction after label")
                return -1
            label_len = len(k[0])
            if (i[label_len] == " ") and (i[label_len + 1] != " "):
                if k[1] in instruction.keys() or k[1] == "mov":
                    return label_len + 1
                else:
                    ErrorFlag += 1
                    ErrorArray.append(f"ERROR: Invalid label syntax at line {line_counter + 1}")
                    return -1
            else:
                ErrorFlag += 1
                ErrorArray.append(f"ERROR: Invalid label syntax at line {line_counter + 1}")
                return -1
        elif len(k)!=1:
            if k[1] == ":":
                ErrorFlag += 1
                ErrorArray.append(f"ERROR: Invalid label syntax at line {line_counter + 1}")
                return -1
            else:
                return 0

        else:
            ErrorFlag += 1
            ErrorArray.append(f"ERROR: Invalid label syntax at line {line_counter + 1}")
            return -1
    else:
        return 0


def apply(i):
    global pcNo, ErrorFlag, flag,addtoLabel
    k = i.split(" ")
    string = ""
    if list(k[0]) == []:
        k = k[1:]

    if k[0] == "var":
        variables[k[1]] = 0
    # seperate conditions for miv immediate and mov register

    if k[0] == "mov" and k[2] not in register.keys():
        try:
            assert  k[2][0]=="$"
        except AssertionError:
            ErrorArray.append("Error: immediate value has incorrect syntax")
            ErrorFlag+=1
            return
        dictreg[k[1]] = int(k[2][1:])
        try:
            assert int(k[2][1:]) <= 255
            string += instruction["movi"] + register[k[1]] + binary(int(k[2][1:]))
        except AssertionError:
            ErrorArray.append(f"ERROR: Immediate value is greater than 8 Bits at line {line_counter}")
            ErrorFlag += 1
            return

    if k[0] == "mov" and k[2] in register.keys():
        string += instruction["movr"] + "00000" + register[k[1]] + register[k[2]]
        dictreg[k[1]] = dictreg[k[2]]

    if k[0] in ["add", "sub", "mul", "xor", "or", "and"]:
        try:
            assert len(k)==4
            if k[1] not in register.keys() or k[2] not in register.keys() or k[3] not in register.keys():
                ErrorArray.append(f"ERROR: Invalid instruction syntax for {k[0]} at line  {line_counter}")
                addtoLabel=False
                return
            string += instruction[k[0]] + "00" + register[k[1]] + register[k[2]] + register[k[3]]
            dictreg[k[1]] = add_sub_mul_xor_or_and(k[0], dictreg[k[1]], dictreg[k[2]])
            if k[0] in ["add", "sub", "mul"]:
                if k[0] == ("add" or "sub" or "mul") and dictreg[k[1]] == -1:
                    flag[-3] = 1
        except AssertionError:
            ErrorArray.append("Insufficient Registers")
            ErrorFlag+=1
            addtoLabel=False
            return

    if k[0] in ["ls", "rs"]:
        if k[1] not in variables.keys():
            ErrorArray.append(f"ERROR: undefined variable at line {line_counter}")
        try:
            assert int(k[2][1:]) <= 255
            string += instruction[k[0]] + register[k[1]] + binary(int(k[2][1:]))
        except AssertionError:
            ErrorArray.append(f"ERROR: Immediate value is greater than 8 Bits at line {line_counter}")
            ErrorFlag += 1
            return
    if k[0] in ["div", "not", "cmp"]:
        string += instruction[k[0]] + "00000" + register[k[1]] + register[k[2]]
        if k[0] == "div":
            dictreg["R0"] = dictreg[k[1]] // dictreg[k[2]]
            dictreg["R1"] = dictreg[k[1]] % dictreg[k[2]]
        # if k[0]=="not":
        #     #to be done
        #     print("to be done")
        if k[0] == "cmp":
            flag = flagfunc(dictreg[k[1]], dictreg[k[2]], flag)
    if k[0] in ["ld", "st"]:
        # dictreg stuff is left
        string += instruction[k[0]] + register[k[1]] + binary(pcNo)
        pcNo += 1
    if k[0] in ["jmp", "jlt", "jgt", "je"] and k[1] in label.keys():
        string += instruction[k[0]] + "000" + label[k[1]][0]
    if k[0] in ["jmp", "jlt", "jgt", "je"] and k[1] not in label.keys():
        ErrorArray.append(f"ERROR: Invalid memory address at line {line_counter}")
    if k[0] == "hlt":
        string += instruction[k[0]] + "00000000000"
    arr.append(string)


hltFlag = 0
#print(x,len(s),s)
for i in range(x, len(s)):
  #  print(i)
    k = s[i].split(" ")

    if k[0] == "var":
        ErrorFlag += 1
        ErrorArray.append(f"ERROR: Var declared at incorrect position at line {i + 1}")

    if i == len(s) - 1:
        if k[0] != "hlt":
            hltFlag += 1
    if i < len(s) - 1:
        if k[0] == "hlt":
            ErrorFlag += 1
            ErrorArray.append(f"ERROR: hlt used before last instruction at line {i + 1}")

if hltFlag == 1:
    ErrorFlag += 1
    ErrorArray.append("ERROR: hlt not in given file")

function(s)
if ErrorFlag == 0:
    for i in range(x, len(arr)):
        print(arr[i])
for i in ErrorArray:
    print(i)
f.close()
f = open('Myfile.txt', 'w')
f.write("")
f.close()
