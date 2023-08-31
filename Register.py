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



    def set_af( self, af):
        af &= 0xffff
        self.a  = hi( af)
        self.f  = lo( af)

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

    def set_bc( self, bc):
        self.bc = bc

    def set_d( self, value):
        if value < 0 or value > 255:
            raise RangeError
        self.de = ( value << 8) + ( self.de & 0x00ff)

    def set_e( self, value):
        if value < 0 or value > 255:
            raise RangeError
        self.de = ( self.de & 0xff00) + value 

    def set_de( self, de):
        self.de = de

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

    def set_ix( self, ix):
        self.ix = ix

    def set_iy( self, iy):
        self.iy = iy


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

    def bit_( self, value, bit):
        self.f = clr_bit( self.f, self.flag_sub)
        self.f = set_bit( self.f, self.flag_half)
        
        if bit_is_clear( value, bit):
            self.f = set_bit( self.f, self.flag_zero)
        else:
            self.f = clr_bit( self.f, self.flag_zero)


    def dec_( self, value):
        self.f = set_bit( self.f, self.flag_sub)
        self.f = clr_bit( self.f, self.flag_par)

        value -= 1

        if value < 0:
            value &= 0xff
        
        if value > 127:
            self.f = set_bit( self.f, self.flag_sign)
        else:
            self.f = clr_bit( self.f, self.flag_sign)
        
        if value == 0:
            self.f = set_bit( self.f, self.flag_zero)
        else:
            self.f = clr_bit( self.f, self.flag_zero)

        #TODO: flag_half
        return value

    def inc_( self, value):
        self.f = clr_bit( self.f, self.flag_sub)
        self.f = clr_bit( self.f, self.flag_par)

        value += 1

        if value > 255:
            value &= 0xff
        
        if value > 127:
            self.f = set_bit( self.f, self.flag_sign)
        else:
            self.f = clr_bit( self.f, self.flag_sign)
        
        if value == 0:
            self.f = set_bit( self.f, self.flag_zero)
        else:
            self.f = clr_bit( self.f, self.flag_zero)

        #TODO: flag_half
        return value


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

    def push_( self, mem, value):
        mem.write( self.sp - 1, hi( value))
        mem.write( self.sp - 2, lo( value))
        self.sp -= 2


    def pop_( self, mem):
        val_lo = mem.read( self.sp + 0)
        val_hi = mem.read( self.sp + 1)
        value = ( val_hi << 8) + val_lo
        self.sp += 2
        return value

    # missing opcodes:
    #                      07
    #                      17
    #                      27
    # 80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f
    # 90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f
    # a0 a1 a2 a3 a4 a5 a6    a8 a9 aa ab ac ad ae
    # b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf
    # c0    c2    c4                ca    cc    ce
    # d0    d2 d3 d4    d6    d8    da db dc    de
    # e0    e2 e3 e4          e8 e9 ea    ec    ee
    # f0    f2    f4    f6    f8    fa    fc

    def execute( self, mem):
        # load command
        cmd = mem.read( self.pc)

        if cmd == 0x00:
            self.pc += 1
            result = "NOP"

        elif cmd == 0x01:
            val_lo = mem.read( self.pc + 1)
            val_hi = mem.read( self.pc + 2)
            value = ( val_hi << 8) + val_lo
            self.set_bc( value)
            self.pc += 3
            result = ( "LD BC, 0%04Xh" % value)

        elif cmd == 0x02:
            mem.write( self.bc, self.a)
            self.pc += 1
            result = ( "LD (BC), A")

        elif cmd == 0x03:
            self.bc += 1
            self.pc += 1
            result = ( "INC BC")

        elif cmd == 0x04:
            value = hi( self.bc)
            value = self.inc_( value)
            self.set_b( value)
            self.pc += 1
            result = ( "INC B")

        elif cmd == 0x05:
            value = hi( self.bc)
            value = self.dec_( value)
            self.set_b( value)
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

        elif cmd == 0x09:
            self.hl += self.bc
            self.hl %= 0xffff
            self.pc += 1
            result = ( "ADD HL,BC")

        elif cmd == 0x0a:
            value = mem.read( self.bc)
            self.a = value
            self.pc += 1
            result = ( "LD A, (BC)")

        elif cmd == 0x0b:
            self.bc -= 1
            self.pc += 1
            result = ( "DEC BC")

        elif cmd == 0x0c:
            value = lo( self.bc)
            value = self.inc_( value)
            self.set_c( value)
            self.pc += 1
            result = ( "INC C")

        elif cmd == 0x0d:
            value = lo( self.bc)
            value = self.dec_( value)
            self.set_c( value)
            self.pc += 1
            result = ( "DEC C")

        elif cmd == 0x0e:
            value = mem.read( self.pc + 1)
            self.set_c( value)
            self.pc += 2
            result = ( "LD C, 0%02Xh" % value)
        
        elif cmd == 0x0f:
            new_a = self.a >> 1
            new_cy = self.a & 0x01
            if bit_is_set( self.a, 0):
                new_a |= 0x80
            self.a = new_a
            if new_cy > 0:
                self.f = set_bit( self.f, self.flag_carry)
            else:
                self.f = clr_bit( self.f, self.flag_carry)
            self.pc += 1
            result = ( "RRCA")

        elif cmd == 0x10:
            # dec b
            b = hi( self.bc)
            b = self.dec_( b)
            self.set_b( b)
            # jr nz,xx
            offset = mem.read( self.pc + 1)
            if offset > 127:
                offset -= 256 
            if bit_is_clear( self.f, self.flag_zero):
                self.pc = self.pc + offset
            self.pc += 2
            result = ( "DJNZ %+i" % offset)

        elif cmd == 0x11:
            val_lo = mem.read( self.pc + 1)
            val_hi = mem.read( self.pc + 2)
            value = ( val_hi << 8) + val_lo
            self.set_de( value)
            self.pc += 3
            result = ( "LD DE, 0%04Xh" % value)

        elif cmd == 0x12:
            mem.write( self.de, self.a)
            self.pc += 1
            result = ( "LD (DE), A")

        elif cmd == 0x13:
            self.de += 1
            self.pc += 1
            result = ( "INC DE")

        elif cmd == 0x14:
            value = hi( self.de)
            value = self.inc_( value)
            self.set_d( value)
            self.pc += 1
            result = ( "INC D")

        elif cmd == 0x15:
            value = hi( self.de)
            value = self.dec_( value)
            self.set_d( value)
            self.pc += 1
            result = ( "DEC D")

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

        elif cmd == 0x19:
            self.hl += self.de
            self.hl %= 0xffff
            self.pc += 1
            result = ( "ADD HL,DE")

        elif cmd == 0x1a:
            value = mem.read( self.de)
            self.a = value
            self.pc += 1
            result = ( "LD A, (DE)")

        elif cmd == 0x1b:
            self.de -= 1
            self.pc += 1
            result = ( "DEC DE")

        elif cmd == 0x1c:
            value = lo( self.de)
            value = self.inc_( value)
            self.set_e( value)
            self.pc += 1
            result = ( "INC E")

        elif cmd == 0x1d:
            value = lo( self.de)
            value = self.dec_( value)
            self.set_e( value)
            self.pc += 1
            result = ( "DEC E")

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
            offset = mem.read( self.pc + 1)
            if offset > 127:
                offset -= 256 
            if bit_is_clear( self.f, self.flag_zero):
                self.pc = self.pc + offset
            self.pc += 2
            result = ( "JR NZ, %+i" % offset )

        elif cmd == 0x21:
            value = mem.read16( self.pc + 1)
            self.set_hl( value)
            self.pc += 3
            result = ( "LD HL, 0%04Xh" % value)

        elif cmd == 0x22:
            addr = mem.read16( self.pc + 1)
            mem.write16( addr, self.hl)
            self.pc += 3
            result = ( "LD (0%04Xh), HL" % addr)


        elif cmd == 0x23:
            self.hl += 1
            self.pc += 1
            result = ( "INC HL")

        elif cmd == 0x24:
            value = hi( self.hl)
            value = self.inc_( value)
            self.set_h( value)
            self.pc += 1
            result = ( "INC H")

        elif cmd == 0x25:
            value = hi( self.hl)
            value = self.dec_( value)
            self.set_h( value)
            self.pc += 1
            result = ( "DEC H")

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

        elif cmd == 0x29:
            self.hl += self.hl
            self.hl %= 0xffff
            self.pc += 1
            result = ( "ADD HL,HL")
        
        elif cmd == 0x2a:
            addr = mem.read16( self.pc + 1)
            self.set_hl( mem.read16( addr))
            self.pc += 3
            result = ( "LD HL,(0%04Xh)" % addr)

        elif cmd == 0x2b:
            self.hl -= 1
            self.pc += 1
            result = ( "DEC HL")

        elif cmd == 0x2c:
            value = lo( self.hl)
            value = self.inc_( value)
            self.set_l( value)
            self.pc += 1
            result = ( "INC L")

        elif cmd == 0x2d:
            value = lo( self.hl)
            value = self.dec_( value)
            self.set_l( value)
            self.pc += 1
            result = ( "DEC L")

        elif cmd == 0x2e:
            value = mem.read( self.pc + 1)
            self.set_l( value)
            self.pc += 2
            result = ( "LD L, 0%02Xh" % value)
        
        elif cmd == 0x2f:
            self.f = set_bit( self.f, self.flag_half)
            self.f = set_bit( self.f, self.flag_sub)
            a = ~(self.a + 1)
            self.pc += 1
            result = ( "CPL")

        elif cmd == 0x30:
            value = mem.read( self.pc + 1)
            if value > 127:
                value -= 256 
            if bit_is_clear( self.f, self.flag_carry):
                self.pc = self.pc + value
            self.pc += 2
            result = ( "JR NC, %+i" % value )

        elif cmd == 0x31:
            value = mem.read16( self.pc + 1)
            self.set_sp( value)
            self.pc += 3
            result = ( "LD SP, 0%04Xh" % value)

        elif cmd == 0x32:
            addr = mem.read16( self.pc + 1)
            mem.write( addr, self.a)
            self.pc += 3
            result = ( "LD (0%04X), A" % addr)

        elif cmd == 0x33:
            self.sp += 1
            self.pc += 1
            result = ( "INC SP")

        elif cmd == 0x34:
            value = mem.read( self.hl)
            value = self.inc_( value)
            mem.write( self.hl, value)
            self.pc += 1
            result = ( "INC (HL)")

        elif cmd == 0x35:
            value = mem.read( self.hl)
            value = self.dec_( value)
            mem.write( self.hl, value)
            self.pc += 1
            result = ( "DEC (HL)")

        elif cmd == 0x36:
            value = mem.read( self.pc + 1)
            mem.write( self.hl, value)
            self.pc += 2
            result = ( "LD (HL), ß%02Xh" % value)

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

        elif cmd == 0x39:
            self.hl += self.sp
            self.hl %= 0xffff
            self.pc += 1
            result = ( "ADD HL,SP")

        elif cmd == 0x3a:
            addr = mem.read16( self.pc + 1)
            self.a = mem.read( addr)
            self.pc += 3
            result = ( "LD A, (0%04X)" % addr)

        elif cmd == 0x3b:
            self.sp -= 1
            self.pc += 1
            result = ( "DEC SP")
        
        elif cmd == 0x3c:
            self.a = self.inc_( self.a)
            self.pc += 1
            result = ( "INC A")
        
        elif cmd == 0x3d:
            self.a = self.dec_( self.a)
            self.pc += 1
            result = ( "DEC A")

        elif cmd == 0x3e:
            value = mem.read( self.pc + 1)
            self.a = value
            self.pc += 2
            result = ( "LD A, 0%02Xh" % value)

        elif cmd == 0x3f:
            if bit_is_set( self.f, self.flag_carry):
                self.f = clr_bit( self.f, self.flag_carry)
            else:
                self.f = set_bit( self.f, self.flag_carry)
            self.f = clr_bit( self.f, self.flag_sub)
            self.pc += 1
            result = ( "CCF")

        elif cmd == 0x40:
            value = hi( self.bc)
            self.set_b( value)
            self.pc += 1
            result = ( "LD B, B" % value)

        elif cmd == 0x41:
            value = lo( self.bc)
            self.set_b( value)
            self.pc += 1
            result = ( "LD B, C" % value)

        elif cmd == 0x42:
            value = hi( self.de)
            self.set_b( value)
            self.pc += 1
            result = ( "LD B, D" % value)

        elif cmd == 0x43:
            value = lo( self.de)
            self.set_b( value)
            self.pc += 1
            result = ( "LD B, E" % value)

        elif cmd == 0x44:
            value = hi( self.hl)
            self.set_b( value)
            self.pc += 1
            result = ( "LD B, H" % value)

        elif cmd == 0x45:
            value = lo( self.hl)
            self.set_b( value)
            self.pc += 1
            result = ( "LD B, L" % value)

        elif cmd == 0x46:
            value = mem.read( self.hl)
            self.set_b( value)
            self.pc += 1
            result = ( "LD B, (HL)")

        elif cmd == 0x47:
            self.set_b( self.a)
            self.pc += 1
            result = ( "LD B, A")

        elif cmd == 0x48:
            value = hi( self.bc)
            self.set_c( value)
            self.pc += 1
            result = ( "LD C, B" % value)

        elif cmd == 0x49:
            value = lo( self.bc)
            self.set_c( value)
            self.pc += 1
            result = ( "LD C, C" % value)

        elif cmd == 0x4a:
            value = hi( self.de)
            self.set_c( value)
            self.pc += 1
            result = ( "LD C, D" % value)

        elif cmd == 0x4b:
            value = lo( self.de)
            self.set_c( value)
            self.pc += 1
            result = ( "LD C, E" % value)

        elif cmd == 0x4c:
            value = hi( self.hl)
            self.set_c( value)
            self.pc += 1
            result = ( "LD C, H" % value)

        elif cmd == 0x4d:
            value = lo( self.hl)
            self.set_c( value)
            self.pc += 1
            result = ( "LD C, L")

        elif cmd == 0x4e:
            value = mem.read( self.hl)
            self.set_c( value)
            self.pc += 1
            result = ( "LD C, (HL)")

        elif cmd == 0x4f:
            self.set_c( self.a)
            self.pc += 1
            result = ( "LD C, A")

        elif cmd == 0x50:
            value = hi( self.bc)
            self.set_d( value)
            self.pc += 1
            result = ( "LD D, B")

        elif cmd == 0x51:
            value = lo( self.bc)
            self.set_d( value)
            self.pc += 1
            result = ( "LD D, C")

        elif cmd == 0x52:
            value = hi( self.de)
            self.set_d( value)
            self.pc += 1
            result = ( "LD D, D")

        elif cmd == 0x53:
            value = lo( self.de)
            self.set_d( value)
            self.pc += 1
            result = ( "LD D, E")

        elif cmd == 0x54:
            value = hi( self.hl)
            self.set_d( value)
            self.pc += 1
            result = ( "LD D, H")

        elif cmd == 0x55:
            value = lo( self.hl)
            self.set_d( value)
            self.pc += 1
            result = ( "LD D, L")

        elif cmd == 0x56:
            value = mem.read( self.hl)
            self.set_d( value)
            self.pc += 1
            result = ( "LD D, (HL)")

        elif cmd == 0x57:
            self.set_d( self.a)
            self.pc += 1
            result = ( "LD D, A")

        elif cmd == 0x58:
            value = hi( self.bc)
            self.set_e( value)
            self.pc += 1
            result = ( "LD E, B")

        elif cmd == 0x59:
            value = lo( self.bc)
            self.set_e( value)
            self.pc += 1
            result = ( "LD E, C")

        elif cmd == 0x5a:
            value = hi( self.de)
            self.set_e( value)
            self.pc += 1
            result = ( "LD E, D")

        elif cmd == 0x5b:
            value = lo( self.de)
            self.set_e( value)
            self.pc += 1
            result = ( "LD E, E")

        elif cmd == 0x5c:
            value = hi( self.hl)
            self.set_e( value)
            self.pc += 1
            result = ( "LD E, H")

        elif cmd == 0x5d:
            value = lo( self.hl)
            self.set_e( value)
            self.pc += 1
            result = ( "LD E, L")

        elif cmd == 0x5e:
            value = mem.read( self.hl)
            self.set_e( value)
            self.pc += 1
            result = ( "LD E, (HL)")

        elif cmd == 0x5f:
            self.set_e( self.a)
            self.pc += 1
            result = ( "LD E, A")

        elif cmd == 0x60:
            value = hi( self.bc)
            self.set_h( value)
            self.pc += 1
            result = ( "LD H, B")

        elif cmd == 0x61:
            value = lo( self.bc)
            self.set_h( value)
            self.pc += 1
            result = ( "LD H, C")

        elif cmd == 0x62:
            value = hi( self.de)
            self.set_h( value)
            self.pc += 1
            result = ( "LD H, D")

        elif cmd == 0x63:
            value = lo( self.de)
            self.set_h( value)
            self.pc += 1
            result = ( "LD H, E")

        elif cmd == 0x64:
            value = hi( self.hl)
            self.set_h( value)
            self.pc += 1
            result = ( "LD H, H")

        elif cmd == 0x65:
            value = lo( self.hl)
            self.set_h( value)
            self.pc += 1
            result = ( "LD H, L")

        elif cmd == 0x66:
            value = mem.read( self.hl)
            self.set_h( value)
            self.pc += 1
            result = ( "LD H, (HL)")

        elif cmd == 0x67:
            self.set_h( self.a)
            self.pc += 1
            result = ( "LD H, A")

        elif cmd == 0x68:
            value = hi( self.bc)
            self.set_l( value)
            self.pc += 1
            result = ( "LD L, B")

        elif cmd == 0x69:
            value = lo( self.bc)
            self.set_l( value)
            self.pc += 1
            result = ( "LD L, C")

        elif cmd == 0x6a:
            value = hi( self.de)
            self.set_l( value)
            self.pc += 1
            result = ( "LD L, D")

        elif cmd == 0x6b:
            value = lo( self.de)
            self.set_l( value)
            self.pc += 1
            result = ( "LD L, E")

        elif cmd == 0x6c:
            value = hi( self.hl)
            self.set_l( value)
            self.pc += 1
            result = ( "LD L, H")

        elif cmd == 0x6d:
            value = lo( self.hl)
            self.set_l( value)
            self.pc += 1
            result = ( "LD L, L")

        elif cmd == 0x6e:
            value = mem.read( self.hl)
            self.set_l( value)
            self.pc += 1
            result = ( "LD L, (HL)")

        elif cmd == 0x6f:
            self.set_l( self.a)
            self.pc += 1
            result = ( "LD L, A")

        elif cmd == 0x70:
            mem.write( self.hl, hi( self.bc))
            self.pc += 1
            result = ( "LD (HL), B")

        elif cmd == 0x71:
            mem.write( self.hl, lo( self.bc))
            self.pc += 1
            result = ( "LD (HL), C")

        elif cmd == 0x72:
            mem.write( self.hl, hi( self.de))
            self.pc += 1
            result = ( "LD (HL), D")

        elif cmd == 0x73:
            mem.write( self.hl, lo( self.de))
            self.pc += 1
            result = ( "LD (HL), E")

        elif cmd == 0x74:
            mem.write( self.hl, hi( self.hl))
            self.pc += 1
            result = ( "LD (HL), H")

        elif cmd == 0x75:
            mem.write( self.hl, lo( self.hl))
            self.pc += 1
            result = ( "LD (HL), L")

        elif cmd == 0x76:
            result = ( "HLT")

        elif cmd == 0x77:
            mem.write( self.hl, self.a)
            self.pc += 1
            result = ( "LD (HL), A")

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

        elif cmd == 0xc1:
            self.bc = self.pop_( mem)
            self.pc += 1
            result = ( "POP BC")

        elif cmd == 0xc3:
            addr = mem.read16( self.pc + 1)
            self.pc = addr
            result = ( "JP 0%04X" % addr)

        elif cmd == 0xc5:
            self.push_( mem, self.bc)
            self.pc += 1
            result = ( "PUSH BC")

        elif cmd == 0xc6:
            value = mem.read( self.pc + 1)
            self.add_( value)
            self.pc += 2
            result = ( "ADD 0%02Xh" % value)

        elif cmd == 0xc7:
            self.push_( mem, self.pc)
            self.pc = 0x00
            result = ( "RST 00h")

        elif cmd == 0xc8:
            if bit_is_set( self.f, self.flag_zero):
                self.pc = self.pop_( mem)
            self.pc += 1
            result = ( "RET Z")

        elif cmd == 0xc9:
            self.pc = self.pop_( mem) + 3
            result = ( "RET")
        
        # enhanced commands
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

        elif cmd == 0xcd:
            self.push_( mem, self.pc)
            addr = mem.read16( self.pc + 1)
            self.pc = addr
            result = ( "CALL 0%04X" % addr)

        elif cmd == 0xcf:
            self.push_( mem, self.pc)
            self.pc = 0x08
            result = ( "RST 08h")

        elif cmd == 0xd1:
            self.de = self.pop_( mem)
            self.pc += 1
            result = ( "POP DE")

        elif cmd == 0xd5:
            self.push_( mem, self.de)
            self.pc += 1
            result = ( "PUSH DE")

        elif cmd == 0xd7:
            self.push_( mem, self.pc)
            self.pc = 0x10
            result = ( "RST 10h")

        elif cmd == 0xd9:
            self.bc, self.bc_ = self.bc_, self.bc
            self.de, self.de_ = self.de_, self.de
            self.hl, self.hl_ = self.hl_, self.hl
            self.pc += 1
            result = ( "EXX")
        
        # enhanced commands
        elif cmd == 0xdd:
            cmd2 = mem.read( self.pc + 1)

            if cmd2 == 0x09:
                self.ix += self.bc
                self.ix %= 0xffff
                self.pc += 2
                result = ( "ADD IX,BC")

            elif cmd2 == 0x19:
                self.ix += self.de
                self.ix %= 0xffff
                self.pc += 2
                result = ( "ADD IX,DE")

            elif cmd2 == 0x21:
                value = mem.read16( self.pc + 2)
                self.set_ix( value)
                self.pc += 4
                result = ( "LD IX, 0%04Xh" % value)

            elif cmd2 == 0x22:
                addr = mem.read16( self.pc + 2)
                mem.write16( addr, self.ix)
                self.pc += 4
                result = ( "LD (0%04Xh), IX" % addr)
            
            elif cmd2 == 0x2a:
                addr = mem.read16( self.pc + 2)
                self.set_ix( mem.read16( addr))
                self.pc += 4
                result = ( "LD IX,(0%04Xh)" % addr)

            elif cmd2 == 0x34:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                value = mem.read( self.ix + offset)
                value = self.inc_( value)
                mem.write( self.ix + offset, value)
                self.pc += 3
                result = ( "INC (IX+0%02Xh)" % ( offset))

            elif cmd2 == 0x36:
                offset = mem.read( self.pc + 2)
                value  = mem.read( self.pc + 3)
                if offset > 127:
                    offset -= 256 
                mem.write( self.ix + offset, value)
                self.pc += 4
                result = ( "LD (IX+0%02Xh), %02X" % ( offset, value))

            elif cmd2 == 0x46:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                value = mem.read( self.ix + offset)
                self.set_b( value)
                self.pc += 3
                result = ( "LD B, (IX+0%02Xh)" % ( offset))

            elif cmd2 == 0x4e:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                value = mem.read( self.ix + offset)
                self.set_c( value)
                self.pc += 3
                result = ( "LD C, (IX+0%02Xh)" % ( offset))

            elif cmd2 == 0x75:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                mem.write( self.ix + offset, lo( self.hl))
                self.pc += 3
                result = ( "LD (IX+0%02Xh), L" % offset)

            elif cmd2 == 0x7e:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                value = mem.read( self.ix + offset)
                self.a = value
                self.pc += 3
                result = ( "LD A, (IX+0%02Xh)" % ( offset))
            
            elif cmd2 == 0xcb:
                offset = mem.read( self.pc + 2)
                cmd4   = mem.read( self.pc + 3)
                if offset > 127:
                    offset -= 256 

                if cmd4 == 0x46:
                    value = mem.read( self.ix + offset)
                    self.bit_( value, 0)
                    self.pc += 4
                    result = ( "BIT 0,(IX%+i)" % offset)

                elif cmd4 == 0x4e:
                    value = mem.read( self.ix + offset)
                    self.bit_( value, 1)
                    self.pc += 4
                    result = ( "BIT 1,(IX%+i)" % offset)

                elif cmd4 == 0x56:
                    value = mem.read( self.ix + offset)
                    self.bit_( value, 2)
                    self.pc += 4
                    result = ( "BIT 2,(IX%+i)" % offset)

                elif cmd4 == 0x5e:
                    value = mem.read( self.ix + offset)
                    self.bit_( value, 3)
                    self.pc += 4
                    result = ( "BIT 3,(IX%+i)" % offset)

                elif cmd4 == 0x66:
                    value = mem.read( self.ix + offset)
                    self.bit_( value, 4)
                    self.pc += 4
                    result = ( "BIT 4,(IX%+i)" % offset)

                elif cmd4 == 0x6e:
                    value = mem.read( self.ix + offset)
                    self.bit_( value, 5)
                    self.pc += 4
                    result = ( "BIT 5,(IX%+i)" % offset)

                elif cmd4 == 0x76:
                    value = mem.read( self.ix + offset)
                    self.bit_( value, 6)
                    self.pc += 4
                    result = ( "BIT 6,(IX%+i)" % offset)

                elif cmd4 == 0x7e:
                    value = mem.read( self.ix + offset)
                    self.bit_( value, 7)
                    self.pc += 4
                    result = ( "BIT 7,(IX%+i)" % offset)

                else:
                    self.pc += 4
                    result = ( "subcommand DDCB%02X%02X not implmented!  " % ( offset, cmd3))

            elif cmd2 == 0xe1:
                self.ix = self.pop_( mem)
                self.pc += 2
                result = ( "POP IX")

            elif cmd2 == 0xe5:
                self.push_( mem, self.ix)
                self.pc += 2
                result = ( "PUSH IX")

            elif cmd2 == 0xf9:
                self.set_sp( self.ix)
                self.pc += 2
                result = ( "LD SP, IX")

            else:
                self.pc += 2
                result = ( "subcommand DD%02X not implmented!  " % cmd2)
                #raise ValueError

        elif cmd == 0xdf:
            self.push_( mem, self.pc)
            self.pc = 0x18
            result = ( "RST 18h")

        elif cmd == 0xe1:
            self.hl = self.pop_( mem)
            self.pc += 1
            result = ( "POP HL")

        elif cmd == 0xe5:
            self.push_( mem, self.hl)
            self.pc += 1
            result = ( "PUSH HL")

        elif cmd == 0xe6:
            value = mem.read( self.pc + 1)
            self.and_( value)
            self.pc += 2
            result = ( "AND 0%02Xh" % value)

        elif cmd == 0xe7:
            self.push_( mem, self.pc)
            self.pc = 0x20
            result = ( "RST 20h")

        elif cmd == 0xeb:
            de = self.de
            hl = self.hl
            self.hl = de
            self.de = hl
            self.pc += 1
            result = ( "EX DE,HL")
        
        # enhanced commands
        elif cmd == 0xed:
            cmd2 = mem.read( self.pc + 1)

            if cmd2 == 0x47:
                self.i = self.a
                self.pc += 2
                result = ( "LD I,A")

            elif cmd2 == 0x4f:
                self.r = self.a
                self.pc += 2
                result = ( "LD R,A")

            elif cmd2 == 0xb0:
                while True:
                    mem.write( self.de, mem.read( self.hl))
                    self.de += 1
                    self.hl += 1
                    self.bc -= 1
                    if self.bc == 0:
                        break
                self.pc += 2
                result = ( "LDIR")

            else:
                self.pc += 2
                result = ( "subcommand ED%02X not implmented!  " % cmd2)
                #raise ValueError

        elif cmd == 0xef:
            self.push_( mem, self.pc)
            self.pc = 0x28
            result = ( "RST 28h")

        elif cmd == 0xf1:
            self.set_af( self.pop_( mem))
            self.pc += 1
            result = ( "POP AF")

        elif cmd == 0xf3:
            self.pc += 1
            result = ( "DI")

        elif cmd == 0xf5:
            value = self.a << 8 + self.f
            self.push_( mem, value)
            self.pc += 1
            result = ( "PUSH AF")

        elif cmd == 0xf7:
            self.push_( mem, self.pc)
            self.pc = 0x30
            result = ( "RST 30h")

        elif cmd == 0xf9:
            self.set_sp( self.hl)
            self.pc += 1
            result = ( "LD SP, HL")

        elif cmd == 0xfb:
            self.pc += 1
            result = ( "EI")
        
        # enhanced commands
        elif cmd == 0xfd:
            cmd2 = mem.read( self.pc + 1)

            if cmd2 == 0x09:
                self.iy += self.bc
                self.iy %= 0xffff
                self.pc += 2
                result = ( "ADD IY,BC")

            elif cmd2 == 0x19:
                self.iy += self.de
                self.iy %= 0xffff
                self.pc += 2
                result = ( "ADD IY,DE")
            
            elif cmd2 == 0x21:
                value = mem.read16( self.pc + 2)
                self.set_iy( value)
                self.pc += 4
                result = ( "LD IY, 0%04Xh" % value)

            elif cmd2 == 0x22:
                addr = mem.read16( self.pc + 2)
                mem.write16( addr, self.iy)
                self.pc += 4
                result = ( "LD (0%04Xh), IY" % addr)
            
            elif cmd2 == 0x2a:
                addr = mem.read16( self.pc + 2)
                self.set_iy( mem.read16( addr))
                self.pc += 4
                result = ( "LD IY,(0%04Xh)" % addr)

            elif cmd2 == 0x34:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                value = mem.read( self.iy + offset)
                value = self.inc_( value)
                mem.write( self.iy + offset, value)
                self.pc += 3
                result = ( "INC (IY+0%02Xh)" % ( offset))
            
            elif cmd2 == 0x36:
                offset = mem.read( self.pc + 2)
                value  = mem.read( self.pc + 3)
                if offset > 127:
                    offset -= 256 
                mem.write( self.iy + offset, value)
                self.pc += 4
                result = ( "LD (IY+0%02X), %02X" % ( offset, value))

            elif cmd2 == 0x46:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                value = mem.read( self.iy + offset)
                self.set_b( value)
                self.pc += 3
                result = ( "LD B, (IY+0%02Xh)" % ( offset))

            elif cmd2 == 0x4e:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                value = mem.read( self.iy + offset)
                self.set_c( value)
                self.pc += 3
                result = ( "LD C, (IY+0%02Xh)" % ( offset))

            elif cmd2 == 0x75:
                value = mem.read( self.pc + 2)
                if value > 127:
                    value -= 256 
                mem.write( self.iy + value, lo( self.hl))
                self.pc += 3
                result = ( "LD (IY+0%02Xh), L" % value)

            elif cmd2 == 0x7e:
                offset = mem.read( self.pc + 2)
                if offset > 127:
                    offset -= 256 
                value = mem.read( self.iy + offset)
                self.a = value
                self.pc += 3
                result = ( "LD A, (IY+0%02Xh)" % ( offset))
            
            elif cmd2 == 0xcb:
                offset = mem.read( self.pc + 2)
                cmd4   = mem.read( self.pc + 3)
                if offset > 127:
                    offset -= 256 

                if cmd4 == 0x46:
                    value = mem.read( self.iy + offset)
                    self.bit_( value, 0)
                    self.pc += 4
                    result = ( "BIT 0,(IY%+i)" % offset)

                elif cmd4 == 0x4e:
                    value = mem.read( self.iy + offset)
                    self.bit_( value, 1)
                    self.pc += 4
                    result = ( "BIT 1,(IY%+i)" % offset)

                elif cmd4 == 0x56:
                    value = mem.read( self.iy + offset)
                    self.bit_( value, 2)
                    self.pc += 4
                    result = ( "BIT 2,(IY%+i)" % offset)

                elif cmd4 == 0x5e:
                    value = mem.read( self.iy + offset)
                    self.bit_( value, 3)
                    self.pc += 4
                    result = ( "BIT 3,(IY%+i)" % offset)

                elif cmd4 == 0x66:
                    value = mem.read( self.iy + offset)
                    self.bit_( value, 4)
                    self.pc += 4
                    result = ( "BIT 4,(IY%+i)" % offset)

                elif cmd4 == 0x6e:
                    value = mem.read( self.iy + offset)
                    self.bit_( value, 5)
                    self.pc += 4
                    result = ( "BIT 5,(IY%+i)" % offset)

                elif cmd4 == 0x76:
                    value = mem.read( self.iy + offset)
                    self.bit_( value, 6)
                    self.pc += 4
                    result = ( "BIT 6,(IY%+i)" % offset)

                elif cmd4 == 0x7e:
                    value = mem.read( self.iy + offset)
                    self.bit_( value, 7)
                    self.pc += 4
                    result = ( "BIT 7,(IY%+i)" % offset)

                else:
                    self.pc += 4
                    result = ( "subcommand FDCB%02X%02X not implmented!  " % ( offset, cmd3))


            elif cmd2 == 0xe1:
                self.iy = self.pop_( mem)
                self.pc += 2
                result = ( "POP IY")

            elif cmd2 == 0xe5:
                self.push_( mem, self.iy)
                self.pc += 2
                result = ( "PUSH IY")

            elif cmd2 == 0xf9:
                self.set_sp( self.iy)
                self.pc += 2
                result = ( "LD SP, IY")

            else:
                self.pc += 2
                result = ( "subcommand DD%02X not implmented!  " % cmd2)
                #raise ValueError

        elif cmd == 0xfe:
            value = mem.read( self.pc + 1)
            self.compare( value)
            self.pc += 2
            result = ( "CP 0%02Xh" % value)

        elif cmd == 0xff:
            self.push_( mem, self.pc)
            self.pc = 0x38
            result = ( "RST 38h")

        else:
            self.pc += 1
            result = ( "command not implmented!  ")
            #raise ValueError
        

        self.a  &= 0xff
        self.bc &= 0xffff
        self.de &= 0xffff
        self.hl &= 0xffff
        self.pc &= 0xffff
        self.sp &= 0xffff
        
        # refresh
        self.r += 1
        self.r = self.r % 0x7f
        
        return( "cmd: 0%02Xh   %-17s" % ( cmd, result))
