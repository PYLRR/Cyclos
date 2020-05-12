# -*- coding: utf-8 -*-
from src.protocole.protocolError import ProtocolError
from src.protocole.Term import Term


class Type(Term):
    """class used to describe atomic types (noncea, nonceb etc...)"""

    # creates a type with a given name and two booleans representing the fact they are honest and public (or not)
    def __init__(self, name, honest, public):
        Term.__init__(self)
        # boolean that is true if the type is honest
        self.honest = honest
        # boolean that is true if the type is public
        self.public = public
        # string representing this type (ex : noncea)
        self.name = name

    # two types are the same if they have the same name, honesty and privacy
    def __eq__(self, obj):
        return isinstance(obj,
                          Type) and obj.name == self.name and obj.honest == self.honest and obj.public == self.public

    # true if the given type has the same name or if the given string is the name
    def sameName(self, obj):
        return (isinstance(obj, Type) and obj.name == self.name) or (isinstance(obj, str) and obj == self.name)

    # returns a hash of the type, the only utility of that is to manage a dictionary with type as keys
    def __hash__(self):
        return hash((self.name, self.honest, self.public))

    # returns the name of the type, its privacy and then its honesty in a string
    def __str__(self):
        return self.name + " (" + ("not public", "public")[self.public] + "," + ("dishonest", "honest")[self.honest] + ")"

    def rho_out(self, rhoOut, pos, reached_key, sym, term):
        if sym:
            rhoOut.append([[self, pos], [reached_key, 0]])
        else:
            rhoOut.append([[self, pos], [0, reached_key]])

    def rho_in(self, rhoIn):
        if not self.honest:
            rhoIn.append(self)

    def get_arg(self, arg, pos):
        arg.append([self, pos])

    def isReachableOut(self):
        return not self.honest

    def isReachableIn(self):
        return not self.honest

    # true if the terms have the same name
    def equals(self, term):
        res = False
        if self.name == term.name:
            res = True
        return res

    # true if the type is public
    def isPublic(self):
        return self.public

    def check_inclusion(self, key):
        if self == 0 or key == 0:
            return True
        return self.equals(key)

    # Currently unused. Checks types are comparable and adds them to the list of elements which will be later compared
    def isTypeCompliant(self, type, list, isConcat):
        if self == type or not isConcat:
            list[0].append(self)
            list[1].append(type)
        return True
