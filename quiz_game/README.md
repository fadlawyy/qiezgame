# 🎯 Quiz Game with Leaderboard

A comprehensive quiz game built with Python that features multiple-choice questions, player scoring, leaderboards, and quiz history tracking.

## 🚀 Features

✅ **Multiple Choice Questions** - Answer questions with A/B/C/D options  
✅ **Auto Scoring** - Automatic score calculation and feedback  
✅ **Player Leaderboard** - Compete with other players for top rankings  
✅ **Quiz History** - Track your past performance and improvement  
✅ **Custom Questions** - Add your own questions to the database  
✅ **Multiple Quiz Lengths** - Choose between 5 or 10 question quizzes  
✅ **Performance Statistics** - View detailed stats and percentages  
✅ **Retry Functionality** - Play multiple quizzes and improve your score  

## 📁 Project Structure

```
quiz_game/
├── main.py           # Main entry point
├── game_engine.py    # Core game logic and UI
├── models.py         # OOP classes (Question, Player, Quiz)
├── database.py       # SQLite database operations
├── quiz_game.db      # SQLite database file
├── requirements.txt  # Dependencies (uses built-in modules)
└── README.md         # This file
```

## 🎮 How to Play

### Prerequisites
1. **Python 3.7+** - The game uses built-in Python modules only
2. **No external dependencies** - SQLite database is included with Python

### Running the Game
1. **Start the Game**:
   ```bash
   cd quiz_game
   python main.py
   ```

2. **Enter Your Name** - Create or login to your player profile

3. **Choose Quiz Type**:
   - Short Quiz (5 questions)
   - Long Quiz (10 questions)

4. **Answer Questions** - Select A, B, C, or D for each question

5. **View Results** - See your score, percentage, and performance feedback

6. **Check Leaderboard** - Compare your scores with other players

## 🏗️ Architecture

### **Object-Oriented Design**

- **`Question`** → Stores question text, options, and correct answer
- **`Player`** → Manages player name, score, and statistics  
- **`Quiz`** → Handles quiz flow, timing, and question management

### **Database Schema**

- **`questions`** → All quiz questions with categories and difficulty
- **`players`** → Player information and registration dates
- **`scores`** → Historical scores with timestamps

## 🎯 Game Features

### **Quiz Gameplay**
- Random question selection
- Multiple difficulty levels (Easy/Medium/Hard)
- Question categories (Science, Math, History, etc.)
- Real-time scoring and feedback
- Timer tracking for performance analysis

### **Leaderboard System**
- Top 10 player rankings
- Percentage-based scoring
- Medal system (🥇🥈🥉) for top performers
- Date tracking for recent achievements

### **Player Statistics**
- Individual quiz history
- Average performance calculation
- Best score tracking
- Total quizzes played

### **Question Management**
- Pre-loaded sample questions
- Add custom questions feature
- Category and difficulty classification
- Question shuffling for variety

## 🔧 Technical Details

- **Language**: Python 3.7+
- **Database**: SQLite (built-in)
- **Dependencies**: None (uses standard library only)
- **Platform**: Cross-platform (Windows, macOS, Linux)

## 🎨 Sample Questions Included

The game comes with 10 pre-loaded questions covering:
- **Geography** (Capital cities, countries)
- **Science** (Planets, chemistry, biology)
- **Mathematics** (Basic arithmetic, geometry)
- **Literature** (Famous authors and works)
- **History** (World events, dates)
- **Technology** (Programming, computers)
- **Art** (Famous paintings and artists)

## 🏆 Scoring System

- **Correct Answer**: +1 point
- **Incorrect Answer**: 0 points
- **Final Score**: Correct answers / Total questions
- **Percentage**: (Score / Total) × 100%

### **Performance Ratings**
- 🌟 **90%+**: Outstanding! Quiz Master!
- 👍 **70-89%**: Great job! Well done!
- 👌 **50-69%**: Not bad! Keep practicing!
- 📚 **Below 50%**: Keep studying and try again!

## 🚀 Getting Started

1. **Clone or download** the quiz game files
2. **Navigate** to the quiz_game directory
3. **Run** `python main.py`
4. **Enter your name** and start playing!

The game will automatically create the SQLite database file (`quiz_game.db`) and populate it with sample questions on first run.

## 🎯 Future Enhancements

Potential features to add:
- Timed questions with countdown
- Multiplayer mode
- Question difficulty progression
- Achievement badges
- Export quiz results
- Web-based interface
- Question categories filter
- Hint system

---

**Have fun testing your knowledge! 🧠✨**
