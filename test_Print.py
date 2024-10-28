import contextlib, io, unittest
from unittest import mock

from grin import parse, Interpret_File
from grin.Interpret_File import file_interpreter
from grin.Labels import extract_labels

class test_Print(unittest.TestCase):

    def test_file_interpreter_handles__print_statement(self):
        grinfile = ['LET MESSAGE "Hello Boo!"',
                    'PRINT MESSAGE',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_printing_literal(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'PRINT 5',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '5\n')

    def test_file_interpreter_handles_statement_with_printing_empty_var(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS MESSAGE',
                    'PRINT WOW',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '0\n')


if __name__ == '__main__':
    unittest.main()