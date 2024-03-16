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
        self.operator_map["!"] = "NEGATION"

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
