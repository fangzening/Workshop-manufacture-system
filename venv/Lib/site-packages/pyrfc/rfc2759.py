#! /usr/bin/env python
# coding: utf-8

from Crypto.Hash import MD4
from Crypto.Cipher import DES
import binascii
from _tools import *

__author__ = 'meisanggou'

"""
    RFC 2759
    https://tools.ietf.org/html/rfc2759.html
"""


def generate_nt_response(auth_challenge, peer_challenge, user_name, u_password):
    """
    RFC 2759
    section 8.1
    GenerateNTResponse
    :param auth_challenge:
    :param peer_challenge:
    :param user_name:
    :param u_password:
    :return: response
    """
    challenge = challenge_hash(peer_challenge, auth_challenge, user_name)
    password_hash = nt_password_hash(u_password)
    response = challenge_response(challenge, password_hash)
    return response


def challenge_hash(peer_challenge, auth_challenge, user_name):
    """
    RFC 2759
    section 8.2
    ChallengeHash
    :param peer_challenge:
    :param auth_challenge:
    :param user_name:
    :return: challenge
    example
    peer_challenge = "\x21\x40\x23\x24\x25\x5E\x26\x2A\x28\x29\x5F\x2B\x3A\x33\x7C\x7E"
    auth_challenge = "\x5B\x5D\x7C\x7D\x7B\x3F\x2F\x3E\x3C\x2C\x60\x21\x32\x26\x26\x28"
    user_name = "User"
    challenge = "\xD0\x2E\x43\x86\xBC\xE9\x12\x26"
    """
    challenge = multi_sha(peer_challenge, auth_challenge, user_name)
    return challenge[:8]


def nt_password_hash(u_password):
    """
    RFC 2759
    section 8.3
    NtPasswordHash
    :param u_password:
    :return: password_hash
    example
    password = "clientPass"
    password_hash = "\x44\xEB\xBA\x8D\x53\x12\xB8\xD6\x11\x47\x44\x11\xF5\x69\x89\xAE"
    """
    h = MD4.new()
    h.update(u_password)
    password_hash = h.digest()
    return password_hash


def challenge_response(challenge, password_hash):
    """
    RFC 2759
    section 8.5
    :param challenge:
    :param password_hash:
    :return: response
    example
    challenge = "\xD0\x2E\x43\x86\xBC\xE9\x12\x26"
    password_hash = "\x44\xEB\xBA\x8D\x53\x12\xB8\xD6\x11\x47\x44\x11\xF5\x69\x89\xAE"
    response = "\x82\x30\x9E\xCD\x8D\x70\x8B\x5E\xA0\x8F\xAA\x39\x81\xCD\x83\x54\x42\x33\x11\x4A\x3D\x85\xD6\xDF"
    """
    response = ""
    z_password_hash = password_hash + "\x00" * (21 - len(password_hash))

    response += des_encrypt(challenge, z_password_hash[:7])
    response += des_encrypt(challenge, z_password_hash[7:14])
    response += des_encrypt(challenge, z_password_hash[14:])

    return response


def des_encrypt(clear, key):
    """
    RFC 2759
    section 8.6
    DesEncrypt
    :param clear:
    :param key:
    :return: cypher
    """
    d2 = DES.new(parity_corrected(key))
    cypher = d2.encrypt(clear)
    return cypher


def generate_authenticator_response(u_password, nt_response, peer_challenge, auth_challenge, user_name):
    """
    RFC 2759
    section 8.7
    GenerateAuthenticatorResponse
    :param u_password:
    :param peer_challenge:
    :param auth_challenge:
    :param user_name:
    :return: auth_response
    """
    magic1 = "\x4D\x61\x67\x69\x63\x20\x73\x65\x72\x76\x65\x72\x20\x74\x6F\x20\x63\x6C\x69\x65\x6E\x74\x20" \
             "\x73\x69\x67\x6E\x69\x6E\x67\x20\x63\x6F\x6E\x73\x74\x61\x6E\x74"
    magic2 = "\x50\x61\x64\x20\x74\x6F\x20\x6D\x61\x6B\x65\x20\x69\x74\x20\x64\x6F\x20\x6D\x6F\x72\x65\x20" \
             "\x74\x68\x61\x6E\x20\x6F\x6E\x65\x20\x69\x74\x65\x72\x61\x74\x69\x6F\x6E"
    password_hash = nt_password_hash(u_password)
    password_hash_hash = nt_password_hash(password_hash)

    digest = multi_sha(password_hash_hash, nt_response, magic1)

    challenge = challenge_hash(peer_challenge, auth_challenge, user_name)

    digest2 = multi_sha(digest, challenge, magic2)

    return "S=%s" % binascii.b2a_hex(digest2).upper()


def generate_authenticator_response2(password_hash, nt_response, peer_challenge, auth_challenge, user_name):
    """
    :param u_password:
    :param peer_challenge:
    :param auth_challenge:
    :param user_name:
    :return: auth_response
    """
    magic1 = "\x4D\x61\x67\x69\x63\x20\x73\x65\x72\x76\x65\x72\x20\x74\x6F\x20\x63\x6C\x69\x65\x6E\x74\x20" \
             "\x73\x69\x67\x6E\x69\x6E\x67\x20\x63\x6F\x6E\x73\x74\x61\x6E\x74"
    magic2 = "\x50\x61\x64\x20\x74\x6F\x20\x6D\x61\x6B\x65\x20\x69\x74\x20\x64\x6F\x20\x6D\x6F\x72\x65\x20" \
             "\x74\x68\x61\x6E\x20\x6F\x6E\x65\x20\x69\x74\x65\x72\x61\x74\x69\x6F\x6E"

    password_hash_hash = nt_password_hash(password_hash)

    digest = multi_sha(password_hash_hash, nt_response, magic1)

    challenge = challenge_hash(peer_challenge, auth_challenge, user_name)

    digest2 = multi_sha(digest, challenge, magic2)

    return "S=%s" % binascii.b2a_hex(digest2).upper()


def check_authenticator_response(u_password, nt_response, peer_challenge, auth_challenge, user_name, received_response):
    """
    RFC 2759
    section 8,8
    :param u_password:
    :param nt_response:
    :param peer_challenge:
    :param auth_challenge:
    :param user_name:
    :param received_response:
    :return:response_ok
    """
    auth_response = generate_authenticator_response(u_password, nt_response, peer_challenge, auth_challenge, user_name)
    return auth_response == received_response
