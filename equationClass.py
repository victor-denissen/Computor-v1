from dataclasses import dataclass

from tokenClass import TokenType


@dataclass
class equation:
    left_side = {}

    right_side = {}

    def __init__(self, tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]
            t = token.type
            if t == TokenType.EQUAL:
                break
            if t == TokenType.VARIABLE or t == TokenType.NUMBER:
                if token.exponent in self.left_side:
                    self.left_side[token.exponent] += token.number
                else:
                    self.left_side[token.exponent] = token.number
            i += 1
        i += 1
        while i < len(tokens):
            token = tokens[i]
            t = token.type
            if t == TokenType.VARIABLE or t == TokenType.NUMBER:
                if token.exponent in self.right_side:
                    self.right_side[token.exponent] += token.number
                else:
                    self.right_side[token.exponent] = token.number
            i += 1

    def print(self):
        for key in self.left_side.keys():
            print(f"{key}:{self.left_side[key]}")
        print("=")
        for key in self.right_side.keys():
            print(f"{key}:{self.right_side[key]}")

    def __str__(self) -> str:
        def format_side(side: dict):
            side = dict(
                sorted(side.items(), key=lambda item: (item[0] == 0, -item[0]))
            )
            if all(value == 0 for value in side.values()):
                return "0"
            string = ""
            """
                [value]x^[key]
            """
            for key, value in side.items():
                if value == 0:  # nothing to print if value == 0
                    continue
                # check if the + between values need to be pronted
                if string and value > 0:
                    string += "+"

                # The logic if printing the number itself
                if key == 0 or value != 1:
                    if value == -1 and key != 0:
                        string += "-"
                    elif value % 1 == 0:
                        string += str(int(value))
                    else:
                        string += str(value)

                if key != 0 and value != 0:
                    string += "x"

                if value != 0 and key != 1 and key != 0:
                    string += "^"
                    if key % 1 == 0:
                        string += str(int(key))
                    else:
                        string += str(key)
            return string

        left = format_side(
            self.left_side,
        )
        right = format_side(
            self.right_side,
        )
        return f"{left}={right}"

    def simplify(self):
        for key, value in self.right_side.items():
            if key in self.left_side:
                self.left_side[key] -= value
                if self.left_side[key] == 0:
                    del self.left_side[key]
            else:
                self.left_side[key] = -value
        self.right_side = {}

    def solve(self):
        if not all(value == 0 for value in self.right_side.values()):
            print("not yet simplified")
            return
        if self.left_side.keys():
            highest_key = max(self.left_side.keys())
            lowest_key = min(self.left_side.keys())
        else:
            highest_key = 0
            lowest_key = 0
        if lowest_key < 0:
            print("negative exponent")
            return
        match highest_key:
            case 0:
                if self.left_side.get(0, 0) == self.right_side.get(0, 0):
                    print("Any input for x will solve")
                else:
                    print("No input for x will solve")
            case 1:
                self.solve_first_degree()
            case 2:
                self.solve_second_degree()
            case _:
                print("Non [0,1,2] exponent, I will not solve")
        return

    def solve_first_degree(self):
        self.right_side[0] = -self.left_side.get(0, 0)
        self.left_side[0] = 0
        self.print()

        self.right_side[0] /= self.left_side.get(1, 1)
        self.left_side[1] = 1

        self.print()

        print(f"solution: {self}")

    def solve_second_degree(self):
        a = self.left_side.get(2, 0)
        b = self.left_side.get(1, 0)
        c = self.left_side.get(0, 0)

        discriminant = b**2 - 4 * a * c
        sol_base = -b / (2 * a)
        if discriminant == 0:
            print("The discriminant is 0, showing solution")
            sol = str(sol_base)
            print(f"sol: {sol}")
            return

        if discriminant > 0:
            root = discriminant ** (1 / 2)
            sol_add = root / (2 * a)
            print("The discriminant is positive, showing solutions")
            sol1 = str(sol_base + sol_add)
            sol2 = str(sol_base - sol_add)
            print(f"sol1: {sol1}\nsol2: {sol2}")
        else:
            print("The discriminant is negative, showing complex solutions")
            discriminant *= -1
            root = discriminant ** (1 / 2)
            sol_add = root / (2 * a)
            sol_base = str(sol_base)
            sol1 = sol_base
            sol1 += " + " if sol_add > 0 else " - "
            sol1 += str(sol_add) + "i"

            sol2 = sol_base
            sol2 += " - " if sol_add > 0 else " + "
            sol2 += str(sol_add) + "i"
            print(f"sol1: {sol1}\nsol2: {sol2}")
