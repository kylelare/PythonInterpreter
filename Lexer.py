from Tokenizer import PythonTokenizer, Token


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
                    for _ in line:
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
                                    # Check if we're in the middle of lexing a double operator token
                                    elif any(c in self.tokenizer.operator_map for c in chunk):
                                        chunk = chunk + char
                                        self.chars.append(chunk)
                                        chunk = ""

                                    # decide if MINUS is being used for negation
                                    elif char == "-":
                                        if char_peek.isdigit() and not chunk.isalpha():
                                            self.chars.append(chunk)
                                            chunk = f"{char}"
                                        else:
                                            self.chars.append(chunk)
                                            self.chars.append(char)
                                            chunk = ""
                                    # handling comments
                                    elif char == "#":
                                        comment_started = True
                                        self.chars.append(chunk)
                                        chunk = ""
                                    # handling items in quotes
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

                # check if sting is an indent
                if string == "    ":
                    token = Token(type="INDENT", literal=string)
                    self.tokens.append(token)

                elif len(string) > 0:
                    # strip any whitespace from string
                    string = string.strip()

                    # check if char is digit string
                    if string.isdigit():
                        token = Token(type="NUMBER", literal=string)
                        self.tokens.append(token)

                    elif string.isalnum():
                        token = Token(type="IDENTIFIER", literal=string)
                        self.tokens.append(token)

                    elif string.startswith('"') and string.endswith('"') or string.startswith("'") and string.endswith("'"):
                        token = Token(type="STRING", literal=string)
                        self.tokens.append(token)

                    elif string.startswith("-") and string[1:].isnumeric():
                        token = Token(type="NUMBER", literal=string)
                        self.tokens.append(token)

                    else:
                        token = Token(type="ILLEGAL", literal=string)
                        self.tokens.append(token)

        # Add token for EOF
        self.tokens.append(Token(type="EOF", literal="EOF"))
