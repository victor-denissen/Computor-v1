import argparse
from tokenClass import Token, TokenType
from equationClass import equation as eq_class


def insert_exponent(tokens):
    i = 0
    last_token = tokens[0]
    while i < len(tokens):
        token = tokens[i]
        if token.type == TokenType.VARIABLE or token.type == TokenType.NUMBER:
            last_token = token  # Store last seen variable
            i += 1
            continue
        if token.type == TokenType.EXPONENT:
            del tokens[i]  # Delete exponent operator
            if last_token.type == TokenType.VARIABLE:
                last_token.exponent = tokens[i].number
            else:
                last_token.number = last_token.number ** tokens[i].number
            del tokens[i]  # Delete exponent number
            continue
        i += 1


def insert_multiply(tokens):
    i = 1
    while i < len(tokens):
        if tokens[i].type == TokenType.VARIABLE:
            if tokens[i - 1].type == TokenType.NUMBER:
                tokens[i].number *= tokens[i - 1].number
                del tokens[i - 1]
                continue
        i += 1


def insert_negative(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i].string == "-":
            if tokens[i + 1]:
                tokens[i + 1].number *= -1
                del tokens[i]
                continue
        i += 1


def multiply(tokens, index1, index2):
    token1: Token = tokens[index1]
    token2: Token = tokens[index2]
    result = token1.number * token2.number

    if token2.type == TokenType.VARIABLE or token1.type == TokenType.VARIABLE:
        token1.exponent += token2.exponent
    if token2.type == TokenType.VARIABLE or token1.type == TokenType.VARIABLE:
        token1.type = TokenType.VARIABLE

    token1.number = result
    del tokens[index2]
    pass


def solve_multiplication(tokens):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.string == "*":
            multiply(tokens, i - 1, i + 1)
            tokens.remove(tokens[i])
            continue
        i += 1

def remove_irrelevant(tokens):
    i = 0;
    while i < len(tokens):
        token = tokens[i]
        if token.type != TokenType.VARIABLE and token.type != TokenType.NUMBER:
            if token.type == TokenType.EQUAL:
                i += 1
                continue
            tokens.remove(token)
            continue
        if token._number == 0.0:
            tokens.remove(token)
            continue
        if token.exponent == 0:
            token.type = TokenType.NUMBER
            token.string_gen()
        i += 1



def main():
    parser = argparse.ArgumentParser(description="polynomial equation")
    parser.add_argument("equation", help="the equation to solve")

    program_args = parser.parse_args()

    equation_str = program_args.equation

    tokens = Token.tokenize_polynomial(equation_str)

    # for token in tokens:
    #     print(token)
    # print()

    insert_negative(tokens)

    insert_exponent(tokens)

    insert_multiply(tokens)

    solve_multiplication(tokens)

    remove_irrelevant(tokens)

    equation = eq_class(tokens)

    equation.simplify()

    print(f"siplified: {equation}")

    equation.solve()

    pass


if __name__ == "__main__":
    main()
