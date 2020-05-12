# -*- coding: utf-8 -*-
from src.protocole.primitive import aenc, pub, senc, sign, concat, vk
from src.protocole.protocolError import ProtocolError


# return the primitive if it exist, None otherwise
def getPrimitive(name, arguments=[], constructedtype=False):
    if name == "pub":
        return pub.pub(arguments, constructedtype)
    elif name == "aenc":
        return aenc.aenc(arguments, constructedtype)
    elif name == "senc":
        return senc.senc(arguments, constructedtype)
    elif name == "sign":
        return sign.sign(arguments, constructedtype)
    elif name == "vk":
        return vk.vk(arguments, constructedtype)
    elif name == "concat" or name == "pair":
        return concat.concat(arguments, constructedtype)
    else:
        raise ProtocolError("No primitive found with the name " + name)
