from database import Database
from models import Question, Player, Quiz
import os
import time
import sys

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    try:
        import codecs
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

class QuizGameEngine:
    """Main game engine that manages the quiz game flow"""
    
    def __init__(self):
        self.db = Database()
        self.current_player = None
        self.current_quiz = None
        
        # Initialize database with sample questions
        self.db.add_sample_questions()
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self):
        """Display welcome message"""
        print("=" * 50)
        print("*** WELCOME TO THE ULTIMATE QUIZ GAME! ***")
        print("=" * 50)
        print("Test your knowledge and compete for the top spot!")
        print()
    
    def get_player_name(self):
        """Get player name and create/retrieve player"""
        while True:
            name = input("Enter your name: ").strip()
            if name:
                player_id = self.db.add_player(name)
                self.current_player = Player(name, player_id)
                return
            print("Please enter a valid name!")
    
    def create_quiz(self, num_questions=5):
        """Create a new quiz with random questions"""
        questions_data = self.db.get_random_questions(num_questions)
        
        if not questions_data:
            print("No questions available in the database!")
            return False
        
        questions = []
        for q_data in questions_data:
            question = Question(
                question_id=q_data[0],
                text=q_data[1],
                option_a=q_data[2],
                option_b=q_data[3],
                option_c=q_data[4],
                option_d=q_data[5],
                correct_answer=q_data[6],
                category=q_data[7],
                difficulty=q_data[8]
            )
            questions.append(question)
        
        self.current_quiz = Quiz(questions)
        self.current_quiz.shuffle_questions()
        return True
    
    def play_quiz(self):
        """Main quiz gameplay loop"""
        if not self.current_quiz:
            print("No quiz available!")
            return
        
        self.current_player.reset_score()
        self.current_quiz.start_quiz()
        
        print(f"\n*** Starting Quiz for {self.current_player.name}! ***")
        print(f"*** {len(self.current_quiz.questions)} questions await you! ***\n")
        
        question_number = 1
        
        while self.current_quiz.has_next_question():
            current_question = self.current_quiz.get_current_question()
            
            print(f"Question {question_number}/{len(self.current_quiz.questions)}")
            print(f"Category: {current_question.category} | Difficulty: {current_question.difficulty}")
            print("-" * 50)
            print(f"{current_question.text}")
            print()
            print(current_question.get_options_text())
            print()
            
            # Get player's answer
            while True:
                answer = input("Your answer (A/B/C/D): ").strip().upper()
                if answer in ['A', 'B', 'C', 'D']:
                    break
                print("Please enter A, B, C, or D!")
            
            # Process the answer
            is_correct = self.current_quiz.answer_current_question(self.current_player, answer)
            
            if is_correct:
                print("*** CORRECT! Well done! ***")
            else:
                correct_option = current_question.correct_answer
                correct_text = current_question.options[correct_option]
                print(f"*** INCORRECT! The correct answer was {correct_option}: {correct_text} ***")
            
            print(f"Current Score: {self.current_player.current_score}/{self.current_player.total_questions_answered}")
            
            if self.current_quiz.has_next_question():
                input("\nPress Enter to continue...")
                self.clear_screen()
            
            question_number += 1
        
        # Quiz completed
        self.show_quiz_results()
        self.save_quiz_results()
    
    def show_quiz_results(self):
        """Display quiz results"""
        print("\n" + "=" * 50)
        print("*** QUIZ COMPLETED! ***")
        print("=" * 50)
        
        score = self.current_player.current_score
        total = self.current_player.total_questions_answered
        percentage = self.current_player.get_percentage()
        duration = self.current_quiz.get_duration()
        
        print(f"Player: {self.current_player.name}")
        print(f"Final Score: {score}/{total} ({percentage}%)")
        print(f"Time Taken: {duration:.1f} seconds")
        
        # Performance feedback
        if percentage >= 90:
            print("*** Outstanding! You're a quiz master! ***")
        elif percentage >= 70:
            print("*** Great job! Well done! ***")
        elif percentage >= 50:
            print("*** Not bad! Keep practicing! ***")
        else:
            print("*** Keep studying and try again! ***")
    
    def save_quiz_results(self):
        """Save the quiz results to database"""
        self.db.save_score(
            self.current_player.id,
            self.current_player.current_score,
            self.current_player.total_questions_answered
        )
        print("\n*** Your score has been saved! ***")
    
    def show_leaderboard(self):
        """Display the leaderboard"""
        print("\n" + "=" * 60)
        print("*** LEADERBOARD - TOP PERFORMERS ***")
        print("=" * 60)
        
        leaderboard = self.db.get_leaderboard(10)
        
        if not leaderboard:
            print("No scores recorded yet. Be the first to play!")
            return
        
        print(f"{'Rank':<5} {'Name':<15} {'Score':<10} {'Percentage':<12} {'Date':<20}")
        print("-" * 60)
        
        for i, (name, score, total, date, percentage) in enumerate(leaderboard, 1):
            # Format date
            formatted_date = date[:16] if len(date) > 16 else date
            
            # Add rankings for top 3
            if i == 1:
                rank = "[1st]"
            elif i == 2:
                rank = "[2nd]"
            elif i == 3:
                rank = "[3rd]"
            else:
                rank = f"  {i}  "
            
            print(f"{rank:<5} {name:<15} {score}/{total:<6} {percentage}%{'':<7} {formatted_date}")
    
    def show_player_history(self):
        """Show current player's quiz history"""
        if not self.current_player:
            print("No player selected!")
            return
        
        print(f"\n*** Quiz History for {self.current_player.name} ***")
        print("=" * 50)
        
        history = self.db.get_player_history(self.current_player.name)
        
        if not history:
            print("No quiz history found. Play your first quiz!")
            return
        
        print(f"{'Quiz #':<8} {'Score':<10} {'Percentage':<12} {'Date':<20}")
        print("-" * 50)
        
        for i, (score, total, date, percentage) in enumerate(history, 1):
            formatted_date = date[:16] if len(date) > 16 else date
            print(f"{i:<8} {score}/{total:<6} {percentage}%{'':<7} {formatted_date}")
        
        # Calculate statistics
        total_quizzes = len(history)
        avg_percentage = sum(h[3] for h in history) / total_quizzes
        best_score = max(history, key=lambda x: x[3])
        
        print(f"\n*** Statistics: ***")
        print(f"Total Quizzes: {total_quizzes}")
        print(f"Average Score: {avg_percentage:.1f}%")
        print(f"Best Performance: {best_score[0]}/{best_score[1]} ({best_score[3]}%)")
    
    def add_custom_question(self):
        """Allow adding custom questions to the database"""
        print("\n*** Add a New Question ***")
        print("=" * 30)
        
        text = input("Enter the question: ").strip()
        if not text:
            print("Question cannot be empty!")
            return
        
        print("\nEnter the four options:")
        option_a = input("Option A: ").strip()
        option_b = input("Option B: ").strip()
        option_c = input("Option C: ").strip()
        option_d = input("Option D: ").strip()
        
        if not all([option_a, option_b, option_c, option_d]):
            print("All options must be provided!")
            return
        
        while True:
            correct = input("Which option is correct? (A/B/C/D): ").strip().upper()
            if correct in ['A', 'B', 'C', 'D']:
                break
            print("Please enter A, B, C, or D!")
        
        category = input("Category (optional, default 'General'): ").strip() or "General"
        
        while True:
            difficulty = input("Difficulty (Easy/Medium/Hard, default 'Medium'): ").strip().title()
            if difficulty in ['Easy', 'Medium', 'Hard', '']:
                difficulty = difficulty or 'Medium'
                break
            print("Please enter Easy, Medium, or Hard!")
        
        # Add to database
        self.db.add_question(text, option_a, option_b, option_c, option_d, correct, category, difficulty)
        print("\n*** Question added successfully! ***")
    
    def show_main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            print("\n" + "=" * 40)
            print("*** QUIZ GAME MAIN MENU ***")
            print("=" * 40)
            
            if self.current_player:
                print(f"Current Player: {self.current_player.name}")
            
            print("\n1. Play Quiz (5 questions)")
            print("2. Play Long Quiz (10 questions)")
            print("3. View Leaderboard")
            print("4. View My History")
            print("5. Add Custom Question")
            print("6. Change Player")
            print("7. Exit Game")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                if self.create_quiz(5):
                    self.clear_screen()
                    self.play_quiz()
                    input("\nPress Enter to return to menu...")
                    self.clear_screen()
            
            elif choice == '2':
                if self.create_quiz(10):
                    self.clear_screen()
                    self.play_quiz()
                    input("\nPress Enter to return to menu...")
                    self.clear_screen()
            
            elif choice == '3':
                self.show_leaderboard()
                input("\nPress Enter to return to menu...")
                self.clear_screen()
            
            elif choice == '4':
                self.show_player_history()
                input("\nPress Enter to return to menu...")
                self.clear_screen()
            
            elif choice == '5':
                self.add_custom_question()
                input("\nPress Enter to return to menu...")
                self.clear_screen()
            
            elif choice == '6':
                self.get_player_name()
                self.clear_screen()
            
            elif choice == '7':
                print("\n*** Thanks for playing! See you next time! ***")
                break
            
            else:
                print("Invalid choice! Please enter 1-7.")
    
    def run(self):
        """Start the quiz game"""
        self.clear_screen()
        self.display_welcome()
        self.get_player_name()
        self.clear_screen()
        self.show_main_menu()
