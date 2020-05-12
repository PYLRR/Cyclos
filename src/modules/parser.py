# -*- coding: utf-8 -*-

import os
from lark import Lark, Token
from src.protocole.Type import Type
from src.protocole.Transaction import Transaction
from src.protocole.Action import Action
from src.protocole.Primitive import Primitive
from src.protocole.primitive.primitiveFactory import getPrimitive
from src.protocole.EGreekCharacters import EGreekCharacters
from src.protocole.Protocol import Protocol
from src.protocole.Variable import Variable
from src.protocole.protocolError import ProtocolError

mapVarType = {}


# takes a file path string as input and returns a protocol corresponding to it
def parseFromFile(file):
    f = open(file, "r")
    string = f.read()
    f.close()
    res = parse(string)
    res.name = os.path.splitext(file)[0]
    return res


# takes a string as input, parses it using a lark grammar, explores the tree and builds a protocol with it.
# then, the protocol is returned
def parse(text):
    grammar = """
    start : ((transaction | public | private |  unknown) SINGLE_NEWLINE+)*
    unknown: /.+/
    
    MONOLINECOMMENT: SINGLE_NEWLINE* /\/\/.*/
            | SINGLE_NEWLINE* /%.*/
    MULTILINECOMMENT: SINGLE_NEWLINE* /\/\*(\*+[^\/\*]|[^*])*\*\//
    
    %ignore MONOLINECOMMENT
    %ignore MULTILINECOMMENT
    
    public: SINGLE_NEWLINE* "public:" (SINGLE_NEWLINE* vardeclaration)*
    private: SINGLE_NEWLINE* "private:" (SINGLE_NEWLINE* vardeclaration)*
    
    vardeclaration: SPACE* var SPACE* ":" SPACE* type SPACE*
    var: NAME_WITHOUT_SPACE
    type: NAME_WITHOUT_SPACE
    
    transaction: SINGLE_NEWLINE* (SINGLE_NEWLINE action)+ SINGLE_NEWLINE*
    
    action: NAMEACTION SPACE* "(" SPACE* channel SPACE* "," SPACE* term SPACE* ")" SPACE*
    NAMEACTION: "in" | "out"
    channel: INT
    
    term: primitive SPACE* "(" SPACE* term SPACE* ("," SPACE* term SPACE*)* ")" SPACE*
            | concat
            | typevardeclaration
            | var
    concat: "<" SPACE* term SPACE* ("," SPACE* term SPACE*)* SPACE* ">" SPACE*
    typevardeclaration : var SPACE* ":" SPACE* constructedtype
    constructedtype: primitive SPACE* "(" SPACE* constructedtype SPACE* ("," SPACE* constructedtype SPACE*)* ")" SPACE*
            | typeconcat
            | type
    typeconcat: "<" SPACE* constructedtype SPACE* ("," SPACE* constructedtype SPACE*)* SPACE* ">" SPACE*
    primitive: NAME_WITHOUT_SPACE
    
    %import common.CNAME -> NAME_WITHOUT_SPACE
    NAME: (SPACE* NAME_WITHOUT_SPACE SPACE*)+
    %import common.WS_INLINE -> SPACE
    %import common.LF -> LF
    %import common.CR -> CR
    SINGLE_NEWLINE: LF|CR
    %import common.INT -> INT
    """  # TODO Si on trouve ajouter le symbole EOF pour éviter de devoir aller à la ligne à la fin du fichier pour qu'il soit reconnu
    parser = Lark(grammar, propagate_positions=True, debug=True)  # , ambiguity='explicit')
    tree = parser.parse(text)
    protocol = Protocol()
    protocol.reset()
    try:
        exploreTree(tree, protocol)
        notpublictype = []
        # For types of constant private, if they are found in protocol,
        # we say that the type of those variables is not public.
        # The others types are publics (by default).
        for var in protocol.listVar:
            if not var.onTheFly and not var.public and var.foundInProtocol:
                notpublictype.append(var.type)
        for type in notpublictype:
            listVars = []
            for var in protocol.listVar:
                if isinstance(var.type, Type):
                    if var.type.sameName(type):
                        listVars.append(var)
            for var in listVars:
                var.type.public = False
    finally:
        mapVarType.clear()
    return protocol


# function that defines the term as parent for each of its children (i.e. arguments for a primitive)
def updateParent(term):
    if isinstance(term, Primitive):
        for children in term.arguments:
            children.parent = term
            updateParent(children)


# function used to explore the derivation tree : for each node, it creates variables or primitives and recursivly
# call itself for each children. Each created element is added to the given protocol
def exploreTree(tree, protocol):
    # eliminate blank lines and other weird nodes
    if not (hasattr(tree, "data")): return
    data = tree.data

    # beginning of protocol
    if data == "start":
        for c in tree.children:
            exploreTree(c, protocol)
    # variables declarations bloc
    elif data == "public" or data == "private":
        for vardeclaration in tree.children:
            # skips "weirds" elements of the tree like blanks or newlines
            if not hasattr(vardeclaration, "data") or vardeclaration.data != "vardeclaration":
                continue
            vardeclarationchildren = removeTokenSpace(vardeclaration)
            # gets the variable name
            new_var = vardeclarationchildren[0].children[0]
            # error if variable name already exists
            if new_var in mapVarType:
                raise ProtocolError("Variable " + vardeclarationchildren[0].children[0] + " in line " + str(
                    vardeclaration.meta.line) + " already defined before : the variable names must be unique")
            # For the private constants, the type are honest. The type is put at public when it's instantiate.
            new_type = Type(vardeclarationchildren[1].children[0], data == "private", True)
            # construct variable with given type
            rightTypeDeclared = protocol.getTypeInlist(new_type)
            # new type encountered
            if rightTypeDeclared is None:
                protocol.listTypes.append(new_type)
                nvar = Variable(new_var, False, new_type, data == "public")
                protocol.listVar.append(nvar)
                mapVarType[new_var] = new_type
            # type already exists somewhere, we have to use it
            else:
                mapVarType[new_var] = rightTypeDeclared
                # constants are divided in public and private.
                nvar2 = Variable(new_var, False, new_type, data == "public")
                protocol.listVar.append(nvar2)
                # if rightTypeDeclared.public != new_type.public:
                #    raise ProtocolError("Variable " + new_var + " in line " + str(
                #        vardeclaration.meta.line) + " already defined with another privacy")
                # if the var is declared in public bloc, the variable cannot be honest
                if rightTypeDeclared.honest and data == "public":
                    rightTypeDeclared.honest = False

    # transaction
    elif data == "transaction":
        new_trans = Transaction("", [])
        protocol.listTransactions.append(new_trans)
        for i in range(0, len(tree.children)):
            c = tree.children[i]
            res = exploreTree(c, protocol)
            if res is not None:
                new_trans.actions.append(res)

    # action : we should only be there if a transaction has been found previously
    elif data == "action":
        length = len(protocol.listTransactions) - 1
        div = length / 24
        modulo = length % 24
        # if length < 24:
        #    name = EGreekCharacters(modulo).__str__
        # else:
        #    name = EGreekCharacters(modulo).__str__ + str(div)
        # name += str(len(protocol.listTransactions[len(protocol.listTransactions) - 1].actions)) \
        #        + tree.children[0].children[0]
        type = tree.children[0]
        actionchildren = removeTokenSpace(tree)
        new_action = Action(type == "in",
                            int(actionchildren[0].children[0].value),
                            EGreekCharacters(modulo),
                            str(len(protocol.listTransactions[len(protocol.listTransactions) - 1].actions)),
                            exploreTree(actionchildren[1], protocol))
        updateParent(new_action.rootTerm)
        return new_action

    # term : we should only be there if an action has been found previously
    elif data == "term":
        # primitive (except concat)
        if tree.children[0].data == "primitive":
            arguments = []
            # remove space
            primitivechildren = removeTokenSpace(tree)
            # let's explore arguments
            for i in range(1, len(primitivechildren)):
                arg = exploreTree(primitivechildren[i], protocol)
                if isinstance(arg, str):
                    # variable
                    arg = mapVarType[arg]
                arguments.append(arg)
            try:
                prim = getPrimitive(primitivechildren[0].children[0].__str__(), arguments)
            except ProtocolError as err:
                raise ProtocolError(str(err.args[0]) + " at line " + str(tree.meta.line))
            return prim

        # special case of concat which is not written concat(var1,var2) but <var1,var2>
        elif tree.children[0].data == "concat":
            # primitive concat
            arguments = []
            # remove space
            concatchildren = removeTokenSpace(tree.children[0])
            for i in range(0, len(concatchildren)):
                arg = exploreTree(concatchildren[i], protocol)

                if isinstance(arg, str):
                    # variable
                    arg = mapVarType[arg]

                arguments.append(arg)
            try:
                prim = getPrimitive("concat", arguments)
            except ProtocolError as err:
                raise ProtocolError(str(err.args[0]) + " at line " + str(tree.meta.line))
            return prim

        # vardeclaration : on the fly declarations
        elif tree.children[0].data == "typevardeclaration":
            vardeclaration = tree.children[0]
            vardeclarationchildren = removeTokenSpace(vardeclaration)
            # variable declared on the flight
            new_var = vardeclarationchildren[0].children[0]
            rightTypeDeclared = exploreTree(vardeclarationchildren[1], protocol)
            # type of variables declared on the flight are constants and cannot be honest
            if isinstance(rightTypeDeclared, Type):
                rightTypeDeclared.honest = False
            var = Variable(new_var, True, rightTypeDeclared, True)
            var.foundInProtocol = True
            protocol.listVar.append(var)
            return var
        # variable
        else:
            try:
                var = protocol.getVarInlist(tree.children[0].children[0])
                var.foundInProtocol = True
                return var
            except ProtocolError:
                raise ProtocolError(
                    "Variable undeclared at line " + str(tree.meta.line) + " : " + tree.children[0].children[0])
    # constructed type
    elif data == "constructedtype":
        # primitive (except concat)
        if tree.children[0].data == "primitive":
            arguments = []
            # remove space
            primitivechildren = removeTokenSpace(tree)
            # let's explore arguments
            for i in range(1, len(primitivechildren)):
                arg = exploreTree(primitivechildren[i], protocol)
                arguments.append(arg)
            try:
                prim = getPrimitive(primitivechildren[0].children[0].__str__(), arguments, True)
            except ProtocolError as err:
                raise ProtocolError(str(err.args[0]) + " at line " + str(tree.meta.line))
            return prim

        # special case of concat which is not written concat(var1,var2) but <var1,var2>
        elif tree.children[0].data == "typeconcat":
            # primitive concat
            arguments = []
            # remove space
            concatchildren = removeTokenSpace(tree.children[0])
            for i in range(0, len(concatchildren)):
                arg = exploreTree(concatchildren[i], protocol)
                arguments.append(arg)
            try:
                prim = getPrimitive("concat", arguments, True)
            except ProtocolError as err:
                raise ProtocolError(str(err.args[0]) + " at line " + str(tree.meta.line))
            return prim

        # type declared
        elif tree.children[0].data == "type":
            typechildren = tree.children[0]
            # temporary attributes for Type element
            type = Type(typechildren.children[0], False, True)
            # rightTypeDeclared represents the already defined type that this type has
            rightTypeDeclared = protocol.getTypeInlist(type)
            if rightTypeDeclared is None:  # type currently doesn't exist
                protocol.listTypes.append(type)
                rightTypeDeclared = type
            return rightTypeDeclared
    # unrecognized item, probably an "unknown" non-terminal for Lark
    else:
        print(tree.data)
        raise ProtocolError("Unknown expression at line " + str(tree.meta.line) + " : " + tree.children[0].__str__())


# returns the list of var's children without "Token" elements
def removeTokenSpace(var):
    children = []
    for elem in var.children:
        if not isinstance(elem, Token):
            children.append(elem)
    return children

# executable function used to manually test the parser
if __name__ == '__main__':
    protocol = parseFromFile(
        "../tests/parser/ds-sign.txt")  # "../tests/parser/protocoleDenningSacco" "../tests/parser/ns-sc.txt") #
    protocol.testTypeCompliance()

    print("\n\nVARIABLES FOUND :")
    print("public:")
    for var in protocol.listVar:
        if not var.isDeclaredOnTheFly() and var.public:
            print(var.toStringOnVarDeclaration())
    print("\n\nprivate:")
    for var in protocol.listVar:
        if not var.isDeclaredOnTheFly() and not var.public:
            print(var.toStringOnVarDeclaration())

    print("\n\nTRANSACTIONS FOUND :")
    for trans in protocol.listTransactions:
        print(trans.label)
        for action in trans.actions:
            print("-" + action.__str__())

    print("\n\nTYPES FOUND :")
    for type in protocol.listTypes:
        print(type)
