import random


class GameState:
    def __init__(self):
        # Generate game parameters
        self.bomb_number_code = str(random.randint(1000, 9999))
        self.correct_bomb_number_code = self.bomb_number_code
        self.symbols = ["%", "!", ";", "&"]
        self.choose_symbol_order = random.sample(self.symbols, len(self.symbols))
        self.correct_symbol_order = self.choose_symbol_order
        self.wire_colors = ["red", "green", "blue"]
        self.choose_wire = random.choice(self.wire_colors)
        self.correct_wire = self.choose_wire

        # Generate encrypted wire data
        self.shift_count = random.randint(1, 25)
        self.encrypted_wire = self.caesar_cipher_custom_shift(self.correct_wire, self.shift_count)
        self.encrypted_hint = self.caesar_cipher_custom_shift("A", self.shift_count)

        # Generate symbol clues
        self.symbol_clues = self.generate_logic_clues()

        # Generate math equations
        self.math_equations = self.generate_math_equations_from_code()

        # Create puzzle list
        self.puzzles = [
            {"type": "decrypt", "question": f"Decrypt: {self.encrypted_wire}, using A -> {self.encrypted_hint}",
             "answer": self.correct_wire},
            {"type": "symbol",
             "question": f"Enter the correct symbol order: %, !, ;, &, using only these clues \n {self.symbol_clues}",
             "answer": "".join(self.correct_symbol_order)},
            {"type": "code", "question": f"Crack the bomb code:\n {self.math_equations}",
             "answer": self.correct_bomb_number_code}
        ]

    def caesar_cipher_custom_shift(self, message, shift):
        encrypted_message = ""
        for char in message:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                encrypted_message += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            else:
                encrypted_message += char
        return encrypted_message

    def generate_logic_clues(self):
        clues = []
        index_map = {symbol: i for i, symbol in enumerate(self.correct_symbol_order)}

        clues.append(f"The {self.correct_symbol_order[1]} comes after the {self.correct_symbol_order[0]}.")
        clues.append(f"The {self.correct_symbol_order[2]} is before the {self.correct_symbol_order[3]}.")

        if index_map["!"] != 3:
            clues.append("The ! is not the last symbol.")
        if index_map["&"] > index_map[";"]:
            clues.append("The & comes after the ;.")
        if index_map["%"] < index_map["!"]:
            clues.append("The % comes before the !.")

        return clues

    def generate_math_equations_from_code(self):
        equations = []
        for digit in self.correct_bomb_number_code:
            target_result = int(digit)
            operation = random.choice(["+", "-", "*", "/"])

            if operation == "+":
                num1 = random.randint(1, target_result)
                num2 = target_result - num1
            elif operation == "-":
                num1 = random.randint(target_result, 9)
                num2 = num1 - target_result
            elif operation == "*":
                possible_factors = [i for i in range(1, 10) if target_result % i == 0]
                num1 = random.choice(possible_factors) if possible_factors else 1
                num2 = target_result // num1
            else:  # division
                num2 = random.randint(1, 5)
                num1 = target_result * num2

            equation = f"{num1} {operation} {num2} = ?"
            equations.append(equation)

        return equations

    def generate_puzzle(self, i):

        return self.puzzles[i]