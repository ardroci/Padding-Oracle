#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging

import re
import array
import socket
import time
import io
import binascii
from binascii import unhexlify, hexlify
import itertools

from Homework3 import *

__author__ = "Ricardo Oliveira"
__copyright__ = "Ricardo Oliveira"
__license__ = "mit"

_logger = logging.getLogger(__name__)


def parse_args(args):
    """
    Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Padding Oracle Attack.")
    parser.add_argument(
        '-c',
        '--ciphertext',
        dest="ciphertext",
        help="Ciphertext",
        required=True)
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info("Starting crazy calculations...")

    ciphertext = args.ciphertext
    socket.setdefaulttimeout(10)
    po = PaddingOracle()

    block_size = 8
    valide_values, result = [], []
    blocks = split_len(ciphertext, length = 2 * block_size)
    if len(blocks) < 2:
        print("I can't work with this.")
        sys.exit(2)

    IV = blocks[0]

    for block in range(1,len(blocks)):
        _logger.info('{0}: {1}'.format('Block number', block))
        for i in range(0, block_size):
            _logger.info('{0}: {1}'.format('Byte', i))
            bl = blocks[block-1]
            bp = block_padding(i)
            for ct_pos in itertools.chain(range(97, 123), range(48, 58),
                                          range(2,9), range(30,33)):
                bk = block_search_byte(i, ct_pos, valide_values)
                temp = sxor(bk, bl)
                cb = sxor(temp, bp)
                cy = blocks[block]
                flag = po.query(cb + cy)

                if flag==True:
                    valide_values.insert(0,'{:02x}'.format(ct_pos))
                    _logger.info(unhexlify(''.join(valide_values)))
                    break

            if len(valide_values)!=i+1:
                print('Something went wrong!!')
                sys.exit(2)

        result.insert(len(valide_values),''.join(valide_values))
        valide_values = []
        _logger.info('{0}{1}{2}'.format(text_colors.YELLOW,
                                        unhexlify(''.join(result)),
                                        text_colors.ENDC))
    print('{0}{1}{2}{3}'.format('Solution: ',
                                text_colors.YELLOW,
                                unhexlify(''.join(result)),
                                text_colors.ENDC))
    _logger.info("Script ends here")


def run():
    """
    Entry point for console_scripts
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
