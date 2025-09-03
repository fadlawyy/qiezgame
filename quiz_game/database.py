import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'quiz_game.db')
        self.init_database()
    
    def get_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            raise
    
    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                difficulty TEXT DEFAULT 'Medium'
            )
        ''')
        
        # Create players table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_sample_questions(self):
        """Add some sample questions to get started"""
        sample_questions = [
            ("What is the capital of France?", "London", "Berlin", "Paris", "Madrid", "C", "Geography", "Easy"),
            ("Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "B", "Science", "Easy"),
            ("What is 2 + 2?", "3", "4", "5", "6", "B", "Math", "Easy"),
            ("Who wrote 'Romeo and Juliet'?", "Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain", "B", "Literature", "Medium"),
            ("What is the largest mammal in the world?", "Elephant", "Blue Whale", "Giraffe", "Hippopotamus", "B", "Science", "Medium"),
            ("In which year did World War II end?", "1944", "1945", "1946", "1947", "B", "History", "Medium"),
            ("What is the chemical symbol for gold?", "Go", "Gd", "Au", "Ag", "C", "Science", "Hard"),
            ("Which programming language is known for its use in web development?", "C++", "Java", "JavaScript", "Assembly", "C", "Technology", "Medium"),
            ("What is the square root of 144?", "11", "12", "13", "14", "B", "Math", "Easy"),
            ("Who painted the Mona Lisa?", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo", "C", "Art", "Medium")
        ]
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check if questions already exist
        cursor.execute("SELECT COUNT(*) FROM questions")
        if cursor.fetchone()[0] == 0:
            for question in sample_questions:
                cursor.execute('''
                    INSERT INTO questions (text, option_a, option_b, option_c, option_d, correct_answer, category, difficulty)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', question)
            conn.commit()
            print("Sample questions added to database!")
        
        conn.close()
    
    def add_question(self, text, option_a, option_b, option_c, option_d, correct_answer, category="General", difficulty="Medium"):
        """Add a new question to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO questions (text, option_a, option_b, option_c, option_d, correct_answer, category, difficulty)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (text, option_a, option_b, option_c, option_d, correct_answer, category, difficulty))
        
        conn.commit()
        conn.close()
    
    def get_random_questions(self, count=5):
        """Get random questions from the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, text, option_a, option_b, option_c, option_d, correct_answer, category, difficulty
            FROM questions ORDER BY RANDOM() LIMIT ?
        ''', (count,))
        
        questions = cursor.fetchall()
        conn.close()
        return questions
    
    def add_player(self, name):
        """Add a new player or get existing player ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO players (name) VALUES (?)', (name,))
            player_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Player already exists, get their ID
            cursor.execute('SELECT id FROM players WHERE name = ?', (name,))
            player_id = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        return player_id
    
    def save_score(self, player_id, score, total_questions):
        """Save a player's quiz score"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scores (player_id, score, total_questions)
            VALUES (?, ?, ?)
        ''', (player_id, score, total_questions))
        
        conn.commit()
        conn.close()
    
    def get_leaderboard(self, limit=10):
        """Get the top scores for the leaderboard"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.name, s.score, s.total_questions, s.quiz_date,
                   ROUND((s.score * 100.0 / s.total_questions), 2) as percentage
            FROM scores s
            JOIN players p ON s.player_id = p.id
            ORDER BY percentage DESC, s.score DESC, s.quiz_date DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def get_player_history(self, player_name):
        """Get a player's quiz history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.score, s.total_questions, s.quiz_date,
                   ROUND((s.score * 100.0 / s.total_questions), 2) as percentage
            FROM scores s
            JOIN players p ON s.player_id = p.id
            WHERE p.name = ?
            ORDER BY s.quiz_date DESC
        ''', (player_name,))
        
        results = cursor.fetchall()
        conn.close()
        return results
