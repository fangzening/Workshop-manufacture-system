#! /usr/bin/env python
# coding: utf-8

from _tools import *


__author__ = 'meisanggou'

"""
    RFC 3079
    https://tools.ietf.org/html/rfc3079
"""


def mppe_key_derivation_master_key(password_hash_hash, nt_response):
    """
    RFC 3079 MPPE Key Derivation
    3.4.  Key Derivation Functions
    GetMasterKey
    :param password_hash_hash:
    :param nt_response:
    :return: master_key
    """
    magic1 = "\x54\x68\x69\x73\x20\x69\x73\x20\x74\x68\x65\x20\x4d\x50\x50\x45\x20" \
             "\x4d\x61\x73\x74\x65\x72\x20\x4b\x65\x79"
    digest = multi_sha(password_hash_hash, nt_response, magic1)
    return digest[:16]


def mppe_key_derivation_asymetric_start_key(master_key, session_key_length, is_send, is_server):
    """
    RFC 3079 MPPE Key Derivation
    3.4.  Key Derivation Functions
    GetAsymetricStartKey
    :param master_key:
    :param session_key_length:
    :param is_send:
    :param is_server:
    :return:
    """
    shs_pad1 = "\x00" * 40

    shs_pad2 = "\xf2" * 40

    magic2 = "\x4f\x6e\x20\x74\x68\x65\x20\x63\x6c\x69\x65\x6e\x74\x20\x73\x69\x64\x65\x2c\x20\x74\x68\x69\x73\x20" \
             "\x69\x73\x20\x74\x68\x65\x20\x73\x65\x6e\x64\x20\x6b\x65\x79\x3b\x20\x6f\x6e\x20\x74\x68\x65\x20\x73" \
             "\x65\x72\x76\x65\x72\x20\x73\x69\x64\x65\x2c\x20\x69\x74\x20\x69\x73\x20\x74\x68\x65\x20\x72\x65\x63" \
             "\x65\x69\x76\x65\x20\x6b\x65\x79\x2e"

    magic3 = "\x4f\x6e\x20\x74\x68\x65\x20\x63\x6c\x69\x65\x6e\x74\x20\x73\x69\x64\x65\x2c\x20\x74\x68\x69\x73\x20" \
             "\x69\x73\x20\x74\x68\x65\x20\x72\x65\x63\x65\x69\x76\x65\x20\x6b\x65\x79\x3b\x20\x6f\x6e\x20\x74\x68" \
             "\x65\x20\x73\x65\x72\x76\x65\x72\x20\x73\x69\x64\x65\x2c\x20\x69\x74\x20\x69\x73\x20\x74\x68\x65\x20" \
             "\x73\x65\x6e\x64\x20\x6b\x65\x79\x2e"

    if is_send:
        if is_server:
            s = magic3
        else:
            s = magic2
    else:
        if is_server:
            s = magic2
        else:
            s = magic3
    digest = multi_sha(master_key, shs_pad1, s, shs_pad2)
    return digest[:session_key_length / 8]
