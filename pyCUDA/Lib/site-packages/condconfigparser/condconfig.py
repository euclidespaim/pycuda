# -*- coding: utf-8 -*-

# condconfig.py --- RawConditionalConfig class for CondConfigParser
#
# Copyright (c) 2014, 2015, Florent Rougon
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

""":class:`RawConditionalConfig` class for CondConfigParser.

This module defines the :class:`condconfigparser.RawConditionalConfig`
class, which is the main application programming interface for using
CondConfigParser.

"""

import io
import functools
import operator

from .exceptions import InvalidUsage, UndefinedVariablesInAssignment, \
    UndefinedVariablesInPredicate
from .lexer import Lexer
from .parser import Parser


class DummyContextManager:
    """Do-nothing context manager.

    When used in a :python:keyword:`with` statement, instances of this
    class simply return the object that was passed to the constructor.

    """
    def __init__(self, stream):
        self.stream = stream

    def __enter__(self):
        return self.stream

    def __exit__(self, *exc):
        return False


class RawConditionalConfig:
    """Class for dealing with files conforming to CondConfigParser syntax.

    This class provides the main part of the API for using
    CondConfigParser.

    """
    def __init__(self, input, extvars=()):
        """Initialize a :class:`RawConditionalConfig` instance.

        :param input:   input stream or string ("configuration file")
        :type input:    file-like or string
        :param extvars: indicates the :term:`external variables
                        <external variable>`
        :type extvars:  sequence or set
        :return:        a :class:`RawConditionalConfig` instance

        Read the configuration from *input* and check that the variables
        used therein can all be computed, directly or indirectly from
        the variables whose names are listed in *extvars*.

        """
        if isinstance(input, str):
            ctxManager = io.StringIO(input)
        else:
            ctxManager = DummyContextManager(input)

        with ctxManager as stream:
            lexer = Lexer(stream)
            # Root node of the abstract syntax tree
            self._tree = Parser(lexer).buildTree()

        self._assignments = self._tree.assignments
        self._config = self._tree.config

        #: Names of variables defined externally, *i.e.*, not in the
        #: configuration file
        self.extvars = extvars
        self._checkUsesOfUndefinedVariables()

    def _checkAssignments(self):
        """Check that all variable assignments can be executed.

        Check that all variable assignments can be executed, assuming
        that all variables whose names are listed in :attr:`extvars` are
        defined.

        If at least one variable assignment makes use of an undefined
        variable, raise :exc:`UndefinedVariablesInAssignment`.
        Otherwise, return the set of all defined variables (well, their
        names).

        """
        # Set of variables that are well-defined (whose value can be computed
        # using the already-defined variables)
        defined = set(self.extvars)

        for variableNode, tree in self._assignments:
            undef = tree.undefVariables(defined)
            if undef:
                raise UndefinedVariablesInAssignment(variableNode.token, undef)
            else:
                defined.add(variableNode.name)

        return defined

    def _checkPredicates(self, definedVars):
        """Check that all predicates can be evaluated.

        Raise :exc:`UndefinedVariablesInPredicate` if, and only if at
        least one predicate uses an undefined variable.

        """
        for section in self._config:
            undef = section.predicate.undefVariables(definedVars)
            if undef:
                raise UndefinedVariablesInPredicate(section.startToken, undef)

    def _checkUsesOfUndefinedVariables(self):
        """
        Check that no variable assignment or predicate uses undefined variables.

        Raise :exc:`UndefinedVariablesInAssignment` or
        :exc:`UndefinedVariablesInPredicate` appropriately, otherwise
        return the set of all defined variables (well, their names).

        """
        definedVars = self._checkAssignments()
        self._checkPredicates(definedVars)

        return definedVars

    def computeVars(self, context):
        """Perform all variable assignments.

        :param dict context:
                 mapping giving the value to use for every
                 :term:`external variable`. More precisely, for each
                 name of an external variable, it gives the value for
                 initialization of this variable before starting to
                 perform variable assignments.
        :return: a new dictionary giving the value of every variable, be
                 it external or not.

        """
        for varName in self.extvars:
            if varName not in context:
                raise InvalidUsage("missing external variable in 'context' "
                                   "argument: {!r}".format(varName))

        variables = dict(context)    # new dict object

        for variableNode, tree in self._assignments:
            variables[variableNode.name] = tree.eval(variables)

        return variables

    def eval(self, context, *, flat=False):
        r"""Compute the values of variables and evaluate predicates.

        :param dict context:
           mapping giving the value to use for every :term:`external
           variable`. More precisely, for each name of an external
           variable, it gives the value for initialization of this
           variable before starting to perform variable assignments.
        :param bool flat:
           if true, the second element of the return value will be a
           list of :term:`raw configuration lines <raw configuration
           line>`; otherwise, it will be a list of lists of raw
           configuration lines, one for each section, starting with the
           :ref:`default, unconditional section
           <default-unconditional-section>`.
        :return:
           a :class:`tuple` of the form :samp:`({variables}, {lines})`
           where:

             - *variables* is a new dictionary giving the value of every
               variable, be it external or not;
             - *lines* is a list as indicated above in the *flat*
               parameter description.

        The following interactive session illustrates the effect of the
        *flat* argument::

          >>> cfg = '''\
          ... { var1 = (extvar1 == "foobar") # parentheses only for clarity
          ...   var2 = var1 and "baz" in extvar2 }
          ...
          ... raw cfg default1
          ... raw cfg default2
          ...
          ... [ var2 or extvar1 == "quux" ]
          ... raw cfg a1
          ... raw cfg a2
          ... raw cfg a3
          ...
          ... [ var1 ]
          ... raw cfg b1
          ... raw cfg b2
          ...
          ... [ not var1 ]
          ... raw cfg c1
          ... raw cfg c2
          ... '''
          >>> config = RawConditionalConfig(cfg, extvars=("extvar1", "extvar2"))
          >>> context = {"extvar1": "quux",
          ...            "extvar2": [12, "abc", [False, "def"]]}
          >>> [config.eval(context), config.eval(context, flat=True)] == \
          ... [({'extvar1': 'quux',
          ...    'extvar2': [12, 'abc', [False, 'def']],
          ...    'var1': False,
          ...    'var2': False},
          ...   [['raw cfg default1', 'raw cfg default2'],
          ...    ['raw cfg a1', 'raw cfg a2', 'raw cfg a3'],
          ...    ['raw cfg c1', 'raw cfg c2']]),
          ...  ({'extvar1': 'quux',
          ...    'extvar2': [12, 'abc', [False, 'def']],
          ...    'var1': False,
          ...    'var2': False},
          ...   ['raw cfg default1',
          ...    'raw cfg default2',
          ...    'raw cfg a1',
          ...    'raw cfg a2',
          ...    'raw cfg a3',
          ...    'raw cfg c1',
          ...    'raw cfg c2'])]
          True
          >>>

        The default value for the *flat* parameter (``False``) preserves
        as much information as possible, allowing user applications to
        implement things such as :ref:`conditional sections
        <conditional-sections>` overriding the :ref:`default,
        unconditional section <default-unconditional-section>`.

        """
        variables = self.computeVars(context)
        res = [self._config.defaultConfigLines]

        for section in self._config.sections:
            if section.predicate.eval(variables):
                res.append(section.rawConfigLines)

        if flat:
            return (variables, functools.reduce(operator.add, res, []))
        else:
            return (variables, res)
