import gradio as gr
import random
from quiz_data import QUIZ_QUESTIONS

# Shuffle the questions when the app launches
def generate_question_texts():
    question_list = [q["question"] for q in QUIZ_QUESTIONS]
    random.shuffle(question_list)
    return question_list

# Check user's answer and update score
def check_answer(selected_option, question_text, score):
    question_index = next((i for i, q in enumerate(QUIZ_QUESTIONS) if q["question"] == question_text), None)
    if question_index is None:
        return "Error: Question not found", score
    
    correct_answer = QUIZ_QUESTIONS[question_index]["answer"]
    if selected_option == correct_answer:
        score += 1
        return f"Correct! | Score: {score}", score
    else:
        hint = QUIZ_QUESTIONS[question_index].get("hint", "No hint available.")
        return f"Incorrect. The correct answer is: {correct_answer}. Hint: {hint} | Score: {score}", score

# Find question and its options
def quiz_interface(question_text):
    question_idx = next((i for i, q in enumerate(QUIZ_QUESTIONS) if q["question"] == question_text), None)
    if question_idx is None:
        return None, []
    return question_text, QUIZ_QUESTIONS[question_idx]["options"]

# Reset the quiz
def reset_quiz():
    return "Score reset to 0!", 0

def build_quiz_app():
    question_list = generate_question_texts()

    with gr.Blocks() as demo:
        question_dropdown = gr.Dropdown(label="Select a question", choices=question_list)
        question_display = gr.Textbox(label="Question", interactive=False)
        options_radio = gr.Radio(label="Choose your answer", choices=[])
        feedback_box = gr.Textbox(label="Feedback", interactive=False)
        score_state = gr.State(value=0)
        reset_button = gr.Button("Retry Quiz")

        def update_question(question_text):
            q_text, opts = quiz_interface(question_text)
            if q_text is None:
                return gr.update(value="No question found"), gr.update(choices=[])
            return gr.update(value=q_text), gr.update(choices=opts)

        question_dropdown.change(
            fn=update_question,
            inputs=[question_dropdown],
            outputs=[question_display, options_radio]
        )

        check_button = gr.Button("Check")
        check_button.click(
            fn=check_answer,
            inputs=[options_radio, question_display, score_state],
            outputs=[feedback_box, score_state]
        )

        reset_button.click(
            fn=reset_quiz,
            inputs=[],
            outputs=[feedback_box, score_state]
        )

    return demo

if __name__ == "__main__":
    demo = build_quiz_app()
    demo.launch()
