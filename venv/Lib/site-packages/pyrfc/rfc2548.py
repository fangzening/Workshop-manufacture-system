#! /usr/bin/env python
# coding: utf-8

import random
import hashlib


__author__ = 'meisanggou'

"""
    RFC 2548
    https://tools.ietf.org/html/rfc2548
"""


def generate_mppe_key(secret, authenticator, session_key, salt=None):
    """

    :param secret:
    :param authenticator:
    :param session_key:
    :param salt:
    :return:
    """
    # generate salt
    if salt is None:
        salt = chr(random.randint(128, 255)) + chr(random.randint(0, 255))
    # padding session_key
    pad_session_key = chr(len(session_key)) + session_key
    pad_session_key += "\x00" * (32 - (len(pad_session_key)) % 32)
    c = salt
    t_c = authenticator + salt
    for i in range(0, len(pad_session_key), 16):
        p_i = pad_session_key[i:i + 16]
        h = hashlib.md5()
        h.update(secret + t_c)
        b_i = h.digest()
        t_c = ""
        for i in range(len(b_i)):
            p_item = p_i[i]
            b_item = b_i[i]
            o_p = ord(p_item)
            o_b = ord(b_item)
            t_c += chr(o_p ^ o_b)
        c += t_c
    return c


def decrypt_mppe_key(secret, authenticator, en_key):
    salt = en_key[:2]
    c = en_key[2:]
    t_c = authenticator + salt
    p_i = ""
    for i in range(0, len(c), 16):
        c_i = c[i:i + 16]
        h = hashlib.md5()
        h.update(secret + t_c)
        b_i = h.digest()
        for i in range(len(b_i)):
            c_item = c_i[i]
            b_item = b_i[i]
            o_c = ord(c_item)
            o_b = ord(b_item)
            p_i += chr(o_c ^ o_b)
        t_c = c_i
    key = p_i[1: 1 + ord(p_i[0])]
    return key
