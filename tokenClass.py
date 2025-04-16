from dataclasses import dataclass
from enum import Enum
import re


class TokenType(Enum):
    NUMBER = "number"
    VARIABLE = "variable"
    OPERATOR = "operator"
    EXPONENT = "exponent"
    EQUAL = "equal"
    UNKNOWN = "unknown"


@dataclass
class Token:
    string: str
    _type: TokenType
    _number: int = 1
    _exponent: int = 0

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type
        self.string_gen()

    @property
    def exponent(self):
        return self._exponent

    @exponent.setter
    def exponent(self, exponent):
        self._exponent = exponent
        self.string_gen()

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number
        self.string_gen()

    @staticmethod
    def tokenize_polynomial(equation: str):
        pattern = r"(\d+\.?\d*|[a-zA-Z]+|[\^\+\-\*/=()])"
        raw_tokens = re.findall(pattern, equation.replace(" ", ""))

        tokens = []
        for raw in raw_tokens:
            if raw in "+-*/":
                tokens.append(Token(raw, TokenType.OPERATOR))
            elif raw == "=":
                tokens.append(Token(raw, TokenType.EQUAL))
            elif raw == "^":
                tokens.append(Token(raw, TokenType.EXPONENT))
            elif raw.isdigit() or re.match(r"^\d+\.\d+$", raw):
                tokens.append(Token(raw, TokenType.NUMBER, _number=int(raw)))
            elif raw.isalpha():
                tokens.append(Token(raw, TokenType.VARIABLE, _exponent=1))
            else:
                tokens.append(Token(raw, TokenType.UNKNOWN))
        return tokens

    def string_gen(self):
        if self.type == TokenType.VARIABLE and self.number == 1:
            string = ""
        else:
            string = str(self.number)
        if self.type == TokenType.VARIABLE:
            string += "x"
            if self.exponent > 1:
                string += "^" + str(self.exponent)
        self.string = string
