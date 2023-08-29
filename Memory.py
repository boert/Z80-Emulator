class Memory:
    
    def __init__( self):
        self.mem = bytearray( 65536)


    def load( self, filename, offset = 0, length = -1):
        with open( filename, 'rb') as file:
            binary_data = file.read()
            index = 0
            for by in binary_data:
                if length == 0:
                    break
                length -= 1
                self.mem[ index + offset] = by
                index += 1

        print( "report: load %i bytes at 0x%04X" % ( index, offset))

    def hexdump( self, start = 0, length = 0x20, width = 8):
        index = start
        print( "%04X: " % index, end = '')
        for i in range( length):
            print( "%02X " % self.mem[ index], end = '')
            index += 1
            if i % 4 == 3:
                print( " ", end = '')
            if ( i % width) == ( width - 1):
                print()
                print( "%04X: " % index, end = '')
        print()
    
    def read( self, address):
        return self.mem[ address]

    def read16( self, address):
        val_lo = self.mem[ address]
        val_hi = self.mem[ address + 1]
        value = ( val_hi << 8) + val_lo
        return value
    
    def write( self, address, data):
        self.mem[ address] = data

    def write16( self, address, data):
        self.mem[ address + 0] = data & 0xff
        self.mem[ address + 1] = data >> 8
