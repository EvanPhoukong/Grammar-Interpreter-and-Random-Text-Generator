import contextlib, io, unittest
from unittest import mock

from grin import parse, Interpret_File
from grin.Interpret_File import file_interpreter
from grin.Labels import extract_labels

class test_GOSUB(unittest.TestCase):
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

    def test_file_interpreter_handles_multiple_GOSUB_with_variable(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LET b 10',
                    'GOSUB b',
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

    def test_file_interpreter_handles_infinite_GOSUB_via_label(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LET b 10',
                    'HEY: GOSUB "HEY" IF 1 = 1',
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

    def test_file_interpreter_handles_error_via_GOSUB_with_label(self):
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

    def test_file_interpreter_handles_GOSUB_using_label_and_conditional_that_fails(self):
        grinfile = ['BRO: LET MESSAGE "Hello Boo!"',
                    'LET MESS 3',
                    'LAB: GOSUB 5 IF 2 = 4',
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

if __name__ == '__main__':
    unittest.main()