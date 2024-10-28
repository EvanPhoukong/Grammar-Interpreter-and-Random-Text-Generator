import contextlib, io, unittest
from unittest import mock

from grin import parse, Interpret_File
from grin.Interpret_File import file_interpreter
from grin.Labels import extract_labels

class test_Let(unittest.TestCase):

    def test_file_interpreter_handles_let_and_print_statement(self):
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

    def test_file_interpreter_handles_statement_with_label_and_END(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'PRINT MESSAGE',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_statement_with_Let_var_to_var_assignment(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS MESSAGE',
                    'PRINT MESS',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

if __name__ == '__main__':
    unittest.main()