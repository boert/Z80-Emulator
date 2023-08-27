class Memory:
    
    def __init__( self):
        self.mem = bytearray( 65536)


    def load( self, filename, offset = 0):
        with open( filename, 'rb') as file:
            binary_data = file.read()
            index = 0
            for by in binary_data:
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
    
    def write( self, address, data):
        self.mem[ address] = data
