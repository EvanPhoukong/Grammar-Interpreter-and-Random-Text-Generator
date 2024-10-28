import contextlib, io, unittest
from unittest import mock

from grin import parse, Interpret_File
from grin.Interpret_File import file_interpreter
from grin.Labels import extract_labels

class test_Input(unittest.TestCase):

    @mock.patch("grin.Input.input", create = True)
    def test_file_interpreter_handles_innum_statement_with_int_input(self, m_input):
        m_input.side_effect = ['8']
        grinfile = ['INNUM MESSAGE',
                    'PRINT MESSAGE',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '8\n')

    @mock.patch("grin.Input.input", create = True)
    def test_file_interpreter_handles_innum_statement_with_float_input(self, m_input):
        m_input.side_effect = ['8.3']
        grinfile = ['INNUM MESSAGE',
                    'PRINT MESSAGE',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '8.3\n')

    @mock.patch("grin.Input.input", create = True)
    def test_file_interpreter_raises_error_when_innum_statement_has_non_numeric_input(self, m_input):
        m_input.side_effect = ['Hello']
        grinfile = ['INNUM MESSAGE',
                    'PRINT MESSAGE',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR: INNUM only takes integer or float(numeric values) as input.\n')

    @mock.patch("grin.Input.input", create = True)
    def test_file_interpreter_handles_INSTR_statement(self, m_input):
        m_input.side_effect = ['Hello']
        grinfile = ['INSTR MESSAGE',
                    'PRINT MESSAGE',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello\n')

if __name__ == '__main__':
    unittest.main()