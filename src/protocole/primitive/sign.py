# -*- coding: utf-8 -*-
from src.protocole.Type import Type
from src.protocole.Primitive import Primitive
from src.protocole.Term import Term
from src.protocole.Variable import Variable
from src.protocole.protocolError import ProtocolError
class sign(Primitive):
    """class used to describe cryptographic primitive sign"""
    arity = 2

    # Creates a sign primitive with its 2 arguments
    def __init__(self, arguments=[], constructedtype=False):
        super().__init__("sign", arguments, constructedtype)
        try:
            assert isinstance(arguments[0], Term)
        except Exception:
            raise ProtocolError(("", "Constructed type ")[constructedtype] +
                                "sign does not have the right first argument (term) : " + arguments[0].__str__())
        if constructedtype:
            try:
                assert isinstance(arguments[1], Type)
            except Exception:
                raise ProtocolError("Constructed type sign does not have the right second argument (type) : "
                                    + arguments[1].__str__())
        else:
            try:
                assert isinstance(arguments[1], Variable)
            except Exception:
                raise ProtocolError("sign does not have the right second argument (variable) : "
                                    + arguments[1].__str__())

        # the first argument cannot be honest as it is a message
        if isinstance(arguments[0], Variable):
            arguments[0].type.honest = False

    def rho_out(self, rhoOut, pos, reached_key, sym, term):
        if sym:
            rhoOut.append([[self, pos], [reached_key, 0]])
        else:
            rhoOut.append([[self, pos], [0, reached_key]])
        message = self.arguments[0]
        message.rho_out(rhoOut, pos * 10 + 1, reached_key, sym, term)

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
            arg.append([message, pos*10 + 1])
        else:
            message.get_arg(arg, pos*10 + 1)

        if isinstance(key, Variable):
            arg.append([key, pos*10 + 2])
        else:
            key.get_arg(arg, pos*10 + 2)
