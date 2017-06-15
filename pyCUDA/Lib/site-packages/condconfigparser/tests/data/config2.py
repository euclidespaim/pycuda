#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# config2.py --- Automated tests for condconfigparser (reference data for the
#                'config2' test configuration file)
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
                    p.VariableNode(l.VariableToken(1, 3, 'variable1')),
                    p.EqualsTestNode(
                        l.EqualsToken(2, 67),
                        p.OrTestNode(
                            [p.BoolLiteralNode(False),
                             p.EqualsTestNode(
                                    l.EqualsToken(2, 20),
                                    p.StringLiteralNode('aa'),
                                    p.StringLiteralNode('bb')),
                             p.ListLiteralNode(
                                    [p.StringLiteralNode('this'),
                                     p.StringLiteralNode('is'),
                                     p.StringLiteralNode('it')]),
                             p.InTestNode(
                                    l.InToken(2, 60),
                                    p.StringLiteralNode('x'),
                                    p.ListLiteralNode(
                                        []))]),
                        p.AndTestNode(
                            [p.InTestNode(
                                    l.InToken(3, 11),
                                    p.StringLiteralNode('abc'),
                                    p.ListLiteralNode(
                                        [p.BoolLiteralNode(True),
                                         p.BoolLiteralNode(False),
                                         p.StringLiteralNode('abc')])),
                             p.ListLiteralNode(
                                    [p.StringLiteralNode('this'),
                                     p.StringLiteralNode('is'),
                                     p.StringLiteralNode('it')])]))),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(6, 3, 'variable2')),
                    p.AndTestNode(
                        [p.EqualsTestNode(
                                l.EqualsToken(6, 42),
                                p.NotTestNode(
                                    p.AndTestNode(
                                        [p.ListLiteralNode(
                                                [p.StringLiteralNode('a')]),
                                         p.StringLiteralNode('blabla')])),
                                p.AndTestNode(
                                    [p.StringLiteralNode('abc'),
                                     p.BoolLiteralNode(False)])),
                         p.StringLiteralNode('Yup, dude')])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(7, 3, 'variable3')),
                    p.AndTestNode(
                        [p.NotEqualsTestNode(
                                l.NotEqualsToken(7, 42),
                                p.NotTestNode(
                                    p.AndTestNode(
                                        [p.ListLiteralNode(
                                                [p.StringLiteralNode('a')]),
                                         p.StringLiteralNode('blabla')])),
                                p.AndTestNode(
                                    [p.StringLiteralNode('abc'),
                                     p.BoolLiteralNode(True)])),
                         p.StringLiteralNode('Good!')]))]),
    p.ConfigNode(
            [], []))


variables = {'aircraft': 'c172p',
             'airport': 'LFPG',
             'parking': 'XYZ0',
             'scenarios': ['nimitz_demo', 'clemenceau_demo', 'balloon_demo'],
             'variable1': True,
             'variable2': 'Yup, dude',
             'variable3': 'Good!'}

rawConfigLines = [[]]

# Make sure auto-fill-mode doesn't corrupt strings containing whitespace
#
# Local Variables:
# auto-fill-function: nil
# End:
