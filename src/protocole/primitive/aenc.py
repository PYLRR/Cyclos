# -*- coding: utf-8 -*-
from src.protocole.Primitive import Primitive
from src.protocole.Term import Term
from src.protocole import Type
from src.protocole.Variable import Variable
from src.protocole.protocolError import ProtocolError

class aenc(Primitive):
    """class used to describe cryptographic primitive aenc"""
    arity = 2

    # Creates a aenc primitive with its 2 arguments
    def __init__(self, arguments=[], constructedtype=False):
        super().__init__("aenc", arguments, constructedtype)
        try:
            assert isinstance(arguments[0], Term)
        except Exception:
            raise ProtocolError(("", "Constructed type ")[constructedtype] +
                                "aenc does not have the right first argument (term) : " + arguments[0].__str__())
        try:
            assert isinstance(arguments[1], Term)
        except Exception:
            raise ProtocolError(("", "Constructed type ")[constructedtype] +
                                "aenc does not have the right second argument (term) : " + arguments[1].__str__())

        # the first argument cannot be honest as it is a message
        if isinstance(arguments[0], Variable):
            arguments[0].type.honest = False

    def rho_out(self, rhoOut, pos, reached_key, sym, term):
        sym = False
        rhoOut.append([[self, pos], [0, reached_key]])
        message = self.arguments[0]
        key = self.arguments[1]
        if key.isReachableOut():
            if type(key) == Variable:
                message.rho_out(rhoOut, pos * 10 + 1, key.type, sym, term)
            else:
                message.rho_out(rhoOut, pos * 10 + 1, key, sym, term)

    def rho_in(self, rhoIn):
        rhoIn.append(self)
        message = self.arguments[0]
        key = self.arguments[1]
        if key.isReachableIn():
            message.rho_in(rhoIn)
            key.rho_in(rhoIn)

    def get_arg(self, arg, pos):
        message = self.arguments[0]
        key = self.arguments[1]

        if isinstance(message, Variable):
            arg.append([message, pos])
        else:
            message.get_arg(arg, pos*10 + 1)

        if isinstance(key, Variable):
            arg.append([key, pos])
        else:
            key.get_arg(arg, pos*10 + 2)