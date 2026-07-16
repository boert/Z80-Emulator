class IOtest:
    "IO tester"

    def __init__( self, address, value = 0, verbose = False):
        self.address = address
        self.value = value
        self.verbose = verbose

    def read( self, address):
        if self.address == address:
            if self.verbose:
                print( "IO read %04X" % address)
            return self.value

    def write( self, address, data):
        if self.address == address:
            if self.verbose:
                print = ( "IO write %04X = %02X" % ( address, data))
            self.value = data

    def dump( self):
        print( "IO %04X: %02X" % ( self.address, self.value))
