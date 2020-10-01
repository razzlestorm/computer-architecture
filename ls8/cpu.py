"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.pc = 0
        self.ram = [None] * 255
        self.reg = [None] * 8
        '''        
        self.branchtable = {
            0b10100000: self.alu("ADD", self.pc+1, self.pc+2),
            0b10100001: self.alu("SUB", self.pc+1, self.pc+2),
            0b10100010: self.alu("MUL", self.pc+1, self.pc+2),
            0b10100011: self.alu("DIV", self.pc+1, self.pc+2),
            0b10100100: self.alu("MOD", self.pc+1, self.pc+2),
            0b00000001: self.hlt(),
            0b10000010: self.ldi(self.pc+1, self.pc+2),
            0b01000111: self.prn(self.pc+1),
        }
        '''

    def ram_read(self, MAR):
        # Accept Mem Address to read and return stored value
        return self.reg[MAR] or 'Nothing there'
    
    def ram_write(self, MDR, val):
        # take value to write and write it to the ram[memory data register]
        self.reg[MDR] = val

    def load(self, file):
        """Load a program into memory."""

        address = 0

        program = []
        with open(file, 'r') as f:
            for line in f:
                # slice the line up until the point of the comment, if any are found
                line = line[:line.find('#')].strip()
                if line not in ('', '\n', '\r\n'):
                    # convert to int then back to binary for ls8 to read
                    program.append(format(int(line, 2), '#010b'))

        for instruction in program:
            self.ram[address] = int(instruction, 2)
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL" or op == 0b10100010:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

        # self.pc += 3

    def hlt(self):
        self.running = False

    def ldi(self, reg_a, reg_b):
        # seems to be an extra step, could just write to ram here
        self.ram_write(self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def prn(self):
        print(self.ram_read(self.ram[self.pc + 1]))
        self.pc += 2

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

    def run(self):
        """Run the CPU."""
        # TODO: Add garbage handling
    
        while self.running:
            # breakpoint()
            IR = self.ram[self.pc]
            # MUL
            if IR == 0b10100010:
                self.alu(IR, self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 2
            # LDI
            elif IR == 0b10000010:
                self.ram_write(self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 2
            # PRN
            elif IR == 0b01000111:
                print(self.ram_read(self.ram[self.pc + 1]))
                self.pc += 1
            # HLT
            elif IR == 0b00000001:
                self.running = False

            # increment self.pc after running each command
            self.pc += 1




