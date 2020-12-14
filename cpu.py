"""CPU functionality."""


# Notes:

# The Following 2 Examples are for what python uses to read Hexadecimal
# and binary numbers:

# 0b: Reads following numbers in Binary
# 0x: Reads following numbers in Hexadecimal

import sys

# Push
PUSH = 0b01000101

# Pop
POP = 0b01000110

# Halt
HLT = 0b00000001

# Register Immediate
LDI = 0b10000010

# Print Register
PRN = 0b01000111

# Multiply 
MUL = 0b10100010

# 
CMP = 0b10100111

# 
JMP = 0b01010100

# 
JEQ = 0b01010101

# 
JNE = 0b01010110

# mar = Memory Address Register

# mdr = Memory Data Register

# ir = instruction register

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[7] = 0xF4
        self.pc = 0
        self.mar = 0
        self.mdr = 0
        self.terminate = 0
        self.halted = False
        self.ir = 0

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr



    def load(self, filename):
        """Load a program into memory."""
        # fp = FilePointer
        print("loading...")
        address = 0
        with open(filename) as fp:
            print("File Open")
            for line in fp:
                line_split = line.split("#") 
                num = line_split[0]

                try:
                    val = int(num, 2)
                    self.ram_write(val, address)
                    address += 1
                except:
                    continue
        self.terminate = address
        print("end of load")
            



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


        # For future reference:
        # Operand = Quantity. In the case of the example below is how much ram.

    def run(self):
        """Run the CPU."""
        # The default state is on (active)
        while not self.halted:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instruction(ir, operand_a, operand_b)


    def execute_instruction(self, instruction, operand_a, operand_b):

        is_alu = instruction >> 5 & 0b1
        sets_pc = instruction >> 4 & 0b1
        num_operands = (instruction >> 6 & 0b11) + 1

        if not sets_pc:
            if instruction == HLT:
                # Halting goes here, Exits Simulator 
                self.halted = True
            elif instruction == PRN:
                print(self.reg[operand_a])
            elif instruction == LDI:
                # LDI sets value of register to an interger 
                self.reg[operand_a] = operand_b
            elif instruction == PUSH:
                if self.reg[7] > self.terminate + 1: 
                    self.reg[7] -= 1
                else:
                    sys.exit(1)
                register_address = self.ram[self.pc + 1]
                value = self.reg[register_address]
                self.ram[self.reg[7]] = value
            elif instruction == POP:
                register_address = self.ram[self.pc + 1]
                self.reg[register_address] = self.ram[self.reg[7]]
                if self.reg[7] < 0xF4: 
                    self.reg[7] += 1
                else:
                    sys.exit(1)
            elif is_alu:
                self.alu(instruction, operand_a, operand_b)
            else:
                print("Bad Instruction")
            self.pc += num_operands
