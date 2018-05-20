#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib.parse
import urllib.request
import sys
import re
import array
import socket
import time
import io
import binascii
from binascii import unhexlify, hexlify
import itertools

__author__ = "Ricardo Oliveira"
__copyright__ = "Ricardo Oliveira"
__license__ = "mit"

#--------------------------------------------------------------
# Padding Oracle 
# Fornecido pelo Professor da u.c
#--------------------------------------------------------------
TARGET = 'http://penhas.di.ubi.pt:8080/AttackPad/attackpad?id=9&er='

class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib.parse.quote(q)     # Create query URL
        req = urllib.request.Request(target)         # Send HTTP request to server
        try:
            f = urllib.request.urlopen(req)          # Wait for response
            # print ('recieved nothing interesting')
            return False                             #THIS IS RETURN CODE 200 ALL OK
        except urllib.error.HTTPError as e:          #python 2 syntax    
            # printf ("We got http error: %d", e.code)        # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding
#--------------------------------------------------------------

class text_colors:
    MAGENTA = '\033[95m'
    BLUE= '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'

def split_len(ciphertext, length = 8):
    """
    Split ciphertext in 8 bytes blocks.
    :param length: block length
    :param ciphertext: ciphertext
    """
    return [ciphertext[i:i+length] for i in range(0, len(ciphertext), length)]

def block_search_byte(i, pos, l, block_size = 8):
    """
    create custom block for the byte we search
    :param i:
    :param pos:
    :param l:
    """
    hex_char = hex(pos).split('0x')[1].zfill(2)
    return "00"*(block_size-(i+1)) + ("0" if len(hex_char)%2 != 0 else '') + hex_char + ''.join(l)

def block_padding(i, block_size = 8):
    """
    create custom block for the padding
    :param i:
    :param block_size: block length
    """
    l = []
    for t in range(0,i+1):
        l.append(("0" if len(hex(i+1).split('0x')[1])%2 != 0 else '') + (hex(i+1).split('0x')[1]))
    return "00"*(block_size - (i+1)) + ''.join(l)

def sxor(s1,s2):
    """
    Exclusive OR two hexadecimal blocks
    Convert strings to a list of character pair tuples.
    go through each tuple, converting them to ASCII code (ord) perform exclusive or on the ASCII code then convert the result back to ASCII (chr) merge the resulting array of characters as a string
    :param s1: hexdecimal string
    :param s2: hexdecimal string
    """
    a = ''
    for c1, c2 in zip(unhexlify(s1), itertools.cycle(unhexlify(s2))):
        a += ''.join(hex(c1 ^ c2)[2:].zfill(2) )
    return a
