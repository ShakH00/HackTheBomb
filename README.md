# HackTheBomb
This is a game that requires collaboration between 2 players, where the individual titled as player one is meant to try and difuse a bomb with limited time. The  player is meant to know none of the answers except by means of communication. Player 2 has access to a manual that guides them to explaining to their teammate how to disarm the bomb.
## Files:
- main.py
  - this is the code that you run in order to run the game. It can be found in the main project file and contains the code for the title screen and calls on the other files as need for the game to run.
- game_state.py
  - This file is the mediator between player1 and player2 file, where player1.py sends the answers needed to disarm the bomb and player2 receives that information for the user to try and decipher. It can be found in the project files.
- player1.py
  - This file contains the UI and logic of the player1 role. It can be found in the project files and it contains the bomb visuals that the user will see.
- player2.py
  - This file contains the UI and logic for player2. It can be found in the project files and it consists of the manual containing the clues needed to disarm the bomb.
