import contextlib, io, unittest
from unittest import mock

from grin import parse, Interpret_File
from grin.Interpret_File import file_interpreter
from grin.Labels import extract_labels

class test_file_interpreter(unittest.TestCase):

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

    def test_file_interpreter_handles_GOTO_and_GOSUB(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO "LAB"',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2 IF MESS <> 5',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

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

    def test_file_interpreter_handles_multiple_GOTO_statements(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO BRO IF MESS < 4',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_GOTO_with_no_conditional(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '4\n')

    def test_file_interpreter_handles_GOTO_jumping_forward_too_much(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 7',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 5: A GOTO or GOSUB statement attempted to jump to a line that does not exist.\n')

    def test_file_interpreter_handles_GOTO_jumping_back_too_much(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO -5',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 5: A GOTO or GOSUB statement attempted to jump to a line that does not exist.\n')

    def test_file_interpreter_handles_GOTO_jumping_to_nonexistent_label(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO -5',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "HELLO"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 8: A GOTO or GOSUB statement attempted to jump to a line that does not exist.\n')

    def test_file_interpreter_handles_conditional_GOTO_using_greater_than(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 6 > MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '4\n')

    def test_file_interpreter_handles_conditional_GOTO_using_greater_than_is_False(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 2 > MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_conditional_GOTO_using_greater_than_or_eq(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 4 >= MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '4\n')

    def test_file_interpreter_handles_conditional_GOTO_using_greater_than_or_eq_is_false(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 2 >= MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_conditional_GOTO_using_less_than_or_eq_is_false(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 6 <= MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_conditional_GOTO_using_less_than(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 6 < MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_conditional_GOTO_using_less_than_or_eq(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 4 <= MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '4\n')


    def test_file_interpreter_handles_conditional_GOTO_using_eq(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 4 = MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '4\n')

    def test_file_interpreter_handles_conditional_GOTO_using_is_False(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 3 = MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_conditional_GOTO_using_not_eq_is_True(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '4\n')

    def test_file_interpreter_handles_conditional_GOTO_using_not_eq_is_False(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO 5 IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n')

    def test_file_interpreter_handles_conditional_GOTO_using_label(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 5',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '4\n')

    def test_file_interpreter_handles_infinite_GOTO(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOTO 0',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: Executing a GOTO or GOSUB statement would result in an infinite loop.\n')

    def test_file_interpreter_handles_infinite_GOTO_using_label(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOTO "LAB"',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: Executing a GOTO or GOSUB statement would result in an infinite loop.\n')

    def test_file_interpreter_handles_GOTO_using_label_and_conditional(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOTO LAB IF 2 < 4',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: Executing a GOTO or GOSUB statement would result in an infinite loop.\n')

    def test_file_interpreter_handles_GOTO_using_conditional_with_default_var(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOTO 7 IF BOO = WOW',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO CHEESE',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '3\n')

    def test_file_interpreter_handles_GOTO_using_invalid_conditional(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOTO 7 IF BOO = "WOW"',
                    'CHEESE: LET MESS 4',
                    'GOTO YO IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: The conditional expression in a GOSUB or GOTO statement cannot compare two objects due to them being different types.\n')

    def test_file_interpreter_handles_GOTO_using_invalid_label_jump(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOTO "AKENFK" IF 1 = 1',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: A GOTO or GOSUB statement attempted to jump to a line that does not exist.\n')

    def test_file_interpreter_handles_GOTO_with_incompatible_types(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOTO YO IF 1 = "WOW"',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 5 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'PRINT MESSAGE',
                    'YO: PRINT MESS',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: The conditional expression in a GOSUB or GOTO statement cannot compare two objects due to them being different types.\n')


    def test_file_interpreter_handles_return_with_no_GOSUB(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'RETURN',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO YO IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO CHEESE',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2 IF MESS > 5',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: Return statement was reached when there was no GOSUB previously called\n')

    def test_file_interpreter_handles_multiple_GOSUB_statements(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOSUB 10',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO YO IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO CHEESE',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n5\nHello Boo!\n')

    def test_file_interpreter_handles_multiple_GOSUB_conditional_statement(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOSUB 10 IF MESS < 4',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO YO IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO CHEESE',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'Hello Boo!\n5\nHello Boo!\n')

    def test_file_interpreter_handles_multiple_GOSUB_jumping_to_label(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOSUB "LAB" IF MESS < 4',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2 IF MESS > 5',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '5\nHello Boo!\n')

    def test_file_interpreter_handles_multiple_GOSUB_jumping_to_label_with_no_condition(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOSUB "LAB"',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2 IF MESS > 5',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '5\nHello Boo!\n')

    def test_file_interpreter_handles_GOSUB_statement_when_conditional_fails(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOSUB LAB IF MESS > 5',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO YO IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO CHEESE',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2 IF MESS > 5',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '5\nHello Boo!\n')

    def test_file_interpreter_handles_GOSUB_jumping_to_nonexistent_label(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOSUB "KRNGKE" IF MESS < 4',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO YO IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO CHEESE',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2 IF MESS > 5',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: A GOTO or GOSUB statement attempted to jump to a line that does not exist.\n')

    def test_file_interpreter_handles_GOSUB_jumping_to_far(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOSUB 20 IF MESS < 4',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO YO IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2 IF MESS > 5',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: A GOTO or GOSUB statement attempted to jump to a line that does not exist.\n')

    def test_file_interpreter_handles_GOSUB_jumping_to_far_back(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'GOSUB -20 IF MESS < 4',
                    'PRINT 5',
                    'CHEESE: LET MESS 4',
                    'GOTO "YO" IF 4 <> MESS',
                    'PRINT MESSAGE',
                    '.',
                    'GOTO "CHEESE"',
                    'YO: PRINT MESS',
                    'PRINT MESSAGE',
                    'RETURN',
                    'LAB: GOSUB -2 IF MESS > 5',
                    'RETURN',
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 3: A GOTO or GOSUB statement attempted to jump to a line that does not exist.\n')



if __name__ == '__main__':
    unittest.main()