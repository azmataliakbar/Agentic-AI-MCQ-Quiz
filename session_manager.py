import json
import os
from typing import List, Dict, Any

class SessionState:
    def __init__(self):
        self.current_topic = None
        self.current_question = 0
        self.score = 0
        self.answers = []
        self.questions = []
        self.difficulty = "easy"
        self.quiz_started = False
        self.quiz_completed = False
        self.show_feedback = False
        self.feedback_message = ""
        self.feedback_type = ""

    def load_topic(self, topic_name: str, difficulty: str = "easy"):
        """Load questions for a specific topic and difficulty"""
        try:
            # Convert topic name to filename format
            filename = topic_name.lower().replace(' ', '_')
            file_path = f"data/{filename}_questions.json"
            
            with open(file_path, "r") as f:
                all_questions = json.load(f)
            
            # Filter questions by difficulty
            self.questions = [q for q in all_questions if q.get("level", "easy") == difficulty]
            self.current_topic = topic_name
            self.current_question = 0
            self.score = 0
            self.answers = []
            self.difficulty = difficulty
            self.quiz_started = True
            self.quiz_completed = False
            self.show_feedback = False
            return len(self.questions) > 0  # Return True if we found questions
        except FileNotFoundError:
            print(f"Question file not found for topic: {topic_name}")
            return False
        except json.JSONDecodeError:
            print(f"Error parsing JSON for topic: {topic_name}")
            return False

    def get_current_question(self) -> Dict[str, Any]:
        """Get the current question data"""
        if self.current_question < len(self.questions):
            return self.questions[self.current_question]
        return None

    def record_answer(self, answer_index: int) -> bool:
        """Record user's answer and return if it was correct"""
        question = self.get_current_question()
        if question:
            is_correct = (answer_index == question["correct"])
            self.answers.append({
                "question": question["question"],
                "user_answer": answer_index,
                "correct_answer": question["correct"],
                "is_correct": is_correct,
                "options": question["options"]
            })
            if is_correct:
                self.score += 1
            self.current_question += 1
            
            # Check if quiz is completed
            if self.current_question >= len(self.questions):
                self.quiz_completed = True
                
            return is_correct
        return False

    def is_completed(self) -> bool:
        """Check if all questions have been answered"""
        return self.quiz_completed

    def get_results(self) -> Dict[str, Any]:
        """Get quiz results"""
        return {
            "total": len(self.questions),
            "score": self.score,
            "percentage": (self.score / len(self.questions)) * 100 if self.questions else 0,
            "topic": self.current_topic,
            "difficulty": self.difficulty
        }
    
    def reset(self):
        """Reset the session state"""
        self.current_topic = None
        self.current_question = 0
        self.score = 0
        self.answers = []
        self.questions = []
        self.difficulty = "easy"
        self.quiz_started = False
        self.quiz_completed = False
        self.show_feedback = False
        self.feedback_message = ""
        self.feedback_type = ""