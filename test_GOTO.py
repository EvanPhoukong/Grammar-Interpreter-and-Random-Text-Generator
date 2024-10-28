import contextlib, io, unittest
from unittest import mock
from grin import parse, Interpret_File
from grin.Interpret_File import file_interpreter
from grin.Labels import extract_labels


class test_GOTO(unittest.TestCase):

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

    def test_file_interpreter_handles_GOTO_using_label_and_conditional_that_fails(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOTO LAB IF 2 = 4',
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

    def test_file_interpreter_handles_multiple_GOTO_with_variable(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LET b 10',
                    'GOTO b',
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
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), '')

    def test_file_interpreter_handles_infinite_GOTO_via_label(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LET b 10',
                    'HEY: GOTO "HEY" IF 1 =1',
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
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 4: Executing a GOTO or GOSUB statement would result in an infinite loop.\n')

    def test_file_interpreter_handles_error_via_GOTO_with_label(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LET b 10',
                    'HEY: GOTO "HEY" IF 1 = "Hello"',
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
                    '.']
        for e, i in enumerate(grinfile[:]):
            if i == '.':
                grinfile[e] = 'END'
        file = [[token for token in line] for line in parse(grinfile)]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            file_interpreter(extract_labels(file))
        self.assertEqual(output.getvalue(), 'ERROR ON LINE 4: The conditional expression in a GOSUB or GOTO statement cannot compare two objects due to them being different types.\n')

if __name__ == '__main__':
    unittest.main()