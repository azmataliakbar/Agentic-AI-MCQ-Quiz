import json
import os
from typing import Dict, List

# Define available topics and difficulties
TOPICS = {
    "Agent": ["easy", "medium", "hard"],
    "Agent Configuration": ["easy", "medium", "hard"],
    "Handoff": ["easy", "medium", "hard"],
    "Tools": ["easy", "medium", "hard"],
    "Context": ["easy", "medium", "hard"],
    "Streaming": ["easy", "medium", "hard"],
    "Guardrails": ["easy", "medium", "hard"],
    "Tracing": ["easy", "medium", "hard"],
    "Orchestrating Multiple Agents": ["easy", "medium", "hard"],
    "Model Settings": ["easy", "medium", "hard"],
    "Hooks": ["easy", "medium", "hard"],
    "Structure Output": ["easy", "medium", "hard"],
    "Agent Dynamic Instructions": ["easy", "medium", "hard"],
    "Agent Output Types": ["easy", "medium", "hard"],
    "Agent Cloning": ["easy", "medium", "hard"],
    "Agent Model Settings": ["easy", "medium", "hard"],
    "Agent Tool Use Behaviour": ["easy", "medium", "hard"],
    "Agent Reset Tool Choice": ["easy", "medium", "hard"],
    "HandOff Input Type": ["easy", "medium", "hard"],
    "HandOff Input Filter": ["easy", "medium", "hard"],
    "HandOff Is Enabled": ["easy", "medium", "hard"],
    "HandOff On HandOff": ["easy", "medium", "hard"],
    "Runner Custom Runner": ["easy", "medium", "hard"],
    "Runner Max Turns": ["easy", "medium", "hard"],
    "Runner Context": ["easy", "medium", "hard"],
    "Tools Name Override": ["easy", "medium", "hard"],
    "Tools Description Override": ["easy", "medium", "hard"],
    "Tools Is Enabled": ["easy", "medium", "hard"],
    "Tools Failure Error Function": ["easy", "medium", "hard"],
    "Tools Agent As Tools": ["easy", "medium", "hard"],

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