#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# config3.py --- Automated tests for condconfigparser (reference data for the
#                'config3' test configuration file)
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

from ... import lexer as l, parser as p

refTree = \
    p.RootNode(
    p.VarAssignmentsNode(
            [p.AssignmentNode(
                    p.VariableNode(l.VariableToken(1, 3, 'some_variable')),
                    p.OrTestNode(
                        [p.VariableNode(l.VariableToken(1, 19, 'other_variable')),
                         p.VariableNode(l.VariableToken(2, 19, 'another_one')),
                         p.StringLiteralNode("value used if 'other_variable' and 'another_one' are both false in boolean context")])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(6, 3, 'var')),
                    p.ListLiteralNode(
                        [p.StringLiteralNode('with'),
                         p.StringLiteralNode('opening'),
                         p.StringLiteralNode('delimiters'),
                         p.StringLiteralNode('such'),
                         p.StringLiteralNode('as'),
                         p.StringLiteralNode('['),
                         p.StringLiteralNode('and'),
                         p.StringLiteralNode('('),
                         p.StringLiteralNode('this'),
                         p.StringLiteralNode('is'),
                         p.StringLiteralNode('not'),
                         p.StringLiteralNode('necessary.')])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(8, 3, 'var2')),
                    p.OrTestNode(
                        [p.VariableNode(l.VariableToken(8, 11, 'example')),
                         p.AndTestNode(
                                [p.VariableNode(l.VariableToken(9, 11, 'with')),
                                 p.VariableNode(l.VariableToken(10, 11, 'parentheses'))])]))]),
    p.ConfigNode(
            [],
            [p.SectionNode(
                    l.PredicateStartToken(13, 1),
                    p.AndTestNode(
                        [p.VariableNode(l.VariableToken(13, 3, 'var')),
                         p.NotTestNode(
                                p.VariableNode(l.VariableToken(14, 7, 'var2')))]), ['Exception: raw configuration lines are so "raw" that handling comments and \\', 'continuation lines is up to the user application. Therefore, we have THREE', 'raw configuration lines here, the first of which ends with a backslash.'])]))

# Make sure auto-fill-mode doesn't corrupt strings containing whitespace
#
# Local Variables:
# auto-fill-function: nil
# End:
