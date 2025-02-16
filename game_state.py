import random
from utility import write_puzzle_info, read_puzzle_info


class GameState:
    def __init__(self):
        self.bomb_number_code = None
        self.correct_wire = None
        self.correct_symbol_order = None
        self.puzzles = None
        self.puzzle_info = None
        self.initialized = False

    def initialize(self):
        if not self.initialized:
            self.bomb_number_code = str(random.randint(1000, 9999))
            self.correct_wire = random.choice(["red", "green", "blue"])
            self.correct_symbol_order = random.sample(["%", "!", ";", "&"], 4)
            self.generate_puzzles()
            write_puzzle_info(self.correct_wire, self.correct_symbol_order, self.bomb_number_code)
            self.initialized = True

    def generate_puzzles(self):
        shift_count = random.randint(1, 25)
        encrypted_wire = self.caesar_cipher_custom_shift(self.correct_wire, shift_count)
        encrypted_hint = self.caesar_cipher_custom_shift("A", shift_count)
        symbol_clues = self.generate_logic_clues()
        math_equations = self.generate_math_equations_from_code()

        self.puzzles = [
            {"type": "decrypt",
             "question": f"Decrypt: {encrypted_wire}, using A -> {encrypted_hint}",
             "answer": self.correct_wire},
            {"type": "symbol",
             "question": f"Enter the correct symbol order: %, !, ;, &, using only these clues -> {symbol_clues}",
             "answer": "".join(self.correct_symbol_order)},
            {"type": "code",
             "question": f"Crack the bomb code: -> {math_equations}",
             "answer": self.bomb_number_code}
        ]

    # Getters
    def get_bomb_code(self):
        return self.bomb_number_code

    def get_correct_wire(self):
        return self.correct_wire

    def get_symbol_order(self):
        return self.correct_symbol_order

    def get_puzzle(self, index):
        if not self.puzzles:
            return None
        return self.puzzles[index]

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
        for digit in self.bomb_number_code:
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

    def load_puzzle_info(self):
        """Load puzzle information from file (Player 2)."""
        self.puzzle_info = read_puzzle_info()
        if self.puzzle_info:
            self.correct_wire = self.puzzle_info['WIRE']
            self.correct_symbol_order = self.puzzle_info['SYMBOLS']
            self.bomb_number_code = self.puzzle_info['CODE']
            self.generate_puzzles()
            self.initialized = True
            return True
        return False