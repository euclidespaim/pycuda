# -*- coding: utf-8 -*-

# lexer.py --- Lexer module of CondConfigParser
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

"""Lexer module of CondConfigParser.

This module defines a :class:`Token` class, one subclass for every token
type, a :class:`TokenType` :class:`enum.Enum` and a :class:`Lexer`
class.

"""
import re
import collections
import enum

from .exceptions import ParseError


# Taken from the enum documentation
class AutoNumber(enum.Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

@enum.unique
# enum.IntEnum could be more appropriate if one wanted to use actual parse
# tables typical of LL(k) grammars.
class TokenType(AutoNumber):
    """Identifier objects for token types."""
    newline = ()
    varAssignmentsStart = ()
    varAssignmentsEnd = ()
    predicateStart = ()
    predicateEnd = ()
    listStart = ()
    listEnd = ()
    openParen = ()
    closeParen = ()
    orOp = ()
    andOp = ()
    notOp = ()
    equalsOp = ()
    notEqualsOp = ()
    inOp = ()
    assignOp = ()
    comma = ()
    true = ()
    false = ()
    stringLiteral = ()
    variable = ()
    rawConfigLine = ()

class Token:
    """Class representing a token instance (lexeme).

    :attr:`Token.startline` and :attr:`Token.startcol` are 1-based
    line and column numbers for the first character of the lexeme (i.e.,
    where the token starts in the parsed stream). Assuming it fits on
    one line of the input stream (which is not necessarily the case for
    string literal tokens), the column number of its last character is
    given by:

      :attr:`Token.startcol`  + len(:attr:`Token.string`) - 1.

    Instances of this class must be considered immutable. They can be
    used as dictionary keys and set elements, among others. Since these
    operations assume that the hash value of the object never changes,
    it is an error to modify such an object after an operation that
    relies on its hash value (cf. :meth:`object.__hash__`).

    """

    #: Token type (:class:`TokenType` instance)
    type = None
    #: The raw lexeme, *i.e.*, the exact string read from the parsed file
    string = None
    #: String used for :meth:`~object.__str__`, in particular for the
    #: :class:`NewlineToken`
    stringRepr = None

    def __init__(self, startline, startcol):
        for n in ("startline", "startcol"):
            setattr(self, n, locals()[n])

    # Goes together with __hash__()
    def __eq__(self, other):
        return self.type == other.type and \
               self.string == other.string and \
               self.stringRepr == other.stringRepr and \
               self.startline == other.startline and \
               self.startcol == other.startcol

    def __ne__(self, other):
        return not self.__eq__(other)

    # Goes together with __eq__()
    def __hash__(self):
        return (self.type.value ^ hash(self.string) ^ hash(self.stringRepr) ^
                self.startline ^ self.startcol)

    def __str__(self):
        return '<{} "{}" {}:{}>'.format(self.type.name, self.stringRepr,
                                        self.startline, self.startcol)

    def __repr__(self):
        return "{}.{}({!r}, {!r})".format(
            __name__, type(self).__name__, self.startline, self.startcol)

    # Useful when creating an exception related to a token
    def pos(self):
        return (self.startline, self.startcol)

    def formatStartPos(self):
        return "{}:{}".format(self.startline, self.startcol)


class NewlineToken(Token):
    type = TokenType.newline
    string = "\n"
    stringRepr = r"\n"

class VarAssignmentsStartToken(Token):
    type = TokenType.varAssignmentsStart
    string = stringRepr = "{"

class VarAssignmentsEndToken(Token):
    type = TokenType.varAssignmentsEnd
    string = stringRepr = "}"

class PredicateStartToken(Token):
    type = TokenType.predicateStart
    string = stringRepr = "["

class PredicateEndToken(Token):
    type = TokenType.predicateEnd
    string = stringRepr = "]"

class ListStartToken(Token):
    type = TokenType.listStart
    string = stringRepr = "["

class ListEndToken(Token):
    type = TokenType.listEnd
    string = stringRepr = "]"

class OpenParenToken(Token):
    type = TokenType.openParen
    string = stringRepr = "("

class CloseParenToken(Token):
    type = TokenType.closeParen
    string = stringRepr = ")"

class OrToken(Token):
    type = TokenType.orOp
    string = stringRepr = "or"

class AndToken(Token):
    type = TokenType.andOp
    string = stringRepr = "and"

class NotToken(Token):
    type = TokenType.notOp
    string = stringRepr = "not"

class EqualsToken(Token):
    type = TokenType.equalsOp
    string = stringRepr = "=="

class NotEqualsToken(Token):
    type = TokenType.notEqualsOp
    string = stringRepr = "!="

class InToken(Token):
    type = TokenType.inOp
    string = stringRepr = "in"

class AssignToken(Token):
    type = TokenType.assignOp
    string = stringRepr = "="

class CommaToken(Token):
    type = TokenType.comma
    string = stringRepr = ","

class TrueToken(Token):
    type = TokenType.true
    string = stringRepr = "True"

class FalseToken(Token):
    type = TokenType.false
    string = stringRepr = "False"

class StringLiteralToken(Token):
    type = TokenType.stringLiteral

    def __init__(self, startline, startcol, unprocessedString, value):
        Token.__init__(self, startline, startcol)
        self.string = self.stringRepr = unprocessedString
        #: String obtained after escape sequences expansion in the
        #: string literal
        self.value = value

    # No need to define __eq__(): if two instances have the same
    # 'unprocessedString' (stored in self.string), then they necessarily have
    # the same value in the 'value' attribute.

    def __repr__(self):
        return "{}.{}({!r}, {!r}, {!r}, {!r})".format(
            __name__, type(self).__name__,
            self.startline, self.startcol, self.string, self.value)

class VariableToken(Token):
    type = TokenType.variable

    def __init__(self, startline, startcol, name):
        Token.__init__(self, startline, startcol)
        self.string = self.stringRepr = name

    def __repr__(self):
        return "{}.{}({!r}, {!r}, {!r})".format(
            __name__, type(self).__name__,
            self.startline, self.startcol, self.string)

class RawConfigLineToken(Token):
    type = TokenType.rawConfigLine

    def __init__(self, startline, startcol, line):
        Token.__init__(self, startline, startcol)
        self.string = self.stringRepr = line

    def __repr__(self):
        return "{}.{}({!r}, {!r}, {!r})".format(
            __name__, type(self).__name__,
            self.startline, self.startcol, self.string)

#: Which token(s) may be closed by a given closing delimiter
mayClose = {")": (OpenParenToken,),
            "}": (VarAssignmentsStartToken,),
            "]": (ListStartToken, PredicateStartToken)}


class Lexer:
    WSandComments_cre = re.compile(r" *(#.*)?")
    keywordOrVariable_cre = re.compile(r"\b ([a-zA-Z0-9_]+) \b", re.VERBOSE)
    equalsOp_cre = re.compile(r"==[^=!]")
    notEqualsOp_cre = re.compile(r"!=[^=!]")
    assign_cre = re.compile(r"=[^=!]")
    backslashNewline_cre = re.compile(r"\\\n")

    def __init__(self, stream):
        self.stream = stream
        self.line = 1           # Typical line numbering scheme
        self.col = 1            # No universal consensus here...
        self.curline = stream.readline()

    def readline(self):
        self.curline = self.stream.readline()
        if self.curline:
            self.line += 1
            self.col = 1
        return self.curline

    def peek(self):
        try:
            c = self.curline[self.col - 1]
        except IndexError:
            return ""           # EOF
        else:
            return c            # Return \n at the end of a line

    def skipWSandComments(self):
        """Skip spaces and comments (all on a single line)."""
        mo = self.WSandComments_cre.match(self.curline, self.col - 1)
        if mo:
            self.col += mo.end() - mo.start() # Quicker than len(mo.group())?
        return mo

    def skipWSNLandComments(self, delimStack=None):
        """Skip a possibly-multiline mix of spaces and comments.

        By default, :class:`NewlineToken` instances are collected as
        encountered and returned in the form of a list. However, if
        *delimStack* is a non-empty delimiter stack, some of the newline
        tokens are selectively omitted from the returned list.

        """
        ignoreNewlineTokens = False
        # When delimStack is passed and non-empty, newline tokens are ignored
        # if and only if we are:
        #
        #   (a) inside a <predicate>;
        #
        #   (b) or inside a <varAssignments> and there is at least a
        #       <listStart> "[" or an <openParen> "(" that has not been closed.
        if delimStack:
            if delimStack[0].type == TokenType.predicateStart:
                ignoreNewlineTokens = True
            else:
                assert delimStack[0].type == TokenType.varAssignmentsStart, \
                    delimStack[0]
                for t in delimStack:
                    if t.type in (TokenType.listStart, TokenType.openParen):
                        ignoreNewlineTokens = True
                        break

        newlineTokens = []
        while True:
            self.skipWSandComments() # stops before an eventual \n char
            c = self.peek()

            if not c:
                break           # EOF
            elif c == "\n":
                if not ignoreNewlineTokens:
                    newlineTokens.append(NewlineToken(self.line, self.col))
                self.readline()
            else:
                break

        return newlineTokens

    def scanStringLiteralToken(self):
        # Remember where the string literal starts
        startline, startcol = self.line, self.col
        i = self.col
        assert i > 0 and self.curline[i-1] == '"', (i, self.curline)
        # Will be set to True when we encounter an unescaped \ character
        processingEscape = False
        unprocessed = []        # Before escape sequences processing
        chars = []              # After escape sequences processing

        while True:
            try:
                c = self.curline[i]
            except IndexError:
                if self.curline[self.col-1:].endswith("\n"):
                    text = self.curline[self.col-1:-1]
                else:
                    text = self.curline[self.col-1:]
                raise ParseError(
                    (self.line, i+1), "EOF reached while reading a "
                    "string literal: {}".format(text))

            if processingEscape:
                if c == "\\":
                    chars.append("\\")
                elif c == "n":
                    chars.append("\n")
                elif c == "t":
                    chars.append("\t")
                elif c == '"':
                    chars.append('"')
                elif c == "\n": # backslash-newline escape sequence
                    self.readline()
                    i = -1
                else:
                    raise ParseError(
                        (self.line, i), "invalid escape sequence in string "
                        "literal: {}".format(self.curline[i-1:i+1]))
                processingEscape = False
            elif c == "\\":
                processingEscape = True
            elif c == '"':
                break           # end of the string literal
            else:
                chars.append(c)

            unprocessed.append(c)
            i += 1

        # self.line is automatically updated whenever self.readline() is
        # called.
        self.col = i + 2
        return (startline, startcol, ''.join(unprocessed), ''.join(chars))

    def checkMatchingDelimiters(self, delimStack, closing, closingName,
                                opening, openingName):
        try:
            t = delimStack[-1]  # top of the stack
        except IndexError:
            raise ParseError(
                (self.line, self.col), "{} '{}' without any matching {} '{}'"
                .format(closingName, closing, openingName, opening))

        if not isinstance(t, mayClose[closing]):
            raise ParseError(
                (self.line, self.col),
                "{} '{}' can't close '{}' at {}".format(
                    closingName, closing, t.string, t.formatStartPos()))

    def scanBalancedTokens(self, delimStack):
        """Scan a balanced sequence of tokens.

        Normally, the token sequence should start right after a
        :class:`VarAssignmentsStartToken` (``{``) or
        :class:`ListStartToken` (``[``), which should be found at the
        top of *delimStack*. All subsequent tokens will be scanned and
        yielded until a ``}`` or ``]`` matching the top of *delimStack*
        is found. The method does not consume that closing delimiter,
        for symmetry with the handling of the opening delimiter.

        """
        while True:
            yield from self.skipWSNLandComments(delimStack=delimStack)

            c = self.peek()
            if not c:
                break           # EOF

            if c == "{":
                # It is probably an error to have an opening bracket
                # here, however the parser is in a better position to
                # decide on that matter.
                token = VarAssignmentsStartToken(self.line, self.col)
                delimStack.append(token)
            elif c == "[":
                token = ListStartToken(self.line, self.col)
                delimStack.append(token)
            elif c == "(":
                token = OpenParenToken(self.line, self.col)
                delimStack.append(token)
            elif c == "}":
                self.checkMatchingDelimiters(
                    delimStack, "}", "closing brace", "{", "opening brace")
                if len(delimStack) == 1:
                    break
                else:
                    st = delimStack.pop() # start token
                    assert st.type is TokenType.varAssignmentsStart, st.type
                    token = VarAssignmentsEndToken(self.line, self.col)
            elif c == "]":
                self.checkMatchingDelimiters(
                    delimStack, "]", "closing bracket", "[", "opening bracket")
                if len(delimStack) == 1:
                    break
                else:
                    st = delimStack.pop() # matching opening token
                    assert st.type is TokenType.listStart, st.type
                    token = ListEndToken(self.line, self.col)
            elif c == ")":
                self.checkMatchingDelimiters(delimStack,
                                             ")", "closing parenthesis",
                                             "(", "opening parenthesis")
                st = delimStack.pop() # matching opening token
                assert st.type is TokenType.openParen, st.type
                token = CloseParenToken(self.line, self.col)
            elif c == ",":
                token = CommaToken(self.line, self.col)
            elif c == '"':
                token = StringLiteralToken(*self.scanStringLiteralToken())
            else:
                mo = self.keywordOrVariable_cre.match(self.curline,
                                                      self.col - 1)
                if mo:
                    word = mo.group(1)
                    for kw, t in (("or", OrToken),
                                  ("and", AndToken),
                                  ("not", NotToken),
                                  ("in", InToken),
                                  ("True", TrueToken),
                                  ("False", FalseToken)):
                        if word == kw:
                            token = t(self.line, self.col)
                            break
                    else:
                        token = VariableToken(self.line, self.col, word)
                else:
                    # Whether to "continue" to the start of the outer loop once
                    # the following (inner) loop is over.
                    contAfterLoop = False
                    for regexp, t in ((self.equalsOp_cre, EqualsToken),
                                      (self.notEqualsOp_cre, NotEqualsToken),
                                      (self.assign_cre, AssignToken),
                                      (self.backslashNewline_cre, "bsNl")):
                        mo = regexp.match(self.curline, self.col - 1)
                        if mo and t == "bsNl":
                            # Backslash followed by a newline → ignore
                            self.readline()
                            # No token, no automatic self.col advance
                            contAfterLoop = True
                            break
                        elif mo:
                            token = t(self.line, self.col)
                            break
                    else:
                        text = self.curline[self.col-1:]
                        if text.endswith("\n"):
                            text = text[:-1]
                        assert text, text
                        raise ParseError((self.line, self.col),
                                         "does not start with a valid "
                                         "token: {}".format(text))
                    if contAfterLoop:
                        continue

            # String literals tokens are handled separately because they may
            # span multiple lines.
            if not isinstance(token, StringLiteralToken):
                self.col += len(token.string) # advance in the input stream
            yield token

    def scanEnclosedTokenGroup(self):
        """Scan a :token:`varAssignments` or :token:`predicate`."""
        # Stack where opening delimiters will be stored in order to
        # check that they are properly matched by the corresponding
        # closing delimiters.
        #
        # Keeping track of the set of currently opened brackets and
        # braces in the lexer is necessary because it must behave
        # differently depending on whether it is inside a
        # <varAssignments> or <predicate>, or outside both of these
        # (newlines are treated differently, for one; as a little bonus,
        # this allows the lexer to generate either a <listEnd> or a
        # <predicateEnd> for an encountered ']', depending on the
        # nesting level).
        delimStack = collections.deque()
        c = self.peek()

        if c == "{":
            t = VarAssignmentsStartToken(self.line, self.col)
        elif c == "[":
            t = PredicateStartToken(self.line, self.col)
        else:
            assert False, "expected '{{' or '[' instead of '{}'".format(c)

        delimStack.append(t)    # this is a "push"
        self.col += 1           # advance in the input stream
        yield t
        # Scan all tokens inside the group, making sure that all opening
        # and closing delimiters come in matching pairs.
        yield from self.scanBalancedTokens(delimStack)
        ot = delimStack.pop()   # the opening { or [
        cc = self.peek()

        if not cc:
            raise ParseError((self.line, self.col),
                             "EOF reached while reading a <predicate>")
        elif cc == "}":
            assert c == "{", "expected '{{' instead of '{}'".format(c)
            assert ot.type is TokenType.varAssignmentsStart, ot.type
            yield VarAssignmentsEndToken(self.line, self.col)
        else:
            assert cc == "]", "expected ']' instead of '{}'".format(cc)
            assert c == "[", "expected '[' instead of '{}'".format(c)
            assert ot.type is TokenType.predicateStart, ot.type
            yield PredicateEndToken(self.line, self.col)

        self.col += 1           # advance in the input stream
        yield from self.skipWSNLandComments()

    def scanRawConfig(self):
        """Scan a :token:`rawConfigLine`."""
        while True:
            c = self.peek()

            # A '[' at the beginning of a line (possibly following
            # whitespace) marks the beginning of the next <predicate>.
            if not c or c == "[":
                break

            text = self.curline[self.col-1:]
            if text.endswith("\n"):
                text = text[:-1]
            yield RawConfigLineToken(self.line, self.col, text)
            self.readline()
            self.skipWSNLandComments()

    def tokenGenerator(self):
        """Generate all tokens from the input stream."""
        # Skip initial whitespace and comments
        self.skipWSNLandComments()
        c = self.peek()

        if not c:
            return              # EOF
        elif c == "{":
            # The optional <varAssignments> section is present, read it.
            yield from self.scanEnclosedTokenGroup()

        while True:
            # Scan zero or more <rawConfigLine> tokens.
            yield from self.scanRawConfig()
            if not self.peek(): break
            # Scan a <predicate>.
            yield from self.scanEnclosedTokenGroup()
            if not self.peek(): break
