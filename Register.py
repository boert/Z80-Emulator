##############################
# helper functions

def bit_is_set( byte, bitpos):
    if byte & ( 1 << bitpos):
        return True
    return False

def bit_is_clear( byte, bitpos):
    if byte & ( 1 << bitpos):
        return False
    return True


def set_bit( byte, bit):
    result = byte | (1 << bit)
    return result

def clr_bit( byte, bit):
    result = byte & ~(1 << bit)
    return result

def lo( word):
    return word & 0xff

def hi( word):
    return word >> 8



##############################
# main class
class Register:

    # bit numbers of flags
    flag_carry = 0
    flag_sub = 1
    flag_par = 2
    flag_tree = 3
    flag_half = 4
    flag_five = 5
    flag_zero = 6
    flag_sign = 7


    def __init__( self):
        self.pc  = 0
        self.sp  = 0xfffe
        self.i   = 0
        self.r   = 0
                 
        self.a   = 0
        self.a_  = 0xff
        self.f   = 0
        self.f_  = 0xff
        
        self.bc  = 0
        self.bc_ = 0xffff
        self.de  = 0
        self.de_ = 0xffff
        self.hl  = 0
        self.hl_ = 0xffff
        self.ix  = 0
        self.iy  = 0


    def print( self):
        print("A  -Flags-- B C  D E  H L  M  IX   IY   I") 
        print("%02X %s %04X %04X %04X .. %04X %04X %02X" % ( self.a, self.flags_to_str( self.f), self.bc, self.de, self.hl,  self.ix, self.iy, self.i))
        print("A' -Flags'- B'C' D'E' H'L' M' SP   PC   R") 
        print("%02X %s %04X %04X %04X .. %04X %04X %02X" % ( self.a_, self.flags_to_str( self.f_), self.bc_, self.de_, self.hl_,  self.sp, self.pc, self.r))


    def print_one( self):
        print("A=%02X F=%s BC=%04X DE=%04X HL=%04X  IX=%04X IY=%04X  I=%02X A'=%02X F'=%s BC'=%04X DE'=%04X HL'=%04X  SP=%04X PC=%04X  R=%02X" % ( self.a, self.flags_to_str( self.f), self.bc, self.de, self.hl,self.ix, self.iy, self.i, self.a_, self.flags_to_str( self.f_), self.bc_, self.de_, self.hl_,  self.sp, self.pc, self.r))

    # convert flag register to printable string
    def flags_to_str( self, flag_reg):

        flag_str = ""

        if bit_is_set( flag_reg, self.flag_sign):
            flag_str += "S"
        else:
            flag_str += "."

        if bit_is_set( flag_reg, self.flag_zero):
            flag_str += "Z"
        else:
            flag_str += "."

        if bit_is_set( flag_reg, self.flag_five):
            flag_str += "5"
        else:
            flag_str += "."

        if bit_is_set( flag_reg, self.flag_half):
            flag_str += "H"
        else:
            flag_str += "."

        if bit_is_set( flag_reg, self.flag_tree):
            flag_str += "3"
        else:
            flag_str += "."

        if bit_is_set( flag_reg, self.flag_par):
            flag_str += "P"
        else:
            flag_str += "v"

        if bit_is_set( flag_reg, self.flag_sub):
            flag_str += "N"
        else:
            flag_str += "."

        if bit_is_set( flag_reg, self.flag_carry):
            flag_str += "C"
        else:
            flag_str += "."

        return flag_str



    def set_pc( self, pc):
        pc &= 0xffff
        self.pc = pc

    def set_sp( self, sp):
        sp &= 0xffff
        self.sp = sp

    def set_b( self, value):
        if value < 0 or value > 255:
            raise RangeError
        self.bc = ( value << 8) + ( self.bc & 0x00ff)

    def set_c( self, value):
        if value < 0 or value > 255:
            raise RangeError
        self.bc = ( self.bc & 0xff00) + value 

    def set_d( self, value):
        if value < 0 or value > 255:
            raise RangeError
        self.de = ( value << 8) + ( self.de & 0x00ff)

    def set_e( self, value):
        if value < 0 or value > 255:
            raise RangeError
        self.de = ( self.de & 0xff00) + value 

    def set_h( self, value):
        if value < 0 or value > 255:
            raise RangeError
        self.hl = ( value << 8) + ( self.hl & 0x00ff)

    def set_l( self, value):
        if value < 0 or value > 255:
            raise RangeError
        self.hl = ( self.hl & 0xff00) + value 

    def set_hl( self, hl):
        self.hl = hl


    def compare( self, value):
        self.f = set_bit( self.f, self.flag_sub)
        self.f = clr_bit( self.f, self.flag_par)

        diff = self.a - value
        diff &= 0xff
        
        if diff > 127:
            self.f = set_bit( self.f, self.flag_sign)
        else:
            self.f = clr_bit( self.f, self.flag_sign)
        
        if diff == 0:
            self.f = set_bit( self.f, self.flag_zero)
        else:
            self.f = clr_bit( self.f, self.flag_zero)
        
        if value > self.a:
            self.f = set_bit( self.f, self.flag_carry)
        else:
            self.f = clr_bit( self.f, self.flag_carry)

        # TODO: half carry


    def add_( self, value):
        self.f = clr_bit( self.f, self.flag_sub)
        self.f = clr_bit( self.f, self.flag_par)

        self.a = self.a + value

        if self.a > 256:
            self.f = set_bit( self.f, self.flag_carry)
            self.a = self.a & 0xff
        else:
            self.f = clr_bit( self.f, self.flag_carry)
        
        if self.a > 127:
            self.f = set_bit( self.f, self.flag_sign)
        else:
            self.f = clr_bit( self.f, self.flag_sign)
        
        if self.a == 0:
            self.f = set_bit( self.f, self.flag_zero)
        else:
            self.f = clr_bit( self.f, self.flag_zero)

        #TODO: flag_half


    def and_( self, value):
        self.f = clr_bit( self.f, self.flag_sub)
        self.f = set_bit( self.f, self.flag_par)
        self.f = clr_bit( self.f, self.flag_carry)
        self.f = set_bit( self.f, self.flag_half)

        self.a = self.a & value
        
        if self.a < 0:
            self.f = set_bit( self.f, self.flag_sign)
        else:
            self.f = clr_bit( self.f, self.flag_sign)
        
        if self.a == 0:
            self.f = set_bit( self.f, self.flag_zero)
        else:
            self.f = clr_bit( self.f, self.flag_zero)


    def xor_( self, value):
        self.f = clr_bit( self.f, self.flag_sub)
        self.f = set_bit( self.f, self.flag_par)
        self.f = clr_bit( self.f, self.flag_carry)
        self.f = set_bit( self.f, self.flag_half)

        self.a = self.a ^ value
        
        if self.a < 0:
            self.f = set_bit( self.f, self.flag_sign)
        else:
            self.f = clr_bit( self.f, self.flag_sign)
        
        if self.a == 0:
            self.f = set_bit( self.f, self.flag_zero)
        else:
            self.f = clr_bit( self.f, self.flag_zero)



    def execute( self, mem):
        # load command
        cmd = mem.read( self.pc)

        if cmd == 0x00:
            self.pc += 1
            result = "NOP"

        elif cmd == 0x02:
            mem.write( self.bc, self.a)
            self.pc += 1
            result = ( "LD (BC), A")

        elif cmd == 0x03:
            self.bc += 1
            result = ( "INC BC")

        elif cmd == 0x04:
            b = hi( self.bc)
            c = lo( self.bc)
            b += 1
            b &= 0xff
            self.bc = b << 8 | c 
            self.f = set_bit( self.f, self.flag_sub)
            self.f = clr_bit( self.f, self.flag_par)
            
            if b > 127:
                self.f = set_bit( self.f, self.flag_sign)
            else:
                self.f = clr_bit( self.f, self.flag_sign)
            
            if b == 0:
                self.f = set_bit( self.f, self.flag_zero)
            else:
                self.f = clr_bit( self.f, self.flag_zero)
            # TODO: carry
            # TODO: half carry
            self.pc += 1
            result = ( "INC B")

        elif cmd == 0x05:
            b = hi( self.bc)
            c = lo( self.bc)
            b -= 1
            b &= 0xff
            self.bc = b << 8 | c 
            self.f = set_bit( self.f, self.flag_sub)
            self.f = clr_bit( self.f, self.flag_par)
            
            if b > 127:
                self.f = set_bit( self.f, self.flag_sign)
            else:
                self.f = clr_bit( self.f, self.flag_sign)
            
            if b == 0:
                self.f = set_bit( self.f, self.flag_zero)
            else:
                self.f = clr_bit( self.f, self.flag_zero)
            # TODO: carry
            # TODO: half carry
            self.pc += 1
            result = ( "DEC B")

        elif cmd == 0x06:
            value = mem.read( self.pc + 1)
            self.set_b( value)
            self.pc += 2
            result = ( "LD B, 0%02Xh" % value)

        elif cmd == 0x08:
            af  = self.af
            af_ = self.af_
            self.af  = af_
            self.af_ = af
            self.pc += 1
            result = ( "EX AF,AF'")

        elif cmd == 0x0B:
            self.bc -= 1
            self.pc += 1
            result = ( "DEC BC")

        elif cmd == 0x0e:
            value = mem.read( self.pc + 1)
            self.set_c( value)
            self.pc += 2
            result = ( "LD C, 0%02Xh" % value)

        elif cmd == 0x13:
            self.de += 1
            self.pc += 1
            result = ( "INC DE")

        elif cmd == 0x16:
            value = mem.read( self.pc + 1)
            self.set_d( value)
            self.pc += 2
            result = ( "LD D, 0%02Xh" % value)

        elif cmd == 0x18:
            value = mem.read( self.pc + 1)
            if value > 127:
                value -= 256 
            self.pc = self.pc + value
            self.pc += 2
            result = ( "JR %+i" % value )

        elif cmd == 0x1B:
            self.de -= 1
            self.pc += 1
            result = ( "DEC DE")

        elif cmd == 0x1e:
            value = mem.read( self.pc + 1)
            self.set_e( value)
            self.pc += 2
            result = ( "LD E, 0%02Xh" % value)

        elif cmd == 0x1f:
            new_a = self.a >> 1
            new_cy = self.a & 0x01
            if bit_is_set( self.f, self.flag_carry):
                new_a |= 0x80
            self.a = new_a
            if new_cy > 0:
                self.f = set_bit( self.f, self.flag_carry)
            else:
                self.f = clr_bit( self.f, self.flag_carry)
            self.pc += 1
            result = ( "RRA")

        elif cmd == 0x20:
            value = mem.read( self.pc + 1)
            if value > 127:
                value -= 256 
            if bit_is_clear( self.f, self.flag_zero):
                self.pc = self.pc + value
            self.pc += 2
            result = ( "JR NZ, %+i" % value )

        elif cmd == 0x23:
            self.hl += 1
            self.pc += 1
            result = ( "INC HL")

        elif cmd == 0x26:
            value = mem.read( self.pc + 1)
            self.set_h( value)
            self.pc += 2
            result = ( "LD H, 0%02Xh" % value)

        elif cmd == 0x28:
            value = mem.read( self.pc + 1)
            if value > 127:
                value -= 256 
            if bit_is_set( self.f, self.flag_zero):
                self.pc = self.pc + value
            self.pc += 2
            result = ( "JR Z, %+i" % value )

        elif cmd == 0x2B:
            self.hl -= 1
            self.pc += 1
            result = ( "DEC HL")

        elif cmd == 0x2e:
            value = mem.read( self.pc + 1)
            self.set_l( value)
            self.pc += 2
            result = ( "LD L, 0%02Xh" % value)

        elif cmd == 0x30:
            value = mem.read( self.pc + 1)
            if value > 127:
                value -= 256 
            if bit_is_clear( self.f, self.flag_carry):
                self.pc = self.pc + value
            self.pc += 2
            result = ( "JR NC, %+i" % value )

        elif cmd == 0x33:
            self.sp += 1
            self.pc += 1
            result = ( "INC SP")

        elif cmd == 0x37:
            self.f = set_bit( self.f, self.flag_carry)
            self.f = clr_bit( self.f, self.flag_sub)
            self.f = clr_bit( self.f, self.flag_half)
            self.pc += 1
            result = ( "SCF")

        elif cmd == 0x38:
            value = mem.read( self.pc + 1)
            if value > 127:
                value -= 256 
            if bit_is_set( self.f, self.flag_carry):
                self.pc = self.pc + value
            self.pc += 2
            result = ( "JR C, %+i" % value )

        elif cmd == 0x3B:
            self.sp -= 1
            self.pc += 1
            result = ( "DEC SP")

        elif cmd == 0x3e:
            value = mem.read( self.pc + 1)
            self.a = value
            self.pc += 2
            result = ( "LD A, 0%02Xh" % value)

        elif cmd == 0x78:
            self.a = hi( self.bc)
            self.pc += 1
            result = ( "LD A, B")

        elif cmd == 0x79:
            self.a = lo( self.bc)
            self.pc += 1
            result = ( "LD A, C")

        elif cmd == 0x7a:
            self.a = hi( self.de)
            self.pc += 1
            result = ( "LD A, D")

        elif cmd == 0x7b:
            self.a = lo( self.de)
            self.pc += 1
            result = ( "LD A, E")

        elif cmd == 0x7c:
            self.a = hi( self.hl)
            self.pc += 1
            result = ( "LD A, H")

        elif cmd == 0x7d:
            self.a = lo( self.hl)
            self.pc += 1
            result = ( "LD A, L")

        elif cmd == 0x7e:
            value = mem.read( self.hl)
            self.a = value
            self.pc += 1
            result = ( "LD A, (HL)")

        elif cmd == 0x7f:
            self.pc += 1
            result = ( "LD A, A")

        elif cmd == 0xa0:
            value = hi( self.bc)
            self.and_( value)
            self.pc += 1
            result = ( "AND B")

        elif cmd == 0xa7:
            value = self.a
            self.and_( value)
            self.pc += 1
            result = ( "AND A")

        elif cmd == 0xaf:
            value = self.a
            self.xor_( value)
            self.pc += 1
            result = ( "XOR A")

        elif cmd == 0xc6:
            value = mem.read( self.pc + 1)
            self.add_( value)
            self.pc += 2
            result = ( "ADD 0%02Xh" % value)

        elif cmd == 0xc8:
            addr_lo = mem.read( self.sp + 0)
            addr_hi = mem.read( self.sp + 1)
            addr = ( addr_hi << 8) + addr_lo
            if bit_is_set( self.f, self.flag_zero):
                self.pc = addr
                self.sp += 2
            self.pc += 1
            result = ( "RET Z")

        elif cmd == 0xc9:
            addr_lo = mem.read( self.sp + 0)
            addr_hi = mem.read( self.sp + 1)
            addr = ( addr_hi << 8) + addr_lo
            self.pc = addr
            self.sp += 3
            result = ( "RET")
        
        elif cmd == 0xcb:
            cmd2 = mem.read( self.pc + 1)

            if cmd2 == 0x07:
                new_b = self.b << 1 | self.b >> 7
                if bit_is_set( self.b, 7):
                    self.f = set_bit( self.f, self.flag_carry)
                else:
                    self.f = clr_bit( self.f, self.flag_carry)
                self.b = new_b
                self.pc += 2
                result = ( "RLC B")
            elif cmd2 == 0x07:
                new_a = self.a << 1 | self.a >> 7
                if bit_is_set( self.a, 7):
                    self.f = set_bit( self.f, self.flag_carry)
                else:
                    self.f = clr_bit( self.f, self.flag_carry)
                self.a = new_a
                self.pc += 2
                result = ( "RLC A")
            elif cmd2 == 0xaf:
                self.a = clr_bit( self.a, 5)
                self.pc += 2
                result = ( "RES 5,A")
            else:
                self.pc += 2
                result = ( "subcommand CB%02X not implmented!  " % cmd2)
                raise ValueError

        elif cmd == 0xd9:
            self.bc, self.bc_ = self.bc_, self.bc
            self.de, self.de_ = self.de_, self.de
            self.hl, self.hl_ = self.hl_, self.hl
            self.pc += 1
            result = ( "EXX")

        elif cmd == 0xe6:
            value = mem.read( self.pc + 1)
            self.and_( value)
            self.pc += 2
            result = ( "AND 0%02Xh" % value)

        elif cmd == 0xeb:
            de = self.de
            hl = self.hl
            self.hl = de
            self.de = hl
            self.pc += 1
            result = ( "EX DE,HL")

        elif cmd == 0xfe:
            value = mem.read( self.pc + 1)
            self.compare( value)
            self.pc += 2
            result = ( "CP 0%02Xh" % value)

        elif cmd == 0xFFF:
            addr_lo = mem.read( self.pc + 1)
            addr_hi = mem.read( self.pc + 2)
            addr = ( addr_hi << 8) + addr_lo
            value = mem.read( addr)
            self.a = value
            self.pc += 3
            result = ( "LD A, ( 0%04Xh)" % addr)

        else:
            self.pc += 1
            result = ( "command not implmented!  ")
            raise ValueError
        

        self.a  &= 0xff
        self.bc &= 0xffff
        self.de &= 0xffff
        self.hl &= 0xffff
        self.pc &= 0xffff
        self.sp &= 0xffff
        
        # refresh
        self.r += 1
        self.r = self.r % 0x7f
        
        return( "cmd: 0%02Xh   %-15s" % ( cmd, result))
