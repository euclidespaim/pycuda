#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# test_parser.py --- Automated tests for condconfigparser.parser
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

import os
import unittest

# With absolute imports (e.g., 'from condconfigparser.lexer import Lexer'),
# one can run the test suite for an installed package like this:
#
#   ( cd base_dir/lib/python3.4/site-packages/condconfigparser && \
#     python3 -m unittest )
#
# instead of:
#
#   ( cd base_dir/lib/python3.4/site-packages/condconfigparser && \
#     python3 -m unittest discover -v -t .. )
from ..lexer import Lexer
from ..parser import Parser


def loadTreeFromCfgFile(cfgFile):
    cfgfilePath = os.path.join(os.path.dirname(__file__), "data", cfgFile)
    with open(cfgfilePath, "r", encoding="utf-8") as f:
        lexer = Lexer(f)
        parser = Parser(lexer)
        tree = parser.buildTree()

    return tree


class TestLexerPlusParser(unittest.TestCase):
    def testComplexExprAroundBinOp(self):
        """Parse expressions of the form ( orTest ) == ( orTest ) and \
analogue with !="""
        from .data.config2 import refTree
        tree = loadTreeFromCfgFile("config2")
        self.assertEqual(tree, refTree)

    def testContinuationLines(self):
        """Parse constructs with continuation lines

        (right, continuation lines are handled at lexer level)"""
        from .data.config3 import refTree
        tree = loadTreeFromCfgFile("config3")
        self.assertEqual(tree, refTree)

    def testLexerPlusParser(self):
        """Parse a complex configuration file"""
        from .data.config1 import refTree
        tree = loadTreeFromCfgFile("config1")
        self.assertEqual(tree, refTree)


if __name__ == "__main__":
    unittest.main()
