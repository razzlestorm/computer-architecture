"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.pc = 0
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.fl = 0b00000000 #00000LGE
                

        self.branchtable = {
            0b10100000: self.alu, # ADD
            0b10100001: self.alu, # SUB
            0b10100010: self.alu, # MUL
            0b10100011: self.alu, # DIV
            0b10100100: self.alu, # MOD
            0b10100111: self.alu # CMP
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01010000: self.call,
            0b00010001: self.ret
        }
        

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

    def call(self, address):
        return_address = self.pc + 2
        self.reg[7] -= 1
        SP = self.reg[7]
        self.ram[SP] = return_address
        reg_idx = self.ram[address]
        sub_address = self.reg[reg_idx]
        self.pc = sub_address

    def ret(self):
        SP = self.reg[7]
        return_address = self.ram[SP]
        self.pc = return_address
        self.reg[7] += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == 0b10100000: # ADD
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 0b10100001: # SUB
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 0b10100010: # MUL
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 0b10100011: # DIV
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == 0b10100100: # MOD
            self.reg[reg_a] %= self.reg[reg_b]
        elif op == 0b10100111: # COMPARE
            #FLAG = 00000LGE
            if reg_a == reg_b:
                self.fl = (self.fl >> 5) ^ 0b001
            else:
                self.fl = (self.fl >> 5) ^ 0b100 if reg_a < reg_b else (self.fl >> 5) ^ 0b010
        else:
            raise Exception("Unsupported ALU operation")

    
    def push(self, address):
        self.reg[7] -= 1
        SP = self.reg[7]
        value = self.reg[address]
        self.ram[SP] = value

    def pop(self, address):
        SP = self.reg[7]
        value = self.ram[SP]
        self.reg[address] = value
        self.reg[7] += 1


    def hlt(self):
        self.running = False

    def ldi(self, reg_a, reg_b):
        # seems to be an extra step, could just write to ram here
        self.ram_write(reg_a, reg_b)

    def prn(self, mem_arg):
        print(self.ram_read(mem_arg))

    def jeq(self, reg_a):
        pass

    def jne(self, reg_a):
        pass

    def jmp(self, reg_a):
        pass

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
            IR = self.ram[self.pc]
            num_of_args = IR >> 6
            alu_check = (IR >> 5) & 0b001 
            pc_set_check = (IR >> 4) & 0b0001
            args = []
            if num_of_args > 0:
                ii = 1
                while ii <= num_of_args:
                    args.append(self.ram[self.pc + ii])
                    ii += 1
            
            if alu_check:
                self.branchtable[IR](IR, (*args))
            else:    
                self.branchtable[IR](*args)
                
            if not pc_set_check:
                self.pc += 1 + num_of_args