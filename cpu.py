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

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 25
        self.ram = [0] * 256
        self.reg[7] = 0xF4
        self.pc = 0
        self.active = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, val):
        self.ram[address] = val



    def load(self, filename):
        """Load a program into memory."""
        # fp = FilePointer
        print("loading...")
        address = 0
        with open(filename) as fp:
            print("File Open")
            for line in fp:
                line_split = line.split("#") 
                num = line_split[0].strip()
                if num == '':
                    continue
                val = int(num, 2)
                self.ram_write(val, address)
                address += 1
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
        while  self.active:
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

    
            if instruction == HLT:
                # Halting goes here, Exits Simulator 
                self.active = False
                self.pc += 1
            elif instruction == LDI:
                # LDI sets value of register to an interger 
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif instruction == PRN:
                print(operand_a)
                self.pc += 2 
            elif instruction == MUL:
                register = self.reg[operand_a] + self.reg[operand_b]
                print(register)
