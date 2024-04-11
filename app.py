from flask import Flask, flash, render_template, url_for, redirect
from nlpAnnotationToolKit.forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '076ba9ea66b35151dac0f36f9aaafa23'

app = Flask(__name__)

exam_questions = {
    1: {"question": "What is the capital of France?", "answer": "Paris"},
    2: {"question": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee"},
}

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', questions=exam_questions)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'success':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check username and password.', 'danger')
            
    return render_template(
        'login.html',
        title='login',
        form=form)



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
