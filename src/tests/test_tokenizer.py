#    pydifact - a python edifact library
#    Copyright (C) 2017  Christian González
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pydifact.Token import Token
from pydifact.Tokenizer import Tokenizer
import unittest


class TokenizerTest(unittest.TestCase):

    def setUp(self):
        self._tokenizer = Tokenizer()

    def _assert_tokens(self, message, expected=[]):
        tokens = self._tokenizer.get_tokens(
            "{message}'".format(message=message))

        expected.append(Token(Token.TERMINATOR, "'"))
        self.assertEqual(expected, tokens)

    def test_basic(self):
        self._assert_tokens("RFF+PD:50515", [
            Token(Token.CONTENT, "RFF"),
            Token(Token.DATA_SEPARATOR, "+"),
            Token(Token.CONTENT, "PD"),
            Token(Token.COMPONENT_SEPARATOR, ":"),
            Token(Token.CONTENT, "50515"),
        ])

    def test_escape(self):
        self._assert_tokens("RFF+PD?:5", [
            Token(Token.CONTENT, "RFF"),
            Token(Token.DATA_SEPARATOR, "+"),
            Token(Token.CONTENT, "PD:5"),
        ])

    def test_double_escape(self):
        self._assert_tokens("RFF+PD??:5", [
            Token(Token.CONTENT, "RFF"),
            Token(Token.DATA_SEPARATOR, "+"),
            Token(Token.CONTENT, "PD?"),
            Token(Token.COMPONENT_SEPARATOR, ":"),
            Token(Token.CONTENT, "5"),
        ])

    def test_triple_escape(self):
        self._assert_tokens("RFF+PD???:5", [
            Token(Token.CONTENT, "RFF"),
            Token(Token.DATA_SEPARATOR, "+"),
            Token(Token.CONTENT, "PD?:5"),
        ])

    def test_quadruple_escape(self):
        self._assert_tokens("RFF+PD????:5", [
            Token(Token.CONTENT, "RFF"),
            Token(Token.DATA_SEPARATOR, "+"),
            Token(Token.CONTENT, "PD??"),
            Token(Token.COMPONENT_SEPARATOR, ":"),
            Token(Token.CONTENT, "5"),
        ])

    def test_ignore_whitespace(self):
        self._assert_tokens("RFF:5'\nDEF:6", [
            Token(Token.CONTENT, "RFF"),
            Token(Token.COMPONENT_SEPARATOR, ":"),
            Token(Token.CONTENT, "5"),
            Token(Token.TERMINATOR, "'"),
            Token(Token.CONTENT, "DEF"),
            Token(Token.COMPONENT_SEPARATOR, ":"),
            Token(Token.CONTENT, "6"),
        ])

    def test_no_terminator(self):
        with self.assertRaises(RuntimeError) as cm:
            self._tokenizer.get_tokens("TEST")
        self.assertEqual(str(cm.exception), "Unexpected end of EDI message")


if __name__ == '__main__':
    unittest.main()