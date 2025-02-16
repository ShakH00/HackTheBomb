def write_puzzle_info(wire_color, symbol_order, bomb_code):
    """Write puzzle information to a file that can be read by Player 2."""
    with open('puzzle_info.txt', 'w') as f:
        f.write(f"WIRE:{wire_color}\n")
        f.write(f"SYMBOLS:{','.join(symbol_order)}\n")
        f.write(f"CODE:{bomb_code}\n")

def read_puzzle_info():
    """Read puzzle information from the file."""
    try:
        with open('puzzle_info.txt', 'r') as f:
            data = {}
            for line in f:
                key, value = line.strip().split(':')
                if key == 'SYMBOLS':
                    data[key] = value.split(',')
                else:
                    data[key] = value
            return data
    except FileNotFoundError:
        print("Puzzle info file not found!")
        return None