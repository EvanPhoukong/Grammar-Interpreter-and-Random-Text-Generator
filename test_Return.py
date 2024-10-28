import contextlib, io, unittest
from unittest import mock

from grin import parse, Interpret_File
from grin.Interpret_File import file_interpreter
from grin.Labels import extract_labels

class test_Arithmetic(unittest.TestCase):

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
        self.assertEqual(output.getvalue(),
                         'ERROR ON LINE 3: Return statement was reached when there was no GOSUB previously called\n')

if __name__ == '__main__':
    unittest.main()