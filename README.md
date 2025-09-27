# Python Roulette Strategy Platform (v4.0)

This is a comprehensive roulette simulator and testing platform built with Python and Tkinter. The project is designed with a clean separation between the game logic engine and the user interface, allowing for robust testing and future expansion into automated strategy agents.

## Key Features

- **Dual Roulette Modes**: Supports both American (with '0' and '00') and European (with '0') wheels.
- **Complete Bet Types**:
    - **1:1 Payouts**: Red/Black, Odd/Even, High/Low (1-18, 19-36).
    - **2:1 Payouts**: Dozens (1-12, 13-24, 25-36) and Columns.
    - **35:1 Payouts**: Bets on a single number.
- **Multi-Bet Capability**: Users can place multiple, distinct bets in a single round.
- **Refined Graphical User Interface (GUI)**: A modern, user-friendly interface for managing funds, placing bets, and viewing spin history. Features include a pop-up number pad for easy single-number selection.
- **Comprehensive Unit Testing**: The project includes a dedicated test suite that verifies the accuracy of the game logic for all betting scenarios and edge cases.

## Project Architecture

The project is intentionally separated into distinct files, each with a clear responsibility:

-   `roulette.py`: **The Rule Book**. This core module defines the `RouletteWheel` class, which contains the fundamental rules of the game, such as the numbers, their colors, column layouts, and the logic for checking if a bet wins or loses against an outcome.
-   `bet.py`: **The Backend Engine**. This file contains the `GameEngine` class. It is the brain of the application, managing the player's balance, tracking bets, calculating profits, and maintaining the game's state. It is a non-visual component.
-   `bet_ui.py`: **The Main Application (Frontend)**. This is the primary user interface that the user interacts with. It imports the `GameEngine` and provides all the visual elements (buttons, labels, etc.). **This is the file you run to play the game.**
-   `test.py`: **The Quality Inspector**. This file contains the automated test suite using Python's `unittest` framework. It rigorously tests the `GameEngine` to ensure all calculations and game logic are correct.
-   `play.py`: **A Simpler, Alternative Simulator**. This is a separate, more basic GUI application for simple spin simulations without the betting component.

## How to Use

This project uses only standard Python libraries, so no external installation is needed.

1.  **To Run the Main Betting Platform**:
    ```bash
    python bet_ui.py
    ```

2.  **To Run the Automated Test Suite**:
    ```bash
    python -m unittest test.py
    ```