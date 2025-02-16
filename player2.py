import socket
import time
import random

HOST = "localhost"
PORT = 5555

puzzles = [
    {"type": "math", "question": "Solve: 12 + 8", "answer": "20"},
    {"type": "logic", "question": "True or False: Fire is cold?", "answer": "False"},
    {"type": "wire", "question": "Which wire should be cut first? (red, green, blue)", "answer": "red"},
    {"type": "symbol", "question": "Enter the correct symbol order: Ω, ∑, Ψ, ★", "answer": "Ω,∑,Ψ,★"},
    {"type": "code", "question": "Crack the bomb code: 3 + 5 - 4 * 2", "answer": "0"}
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
