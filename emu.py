#! /usr/bin/env python3

from Memory import Memory
from Register import Register

# globals
mem = Memory()
reg = Register()

def test( test_index, verbose = True):
    # init regs
    reg.set_hl( test_index)
    reg.set_pc( org)
    reg.set_sp( 0xfffe)
    if verbose:
        reg.print()

    steps = 0
    while True: 
        steps += 1
        result = reg.execute( mem)
        if verbose:
            print( result, end = '')
            reg.print_one()
        if reg.pc == 0:
            break
    result = reg.bc >> 8
    if reg.pc == 0:
        print( "program finish after %d steps!, test value: %02X  result: %d" % ( steps, test_index, result))
    else:
        print( "program stopped!")


def test_xx( test_index, verbose, prebyte):
    # init regs
    reg.set_hl( 0)
    reg.set_pc( org)
    reg.set_sp( 0xfffe)
    if verbose:
        reg.print()

    # init memory
    mem.write( 0, prebyte)
    mem.write( 1, test_index)

    steps = 0
    while True: 
        steps += 1
        result = reg.execute( mem)
        if verbose:
            print( result, end = '')
            reg.print_one()
        if reg.pc == 0:
            break
    result = reg.bc >> 8
    print( "program finish after %d steps!, test value: %02X%02X  result: %d" % ( steps, prebyte, test_index, result))


def test_xxCB( test_index, verbose, prebyte):
    # init regs
    reg.set_hl( 0)
    reg.set_pc( org)
    reg.set_sp( 0xfffe)
    if verbose:
        reg.print()

    # init memory
    mem.write( 0, prebyte)
    mem.write( 1, 0xcb)
    mem.write( 2, test_index)

    steps = 0
    while True: 
        steps += 1
        result = reg.execute( mem)
        if verbose:
            print( result, end = '')
            reg.print_one()
        if reg.pc == 0:
            break
    result = reg.bc >> 8
    print( "program finish after %d steps!, test value: %02XCB%02X  result: %d" % ( steps, prebyte, test_index, result))







print( "Welcome to Z80-Emulator!")

org = 0x100

# load memory
mem.load( 'binary.bin', org)
mem.hexdump( org, 32)


verbose = False
#verbose = True

# ok
if 0:
    # init memory 0..256
    for index in range( 256):
        mem.write( index, index)

    # Test von 0..n
    for test_index in range( 256):
        test( test_index, verbose)
        if test_index % 16 == 15:
            print()



# ok
if 0:
    # Test CB von 0..n
    for test_index in range( 256):
        test_xx( test_index, verbose, 0xcb)
        if test_index % 16 == 15:
            print()

# ok
if 0:
    # Test ED von 0..n
    for test_index in range( 256):
        test_xx( test_index, verbose, 0xed)
        if test_index % 16 == 15:
            print()

# ok
if 0:
    # Test DD von 0..n
    for test_index in range( 256):
        test_xx( test_index, verbose, 0xdd)
        if test_index % 16 == 15:
            print()


# ok
if 0:
    # Test FD von 0..n
    for test_index in range( 256):
        test_xx( test_index, verbose, 0xfd)
        if test_index % 16 == 15:
            print()
# ok
if 0:
    # Test DDCB von 0..n
    for test_index in range( 256):
        test_xxCB( test_index, verbose, 0xdd)
        if test_index % 16 == 15:
            print()

# ok
if 0:
    # Test FDCB von 0..n
    for test_index in range( 256):
        test_xxCB( test_index, verbose, 0xfd)
        if test_index % 16 == 15:
            print()


if 1:
    # Test single command, verbose
    test( 0xC9, True)
