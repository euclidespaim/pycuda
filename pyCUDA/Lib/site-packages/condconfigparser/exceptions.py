# -*- coding: utf-8 -*-

# exceptions.py --- Exceptions defined by CondConfigParser
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

"""Exceptions defined by CondConfigParser."""

class error(Exception):
    """Base class for exceptions in CondConfigParser."""
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.complete_message()

    def __repr__(self):
        return "{0}.{1}({2!r})".format(__name__, type(self).__name__,
                                       self.message)

    def complete_message(self):
        if self.message:
            return "{0}: {1}".format(self.ExceptionShortDescription,
                                     self.message)
        else:
            return self.ExceptionShortDescription

    ExceptionShortDescription = "CondConfigParser generic exception"


class InvalidUsage(error):
    """Exception raised when CondConfigParser is used in an incorrect way."""
    ExceptionShortDescription = "invalid use of CondConfigParser"

class ParseError(error):
    """Exception raised when CondConfigParser finds a syntax error in the \
stream to parse."""
    def __init__(self, pos, msg):
        self.pos = pos
        self.msg = msg
        self.message = "line {}, column {}: {}".format(pos[0], pos[1], msg)

    def __repr__(self):
        return "{0}.{1}({2!r}, {3!r})".format(__name__, type(self).__name__,
                                              self.msg, self.pos)

    ExceptionShortDescription = "unable to parse the configuration"

class UndefinedVariable(error):
    """Exception raised when trying to evaluate an undefined variable.

    Because of the checks on assignments and predicates performed by
    :class:`condconfigparser.condconfig.RawConditionalConfig`'s
    constructor, this exception should not be seen by user code. Please
    report if you find this is not the case.

    """
    def __init__(self, name=None):
        self.name = self.message = name

    ExceptionShortDescription = "undefined variable"

class UndefinedVariablesInAssignmentOrPredicate(error):
    """Exception raised when an assignment or predicate uses a variable \
before it is defined.

    This exception should not be seen by user code. Please report if you find
    this is not the case.

    """
    def __init__(self, production, startToken, undef):
        self.production = production
        self.startToken = startToken
        #: :class:`frozenset` of :class:`condconfigparser.lexer.VariableToken`
        #: instances
        self.undefVariables = undef

        self.ExceptionShortDescription = \
            "undefined variables" if len(undef) > 1 else "undefined variable"

        variables = ", ".join(sorted(
                [ "{t.string} ({t.startline}:{t.startcol})".format(t=tok)
                  for tok in undef ]))

        self.message = "in {} starting at line {}, column {}: {}" \
            .format(production, startToken.startline, startToken.startcol,
                    variables)

class UndefinedVariablesInAssignment(UndefinedVariablesInAssignmentOrPredicate):
    """Exception raised when an assignment uses a variable before it is \
defined."""
    def __init__(self, startToken, undef):
        UndefinedVariablesInAssignmentOrPredicate.__init__(self, "assignment",
                                                           startToken, undef)

class UndefinedVariablesInPredicate(UndefinedVariablesInAssignmentOrPredicate):
    """Exception raised when a predicate uses a variable before it is \
defined."""
    def __init__(self, startToken, undef):
        UndefinedVariablesInAssignmentOrPredicate.__init__(self, "predicate",
                                                           startToken, undef)

class InTestTypeError(error):
    """Exception raised when an :token:`inTest` can't be \
:meth:`~condconfigparser.parser.InTestNode.eval`\ed because of a type \
mismatch."""
    def __init__(self, inToken, origExc):
        self.inToken = inToken
        self.origExc = origExc
        self.message = "line {}, column {}: {}".format(
            inToken.startline, inToken.startcol, origExc)

    def __repr__(self):
        return "{0}.{1}({2!r}, {3!r})".format(__name__, type(self).__name__,
                                              self.inToken, self.origExc)

    ExceptionShortDescription = "mismatching types in membership test"
