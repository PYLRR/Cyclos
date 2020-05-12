# -*- coding: utf-8 -*-
from src.protocole.Type import Type
from src.protocole.Primitive import Primitive
from src.protocole.Term import Term
from src.protocole.Variable import Variable
from src.protocole.protocolError import ProtocolError
class concat(Primitive):
    """class used to describe cryptographic primitive concat"""
    arity = -1

    # Creates a concat primitive with its n arguments
    def __init__(self, arguments=[], constructedtype=False):
        super().__init__("concat", arguments, constructedtype)
        compt=0
        for arg in arguments:
            compt += 1
            try:
                assert isinstance(arg, Term)
                # this argument cannot be honest as it is seen by the attacker
                if self.constructedtype:
                    if isinstance(arg, Type):
                        arg.honest = False
                else:
                    if isinstance(arg, Variable):
                        arg.type.honest = False
            except Exception:
                raise ProtocolError(("", "Constructed type ")[constructedtype]
                                    + "concat does not have the right " + str(compt)
                                    + "argument (term) :" + arg.__str__())

    def rho_out(self, rhoOut, pos, reached_key, sym, term):
        if sym:
            rhoOut.append([[self, pos], [reached_key, 0]])
        else:
            rhoOut.append([[self, pos], [0, reached_key]])
        i = 1
        for a in self.arguments:
            if type(a) == Variable:
                if not term:
                    a.type.rho_out(rhoOut, pos * 10 + i, reached_key, sym, term)
                else:
                    a.rho_out(rhoOut, pos * 10 + i, reached_key, sym, term)
            else:
                a.rho_out(rhoOut, pos * 10 + i, reached_key, sym, term)
            i = i + 1

    def rho_in(self, rhoIn):
        rhoIn.append(self)
        for a in self.arguments:
            a.rho_in(rhoIn)

    def get_arg(self, arg, pos):
        n = 0
        for i in self.arguments:
            if isinstance(i, Variable):
                arg.append([i, pos*10 + n+1])
            else:
                i.get_arg(arg, pos*10 + n+1)
            n = n+1

