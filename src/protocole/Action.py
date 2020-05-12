# -*- coding: utf-8 -*-
from src.protocole.Variable import Variable
from src.protocole.Type import Type
from src.protocole.protocolError import ProtocolError
from src.protocole.EGreekCharacters import EGreekCharacters


class Action:
    """class used to describe actions (like alpha1In,beta2Out...)"""

    # Creates an action with a given type (in/out), channel (1,2...), greek letter, position and root term
    def __init__(self, type, channel, greekCaracter, positionInTransaction, rootterm):
        # boolean which is true if it is "in", false if it is "Out"
        self.type = type
        # integer corresponding to the channel number of the "message"
        self.channel = channel
        # greekCaracter representing the action (ex : alpha)
        self.greekCaracter = greekCaracter
        # position in sequency ex : alpha1In)
        self.positionInTransaction = positionInTransaction
        # term that is the root of a tree representing the whole action
        self.rootTerm = rootterm
        self.label=self.label()

    # prints the action name and the term it contains with its own __str__
    def __str__(self):
        s=""
        g=self.greekCaracter.__str__
        s+=g
        s+=self.positionInTransaction
        if self.type :
            s+="in"
        else :
            s+="out"
        act=self.rootTerm.__str__()
        s+=":" + ("out","in")[self.type] + "(" + str(self.channel) + ","+ act + ")"
        return s

    # returns the name of the action (like alpha1in)
    def label(self):
        s=""
        g=self.greekCaracter.__str__
        s+=g
        s+=self.positionInTransaction
        if self.type :
            s+="in"
        else :
            s+="out"
        return s

    def rho(self):
        if self.type:
            rho = []
            self.rootTerm.rho_in(rho)
        else:
            rho = []
            self.rootTerm.rho_out(rho, 0, 0, True, False)
        return rho

    # returns a list of arguments
    def getArguments(self):
        arg = []
        self.rootTerm.get_arg(arg, 0)
        return arg

    # currently unused. Checks that 2 actions are typecompliant.
    # Compares the action to another, filling 2 lists of subterms (1 for each action) to then compare
    def isTypeCompliant(self, action2):
        print(self.__str__() + "|" + action2.__str__())
        listVars = [[],[]] # This parameter listVars is the list of vars those are unifiable with all terms
        isConcat=False
        if isinstance(self.rootTerm,Variable) and isinstance(action2.rootTerm, Variable):
            if not isinstance(self.rootTerm.type, Type) and not isinstance(action2.rootTerm.type,Type):
                if self.rootTerm.type.constructedtype or action2.rootTerm.type.constructedtype:
                    isConcat=True
        if not self.rootTerm.isTypeCompliant(action2.rootTerm, listVars, isConcat):
            return False
        for i in range(0, len(listVars[0])):
            var0 = listVars[0][i]
            var1 = listVars[1][i]
            type0 = var0.type
            type1 = var1.type
            msgError= "Type-compliance error due to subterm " + str(var0.__str__())\
                      + " of action " + str(self) + " and subterm " + str(var1.__str__())\
                      + " of action " + str(action2.__str__()) + ".\nSubterms " + str(var0.__str__())\
                      + " and " + str(var1.__str__()) + " are unifiable whereas they have different"\
                      + " types: " + str(var0.__str__()) + " has type " + str(type0.__str__())\
                      + " and " + str(var1.__str__()) + " has type "+ str(type1.__str__()) + "."
            if not isinstance(type0, Type) and not isinstance(type1, Type): #it's a constructed type
                listT=[[],[]]
                if not type0.isTypeCompliant(type1, listT, False) :
                    return False
                print(listT)
                for j in range(0, len(listT[0])):
                    if not listT[0][j] == listT[1][j]:
                        print(str(type0.__str__()) + " and " + str(type1.__str__()))
                        raise ProtocolError(msgError)
            else:
                if not type0 == type1: # in listVars if the 2 types are the sames => OK
                                                                # else typecompliance error
                    print(str(type0.__str__()) + " and " + str(type1.__str__()))
                    raise ProtocolError(msgError)
        print("Unifiable !!!")
        return True