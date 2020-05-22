"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.running = True
        self.sp = self.reg[7]
        self.flag = 0b00000000

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0
        with open(sys.argv[1]) as file_:
            for line in file_:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                # print(v)
                self.ram[address] = v
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations. operators and add cheatsheet. whatever we may need we might have to add"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b00000010
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = 0b00000100

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # local variable
        # self.trace()
        while self.running == True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                self.LDI(operand_a, operand_b)
            elif IR == PRN:
                self.PRN(operand_a)
            elif IR == MUL:
                self.MUL(operand_a, operand_b)
            elif IR == PUSH:
                self.PUSH(operand_a)
            elif IR == POP:
                self.POP(operand_a)
            elif IR == CALL:
                self.CALL(operand_a)
            elif IR == RET:
                self.RET(operand_a)
            elif IR == ADD:
                self.ADD(operand_a, operand_b)
            elif IR == CMP:
                self.CMP(operand_a, operand_b)
            elif IR == JMP:
                self.JMP(operand_a)
            elif IR == JEQ:
                self.JEQ(operand_a)
            elif IR == JNE:
                self.JNE(operand_a)
            elif IR == HLT:
                self.HLT()
            else:
                print(
                    f'unknown instruction {IR} at address {self.pc}')
                exit(1)
        # if IR in self.ops:  # Instruction set
        #     self.alu(self.ops[IR], operand_a, operand_b)

        # depending on the value perfrom an instruction set
        # PC needs to be updated to point to the next instruction for the next iteration of the loop in run()

    def MUL(self, oper_a, oper_b):
        self.alu('MUL', oper_a, oper_b)
        self.pc += 3

    def PRN(self, oper_a):
        print(self.reg[oper_a])
        self.pc += 2

    def LDI(self, oper_a, oper_b):
        self.reg[oper_a] = oper_b
        self.pc += 3

    def PUSH(self, oper_a):
        self.sp -= 1
        val = self.reg[oper_a]
        self.ram_write(self.sp, val)
        self.pc += 2

    def POP(self, oper_a):
        self.reg[oper_a] = self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2

    def HLT(self):
        self.running = False
        sys.exit(1)

    def CALL(self, oper_a):
        return_address = self.pc + 2
        self.sp -= 1
        self.ram[self.sp] = return_address
        subroutine_address = self.reg[oper_a]
        self.pc = subroutine_address

    def RET(self, oper_a):
        return_address = self.ram[self.sp]
        self.sp += 1
        self.pc = return_address

    def ADD(self, oper_a, oper_b):
        self.alu('ADD', oper_a, oper_b)
        self.pc += 3

    def CMP(self, oper_a, oper_b):
        self.alu('CMP', oper_a, oper_b)
        self.pc += 3

    def JMP(self, oper_a):
        self.pc = self.reg[oper_a]

    def JEQ(self, oper_a):
        if self.flag == 0b00000001:
            self.JMP(oper_a)
        else:
            self.pc += 2

    def JNE(self, oper_a):
        if self.flag != 0b00000001:
            self.JMP(oper_a)
        else:
            self.pc += 2
