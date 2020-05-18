"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.running = True
        self.ops = {
            'ADD': '10100000 00000aaa 00000bbb',
            'SUB': '10100001 00000aaa 00000bbb',
            'MUL': '10100010 00000aaa 00000bbb',
            'DIV': '10100011 00000aaa 00000bbb',
            'MOD': '10100100 00000aaa 00000bbb',
            'INC': '01100101 00000rrr',
            'DEC': ' 01100110 00000rrr',
            'CMP': '10100111 00000aaa 00000bbb',
            'AND': '10101000 00000aaa 00000bbb',
            'NOT': '01101001 00000rrr',
            'OR': '10101010 00000aaa 00000bbb',
            'XOR': '10101011 00000aaa 00000bbb',
            'SHL': '10101100 00000aaa 00000bbb',
            'SHR': '10101101 00000aaa 00000bbb'
        }

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations. operators and add cheatsheet. whatever we may need we might have to add"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
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
        while self.running == True:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == HLT:
                self.running = False
                sys.exit(1)

            # if IR in self.ops:  # Instruction set
            #     self.alu(self.ops[IR], operand_a, operand_b)

        # depending on the value perfrom an instruction set
        # PC needs to be updated to point to the next instruction for the next iteration of the loop in run()
