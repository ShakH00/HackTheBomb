import socket
import time
import random
import player1

HOST = "localhost"
PORT = 5555

correct_code = player1.bomb_number_code
correct_symbols = player1.correct_symbol_order
correct_wire = player1.correct_wire
def caesar_cipher_custom_shift(message, shift):
    """Encrypt a message using a specified Caesar cipher shift."""
    encrypted_message = ""

    for char in message:
        if char.isalpha():  # Only shift letters
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted_message += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted_message += char  # Keep spaces and punctuation unchanged

    return encrypted_message

shift_count = random.randint(1, 25)
encrypted_wire = caesar_cipher_custom_shift(correct_wire, shift_count)
encrypted_hint = caesar_cipher_custom_shift("A", shift_count)


def generate_logic_clues(symbol_order):
    """Generate logic clues based on the shuffled symbol order."""
    clues = []

    # Get the indexes of each symbol
    index_map = {symbol: i for i, symbol in enumerate(symbol_order)}

    # Generate clues based on their positions
    clues.append(f"The {symbol_order[1]} comes after the {symbol_order[0]}.")  # First clue
    clues.append(f"The {symbol_order[2]} is before the {symbol_order[3]}.")  # Second clue

    # Additional logic constraints
    if index_map["Ω"] != 3:  # Ω is not the last symbol
        clues.append("The Ω is not the last symbol.")
    if index_map["∑"] > index_map["Ψ"]:  # ∑ comes after Ψ
        clues.append("The ∑ comes after the Ψ.")
    if index_map["%"] < index_map["Ω"]:  # ★ comes before Ω
        clues.append("The % comes before the Ω.")

    return clues

clues = generate_logic_clues(correct_symbols)


def generate_math_equations_from_code(code):
    """Generate four math equations where each solution matches a digit in the given 4-digit code."""
    if len(code) != 4 or not code.isdigit():
        raise ValueError("The input code must be exactly 4 digits long.")

    equations = []
    for digit in code:
        target_result = int(digit)

        operation = random.choice(["+", "-", "*", "/"])

        if operation == "+":
            num1 = random.randint(1, target_result)
            num2 = target_result - num1  # Ensure the sum equals the digit

        elif operation == "-":
            num1 = random.randint(target_result, 9)
            num2 = num1 - target_result  # Ensure result matches the digit

        elif operation == "*":
            possible_factors = [i for i in range(1, 10) if target_result % i == 0]  # Find valid factors
            num1 = random.choice(possible_factors)
            num2 = target_result // num1  # Ensure multiplication result matches digit

        elif operation == "/":
            num2 = random.randint(1, 5)  # Small divisor
            num1 = target_result * num2  # Ensure result matches digit
            equation = f"{num1} {operation} {num2} = ?"

        equation = f"{num1} {operation} {num2} = ?"
        equations.append(equation)

    return equations  # Return the generated equations

math_equation = generate_math_equations_from_code(correct_code)

puzzles = [
    {"type": "decipher", "question": f"Decrypt: {encrypted_wire}, using {encrypted_hint}", "answer": correct_wire},
    {"type": "symbol", "question": f"Enter the correct symbol order: Ω, ∑, Ψ, %, using only these clues \n {clues}", "answer": correct_symbols},
    {"type": "code", "question": f"Crack the bomb code:\n {math_equation}", "answer": correct_code}
]

def generate_puzzle():
    return random.choice(puzzles)

def main():
    print("Player 2 (Expert) is connecting to Player 1...")
    time.sleep(2)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to Player 1!")

        while True:
            puzzle = generate_puzzle()
            print("\nPUZZLE:", puzzle["question"])
            user_answer = input("Enter your answer: ").strip()

            if user_answer.lower() == puzzle["answer"].lower():
                print("Correct Answer! Sending info to Player 1...")
                s.sendall(f"SOLUTION: {user_answer}".encode())
            else:
                print("Incorrect! Try again.")

            time.sleep(2)

if __name__ == "__main__":
    main()
