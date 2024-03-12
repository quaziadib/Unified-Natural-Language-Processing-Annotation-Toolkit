from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy database of exam questions and correct answers
exam_questions = {
    1: {"question": "What is the capital of France?", "answer": "Paris"},
    2: {"question": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee"},
    # Add more questions as needed
}

@app.route('/')
def start_exam():
    return render_template('exam.html', questions=exam_questions)

@app.route('/evaluate', methods=['POST'])
def evaluate_exam():
    score = 0
    submitted_answers = request.form
    for question_id, data in exam_questions.items():
        if submitted_answers.get(str(question_id)) == data['answer']:
            score += 1
    if score >= 2:  # Example passing criteria, adjust as needed
        return redirect(url_for('confirmation'))
    else:
        return "Sorry, you did not pass the exam. Please try again."

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
