#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# test_condconfig.py --- Automated tests for condconfigparser.condconfig
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

# With absolute imports (e.g., 'from condconfigparser import InTestTypeError'),
# one can run the test suite for an installed package like this:
#
#   ( cd base_dir/lib/python3.4/site-packages/condconfigparser && \
#     python3 -m unittest )
#
# instead of:
#
#   ( cd base_dir/lib/python3.4/site-packages/condconfigparser && \
#     python3 -m unittest discover -v -t .. )
from .. import InTestTypeError, RawConditionalConfig

# Hook doctest-based tests into the test discovery mechanism
import doctest
from .. import condconfig

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(condconfig))
    return tests


def loadCfgFile(cfgFile, context):
    cfgfilePath = os.path.join(os.path.dirname(__file__), "data", cfgFile)
    with open(cfgfilePath, "r", encoding="utf-8") as f:
        config = RawConditionalConfig(f, context.keys())

    return config


class TestRawConditionalConfigEval(unittest.TestCase):
    sampleContext = {"aircraft": "c172p",
                     "airport": "LFPG",
                     "parking": "XYZ0",
                     "scenarios":
                         ["nimitz_demo", "clemenceau_demo", "balloon_demo"]}

    def testEvalOnComplexCfgFile(self):
        """Process a complex configuration file with RawConditionalConfig.eval()"""
        from .data.config1 import variables, rawConfigLines
        config = loadCfgFile("config1", self.sampleContext)

        self.assertEqual(config.eval(self.sampleContext),
                         (variables, rawConfigLines))

    def testEvalOnFileWithParenthesizedOrTestBinOpOperands(self):
        """Process a file with parenthesized orTest binop operands with \
RawConditionalConfig.eval()

        The file has expressions of the form ( orTest ) == ( orTest )
        and analogue with !=.

        """
        from .data.config1 import variables, rawConfigLines
        config = loadCfgFile("config1", self.sampleContext)

        self.assertEqual(config.eval(self.sampleContext),
                         (variables, rawConfigLines))

    def testInTestWithMismatchingTypes(self):
        """Test that InTestTypeError is raised when performing invalid \
membership tests"""
        config = RawConditionalConfig('{ var = [] in "abcd" }\n',
                                      extvars=())
        with self.assertRaises(InTestTypeError):
            config.eval({})

        config2 = RawConditionalConfig('{ s = "abcd"\n'
                                       '  var = [] in s }\n',
                                       extvars=())
        with self.assertRaises(InTestTypeError):
            config2.eval({})

        config3 = RawConditionalConfig('{ l = []\n'
                                       '  var = l in "abcd" }\n',
                                       extvars=())
        with self.assertRaises(InTestTypeError):
            config3.eval({})

    def testOrderOfVariableAssignments(self):
        """Test that variable assignments are carried out in the proper order"""
        config = RawConditionalConfig("""
{ a = "abc"
  b = a
  a = [b] }\n""",
                                      extvars=())
        self.assertEqual(config.eval({}), ({"a": ["abc"],
                                            "b": "abc"},
                                           [[]]))

if __name__ == "__main__":
    unittest.main()
