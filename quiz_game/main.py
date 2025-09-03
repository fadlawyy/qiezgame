#!/usr/bin/env python3
"""
Quiz Game with Leaderboard
A fun quiz game where players answer questions and compete on a leaderboard.

Features:
- Multiple choice questions with auto-scoring
- Player leaderboard with rankings
- Quiz history tracking
- Custom question addition
- Different quiz lengths (5 or 10 questions)
- Performance statistics
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        os.system('chcp 65001 >nul 2>&1')  # Set UTF-8 code page
    except:
        pass

from game_engine import QuizGameEngine

def main():
    """Main entry point for the quiz game"""
    try:
        game = QuizGameEngine()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()
