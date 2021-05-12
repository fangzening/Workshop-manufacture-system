#! /usr/bin/env python
# coding: utf-8

import hashlib

__author__ = 'meisanggou'

"""
    Tools
"""


def multi_sha(*args):
    hs = hashlib.sha1(args[0])
    for i in range(1, len(args)):
        hs.update(args[i])
    digest = hs.digest()
    return digest


def unicode_password(password):
    u_password = ""
    for c in password:
        u_password += c
        u_password += "\x00"
    return u_password


def parity_corrected(v):
    """

    :param v:
    :return:
    example
    v = "\xFC\x15\x6A\xF7\xED\xCD\x6C"
    pv = "\xFD\x0B\x5B\x5E\x7F\x6E\x34\xD9"
    """
    s = ""
    for i in v:
        s += bin(ord(i))[2:].zfill(8)
    pv = ""
    temp_s = ""
    temp_b = 0
    for i in range(len(s)):
        temp_s += s[i]
        temp_b += int(s[i])
        if i % 7 == 6:
            temp_s += "%s" % ((temp_b + 1) % 2)
            pv += chr(int(temp_s, 2))
            temp_b = 0
            temp_s = ""
    return pv