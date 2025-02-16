# HackTheBomb
## Submission for CalgaryHacks2025 - Topic 3

## Getting Started
1. Ensure Python and Pygame are installed
2. Clone the repository
3. Run `main.py` to start the game
4. Select roles for each player (Defuser or Expert)
5. Begin defusing!

**If you are playing on different devices:**
1. **Hamachi/VPN** required in order to connect via socket
2. The following are needed:

- In `player1.py`: player1 has his own ip in player1.py
  - Can be seen in line 133 of `player1.py`

``HOST = "player1's ip"`` replace string with ip

- In `player2.py`: player2 has player1's ip in player2.py
  - Can be seen in line 41 of `player2.py`

``HOST = "player2's ip"`` replace string with ip

3. Player 1 runs `player1.py` and must do the following:

- Send `puzzle_info.txt` data (that has been generated by running `player1.py`) to player 2
- Player 2 replaces the current `puzzle_info.txt` to match player 1's

4. Player 2 runs `player2.py`

Note: It is buggy.

## Controls
### Defuser (Player 1):
- Mouse to interact with bomb components
- Number keys for code input
- Click to cut wires
- Click to input symbols

### Expert (Player 2):
- Mouse to select modules and send messages
- Keyboard for custom message input
- Quick message buttons for common instructions

## Inspiration
HackTheBomb was inspired by the high-stakes collaborative gameplay of games like "Keep Talking and Nobody Explodes." We wanted to create an experience that tests not just individual problem-solving skills, but also communication and teamwork under pressure. The concept of having one player with the manual and another with the bomb creates an intense dynamic where clear communication becomes literally a matter of virtual life and death.

## What it does
HackTheBomb is a two-player collaborative puzzle game where players must work together to defuse a virtual bomb. The game features:

- **Player 1 (Defuser)**: Interacts with a graphical bomb interface containing:
  - Three colored wires (red, green, blue)
  - A symbol keypad with four symbols (%, !, ;, &)
  - A numerical code input system
  - A countdown timer
  - A detonator button
  - Visual feedback for all interactions

- **Player 2 (Expert)**: Has access to:
  - A terminal-style interface with the bomb defusal manual
  - Detailed instructions for each module
  - Quick-message system for urgent communication
  - Custom message input for detailed instructions
  - Module-specific puzzle information

## How we built it
The game was built using:

- **Technologies**:
   - Python as the primary programming language
   - Pygame for graphics and game mechanics
   - Socket programming for player communication using Hamachi
   - File I/O for sharing puzzle information

- **Components**:
   - `main.py`: Game launcher with player role selection
   - `game_state.py`: Central game logic and puzzle generation
   - `player1.py`: Defuser interface and bomb mechanics
   - `player2.py`: Expert interface and manual system
   - `utility.py`: Shared utility functions for file operations

- **Game Mechanics**:
   - Randomized puzzle generation for replayability
   - Real-time network communication between players
   - Multi-module puzzle system
   - Timer-based gameplay
   - State management for puzzle completion

## Challenges we ran into
- **Networking Complexity**: Implementing reliable real-time communication between the two players required careful handling of socket programming and data synchronization.

- **State Management**: Coordinating game state between two separate applications while maintaining consistency proved challenging, especially with multiple puzzle modules.

- **User Interface Design**: Creating an intuitive interface for both players that could convey complex information without overwhelming them required multiple iterations.

- **Puzzle Generation**: Developing a system that could generate random but solvable puzzles while maintaining game balance was particularly challenging.

- **Error Handling**: Implementing robust error handling for network disconnections, incorrect inputs, and various edge cases required significant testing and refinement.

## Accomplishments that we're proud of
1. Created a fully functional multiplayer game with real-time communication
2. Implemented an engaging puzzle system with multiple modules
3. Developed a clean and intuitive user interface for both players
4. Successfully integrated randomized puzzle generation
5. Created a balanced difficulty curve that challenges players without frustrating them

## What we learned
- Advanced Pygame development techniques
- Network programming with sockets in Python
- State management in multiplayer applications
- User interface design principles
- Game balance and puzzle design
- Error handling in networked applications
- The importance of clear communication in collaborative games

## What's next for HackTheBomb
1. **Additional Puzzle Modules**:
   - Morse code module
   - Pattern recognition puzzles
   - Color sequence challenges
   - Sound-based puzzles

2. **Enhanced Features**:
   - Difficulty levels
   - Custom puzzle creation tools
   - Achievement system
   - Tutorial mode
   - Leaderboards

3. **Technical Improvements**:
   - Cross-platform compatibility
   - Enhanced graphics and animations
   - Improved network stability
   - Save/load functionality
   - Spectator mode

## Built With
- Python
- Pygame
- Socket Programming
  - Hamachi/FortiClientVPN
- File I/O
- Random Number Generation
- Caesar Cipher Encryption
- Event-Driven Programming
- Object-Oriented Design
- 

## Screenshots
You can view them in the [screenshots](https://github.com/ShakH00/HackTheBomb/tree/main/screenshots) directory
