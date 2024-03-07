"""
Python Interpreter for Interpreting Python Code
"""

# Todo make negative numbers and prefix operators work
# Todo make code blocks work
# Todo make if x in n work

from pydantic import BaseModel


class Token(BaseModel):
    type: str
    literal: str


class PythonTokenizer:

    def __init__(self):
        self.operator_map = {}
        self.dbl_operator_map = {}
        self.keyword_map = {}

        self.build_single_operator_map()
        self.build_double_operator_map()
        self.build_keyword_map()

    def build_single_operator_map(self):
        # symbols
        self.operator_map[':'] = "COLON"
        self.operator_map[';'] = "SEMICOLON"
        self.operator_map[','] = "COMMA"
        self.operator_map['('] = "LPAREN"
        self.operator_map[')'] = "RPAREN"
        self.operator_map['['] = "LBRACKET"
        self.operator_map[']'] = "RBRACKET"
        self.operator_map['{'] = "LCURLYPAREN"
        self.operator_map['}'] = "RCURLYPAREN"
        self.operator_map['\n'] = "NEWLINE"
        self.operator_map['"'] = "DOUBLEQUOTE"
        self.operator_map["'"] = "SINGLEQUOTE"
        self.operator_map["#"] = "COMMENTSTART"

        # arithmatic
        self.operator_map["+"] = "PLUS"
        self.operator_map["-"] = "MINUS"
        self.operator_map["*"] = "TIMES"
        self.operator_map["/"] = "DIV"
        self.operator_map["%"] = "MODULO"

        # comparison
        self.operator_map["="] = "EQUALS"
        self.operator_map[">"] = "GREATERTHAN"
        self.operator_map["<"] = "LESSTHAN"

    def build_double_operator_map(self):
        self.dbl_operator_map["=="] = "ISEQUAL"
        self.dbl_operator_map["!="] = "ISUNEQUAL"
        self.dbl_operator_map[">="] = "GREATERTHANOREQUALTO"
        self.dbl_operator_map["<="] = "LESSTHANOREQUALTO"

    def build_keyword_map(self):
        self.keyword_map["if"] = "IF"
        self.keyword_map["elif"] = "ELSEIF"
        self.keyword_map["else"] = "ELSE"
        self.keyword_map["for"] = "FOR"
        self.keyword_map["is"] = "IS"
        self.keyword_map["in"] = "IN"
        self.keyword_map["print"] = "PRINT"
        self.keyword_map["def"] = "DEFINE"
        self.keyword_map["return"] = "RETURN"
        self.keyword_map["and"] = "AND"
        self.keyword_map["or"] = "OR"
        self.keyword_map["not"] = "NOT"
        self.keyword_map["True"] = "TRUE"
        self.keyword_map["False"] = "FALSE"
        self.keyword_map["pass"] = "PASS"


class PythonLexer:

    def __init__(self, file):
        self.token_map = {}
        self.chars = []
        self.tokens = []
        self.tokenizer = PythonTokenizer()
        self.get_tokens_from_file(file=file)
        self.tokenize()

    def get_tokens_from_file(self, file):
        with open(file, "r") as test:
            quote_started = False
            for line in test:
                comment_started = False
                line_idx = -1
                chunk = ""

                if len(line) > 1:  # skipping lines only containing newline character
                    for c in line:
                        line_idx += 1
                        char = line[line_idx]
                        if line_idx < len(line) - 1 and not comment_started:
                            char_peek = line[line_idx + 1]

                            if quote_started:
                                chunk = chunk + char
                                if char == "'" or char == '"':
                                    quote_started = False
                                    self.chars.append(chunk)
                                    chunk = ""
                            else:
                                # handling spaces and tabs
                                if char == " ":
                                    if char_peek != " ":
                                        # finish tab
                                        if chunk == "   ":
                                            chunk = chunk + " "
                                            self.chars.append(chunk)
                                            chunk = ""
                                        else:
                                            self.chars.append(chunk)
                                            chunk = ""
                                    else:
                                        chunk = chunk + " "
                                        # group 4 spaces to be an indent
                                        if chunk == "    ":
                                            self.chars.append(chunk)
                                elif char + char_peek == "\n":
                                    self.chars.append(chunk)
                                    self.chars.append(char)
                                    chunk = ""
                                elif char in self.tokenizer.operator_map:
                                    # Check if it's a double operator
                                    if char + char_peek in self.tokenizer.dbl_operator_map:
                                        self.chars.append(chunk)
                                        chunk = f"{char}"
                                    # Check if we're in the middle of parsing a double token
                                    elif any(c in self.tokenizer.operator_map for c in chunk):
                                        chunk = chunk + char
                                        self.chars.append(chunk)
                                        chunk = ""
                                    elif char == "#":
                                        comment_started = True
                                        self.chars.append(chunk)
                                        chunk = ""
                                    elif char == '"' or char == "'":
                                        quote_started = True
                                        self.chars.append(chunk)
                                        chunk = f"{char}"
                                    # We hit single operator; append current chunk and then append operator
                                    else:
                                        self.chars.append(chunk)
                                        self.chars.append(char)
                                        chunk = ""
                                else:
                                    chunk = chunk + char

                        # handle end of line characters
                        else:
                            if char == "\n":
                                self.chars.append(chunk)
                                self.chars.append(char)
                                chunk = ""

    def tokenize(self):
        print("Tokenizing:", self.chars)

        for string in self.chars:

            # check if character is a keyword
            keyword_check = self.tokenizer.keyword_map.get(string, False)
            if keyword_check:
                token = Token(type=keyword_check, literal=string)
                self.tokens.append(token)

            # check if character is an operator
            operator_check = self.tokenizer.operator_map.get(string, False)
            if operator_check:
                token = Token(type=operator_check, literal=string)
                self.tokens.append(token)

            # check if character is a double operator
            dbl_operator_check = self.tokenizer.dbl_operator_map.get(string, False)
            if dbl_operator_check:
                token = Token(type=dbl_operator_check, literal=string)
                self.tokens.append(token)

            if not operator_check and not dbl_operator_check and not keyword_check:

                if len(string) == 0:
                    # Hit whitespace, we can just eat them by ignoring them here
                    pass

                # check if sting is an indent
                elif string == "    ":
                    token = Token(type="INDENT", literal=string)
                    self.tokens.append(token)

                # check if char is digit string
                elif string.isdigit():
                    token = Token(type="NUMBER", literal=string)
                    self.tokens.append(token)

                elif string.isalnum():
                    token = Token(type="IDENTIFIER", literal=string)
                    self.tokens.append(token)

                else:
                    token = Token(type="ILLEGAL", literal=string)
                    self.tokens.append(token)

        # Add token for EOF
        self.tokens.append(Token(type="EOF", literal="EOF"))
        print(self.tokens)


class BinaryOperatorNode(BaseModel):
    left: str = None
    operator: str = None
    right: str = None


class ExpressionNode(BaseModel):
    left: str = None
    operator: str = None
    right: str = None


class LoopNode(BaseModel):
    loop_type: str = None
    left: str = None
    comparison: str = None
    right: str = None


class PythonParser:
    """
    Using LL(1) parser
    """

    def __init__(self, lexed_tokens=None):
        self.tokens = lexed_tokens
        self.ast = []
        self.current_token = None
        self.next_token = None
        self.index = 0
        self.advance()  # initialize
        self.parse_tokens()

    def parse_tokens(self):

        while self.current_token.type != "EOF":
            if self.current_token.type in "IF":
                self.parse_if_statement()

            elif self.next_token.type in ("EQUALS", "PLUS", "MINUS", "TIMES", "DIV", "MODULO"):
                self.parse_binary_op_statement()

            self.advance()

    def advance(self):
        self.current_token = self.tokens[self.index]
        if self.index < len(self.tokens) - 1:
            self.next_token = self.tokens[self.index + 1]
            self.index += 1
        else:
            # Hit EOF
            self.next_token = None

    def parse_expression(self):
        left = self.current_token.literal
        self.advance()
        operator = self.current_token.literal
        self.advance()
        right = self.current_token.literal
        exp_node = ExpressionNode(left=left, operator=operator, right=right)
        self.ast.append(exp_node)

    def parse_if_statement(self):
        print("if")
        loop_type = self.current_token.type
        self.advance()
        left = self.current_token.literal
        self.advance()
        op = self.current_token.literal

        if op == "in":
            print("hit in", self.current_token)
            self.advance()
            print("hit in", self.current_token)

            self.parse_expression()
        else:
            self.advance()
            right = self.current_token.literal
            # advance once more to get colon
            self.advance()
            if self.current_token.type != "COLON":
                print(loop_type, left, op, right)
                raise SyntaxError("Missing semicolon")
            # skip newline
            self.advance()
            # check for indent on next line
            self.advance()
            if self.current_token.type != "INDENT":
                print(self.current_token.type)
                raise SyntaxError("Missing indent")
            if_node = LoopNode(loop_type=loop_type, left=left, comparison=op, right=right)
            self.ast.append(if_node)

    def parse_binary_op_statement(self):
        print("parsing statement")

        identifier = self.current_token.literal
        self.advance()
        operator = self.current_token.literal
        self.advance()
        value = self.current_token.literal

        bop = BinaryOperatorNode(left=identifier, operator=operator, right=value)
        self.ast.append(bop)
        print(self.ast)


class PythonEvaluator:
    def __init__(self, ast=None):
        self.ast = ast
        self.eval_ast()

    def eval_ast(self):
        print("evaluating AST:", self.ast)

        for node in self.ast:
            print(node)


if __name__ == "__main__":
    lxr = PythonLexer(file="interpreter_test.py")
    prsr = PythonParser(lxr.tokens)
    eval = PythonEvaluator(prsr.ast)
