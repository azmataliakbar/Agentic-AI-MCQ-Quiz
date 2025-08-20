import json
import os
from typing import Dict, List

# Define available topics and difficulties
TOPICS = {
    "Agent": ["easy", "medium", "hard"],
    "Agent Configuration": ["easy", "medium", "hard"],
    "Handoff": ["easy", "medium", "hard"],
    "Tools": ["easy", "medium", "hard"],
    "Context": ["easy", "medium", "hard"]
}

def get_available_topics() -> Dict[str, List[str]]:
    """Get all available topics and their difficulties"""
    return TOPICS

def get_topic_file_path(topic_name: str) -> str:
    """Get the file path for a topic"""
    return f"data/{topic_name.lower().replace(' ', '_')}_questions.json"

def load_questions(topic_name: str, difficulty: str = "easy") -> List[Dict]:
    """Load questions for a specific topic and difficulty"""
    try:
        file_path = get_topic_file_path(topic_name)
        if not os.path.exists(file_path):
            return []
            
        with open(file_path, "r") as f:
            all_questions = json.load(f)
        
        # Filter questions by difficulty
        return [q for q in all_questions if q.get("level", "easy") == difficulty]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_question_count(topic_name: str, difficulty: str = "easy") -> int:
    """Get the number of questions for a topic and difficulty"""
    questions = load_questions(topic_name, difficulty)
    return len(questions)