from dataclasses import dataclass

from tokenClass import TokenType
import math


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
            if token.exponent in self.right_side:
                self.right_side[token.exponent] += token.number
            else:
                self.right_side[token.exponent] = token.number
            i += 1

    def __str__(self) -> str:
        def format_side(side: dict):
            side = dict(
                sorted(side.items(), key=lambda item: item[0], reverse=True)
            )
            if all(value == 0 for value in side.values()):
                return "0"
            string = ""
            for key, value in side.items():
                if value == 0:
                    continue
                if key == value == 1:
                    return "x"
                if string and value > 0:
                    string += "+"
                string += str(value)
                if key == 1:
                    string += "x"
                elif key != 0:
                    string += "x^" + str(key)
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
            else:
                self.left_side[key] = -value
        self.right_side = {}

    def solve(self):
        if not all(value == 0 for value in self.right_side.values()):
            print("not yet simplified")
            return
        highest_key = max(self.left_side.keys())
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
                print("unsolvable")
        return

    def solve_first_degree(self):
        self.right_side[0] = -self.left_side[0]
        self.left_side[0] = 0
        self.right_side[0] /= self.left_side[1]
        self.left_side[1] = 1
        print(f"solution: {self}")

    def solve_second_degree(self):
        a = self.left_side.get(2, 0)
        b = self.left_side.get(1, 0)
        c = self.left_side.get(0, 0)

        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            discriminant *= -1
            complex = True
            print("The discriminant is negative, showing complex solutions")
        else:
            complex = False
            print("The discriminant is positive, showing solutions")

        root = math.sqrt(discriminant)
        sol_base = -b / (2 * a)
        sol_add = root / (2 * a)

        if not complex:
            sol1 = str(sol_base + sol_add)
            sol2 = str(sol_base - sol_add)
        else:
            sol_base = str(sol_base)
            sol1 = sol_base
            sol1 += " + " if sol_add > 0 else " - "
            sol1 += str(sol_add) + "i"

            sol2 = sol_base
            sol2 += "-" if sol_add > 0 else " + "
            sol2 += str(sol_add) + "i"
        print(f"sol1: {sol1}\nsol2: {sol2}")
