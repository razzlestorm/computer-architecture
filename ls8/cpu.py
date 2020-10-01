"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 255
        self.reg = [None] * 8
        self.pc = 0

    def ram_read(self, MAR):
        # Accept Mem Address to read and return stored value
        return self.ram[MAR] or 'Nothing there'
    
    def ram_write(self, MDR, val):
        # take value to write and write it to the ram[memory data register]
        self.ram[MDR] = val

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

    def run(self):
        """Run the CPU."""
        # TODO: Add garbage handling
        running = True
    
        while running:
            IR = self.ram[self.pc]

            # LDI
            if IR == 0b10000010:
                self.ram_write(self.ram[self.pc + 1], self.ram[self.pc + 2])

            # PRN
            elif IR == 0b01000111:
                print(self.ram_read(self.ram[self.pc + 1]))

            # HLT
            elif IR == 0b00000001:
                break

            # increment self.pc after running each command
            self.pc += 1




