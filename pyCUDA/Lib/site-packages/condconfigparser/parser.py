# -*- coding: utf-8 -*-

# parser.py --- Parser module of CondConfigParser
#
# Copyright (c) 2014, Florent Rougon
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of the CondConfigParser Project.

"""Parser module of CondConfigParser.

This module defines a :class:`Node` class, one subclass for every node
type that can occur in the abstract syntax tree, and a :class:`Parser`
class which implements the configuration file parsing using the output
of the lexer (:class:`condconfigparser.lexer.Lexer`).

"""


import re
import collections
import textwrap                 # minor use, could be easily replaced

from .exceptions import ParseError, UndefinedVariable, InTestTypeError
from .lexer import TokenType


class Node:
    """Node class for the abstract syntax tree.

    This class defines all the usual :class:`list` methods; they act on
    the list referenced to by the :attr:`children` attribute.

    Data belonging to the node that is not in the form of a
    :class:`Node` instance (or instance of a subclass) must be stored in
    other attributes than :attr:`children`.

    This class implements :meth:`object.__eq__` and
    :meth:`object.__ne__` for equality testing. This allows one to
    compare two abstract syntax trees by using ``==`` or ``!=`` with the
    two root nodes.

    """
    def __init__(self, children=None):
        #: List of children nodes (:class:`Node` instances)
        self.children = [] if children is None else children

    def __eq__(self, other):
        return type(self) == type(other) and \
            self.children == other.children

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getattr__(self, name):
        if name in ("append", "extend"):
            return getattr(self.children, name)

    def __len__(self):
        return self.children.__len__()

    def __getitem__(self, key):
        return self.children.__getitem__(key)

    def __delitem__(self, key):
        return self.children.__delitem__(key)

    def __setitem__(self, key, value):
        return self.children.__setitem__(key, value)

    def __iter__(self):
        return self.children.__iter__()

    def __reversed__(self):
        return self.children.__reversed__()

    def __contains__(self, item):
        return self.children.__contains__(item)

    def __str__(self):
        return "<{}>".format(type(self).__name__)

    def __repr__(self):
        return "{0}.{1}({2!r})".format(__name__, type(self).__name__,
                                       self.children)

    def __format__(self, format_spec):
        """Support for :samp:`format({node}, "tree")` and \
:samp:`"{:tree}".format({node})`."""
        if not format_spec:
            return str(self)
        else:
            assert format_spec == "tree", format_spec
            if self.children:
                indent = 2
                childLines = '\n'.join(
                    [ textwrap.indent("{:tree}".format(child), " "*indent)
                      for child in self.children ])

                return "{}\n{}".format(self, childLines)
            else:
                return str(self)

    @classmethod
    def simplify(cls, node, parent, childNum):
        """Recursively replace useless :class:`AndTestNode` and \
:class:`OrTestNode` instances.

        Every :class:`AndTestNode` or :class:`OrTestNode` that only has
        one child is replaced with this only child. This process is
        recursively done on all children of *node*.

        Return the possibly-new root node of the tree.

        """
        res = node
        if isinstance(node, (AndTestNode, OrTestNode)) and \
                len(node.children) == 1:
            if parent is None:
                res = cls.simplify(node.children[0], None, None)
            else:
                parent.children[childNum] = node.children[0]
                cls.simplify(node.children[0], parent, childNum)
        else:
            for i, child in enumerate(node.children):
                cls.simplify(child, node, i)

        return res

    def undefVariables(self, varNames):
        """Return the set of undefined variables for the tree rooted at *self*.

        This method recursively explores the subtree rooted at *self*.
        If any node encountered refers to a variable whose name is not
        in *varNames*, it remembers that variable as undefined.

        The return value is a :class:`frozenset` containing a
        :class:`condconfigparser.lexer.VariableToken` instance for every
        instance of an undefined variable in the tree rooted at *self*.

        """
        return frozenset().union(
            *[ child.undefVariables(varNames) for child in self.children ])


class RootNode(Node):
    """Node representing the root of the abstract syntax tree for a \
config file/stream.

    Corresponds to the :token:`root` grammar production.

    """
    def __init__(self, assignments, config):
        Node.__init__(self, [assignments, config])

    def __repr__(self):
        return "{}.{}({!r}, {!r})".format(__name__, type(self).__name__,
                                          self.assignments, self.config)

    # Convenience properties
    @property
    def assignments(self):
        """:class:`VarAssignmentsNode` instance."""
        return self.children[0]

    @assignments.setter
    def assignments(self, value):
        self.children[0] = value

    @property
    def config(self):
        """:class:`ConfigNode` instance."""
        return self.children[1]

    @config.setter
    def config(self, value):
        self.children[1] = value


class VarAssignmentsNode(Node):
    """Node representing zero or more variable assignments.

    Corresponds to the :token:`varAssignments` grammar production.
    """


class AssignmentNode(Node):
    """Node representing a variable assignment.

    Corresponds to the :token:`variableAssignment` grammar production.

    """
    def __init__(self, lhs, rhs):
        Node.__init__(self, [lhs, rhs])

    def __repr__(self):
        return "{}.{}({!r}, {!r})".format(__name__, type(self).__name__,
                                          self.lhs, self.rhs)

    # Convenience properties to access the left hand side, variable name and
    # right hand side of the assignment
    @property
    def lhs(self):
        """:class:`VariableNode` instance for the assigned-to variable."""
        return self.children[0]

    @lhs.setter
    def lhs(self, value):
        self.children[0] = value

    @property
    def name(self):
        """Name of the assigned-to variable."""
        return self.children[0].name

    @property
    def rhs(self):
        """:class:`Node` instance representing the expression that defines \
the variable."""
        return self.children[1]

    @rhs.setter
    def rhs(self, value):
        self.children[1] = value


def _truncateConfigLines(cfgLines):
    l = []
    for line in cfgLines:
        # Truncate the config lines since they will all be printed on a
        # single line...
        if len(line) >= 15:
            # 10 + len(" ...") = 15 - 1
            l.append("{} ...".format(line[:10]))
        else:
            l.append(line)

    return l


class ConfigNode(Node):
    """Node representing the default, unconditional section of the config \
file as well as the list of its conditional sections.

    Corresponds to the :token:`config` grammar production.

    """
    def __init__(self, defaultConfigLines=None, sections=None):
        defaultConfigLines = \
            defaultConfigLines if defaultConfigLines is not None else []
        sections = sections if sections is not None else []

        Node.__init__(self, sections)
        #: List of unconditional configuration lines (:class:`str` instances)
        self.defaultConfigLines = defaultConfigLines

    def __eq__(self, other):
        return type(self) == type(other) and \
            self.children == other.children and \
            self.defaultConfigLines == other.defaultConfigLines

    def __repr__(self):
        return "{}.{}({!r}, {!r})".format(__name__, type(self).__name__,
                                          self.defaultConfigLines,
                                          self.sections)

    def __str__(self):
        return "<{} {!r}>".format(type(self).__name__,
            _truncateConfigLines(self.defaultConfigLines))

    # Convenience property
    @property
    def sections(self):
        """List of :class:`SectionNode` instances."""
        return self.children

    @sections.setter
    def sections(self, value):
        self.children = value


class SectionNode(Node):
    """Node representing a conditional section of the config file.

    Corresponds to the :token:`section` grammar production.

    """
    def __init__(self, startToken, predicate, rawConfigLines):
        Node.__init__(self, [predicate])
        for n in ("startToken", "rawConfigLines"):
            setattr(self, n, locals()[n])

    def __eq__(self, other):
        return type(self) == type(other) and \
            self.children == other.children and \
            self.startToken == other.startToken and \
            self.rawConfigLines == other.rawConfigLines

    def __repr__(self):
        return "{}.{}({!r}, {!r}, {!r})".format(
            __name__, type(self).__name__,
            self.startToken, self.predicate, self.rawConfigLines)

    def __str__(self):
        return "<{} {!r}>".format(type(self).__name__,
            _truncateConfigLines(self.rawConfigLines))

    # Convenience property
    @property
    def predicate(self):
        """Abstract syntax tree representing the predicate.

        This may be an :class:`OrTestNode`, an :class:`AndTestNode`, a
        :class:`ListLiteralNode`, etc. In any case, it is an instance of
        a :class:`Node` subclass.

        """
        return self.children[0]

    @predicate.setter
    def predicate(self, value):
        self.children[0] = value


class OrTestNode(Node):
    """Node representing a short-circuit, logical ``or`` test.

    The semantics are the same as in Python, including the result of the
    evaluation. cf.

      https://docs.python.org/3/reference/expressions.html#boolean-operations

    Corresponds to the :token:`orTest` grammar production.

    """
    def eval(self, context):
        """Return the node value, after recursive evaluation of its children."""
        for child in self.children:
            res = child.eval(context)
            if res:
                break

        return res


class AndTestNode(Node):
    """Node representing a short-circuit, logical ``and`` test.

    The semantics are the same as in Python, including the result of the
    evaluation. cf.

      https://docs.python.org/3/reference/expressions.html#boolean-operations

    Corresponds to the :token:`andTest` grammar production.

    """
    def eval(self, context):
        """Return the node value, after recursive evaluation of its children."""
        for child in self.children:
            res = child.eval(context)
            if not res:
                break

        return res


class NotTestNode(Node):
    """Node representing a logical ``not`` test.

    Related to the :token:`notTest` grammar production.

    """
    def __init__(self, child):
        Node.__init__(self, [child])

    def __repr__(self):
        return "{}.{}({!r})".format(__name__, type(self).__name__, self.child)

    def eval(self, context):
        """Return the node value, after recursive evaluation of its child."""
        return not self.child.eval(context)

    # Convenience property
    @property
    def child(self):
        """Child node of the :class:`NotTestNode` instance.

        It is an instance of a :class:`Node` subclass.

        """
        return self.children[0]

    @child.setter
    def child(self, value):
        self.children[0] = value


class BinOpNodeBase(Node):
    """Base class for nodes having ``lOp`` and ``rOp`` properties."""

    def __init__(self, opToken, lOp, rOp):
        """Initialize a :class:`BinOpNodeBase` instance.

        *opToken* is the binary operator token instance (lexeme). It may
        be used to obtain the start/end line and column numbers of the
        binary operator, for instance.

        *lOp* and *rOp* are the left and right operands and must be
        instances of a subclass of :class:`Node`.

        """
        Node.__init__(self, [lOp, rOp])
        self.opToken = opToken

    def __repr__(self):
        return "{}.{}({!r}, {!r}, {!r})".format(
            __name__, type(self).__name__, self.opToken, self.lOp, self.rOp)

    # Convenience properties to access the left and right operands of
    # the binary operator
    @property
    def lOp(self):
        """Left operand of the binary operator.

        It is an instance of a subclass of :class:`Node`.

        """
        return self.children[0]

    @lOp.setter
    def lOp(self, value):
        self.children[0] = value

    @property
    def rOp(self):
        """Right operand of the binary operator.

        It is an instance of a subclass of :class:`Node`.

        """
        return self.children[1]

    @rOp.setter
    def rOp(self, value):
        self.children[1] = value


class EqualsTestNode(BinOpNodeBase):
    """Node representing an ``==`` test.

    Corresponds to the :token:`equalsTest` grammar production.

    """
    def eval(self, context):
        """Return the node value, after recursive evaluation of its children."""
        return self.lOp.eval(context) == self.rOp.eval(context)


class NotEqualsTestNode(BinOpNodeBase):
    """Node representing an ``!=`` test.

    Corresponds to the :token:`notEqualsTest` grammar production.

    """
    def eval(self, context):
        """Return the node value, after recursive evaluation of its children."""
        return self.lOp.eval(context) != self.rOp.eval(context)


class InTestNode(BinOpNodeBase):
    """Node representing an ``in`` test.

    Corresponds to the :token:`inTest` grammar production.

    """
    def eval(self, context):
        """Return the node value, after recursive evaluation of its children."""
        try:
            res = self.lOp.eval(context) in self.rOp.eval(context)
        except TypeError as e:
            raise InTestTypeError(self.opToken, e) from e

        return res


class VariableNode(Node):
    """Node representing a variable reference.

    Corresponds to the :token:`variable` grammar symbol.

    """
    def __init__(self, variableToken):
        Node.__init__(self)
        #: :class:`condconfigparser.lexer.VariableToken` instance
        self.token = variableToken
        #: Variable name (:class:`str`)
        self.name = variableToken.string

    def __eq__(self, other):
        return type(self) == type(other) and \
            self.token == other.token

    def __repr__(self):
        return "{}.{}({!r})".format(__name__, type(self).__name__, self.token)

    def __str__(self):
        return "<{} {!r}>".format(type(self).__name__, self.name)

    def eval(self, context):
        """Return the node value, according to *context*.

        The node value is the value of the variable whose name is given
        by :attr:`name`, according to *context*.

        """
        try:
            return context[self.name]
        except KeyError as e:
            raise UndefinedVariable(self.name) from e

    def undefVariables(self, varNames):
        """Return the set of undefined variables.

        The set of undefined variables is determined under the
        assumption that every variable with a name in *varNames* is
        defined.

        """
        if self.name in varNames:
            return frozenset()
        else:
            return frozenset((self.token,))


class StringLiteralNode(Node):
    """Node representing a string literal.

    Corresponds to the :token:`stringLiteral` grammar symbol.

    """
    def __init__(self, value):
        Node.__init__(self)
        #: The actual string represented by the node (:class:`str` instance)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and \
            self.value == other.value

    def __repr__(self):
        return "{}.{}({!r})".format(__name__, type(self).__name__, self.value)

    def __str__(self):
        return "<{} {!r}>".format(type(self).__name__, self.value)

    def eval(self, context):
        """Return the node value, which is the string literal represented by \
the node."""
        return self.value


class BoolLiteralNode(Node):
    """Node representing a boolean literal (i.e., ``True`` or ``False``).

    Corresponds to the :token:`boolLiteral` grammar symbol.

    """
    def __init__(self, value):
        Node.__init__(self)
        #: The actual boolean represented by the node (:class:`bool` instance)
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and \
            self.value == other.value

    def __repr__(self):
        return "{}.{}({!r})".format(__name__, type(self).__name__, self.value)

    def __str__(self):
        return "<{} {!r}>".format(type(self).__name__, self.value)

    def eval(self, context):
        """Return the node value, which is the boolean literal represented by \
the node."""
        return self.value


class ListLiteralNode(Node):
    """Node representing a list literal.

    The elements of the list are represented by the :class:`Node`
    instances forming the list referred to by the :attr:`children`
    attribute (same order, of course).

    Corresponds to the :token:`listLiteral` grammar symbol.

    """
    def __init__(self, items):
        Node.__init__(self, items)

    def eval(self, context):
        """Return the node value, which is the list literal represented by \
the node."""
        return [ item.eval(context) for item in self.children ]


class Parser:
    """Parser class of CondConfigParser.

    This class implements a recursive descent parser that performs
    look-ahead in order to avoid any need for backtracking. The
    algorithm is typical of a LL(1) parser that does not use parse
    tables.

    For more information, you may refer to:

      http://dickgrune.com/Books/PTAPG_1st_Edition/

    """
    def __init__(self, lexer):
        #: :class:`condconfigparser.lexer.Lexer` instance
        self.lexer = lexer
        #: Queue holding the tokens generated by the :attr:`lexer`
        self.queue = collections.deque()
        #: Token generator from :attr:`lexer`
        self.tokenGenerator = lexer.tokenGenerator()
        #: Last token popped from :attr:`queue`, i.e., consumed by the parser
        self.lastToken = None

    def enqueue(self, num):
        """Pull *num* tokens from :attr:`tokenGenerator`, pushing them into \
:attr:`queue`."""
        while len(self.queue) < num:
            try:
                self.queue.append(next(self.tokenGenerator))
            except StopIteration:
                break

        return len(self.queue)

    def peekAt(self, index):
        """Look at an element of :attr:`queue` without consuming it.

        If *index* is 0, look at the first unprocessed token in
        :attr:`queue`. If *index* is 1, look at the next unprocessed
        token, etc..

        Return the looked-at token, or ``None`` if it does not exist.

        """
        queueLen = self.enqueue(index+1)
        if index < queueLen:
            return self.queue[index]
        else:
            return None

    def peekSeveral(self, num):
        """Return the topmost *num* tokens without consuming them.

        Return a list of length at most *num*. If EOF is reached before
        enough tokens can be read, the returned list will have less than
        *num* elements.

        If the returned list *l* has at least one element,
        :samp:`{l}[0]` is the first unprocessed token; if it has at
        least two elements, :samp:`{l}[1]` is the second unprocessed
        token, etc.

        """
        queueLen = self.enqueue(num)
        return list(self.queue)[:num]

    def readToken(self):
        """Read a token from :attr:`queue`.

        If there are no tokens in :attr:`queue`, return ``None``.
        Otherwise, consume one token from :attr:`queue`, save it in
        :attr:`lastToken` for later reference and return it.

        """
        if not self.enqueue(1):
            return None         # No more token (EOF)
        else:
            self.lastToken = self.queue.popleft()
            return self.lastToken

    def match1(self, tokenType):
        """Match one token of type *tokenType*.

        Read a token from :attr:`queue`. If none is available or if the
        token is not of type *tokenType*, raise :exc:`ParseError`.
        Otherwise, return the token that was read.

        """
        t = self.readToken()
        if t is None:           # EOF
            raise ParseError((self.lexer.line, self.lexer.col),
                             "EOF reached while trying to read a <{}> token"
                             .format(tokenType.name))
        elif t.type != tokenType:
            raise ParseError(self.lastToken.pos(),
                             "expected a <{}> token, but found a <{}> instead"
                             .format(tokenType.name, t.type.name))

        return t

    def matchZeroOrMore(self, tokenType):
        """Match zero or more tokens of type *tokenType*.

        Return the list of matched tokens (the match is greedy).

        """
        l = []
        while True:
            t = self.peekAt(0)
            if t is None:
                break           # EOF
            elif t.type == tokenType:
                l.append(self.match1(tokenType))
            else:
                break

        return l

    def matchOneOrMore(self, tokenType):
        """Match one or more tokens of type *tokenType*.

        Return the list of matched tokens (the match is greedy). Raise
        :exc:`ParseError` if the first unprocessed token is not of type
        *tokenType*.

        """
        return [self.match1(tokenType)] + self.matchZeroOrMore(tokenType)

    def root(self):
        """Match a :token:`root` production."""
        t = self.peekAt(0)

        if t is None:                             # EOF
            return RootNode(VarAssignmentsNode(), ConfigNode()) # empty
        elif t.type == TokenType.varAssignmentsStart:
            assignments = self.varAssignments()
        else:
            assignments = VarAssignmentsNode() # empty

        return RootNode(assignments, self.config())

    def varAssignments(self):
        """Match a :token:`varAssignments` production."""
        self.match1(TokenType.varAssignmentsStart)
        a = self.varAssigs()
        self.match1(TokenType.varAssignmentsEnd)
        self.matchOneOrMore(TokenType.newline)

        return a

    def varAssigs(self):
        """Match a :token:`varAssigs` production."""
        self.matchZeroOrMore(TokenType.newline)
        assignments = VarAssignmentsNode()

        while True:
            t = self.peekAt(0)
            if t is None:
                break
            elif t.type == TokenType.variable:
                assignments.append(self.variableAssignment())

                nextToken = self.peekAt(0)
                if nextToken is not None and \
                        nextToken.type != TokenType.varAssignmentsEnd:
                    self.matchOneOrMore(TokenType.newline)
            elif t.type == TokenType.varAssignmentsEnd:
                break
            else:
                raise ParseError(self.lastToken.pos(),
                                 "unexpected token while parsing a "
                                 "<varAssigs>: {}".format(self.lastToken))
        return assignments

    def variableAssignment(self):
        """Match a :token:`variableAssignment` production."""
        variable = VariableNode(self.match1(TokenType.variable))
        self.match1(TokenType.assignOp)

        return AssignmentNode(variable, self.orTest())

    def config(self):
        """Match a :token:`config` production."""
        defaultConfigLines = [ t.string for t in
                               self.matchZeroOrMore(TokenType.rawConfigLine) ]
        sections = []

        while True:
            t = self.peekAt(0)
            if t is None:
                break
            else:
                sections.append(self.section())

        return ConfigNode(defaultConfigLines, sections)

    def section(self):
        """Match a :token:`section` production."""
        startToken, predicate = self.predicate()
        rawConfigLines = [ t.string for t in
                           self.matchZeroOrMore(TokenType.rawConfigLine) ]
        return SectionNode(startToken, predicate, rawConfigLines)

    def predicate(self):
        """Match a :token:`predicate` production."""
        startToken = self.match1(TokenType.predicateStart)
        ot = self.orTest()
        self.match1(TokenType.predicateEnd)
        self.matchOneOrMore(TokenType.newline)
        return (startToken, ot)

    def orTest(self):
        """Match an :token:`orTest` production."""
        l = [self.andTest()]
        while True:
            t = self.peekAt(0)
            if t is None or t.type != TokenType.orOp:
                break
            else:
                self.match1(TokenType.orOp)
                l.append(self.andTest())

        return OrTestNode(l)

    def andTest(self):
        """Match an :token:`andTest` production."""
        l = [self.notTest()]
        while True:
            t = self.peekAt(0)
            if t is None or t.type != TokenType.andOp:
                break
            else:
                self.match1(TokenType.andOp)
                l.append(self.notTest())

        return AndTestNode(l)

    def notTest(self):
        """Match a :token:`notTest` production."""
        t = self.peekAt(0)
        if t is None:
            raise ParseError((self.lexer.line, self.lexer.col),
                             "EOF reached while trying to read a <notTest>")
        elif t.type == TokenType.notOp:
            self.match1(TokenType.notOp)
            node = NotTestNode(self.notTest())
        else:
            node = self.atomicBool()

        return node

    def atomicBool(self):
        """Match an :token:`atomicBool` production."""
        # All derivations of <atomicBool> start with an <expr>. In order to
        # avoid any backtracking, we have to factor it out: eat an <expr> now
        # and maybe pass it as parameter to equalsTest(), notEqualsTest() or
        # inTest(), depending on the token following the <expr>.
        expr = self.expr()

        t = self.peekAt(0)
        if t is None:
            return expr
        elif t.type == TokenType.equalsOp:
            return self.equalsTest(expr)
        elif t.type == TokenType.notEqualsOp:
            return self.notEqualsTest(expr)
        elif t.type == TokenType.inOp:
            return self.inTest(expr)
        else:
            return expr

    # cf. comments in atomicBool() concerning the lOp parameter
    def equalsTest(self, lOp):
        """Match an :token:`equalsTest` production."""
        opToken = self.match1(TokenType.equalsOp)
        rOp = self.expr()
        return EqualsTestNode(opToken, lOp, rOp)

    # cf. comments in atomicBool() concerning the lOp parameter
    def notEqualsTest(self, lOp):
        """Match a :token:`notEqualsTest` production."""
        opToken = self.match1(TokenType.notEqualsOp)
        rOp = self.expr()
        return NotEqualsTestNode(opToken, lOp, rOp)

    # cf. comments in atomicBool() concerning the lOp parameter
    def inTest(self, lOp):
        """Match an :token:`inTest` production."""
        opToken = self.match1(TokenType.inOp)
        rOp = self.expr()
        return InTestNode(opToken, lOp, rOp)

    def expr(self):
        """Match an :token:`expr` production."""
        t = self.peekAt(0)
        if t is None:
            raise ParseError((self.lexer.line, self.lexer.col),
                             "EOF reached while trying to read an <expr>")
        elif t.type == TokenType.variable:
            node = VariableNode(self.match1(TokenType.variable))
        elif t.type == TokenType.openParen:
            self.match1(TokenType.openParen)
            node = self.orTest()
            self.match1(TokenType.closeParen)
        else:
            node = self.literal()

        return node

    def literal(self):
        """Match a :token:`literal` production."""
        t = self.peekAt(0)
        if t is None:
            raise ParseError((self.lexer.line, self.lexer.col),
                             "EOF reached while trying to read a <literal>")
        elif t.type == TokenType.stringLiteral:
            return StringLiteralNode(
                self.match1(TokenType.stringLiteral).value)
        elif t.type == TokenType.listStart:
            return self.listLiteral()
        else:
            return self.boolLiteral()

    def boolLiteral(self):
        """Match a :token:`boolLiteral` production."""
        t = self.peekAt(0)
        if t is None:
            raise ParseError((self.lexer.line, self.lexer.col),
                             "EOF reached while trying to read a <boolLiteral>")
        elif t.type == TokenType.true:
            self.match1(TokenType.true)
            return BoolLiteralNode(True)
        else:
            self.match1(TokenType.false)
            return BoolLiteralNode(False)

    def listLiteral(self):
        """Match a :token:`listLiteral` production."""
        self.match1(TokenType.listStart)
        items = []
        # Set to False after the first element has been read
        first = True

        while True:
            t = self.peekAt(0)
            if t is None:
                raise ParseError((self.lexer.line, self.lexer.col),
                                 "EOF reached while trying to read a "
                                 "<listLiteral>")
            elif t.type == TokenType.listEnd:
                self.match1(TokenType.listEnd)
                break
            elif first:
                items.append(self.orTest())
                first = False
            else:
                self.match1(TokenType.comma)
                items.append(self.orTest())

        return ListLiteralNode(items)

    def buildTree(self):
        """Parse a complete configuration file.

        Return the root node of the corresponding abstract syntax tree,
        after simplification (cf. :meth:`Node.simplify`).

        """
        rootNode = self.root()
        return Node.simplify(rootNode, None, None)
