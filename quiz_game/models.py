from datetime import datetime
import random

class Question:
    """Represents a quiz question with multiple choice options"""
    
    def __init__(self, question_id, text, option_a, option_b, option_c, option_d, correct_answer, category="General", difficulty="Medium"):
        self.id = question_id
        self.text = text
        self.options = {
            'A': option_a,
            'B': option_b,
            'C': option_c,
            'D': option_d
        }
        self.correct_answer = correct_answer.upper()
        self.category = category
        self.difficulty = difficulty
    
    def is_correct(self, answer):
        """Check if the provided answer is correct"""
        return answer.upper() == self.correct_answer
    
    def get_options_text(self):
        """Get formatted options text for display"""
        return "\n".join([f"{key}. {value}" for key, value in self.options.items()])
    
    def __str__(self):
        return f"{self.text}\n{self.get_options_text()}"


class Player:
    """Represents a player with name and current score"""
    
    def __init__(self, name, player_id=None):
        self.id = player_id
        self.name = name
        self.current_score = 0
        self.total_questions_answered = 0
    
    def add_point(self):
        """Add a point to the player's current score"""
        self.current_score += 1
    
    def answer_question(self, is_correct):
        """Record that the player answered a question"""
        self.total_questions_answered += 1
        if is_correct:
            self.add_point()
    
    def get_percentage(self):
        """Get the player's current percentage score"""
        if self.total_questions_answered == 0:
            return 0
        return round((self.current_score / self.total_questions_answered) * 100, 2)
    
    def reset_score(self):
        """Reset the player's current score for a new quiz"""
        self.current_score = 0
        self.total_questions_answered = 0
    
    def __str__(self):
        return f"Player: {self.name}, Score: {self.current_score}/{self.total_questions_answered} ({self.get_percentage()}%)"


class Quiz:
    """Manages a quiz session with questions and scoring"""
    
    def __init__(self, questions=None):
        self.questions = questions or []
        self.current_question_index = 0
        self.is_completed = False
        self.start_time = None
        self.end_time = None
    
    def add_question(self, question):
        """Add a question to the quiz"""
        self.questions.append(question)
    
    def start_quiz(self):
        """Start the quiz timer"""
        self.start_time = datetime.now()
        self.current_question_index = 0
        self.is_completed = False
    
    def get_current_question(self):
        """Get the current question"""
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        return None
    
    def answer_current_question(self, player, answer):
        """Process the answer to the current question"""
        current_question = self.get_current_question()
        if current_question is None:
            return False
        
        is_correct = current_question.is_correct(answer)
        player.answer_question(is_correct)
        
        self.current_question_index += 1
        
        # Check if quiz is completed
        if self.current_question_index >= len(self.questions):
            self.complete_quiz()
        
        return is_correct
    
    def complete_quiz(self):
        """Mark the quiz as completed"""
        self.is_completed = True
        self.end_time = datetime.now()
    
    def get_progress(self):
        """Get the current progress of the quiz"""
        return f"{self.current_question_index}/{len(self.questions)}"
    
    def get_duration(self):
        """Get the duration of the quiz"""
        if self.start_time is None:
            return None
        
        end = self.end_time or datetime.now()
        duration = end - self.start_time
        return duration.total_seconds()
    
    def shuffle_questions(self):
        """Shuffle the order of questions"""
        random.shuffle(self.questions)
    
    def has_next_question(self):
        """Check if there are more questions"""
        return self.current_question_index < len(self.questions)
    
    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"Quiz: {len(self.questions)} questions, Progress: {self.get_progress()}, Status: {status}"
