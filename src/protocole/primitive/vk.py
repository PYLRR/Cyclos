# -*- coding: utf-8 -*-
from src.protocole.Primitive import Primitive
from src.protocole.Type import Type
from src.protocole.Variable import Variable
from src.protocole.protocolError import ProtocolError


class vk(Primitive):
    """class used to describe cryptographic primitive vk"""
    arity = 1

    # Creates a vk primitive with its argument
    def __init__(self, arguments=[], constructedtype=False):
        super().__init__("vk", arguments, constructedtype)
        if constructedtype:
            try:
                assert isinstance(arguments[0], Type)
            except Exception:
                raise ProtocolError("Constructed type vk does not have the right argument (type) : "
                                    + arguments[0].__str__())
        else:
            try:
                assert isinstance(arguments[0], Variable)
            except Exception:
                raise ProtocolError("vk does not have the right argument (variable) : " + arguments[0].__str__())


    def rho_out(self, rhoOut, pos, reached_key, sym, term):
        if sym:
            rhoOut.append([[self, pos], [reached_key, 0]])
        else:
            rhoOut.append([[self, pos], [0, reached_key]])

    def rho_in(self, rhoIn):
        rhoIn.append(self)
        self.arguments[0].rho_in(rhoIn)

    def get_arg(self, arg, pos):
        key = self.arguments[0]

        if isinstance(key, Variable):
            arg.append([key, pos*10 + 1])
        else:
            key.getArgument(arg, pos*10 + 1)
