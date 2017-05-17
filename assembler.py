#Opcodes
OpCodes = {
    # Zero operand instructions
    "nop": "1000000000010011",
    "clrc": "1000000000011100",
    "setc": "1000000000011101",
    "add": "00000",
    "sub": "00001",
    "and": "00010",
    "or":  "00011",
    "call": "00100",
    "mov": "00001111",
    "not": "00001000",
    "neg": "00001001",
    "inc": "00001010",
    "dec": "00001011",
    "rlc": "00001100",
    "rrc": "00001101",
    "jmp": "00000011000",
    "jc": "00000011001",
    "jz": "00000011010",
    "jn": "00000011011",
    "in": "00011110",
    "out": "00011111",
    "push": "11010110",
    "pop": "11010111",
    "ret": "11010100",
    "rti": "11010101"
}

#Errors
Errors = {
    -1: "Immediate value out of range",
    -2: "Register value out of range",
}

#Binary Conversion function
def BinaryEquiv(number,numberofbits):
    Three_bits = {
        0: "000",
        1: "001",
        2: "010",
        3: "011",
        4: "100",
        5: "101",
        6: "110",
        7: "111",
    }

    Four_bits = {
        0: "0000",
        1: "0001",
        2: "0010",
        3: "0011",
        4: "0100",
        5: "0101",
        6: "0110",
        7: "0111",
    }
    if numberofbits  == 3:
        return Three_bits[number]
    elif numberofbits == 4:
        return Four_bits[number]


#Convert negative number to binary
def bindigits(n, bits):
    s = bin(n & int("1"*bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)

#Check Register number in range
def CheckRegister(R):
    if int(R) >7:
        return False
    else:
        return True

#Split instruction
def  SplitInstruction(instruction,NumberOfOperands):
    arguments = []
    i = instruction.split()
    arguments.append(i[0])
    i1 = i[1].split(",")
    arguments.append(i1[0])
    arguments.append(i1[1])
    if NumberOfOperands == 3:
        arguments.append(i1[2])

    return arguments
############################## Read File ##############################################
def ReadFile(FilePath):
    #A function that reads file and return list of instructions
    with open(FilePath) as f:
        instructions = f.readlines()
        instructions = [x.strip().lower() for x in instructions]
    i = 0
    first_space = False
    while i<len(instructions):
        #Remove all spaces leave first one
        if " " in instructions[i]:
            s_index = instructions[i].index(' ')
            instructions[i] = instructions[i][0:s_index + 1] + instructions[i][s_index + 1:].replace(" ", "")
        if "#" in instructions[i]:
            index = instructions[i].index("#")
            instructions[i] = instructions[i][0:index-1]
        i += 1
    return instructions

############################ Write to file #####################################################3

def WriteToFile(Filepath,Instructions): ###A function that takes a file path and list of instructions(0's and 1's) and write to file
    o = open(Filepath, 'w')
    for item in Instructions:
        print>> o, item

############################### Build list that will be written to file use the help of other functions ###

def BuildConvertedList(Instructions):
    Final_list  = ["0100000000000000","0100100000000000"]
    NoOperandInstructions = ['nop','clrc','setc']
    MemoryInstructions = ['ldd','std']
    ThreeOperandInstructions = ['add','sub','and','or','call']
    Mov_OneOperand = ['mov','not','neg','inc','dec','rlc','rrc']
    ImmeidateValueInstructions = ['ldm','shl','shr']
    jmp = ['jmp','jc','jz','jn']
    IN_OUT_inst = ['in','out','push','pop']
    ret = ['ret','rti']

    for i in Instructions:
        operation = i.split()[0]
        #Memory instruction case
        if operation in MemoryInstructions:
            Final_list.append(Memory(i,MemoryInstructions.index(operation)))

        #Number that follow instruction
        elif i.isdigit():
            #Error handling
            if len(bin(int(i))) > 16:
                return -1 #Value out of range
            elif int(i) < 0:
                x = bindigits(int(i), 16)
                y = bin(int(x, 2) + 1)
                Final_list.append(y)
            #convert to binary and add
            else:
                Final_list.append(bin(i).zfill(16))

        #No operand instruction case
        elif operation in NoOperandInstructions:
            Final_list.append(OpCodes[operation])

        #Immediate value instruction case
        elif operation in ImmeidateValueInstructions:
            F = ImmediateValue(i,ImmeidateValueInstructions.index(operation))
            for element in F:
                Final_list.append(element)

        #Three operand instruction case
        elif operation in ThreeOperandInstructions:
            Final_list.append(ThreeOperand(i,ThreeOperandInstructions.index(operation),OpCodes[operation]))

        #Move and one operand case
        elif operation in Mov_OneOperand:
            Final_list.append(MovAndOneOperand(i,Mov_OneOperand.index(operation),OpCodes[operation]))

        #Jump instruction case
        elif operation in jmp:
            Final_list.append(Jump(i,jmp.index(operation),OpCodes[operation]))

        # IN ,OUT,PUSH, POP instructions
        elif operation in IN_OUT_inst:
            Final_list.append(IN_OUT_PUSH_POP(i,IN_OUT_inst.index(operation),OpCodes[operation]))

        elif operation in ret:
            inst = "10000000" + OpCodes[operation]
            Final_list.append(inst)

    return Final_list

########################## Memory instructions ###########################################
def Memory(instruction,type):
    RegisterNumber = ""
    operands = SplitInstruction(instruction,2) #Operands = [operation, register number, EA]
    # Check that register number is in range
    if not CheckRegister(operands[1][1:]):
        return -2 #Register value out of range
    else:
        RegisterNumber = BinaryEquiv(int(operands[1][1:]),3)

        ### Handle EA according to range
        EA = ""
        if len(bin(int(operands[2])).zfill(10)) == 11:
            EA = bin(int(operands[2])).zfill(10).replace('b', '')
        elif len(bin(int(operands[2])).zfill(10)) == 12:
            EA = bin(int(operands[2])).zfill(10)[2:]
        else:
            EA = bin(int(operands[2])).zfill(10).replace('b', '0')

        Rdst = BinaryEquiv(int(operands[1][1:]),4)
    if type == 0: #LDD r0 , 3
        return "0"+Rdst+EA+"0"
    elif type == 1:#STD R2, 3
        return "00"+EA[0:3]+RegisterNumber+EA[3:]+"1"

########################## Immediate value instructions ############################################
# LDM  --> type = 0
# SHL  --> type = 1
# SHR  --> type = 2
# Inst Reg, Imm
def ImmediateValue(instruction,type):
    operands = SplitInstruction(instruction,2) #operands = [operation, reg number, imm]
    RegisterNumber = ""
    Imm = ""
    # Check that register number is in range
    if not CheckRegister(operands[1][1:]):
        return -2 #Register value out of range
    else:
        RegisterNumber = bin(int(operands[1][1:])).zfill(4).replace('b', '')
        if len(bin(int(operands[2]))) > 16:
            return -1  # Value out of range
        else:
            Imm = bin(int(operands[2])).zfill(16).replace('b', '0')


    Rdst = BinaryEquiv(int(operands[1][1:]),4)
    returned = "1" + Rdst + "000000100"
    if type == 0:
        return [returned+"00",Imm]
    elif type == 1:
        return [returned+"01",Imm]
    elif type == 2:
        return returned+"10",[Imm]

#################### Three Operand Instruction ################################################
# Add -> type: 0 --- "1" + '"00 000"
# sub -> type: 1 --- "1" + "00 001"
# and -> type: 2 --- "1" + "00 010"
# or -> type: 3 --- "1" + "00 011"
# call -> type: 4 --- "1" + "00 100"
def ThreeOperand(instruction,type,opcode):
    operands = []
    Rdst = ""
    Rsrc1 = ""
    Rsrc2=""

    if type !=4:
        operands = SplitInstruction(instruction, 3)  # operands = [operation,3:rsrc1,3:rsrc2,4:rdst1]
        Rdst = operands[3][1:]
        Rsrc1 = operands[1][1:]
        Rsrc2 = operands[2][1:]
        if not CheckRegister(operands[1][1:]) and CheckRegister(operands[2][1:]) and CheckRegister(operands[3][1:]):
            return -2
        else:
            Rsrc1 = BinaryEquiv(int(Rsrc1),3)
            Rsrc2 = BinaryEquiv(int(Rsrc2),3)
            Rdst = BinaryEquiv(int(Rdst),4)

    elif type ==4:
        operands = instruction.split()  # operands = [operation , rdst]
        if not CheckRegister(operands[1][1:]):
            return -2
        else:
            Rsrc1 = "111"
            Rsrc2 = "110"
            Rdst = BinaryEquiv(int(operands[1][1:]),4)

    return "1"+Rdst+Rsrc1+Rsrc2+opcode

#################################### Move and Normal one operand ####################################################
def MovAndOneOperand (instruction,type,opcode): #Mov Rsrc1, Rdst ; #Not Rdst; dst(4), src(3)
    operands = []
    Rdst = ""
    Rsrc1 = ""

    if type == 0:
        operands = SplitInstruction(instruction, 2)  # operands = [operation,rsrc1,rdst]
        Rdst = operands[2][1:]
        Rsrc1 = operands[1][1:]
        if not CheckRegister(Rdst) and CheckRegister(operands[2][1:]):
            return -2
        else:
            Rsrc1 = BinaryEquiv(int(Rsrc1),3)
            Rdst = BinaryEquiv(int(Rdst),4)

        return "1" + Rdst + Rsrc1 + opcode

    else:
        operands = instruction.split()  # operands = [operation ,rdst]

        Rdst = operands[1][1:]
        if not CheckRegister(Rdst):
            return -2
        else:
            Rdst2 = BinaryEquiv(int(Rdst),3)
            Rdst1 = BinaryEquiv(int(Rdst),4)

        return "1" + Rdst1 + Rdst2 + opcode

##################################### Jumps ###############################################################
# type:0 --> JMP
# type:1 --> JC
# type:2 --> JZ
# type:3 --> JN
def Jump(instruction,type,opcode):
    operands = instruction.split() # operands = [ operation, Rdst ]

    Rdst = operands[1][1:]
    if not CheckRegister(Rdst):
        return -2
    else:
        Rdst = BinaryEquiv(int(Rdst),4)

    return "1" + Rdst + opcode

##############################################################################################################
# IN	"1" + "11 1 1 0"
# OUT	"1" + "11 1 1 1"
def IN_OUT_PUSH_POP(instruction,type,opcode):
    operands = instruction.split() #IN/OUT Rdst
    Rdst = operands[1][1:]

    if type == 0 or type ==3: #IN = 0 , #POP = 3
        if not CheckRegister(Rdst):
            return -2
        else:
            Rdst = BinaryEquiv(int(Rdst),4)
        return "1" + Rdst + "000" +opcode

    elif type == 1 or type == 2: #OUT=1, #PUSH=2
        if not CheckRegister(Rdst):
            return -2
        else:
            Rdst = BinaryEquiv(int(Rdst), 3)
        return "10000"+Rdst+opcode

############################################# ###############################################
##################### Test code ####################################
i = ReadFile('T.txt')
converted = BuildConvertedList(i)
compare = ['1000000000010000','0000000000000000','1000100000010000','0000000000010101','1001000000010000','0000000000011001',
           '1010000000010000','0000000000001100','1010100000010000','0000000000001111','0000000000000111','1001100000011110',
           '1001101101100010','1000100000011011','0000000000000110','1001100000000000','0000000000000111','1010000000011000',
           '1001011111000100','1010100000011000','0000010000000111','1001101100001001','1000000011010100','0000001000000111']
WriteToFile("output.txt",converted)

if len(compare) == len([i for i, j in zip(converted[2:], compare) if i == j]):
    print True






