from pydantic import BaseModel
from Tokenizer import PythonTokenizer, Token


class BinaryOperatorStatementNode(BaseModel):
    left: str = None
    operator: str = None
    right: str = None


class ExpressionNode(BaseModel):
    left: str = None
    operator: str = None
    right: str = None


class IfNode(BaseModel):
    condition: ExpressionNode = None
    statement: str = None


class StatementNode(BaseModel):
    statement: Token = None


class FunctionCallNode(BaseModel):
    function_name: str
    arguments: list = None
    keyword_arguments: list = None


class PythonParser:
    """
    LL(1) parser. This is still a WIP.
    """

    def __init__(self, lexed_tokens=None):
        print("Parsing the following items:", lexed_tokens)
        self.tokenizer = PythonTokenizer()
        self.tokens = lexed_tokens
        self.ast = []
        self.current_token = None
        self.next_token = None
        self.index = 0
        self.advance()  # initialize
        self.parse_tokens()

    def parse_tokens(self):

        while self.current_token.type != "EOF":

            # TODO Finish Keyword Support
            #if self.current_token.literal in self.tokenizer.keyword_map:
            #    print("parsing statement", self.current_token.literal, self.next_token.literal)
            #
            #    #keyword = self.current_token.literal

            if self.next_token.type in ("PLUS", "MINUS", "TIMES", "DIV", "MODULO"):
                self.parse_expression()

            elif self.next_token.type == "EQUALS":
                if self.current_token.type == "IDENTIFIER":
                    identifier = self.current_token.literal
                    self.advance()

                    #if self.next_token.type == "LPAREN":
                    #    # TODO Finish grouped expression support
                    #    #self.parse_grouped_expression()
                    #    pass
                    #else:
                    self.parse_binary_op_statement(left=identifier)

            elif self.current_token.type == "IDENTIFIER":
                self.parse_expression()

            #print("Current AST:", self.ast)
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

    def parse_grouped_expression(self):
        while self.current_token.type != "RPAREN":
            # Todo finish adding logic for grouped expression
            self.advance()

    def parse_if_expression(self):
        # TODO finish if statement logic

        # current token is if
        self.advance()

        # parse condition expressions
        # parse elifs
        # parse else

    def parse_binary_op_statement(self, left=None):
        if left is None:
            left = self.current_token.literal
            self.advance()
        operator = self.current_token.literal
        self.advance()
        right = self.current_token.literal
        bop = BinaryOperatorStatementNode(left=left, operator=operator, right=right)
        self.ast.append(bop)
