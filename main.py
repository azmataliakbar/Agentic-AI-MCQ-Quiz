import streamlit as st
from session_manager import SessionState
from utils.question_loader import get_available_topics, load_questions

# Custom CSS for styling
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #4CAF50;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: bold;
}
.topic-header {
    font-size: 2rem;
    color: #2196F3;
    margin-bottom: 1rem;
    font-weight: bold;
}
.question-text {
    font-size: 1.5rem;
    font-weight: bold;
    color: #4CAF50;
    margin-bottom: 1rem;
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 10px;
    border-left: 5px solid #4CAF50;
}
.result-text {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.correct {
    color: green;
    font-weight: bold;
}
.incorrect {
    color: red;
    font-weight: bold;
}
.option-button {
    width: 100%;
    margin-top: 0.5rem;
    text-align: left;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
    font-weight: bold;
}
.option-button:hover {
    background-color: #f0f0f0;
}
.progress-text {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 1rem;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize all session state variables"""
    if 'session' not in st.session_state:
        st.session_state.session = SessionState()

def start_quiz(topic: str, difficulty: str):
    """Start a new quiz with the selected topic and difficulty"""
    success = st.session_state.session.load_topic(topic, difficulty)
    
    if success:
        st.session_state.session.quiz_started = True
        st.session_state.session.quiz_completed = False
        st.session_state.session.show_feedback = False
    else:
        st.error(f"No questions found for {topic} ({difficulty} level)")

def record_answer(answer_index: int):
    """Record user's answer and provide feedback"""
    session = st.session_state.session
    question = session.questions[session.current_question]
    is_correct = (answer_index == question["correct"])
    
    session.record_answer(answer_index)
    
    # Show feedback
    session.show_feedback = True
    if is_correct:
        session.feedback_message = "✅ Correct!"
        session.feedback_type = "success"
    else:
        correct_answer = question['options'][question['correct']]
        session.feedback_message = f"❌ Incorrect. The correct answer is: {correct_answer}"
        session.feedback_type = "error"

def reset_quiz():
    """Reset the quiz to initial state"""
    st.session_state.session.reset()

def main():
    # Initialize session state
    initialize_session_state()
    session = st.session_state.session
    
    # Main header
    st.markdown('<h1 class="main-header">🧠 Agentic AI MCQ Quiz</h1>', unsafe_allow_html=True)
    
    # Sidebar for topic selection
    with st.sidebar:
        st.markdown(
        """<h2 style='font-size: 2rem; color: #2196F3; margin-bottom: 1.5rem;'>
        📚 Topics
        </h2>""",
        unsafe_allow_html=True
    )
        
        topics = get_available_topics()
        selected_topic = st.selectbox(
            "Select a topic:",
            options=list(topics.keys())
        )
        
        selected_difficulty = st.selectbox(
            "Select difficulty:",
            options=topics[selected_topic]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Quiz", type="primary", use_container_width=True):
                start_quiz(selected_topic, selected_difficulty)
        with col2:
            if st.button("Reset Quiz", use_container_width=True):
                reset_quiz()
                st.rerun()
        # Author
        st.markdown("---")
        st.markdown(
            """<div style='text-align: center; font-size: 1.5rem; color: blue; margin-top: 1rem;'>
            By: <strong>Azmat Ali</strong>
            </div>""",
            unsafe_allow_html=True
        )
    
    # Main content area
    if not session.quiz_started:
        show_welcome()
    elif session.quiz_completed:
        show_results()
    else:
        show_question()


def show_welcome():
    """Display welcome message and instructions"""

    st.markdown("""
    <div style='font-size: 1.6rem;'>
    <h3>🎯 Welcome to Agentic AI MCQ Quiz!</h3>
    
    **<span style='font-size: 1.5rem;'>Test your knowledge on Python, Agentic AI, and SDK concepts.</span>**
    
    ### 📋 Instructions:
    1. Select a topic and difficulty from the sidebar
    2. Click **Start Quiz** to begin
    3. Answer all questions one by one
    4. You'll get immediate feedback after each answer
    5. Your final score will be displayed at the end
    
    **<span style='font-size: 1.5rem;'>Use the sidebar to select a topic and begin your quiz!</span>**
    </div>

    """, unsafe_allow_html=True)

    # Show available topics
    topics = get_available_topics()
    st.markdown("### 📚 Available Topics:")
    for topic, difficulties in topics.items():
        st.markdown(f"""
<div style='font-size: 1.4rem; margin-bottom: 0.5rem;'>
- <strong style='font-size: 1.5rem;'>{topic}</strong> ({', '.join(difficulties)})
</div>

""", unsafe_allow_html=True)
        
# Add author credit at the bottom
    st.markdown("---")  # Adds a divider line
    st.markdown(
        """<div style='text-align: center; font-size: 1.4rem; color: #9C27B0; margin-top: 2rem;'>
        Prepared by: <strong style='font-size: 1.5rem;'>Azmat Ali</strong>
        </div>""", 
        unsafe_allow_html=True
    )

def show_question():
    """Display the current question"""
    session = st.session_state.session
    question_data = session.questions[session.current_question]
    
    # Display progress
    progress = f"Question {session.current_question + 1} of {len(session.questions)}"
    st.markdown(f'<div class="progress-text">{progress}</div>', unsafe_allow_html=True)
    
    # Display the question
    st.markdown(f'<div class="question-text">{question_data["question"]}</div>', 
                unsafe_allow_html=True)
    
    # Display options as buttons
    for i, option in enumerate(question_data['options']):
        if st.button(option, key=f"option_{i}", use_container_width=True):
            record_answer(i)
            st.rerun()
    
    # Show feedback if available
    if session.show_feedback:
        if session.feedback_type == "success":
            st.success(session.feedback_message)
        else:
            st.error(session.feedback_message)
        
        # Add continue button
        if st.button("Continue →", type="primary"):
            session.show_feedback = False
            st.rerun()

    st.markdown("---")  # Adds a divider line
    st.markdown(
        """<div style='text-align: center; font-size: 1.4rem; color: #2196F3; margin-top: 2rem;'>
        Prepared by: <strong style='font-size: 1.5rem;'>Azmat Ali</strong>
        </div>""",
        unsafe_allow_html=True
    )


def show_results():
    """Display quiz results"""
    session = st.session_state.session
    results = session.get_results()
    
    st.balloons()
    st.markdown('<h2 class="topic-header">🎉 Quiz Completed!</h2>', unsafe_allow_html=True)
    st.markdown(f'<h3>Results for {session.current_topic} ({session.difficulty} level):</h3>',
                unsafe_allow_html=True)
    
    # Display score with emoji based on performance
    percentage = results['percentage']
    if percentage >= 80:
        score_emoji = "🏆"
    elif percentage >= 60:
        score_emoji = "⭐"
    else:
        score_emoji = "📚"
    
    st.markdown(f"""
    **{score_emoji} Score:** {results['score']}/{results['total']}  
    **📊 Percentage:** {percentage:.1f}%
    """)
    
    # Display question review
    st.markdown("### 🔍 Question Review:")
    
    for i, answer in enumerate(session.answers):
        status = "✅" if answer['is_correct'] else "❌"
        st.markdown(f"**{status} Q{i+1}:** {answer['question']}")
        
        user_ans_class = "correct" if answer['is_correct'] else "incorrect"
        st.markdown(f'<span class="{user_ans_class}">Your answer: {answer["options"][answer["user_answer"]]}</span>',
                    unsafe_allow_html=True)
        
        if not answer['is_correct']:
            st.markdown(f'<span class="correct">Correct answer: {answer["options"][answer["correct_answer"]]}</span>',
                        unsafe_allow_html=True)
        st.markdown("---")
    
    # Option to start a new quiz
    if st.button("🔄 Start New Quiz", type="primary", use_container_width=True):
        reset_quiz()
        st.rerun()

    st.markdown("---")  # Adds a divider line
    st.markdown(
        """<div style='text-align: center; font-size: 1.4rem; color: #2196F3; margin-top: 2rem;'>
        Prepared by: <strong style='font-size: 1.5rem;'>Azmat Ali</strong>
        </div>""",
        unsafe_allow_html=True
    )
if __name__ == "__main__":
    main()
    