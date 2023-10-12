"""
-*- coding : utf-8 -*-

@Author : ErickRen
@Time : 2023/10/11 17:22
"""

from .DefaultString import LOGIN_PUB_KEY
import base64
# 需要安装pycryptodome
# 这里有可能出现导包导不进去的问题，把site-packages里面的crypto文件夹改为大写Crypto即可
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def RSA_encrypt(user_name: str) -> str:
    """
    RSA公钥加密
    :param user_name: 账号 
    :return: 加密后的账号
    """
    pub_key = LOGIN_PUB_KEY
    rsa_key = RSA.importKey(pub_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    cipher_text = base64.b64encode(cipher.encrypt(user_name.encode(encoding='utf-8')))
    value = cipher_text.decode('utf-8')
    return value