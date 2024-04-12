from nlpAnnotationToolKit import app
from flask import flash, render_template, url_for, redirect
from nlpAnnotationToolKit.forms import RegistrationForm, LoginForm, TextClassificationInputForm

exam_questions = "I am interested"
labels = ['Happy', 'Joy', 'Unhappy']

# TODO: Fix Login Form
# TODO: Fix Registration Form
# TODO: Create Routes for 

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = TextClassificationInputForm()
    return render_template('home.html', form=form, Question=exam_questions, labels=labels)

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