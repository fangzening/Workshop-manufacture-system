#! /usr/bin/env python
# coding: utf-8

from _tools import *

__author__ = 'meisanggou'

"""
    RFC 3078
    https://tools.ietf.org/html/rfc3078
"""


def get_new_key_from_sha(start_key, session_key):
    """

    :param start_key:
    :param session_key:
    :return: interim_key
    """
    sha_pad1 = "\x00" * 40

    sha_pad2 = "\xf2" * 40

    digest = multi_sha(start_key, sha_pad1, session_key, sha_pad2)
    return digest[:len(session_key)]

