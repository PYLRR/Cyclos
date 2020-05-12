# -*- coding: utf-8 -*-
from src.protocole.Type import Type
from src.protocole.Term import Term


class Variable(Term):
    """class used to describe variables (a : noncea, b : nonceb etc...)"""

    # creates a variable with a given name, type and a int equal to 1 if it has been declared on the fly
    def __init__(self, name, declaredOnTheFly, type, public=True):
        # name of the variable
        self.name = name
        # boolean that is true if the variable is declared on the flight
        self.onTheFly = declaredOnTheFly
        # type of the variable
        self.type = type
        # already printed with type
        self.alreadyPrintedType = False
        #  boolean that is true if the constant variable is public, false if private
        self.public = public
        #  boolean that is true if the constant variable is found in protocol, false otherwise
        self.foundInProtocol = False

    # updates the declaredOnTheFly to 1
    def isDeclaredOnTheFly(self):
        return self.onTheFly == 1

    # returns a string containing the variable name, : and its type
    def toStringOnVarDeclaration(self):
        t = self.type.__str__()
        return self.name + ":" + t

    # returns a string containing the variable name, : and its type or just its name
    def __str__(self):
        if self.onTheFly and not (self.alreadyPrintedType):
            self.alreadyPrintedType = True  # self.onTheFly = not(self.onTheFly) #pour l'affichage
            res = self.name + ":" + self.type.__str__()
        else:
            res = self.name
        return res

    # two types are the same if they have the same name, type and onTheFly value
    def __eq__(self, obj):
        return isinstance(obj,
                          Variable) and obj.name == self.name and obj.onTheFly == self.onTheFly and obj.type == self.type

    # returns true if obj has the same name as self or if it is the self.name in case obj is a string
    def sameName(self, obj):
        return (isinstance(obj, Variable) and obj.name == self.name) or (isinstance(obj, str) and obj == self.name)

    def rho_out(self, rhoOut, pos, reached_key, sym, term):
        if term:
            if self.onTheFly:
                term = Type(self.name, False, True)
                term.rho_out(rhoOut, pos, reached_key, sym, term)
            else:
                self.type.rho_out(rhoOut, pos, reached_key, sym, term)
        else:
            self.type.rho_out(rhoOut, pos, reached_key, sym, term)

    def rho_in(self, rhoIn):
        self.type.rho_in(rhoIn)

    def get_arg(self, arg, pos):
        self.type.get_arg(arg, pos)

    def isReachableOut(self):
        return self.type.isReachableOut()

    def isReachableIn(self):
        return self.type.isReachableIn()

    # returns true if var is a variable with the same type
    def equals(self, var):
        return (isinstance(var, Variable) and self.type == var.type) or var.equals(self.type)

    # returns true if self is public
    def isPublic(self):
        return self.type.isPublic()

    def check_inclusion(self, key):
        return self.type.check_inclusion(key)

    # Currently unused. Checks if vars are comparable and adds them to the list of elements that will later compared
    def isTypeCompliant(self, var, list, isConcat):
        if isinstance(self, Variable) and isinstance(var, Variable):
            if self == var or self.onTheFly or var.onTheFly:
                if not isinstance(self.type, Type) and not isinstance(var.type, Type):  # it's a constructed type
                    listT = [[], []]
                    if not self.type.isTypeCompliant(var.type, listT, isConcat):
                        return False
                if not isConcat:
                    list[0].append(self)
                    list[1].append(var)
                    return True
        return False
