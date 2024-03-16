from Lexer import PythonLexer
from Parser import PythonParser
from Evaluator import PythonEvaluator

if __name__ == "__main__":
    lxr = PythonLexer(file="interpreter_test.py")
    prsr = PythonParser(lxr.tokens)
    eval = PythonEvaluator(prsr.ast)
