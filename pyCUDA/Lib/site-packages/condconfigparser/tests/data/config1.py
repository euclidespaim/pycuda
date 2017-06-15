#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# config1.py --- Automated tests for condconfigparser (reference data for the
#                'config1' test configuration file)
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
                    p.VariableNode(l.VariableToken(1, 3, 'a')),
                    p.ListLiteralNode(
                        [p.StringLiteralNode('def'),
                         p.StringLiteralNode('ghi')])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(4, 3, 'b')),
                    p.ListLiteralNode(
                        [p.BoolLiteralNode(True),
                         p.StringLiteralNode('jkl'),
                         p.VariableNode(l.VariableToken(4, 21, 'aircraft')),
                         p.VariableNode(l.VariableToken(4, 31, 'a')),
                         p.VariableNode(l.VariableToken(4, 34, 'airport'))])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(5, 3, 'c')),
                    p.AndTestNode(
                        [p.EqualsTestNode(
                                l.EqualsToken(5, 15),
                                p.VariableNode(l.VariableToken(5, 7, 'parking')),
                                p.StringLiteralNode('XYZ0')),
                         p.InTestNode(
                                l.InToken(5, 35),
                                p.StringLiteralNode('ufo'),
                                p.VariableNode(l.VariableToken(5, 38, 'b')))])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(6, 3, 'd')),
                    p.AndTestNode(
                        [p.EqualsTestNode(
                                l.EqualsToken(6, 16),
                                p.VariableNode(l.VariableToken(6, 8, 'parking')),
                                p.StringLiteralNode('XYZ0')),
                         p.InTestNode(
                                l.InToken(6, 38),
                                p.StringLiteralNode('ufo'),
                                p.VariableNode(l.VariableToken(6, 41, 'b')))])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(7, 3, 'e')),
                    p.EqualsTestNode(
                        l.EqualsToken(7, 9),
                        p.VariableNode(l.VariableToken(7, 7, 'c')),
                        p.VariableNode(l.VariableToken(7, 12, 'd')))),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(9, 3, 'custom_start_pos')),
                    p.BoolLiteralNode(True)),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(10, 3, 'foobar')),
                    p.AndTestNode(
                        [p.BoolLiteralNode(False),
                         p.StringLiteralNode('abc')])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(11, 3, 'baz')),
                    p.OrTestNode(
                        [p.ListLiteralNode(
                                [p.VariableNode(l.VariableToken(11, 10, 'aircraft')),
                                 p.StringLiteralNode('strange\tstring\nwith                     many escape sequences'),
                                 p.ListLiteralNode(
                                        [p.StringLiteralNode('list'),
                                         p.StringLiteralNode('inside'),
                                         p.StringLiteralNode('a'),
                                         p.StringLiteralNode('list')])]),
                         p.NotTestNode(
                                p.ListLiteralNode(
                                    [p.StringLiteralNode('bla')]))])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(14, 3, 'zod')),
                    p.AndTestNode(
                        [p.ListLiteralNode(
                                [p.BoolLiteralNode(True),
                                 p.StringLiteralNode('you'),
                                 p.StringLiteralNode('may'),
                                 p.StringLiteralNode('reference'),
                                 p.StringLiteralNode('baz'),
                                 p.StringLiteralNode('from here')]),
                         p.OrTestNode(
                                [p.VariableNode(l.VariableToken(16, 4, 'a')),
                                 p.VariableNode(l.VariableToken(16, 9, 'b'))])])),
             p.AssignmentNode(
                    p.VariableNode(l.VariableToken(17, 3, 'blabla')),
                    p.VariableNode(l.VariableToken(17, 12, 'zod')))]),
    p.ConfigNode(
            ['--common-options', '--another-one     # with a comment', '\\[ spaces at the end of the line need escaping like this: \\ # easy!', '--normal-option=value'],
            [p.SectionNode(
                    l.PredicateStartToken(26, 1),
                    p.AndTestNode(
                        [p.VariableNode(l.VariableToken(26, 3, 'custom_start_pos')),
                         p.OrTestNode(
                                [p.EqualsTestNode(
                                        l.EqualsToken(26, 33),
                                        p.VariableNode(l.VariableToken(26, 25, 'airport')),
                                        p.StringLiteralNode('KSFO')),
                                 p.OrTestNode(
                                        [p.EqualsTestNode(
                                                l.EqualsToken(27, 36),
                                                p.VariableNode(l.VariableToken(27, 26, 'scenarios')),
                                                p.ListLiteralNode(
                                                    [p.StringLiteralNode('nimitz_demo'),
                                                     p.StringLiteralNode('clemenceau_demo'),
                                                     p.StringLiteralNode('balloon_demo')])),
                                         p.AndTestNode(
                                                [p.InTestNode(
                                                        l.InToken(30, 44),
                                                        p.StringLiteralNode('wingman_demo'),
                                                        p.VariableNode(l.VariableToken(30, 47, 'scenarios'))),
                                                 p.NotEqualsTestNode(
                                                        l.NotEqualsToken(31, 39),
                                                        p.VariableNode(l.VariableToken(31, 30, 'aircraft')),
                                                        p.StringLiteralNode('777-200ER'))])])])]), ['--lon=5.12358614', '--lat=40.1654116']),
             p.SectionNode(
                    l.PredicateStartToken(38, 1),
                    p.AndTestNode(
                        [p.VariableNode(l.VariableToken(38, 3, 'custom_start_pos')),
                         p.OrTestNode(
                                [p.EqualsTestNode(
                                        l.EqualsToken(39, 13),
                                        p.VariableNode(l.VariableToken(39, 4, 'aircraft')),
                                        p.StringLiteralNode('c172p')),
                                 p.AndTestNode(
                                        [p.EqualsTestNode(
                                                l.EqualsToken(40, 14),
                                                p.VariableNode(l.VariableToken(40, 7, 'foobar')),
                                                p.StringLiteralNode('may contain # characters as well as " (escaped)')),
                                         p.NotTestNode(
                                                p.EqualsTestNode(
                                                    l.EqualsToken(41, 20),
                                                    p.VariableNode(l.VariableToken(41, 12, 'airport')),
                                                    p.StringLiteralNode('LFPO')))])])]), ['--com1=120.70', '--com2=122.45                   # comment', '--weird-option=this is a \\# character   # and this is a comment']),
             p.SectionNode(
                    l.PredicateStartToken(46, 1),
                    p.AndTestNode(
                        [p.EqualsTestNode(
                                l.EqualsToken(46, 10),
                                p.VariableNode(l.VariableToken(46, 3, 'blabla')),
                                p.VariableNode(l.VariableToken(46, 13, 'zod'))),
                         p.InTestNode(
                                l.InToken(46, 53),
                                p.ListLiteralNode(
                                    [p.StringLiteralNode('list'),
                                     p.StringLiteralNode('inside'),
                                     p.StringLiteralNode('a'),
                                     p.StringLiteralNode('list')]),
                                p.VariableNode(l.VariableToken(46, 56, 'baz'))),
                         p.EqualsTestNode(
                                l.EqualsToken(47, 7),
                                p.VariableNode(l.VariableToken(47, 3, 'baz')),
                                p.ListLiteralNode(
                                    [p.VariableNode(l.VariableToken(47, 11, 'aircraft')),
                                     p.StringLiteralNode('strange\tstring\nwith                     many escape sequences'),
                                     p.ListLiteralNode(
                                            [p.StringLiteralNode('list'),
                                             p.StringLiteralNode('inside'),
                                             p.StringLiteralNode('a'),
                                             p.StringLiteralNode('list')])]))]), ['--ouin-ouin=argh', '--re-ouin=\\ \\[\\]\\# pouet # et ouais']),
             p.SectionNode(
                    l.PredicateStartToken(53, 1),
                    p.NotTestNode(
                        p.VariableNode(l.VariableToken(53, 7, 'e'))), ['--oh no!'])]))

variables = {'a': ['def', 'ghi'],
             'aircraft': 'c172p',
             'airport': 'LFPG',
             'b': [True, 'jkl', 'c172p', ['def', 'ghi'], 'LFPG'],
             'baz': ["c172p",
                     "strange\tstring\nwith                     "
                     "many escape sequences",
                     ['list', 'inside', 'a', 'list']],
             'blabla': ['def', 'ghi'],
             'c': False,
             'custom_start_pos': True,
             'd': False,
             'e': True,
             'foobar': False,
             'parking': 'XYZ0',
             'scenarios': ['nimitz_demo', 'clemenceau_demo', 'balloon_demo'],
             'zod': ['def', 'ghi']}

rawConfigLines = \
    [['--common-options',
      '--another-one     # with a comment',
      '\\[ spaces at the end of the line need escaping like this: \\ # easy!',
      '--normal-option=value'],
     ['--lon=5.12358614', '--lat=40.1654116'],
     ['--com1=120.70',
      '--com2=122.45                   # comment',
      '--weird-option=this is a \\# character   # and this is a comment'],
     ['--ouin-ouin=argh', '--re-ouin=\\ \\[\\]\\# pouet # et ouais']]

# Make sure auto-fill-mode doesn't corrupt strings containing whitespace
#
# Local Variables:
# auto-fill-function: nil
# End:
