import contextlib, io, unittest
from unittest import mock

from grin import parse, Interpret_File
from grin.Interpret_File import file_interpreter
from grin.Labels import extract_labels

class test_Arithmetic(unittest.TestCase):

    def test_file_interpreter_handles_statement_with_add_between_numbers(self):
        grinfile = ['LET A 3',
                    'ADD A 2',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '5\n')


    def test_file_interpreter_handles_statement_with_add_between_strings(self):
        grinfile = ['LET A Hello',
                    'ADD A " Friend!"',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Friend!\n')


    def test_file_interpreter_handles_error_when_adding_incompatible_types(self):
        grinfile = ['LET A Hello',
                    'ADD A 3',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(),
                         'ERROR ON LINE 2: Addition of the variable and the value is not possible due to them being incompatible types.\n')


    def test_file_interpreter_handles_statement_with_subtraction_between_numbers(self):
        grinfile = ['LET A 3',
                    'SUB A 2',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1\n')


    def test_file_interpreter_handles_error_when_subtracting_incompatible_types(self):
        grinfile = ['LET A Hello',
                    'SUB A 3',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(),
                         'ERROR ON LINE 2: Subtraction of the variable and the value is not possible due to them being incompatible types.\n')


    def test_file_interpreter_handles_statement_with_mult_between_numbers(self):
        grinfile = ['LET A 3',
                    'MULT A 2',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '6\n')


    def test_file_interpreter_handles_statement_with_mult_between_strings(self):
        grinfile = ['LET A Hello',
                    'MULT A 2',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'HelloHello\n')


    def test_file_interpreter_handles_error_when_multiplying_incompatible_types(self):
        grinfile = ['LET A Hello',
                    'MULT A "3"',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(),
                         "ERROR ON LINE 2: Multiplication of the variable and the value. This can be due to the fact that they are incompatible types, or that there was an attempt to multiply a string and negative integer.\n")


    def test_file_interpreter_handles_error_when_multiplying_str_and_negative_int(self):
        grinfile = ['LET A Hello',
                    'MULT A "-3"',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(),
                         'ERROR ON LINE 2: Multiplication of the variable and the value. This can be due to the fact that they are incompatible types, or that there was an attempt to multiply a string and negative integer.\n')


    def test_file_interpreter_handles_statement_with_div_between_ints(self):
        grinfile = ['LET A 3',
                    'DIV A 3',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1\n')


    def test_file_interpreter_handles_statement_with_div_resulting_in_float(self):
        grinfile = ['LET A 3',
                    'DIV A 2',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1.5\n')


    def test_file_interpreter_handles_error_when_dividing_incompatible_types(self):
        grinfile = ['LET A Hello',
                    'DIV A 3',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(),
                         'ERROR ON LINE 2: Division of the variable and the value is not possible due to them being incompatible types.\n')


    def test_file_interpreter_handles_error_when_dividing_by_zero(self):
        grinfile = ['LET A 3',
                    'DIV A 0',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 2: Dividing by zero is not possible.\n')

    def test_file_interpreter_handles_statement_with_subtraction_between_variables(self):
        grinfile = ['LET A 3',
                    'LET b 2',
                    'SUB A b',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1\n')

    def test_file_interpreter_handles_statement_with_addition_between_variables(self):
        grinfile = ['LET A 3',
                    'LET b 2',
                    'ADD A b',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '5\n')

    def test_file_interpreter_handles_statement_with_multiplication_between_variables(self):
        grinfile = ['LET A 3',
                    'LET b 2',
                    'MULT A b',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '6\n')

    def test_file_interpreter_handles_statement_with_multiplication(self):
        grinfile = ['LET A 3',
                    'MULT A 2',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '6\n')

    def test_file_interpreter_handles_statement_with_division_between_variables(self):
        grinfile = ['LET A 3',
                    'LET b 2',
                    'DIV A b',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1.5\n')

    def test_file_interpreter_handles_statement_with_division_between_variables_that_are_floats(self):
        grinfile = ['LET A 3.0',
                    'LET b 3.0',
                    'DIV A b',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1.0\n')

    def test_file_interpreter_handles_statement_with_division_between_numbers_that_are_floats(self):
        grinfile = ['LET A 3.0',
                    'DIV A 3.0',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1.0\n')

    def test_file_interpreter_handles_statement_with_division_between_numbers_that_are_int(self):
        grinfile = ['LET A 3',
                    'DIV A 3',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1\n')

    def test_file_interpreter_handles_statement_with_division_between_variables_that_are_int(self):
        grinfile = ['LET A 3',
                    'LET B 3',
                    'DIV A B',
                    'PRINT A',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '1\n')

    def test_file_interpreter_handles_add_statement_when_left_var_is_defaulted(self):
        grinfile = ['LET A 3',
                    'ADD B A',
                    'PRINT B',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '3\n')

    def test_file_interpreter_handles_add_statement_when_right_var_is_defaulted(self):
        grinfile = ['LET AA 3',
                    'ADD AA BB',
                    'PRINT AA',
                    'END']
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '3\n')

    def test_file_interpreter_handles_sub_statement_when_left_var_is_defaulted(self):
        grinfile = ['LET C 3',
                    'SUB D C',
                    'PRINT D',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '-3\n')

    def test_file_interpreter_handles_sub_statement_when_right_var_is_defaulted(self):
        grinfile = ['LET EEE 3',
                    'SUB EEE DDD',
                    'PRINT EEE',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '3\n')

    def test_file_interpreter_handles_mult_statement_when_left_var_is_defaulted(self):
        grinfile = ['LET AAA 3',
                    'MULT BBB AAA',
                    'PRINT BBB',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '0\n')

    def test_file_interpreter_handles_mult_statement_when_right_var_is_defaulted(self):
        grinfile = ['LET AAAA 3',
                    'MULT AAAA BBBB',
                    'PRINT AAAA',
                    'END']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '0\n')

    def test_file_interpreter_handles_DIV_statement_when_left_var_is_defaulted(self):
        grinfile = ['LET A 3',
                    'DIV B A',
                    'PRINT B',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '0\n')

    def test_file_interpreter_handles_DIV_statement_when_right_var_is_defaulted(self):
        grinfile = ['LET A 3',
                    'DIV A B',
                    'PRINT A',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 2: Dividing by zero is not possible.\n')

    def test_file_interpreter_handles_DIV_statement_when_both_vars_are_defaulted(self):
        grinfile = ['DIV A B',
                    'PRINT A',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 1: Dividing by zero is not possible.\n')

    def test_file_interpreter_handles_MULT_statement_when_both_vars_are_defaulted(self):
        grinfile = ['MULT A B',
                    'PRINT A',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '0\n')

    def test_file_interpreter_handles_SUB_statement_when_both_vars_are_defaulted(self):
        grinfile = ['SUB A B',
                    'PRINT A',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '0\n')

    def test_file_interpreter_handles_ADD_statement_when_both_vars_are_defaulted(self):
        grinfile = ['ADD A B',
                    'PRINT A',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '0\n')

if __name__ == '__main__':
    unittest.main()