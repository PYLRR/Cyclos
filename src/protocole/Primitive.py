# -*- coding: utf-8 -*-
from src.protocole.Variable import Variable
from src.protocole.Type import Type
from src.protocole.Term import Term
from src.protocole.protocolError import ProtocolError

class Primitive(Term):
    """class used to describe cryptographic primitives (aenc, pub, etc...)"""

    # arity of the primitive (i.e. nb of arguments)
    arity = 0

    # Creates a primitive with a given name, a list of arguments and a boolean expressing whether
    # it is constructed or it is a single variable
    def __init__(self, name, arguments=[], constructedtype=False):
        # if arity does not match the number of arguments (arity<0=>there is no fixed arity)
        if len(arguments) != self.arity and self.arity>=0:
            raise ProtocolError("Error : the primitive " + name + " does not match the arity " + str(len(arguments)))
        Term.__init__(self)
        # string representing this primitive (ex : aenc)
        self.name = name
        # list of terms, their amount is the arity of the primitive
        self.arguments = arguments
        # true if it's use to construct a type, false otherwise
        self.constructedtype= constructedtype

    # prints the primitive name and then its arguments with their own __str__
    def __str__(self):
        arguments=""
        for i in range(0, len(self.arguments) - 1):
            arg = self.arguments[i].__str__()
            arguments += arg + ","
        arg = self.arguments[len(self.arguments) - 1].__str__()
        arguments+=arg
        if self.name == "concat":
            res = "<" + arguments + ">"
        else:
            res = self.name + "(" + arguments + ")"
        return res

    def isReachableOut(self):
        return self.arguments[0].isReachableOut()

    def isReachableIn(self):
        return True

    # returns true when term has the same name and arguments as self
    def equals(self, term):
        res = False
        if not type(term) == Variable and not type(term) == Type:
            if (len(self.arguments) == len(term.arguments)) & (self.name == term.name):
                for i in range(len(self.arguments)):
                    res = self.arguments[i].equals(term.arguments[i])
                    if not res:
                        return res
        return res

    # currently unused. Looking for typecompliance, Compares 2 primitives, if they are comparable compares their
    # arguments and returns true except if the arguments are not type compliant
    def isTypeCompliant(self, primitive, list, isConcat):
        if isinstance(self, Primitive) and isinstance(primitive, Primitive):
            if self.name == primitive.name and len(self.arguments) == len(primitive.arguments):
                if self.name == "concat":
                    isConcat = True
                for i in range(0, len(self.arguments)):
                    if not self.arguments[i].isTypeCompliant(primitive.arguments[i], list, isConcat):
                        return False
                return True
            else:
                return False
        else:
            return False

    # returns true if each argument is public
    def isPublic(self):
        res = True
        for i in self.arguments:
            if not i.isPublic():
                res = False
        return res