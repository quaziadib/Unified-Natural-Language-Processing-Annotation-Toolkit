from flask import (
    render_template, 
    url_for, 
    flash, 
    redirect, 
    request, 
    abort
    )
from annotationTool import app, db, bcrypt
from annotationTool.forms import (
    RegistrationForm, 
    LoginForm,
    UpdateAccountForm,
    PostForm,
    ProjectForm,
    ProjectDashboardDropdown,
    TextClassificationDropdown,
    TextGenerationForm,
    Q_A_Form,
    TextEntailmentForm,
    DataRequestForms,
    ExamForm
    )
from annotationTool.models import (
    User, 
    Post,
    Project,
    DataRequest
    )
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image
import pandas as pd 
import random 


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/dataRequest", methods=["GET", "POST"])
def dataRequest():
    form = DataRequestForms()
    if form.validate_on_submit():
        data = DataRequest(
            name = form.name.data,
            projectName = form.projectName.data,
            projectID = form.projectID.data,
            email = form.email.data
        )
        db.session.add(data)
        db.session.commit()
        flash('Your Request has been submitted', 'success')
        return redirect(url_for('home'))

    return render_template('dataRequest.html', form=form, title='Data Request')

@app.route("/projectDashboard")
def projectDashboard():
    p = Project.query.get_or_404(1)
    return render_template('project_dashboard.html', title='About', project=p)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password
            )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/<int:project_id>/register_annotator", methods=['GET', 'POST'])
def register_annotator(project_id):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password,
            project_id=project_id
            )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('annotator_register.html', title='Annotator Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/reports")
def report():
    return render_template('reports.html', title='Report')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


# ------------- Job Post ------------------------

@app.route("/post/new/<int:project_id>", methods=['GET', 'POST'])
@login_required
def new_post(project_id):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, 
            description=form.description.data, 
            requirements=form.requirements.data,
            projectType=form.projectType.data,
            projectID=project_id,
            author=current_user,
            agreement=form.agreement.data
            )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('createJobPost.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('jobPosts.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.requirements = form.requirements.data
        post.projectType = form.projectType.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        post.title = form.title.data
        post.description = form.description.data
        post.requirements = form.requirements.data
        post.projectType = form.projectType.data
    return render_template('createJobPost.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))



# ------------- Project ------------------------
@app.route("/project/new", methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data, 
            description=form.description.data, 
            projectType=form.projectType.data,
            author=current_user,
            labels = form.labels.data,
            datasetLink = form.labels.data
            )
        db.session.add(project)
        db.session.commit()
        flash('Your Project has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('createProject.html', title='New Project',
                           form=form, legend='New Project')


@app.route("/project/<int:project_id>")
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('projects.html', title=project.title, project=project)


@app.route("/project/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.projectType = form.projectType.data
        project.labels = form.labels.data
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('project', project_id=project.id))
    elif request.method == 'GET':
        project.title = form.title.data
        project.description = form.description.data
        project.projectType = form.projectType.data
        project.labels = form.labels.data
    return render_template('createProject.html', title='Update Project',
                           form=form, legend='Update Project')


@app.route("/project/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Your project has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required
def user_projects():
    if current_user.project_id:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        projects = Project.query.filter_by(id=user.project_id).all()
    else:
        user = User.query.filter_by(username=current_user.username).first_or_404()
        projects = Project.query.filter_by(author=user).all()

    return render_template('user_project.html', user=user, projects=projects)

# ---------------------- Text Classification ----------------
def text_fetcher(link_ds):
    df = pd.read_csv(link_ds)
    idx = random.randint(0, df.shape[0]-1)
    while df.is_annotated.iloc[idx] != 0:
        idx = random.randint(0, df.shape[0]-1)
    return df.sentence.iloc[idx], idx
    

def save_dataset():
    pass


@app.route('/classification', methods=['GET', 'POST'])
def text_classification():
    project_data_link = os.path.join(app.root_path, 'static/datasets', 'sentiment_train.csv')
    text, idx = text_fetcher(project_data_link)
    form = TextClassificationDropdown()
    form.label_type.choices = [('1', 'Positive'), ('2', 'Negative')]
    if form.validate_on_submit():
        df = pd.read_csv(project_data_link)
        df.label.iloc[idx] = form.label_type.data
        df.is_annotated.iloc[idx] = 1
        df.to_csv(project_data_link, index=False)
        #flash(f'Annotated at {idx} index. and {df.is_annotated.iloc[idx]}, Sentence: { df.sentence.iloc[idx] }, label: { df.label.iloc[idx] }', 'success')
        return render_template('text_classification.html', text=text, idx=idx, form=form)
    return render_template('text_classification.html', text=text, idx=idx, form=form)

# ---------------------- Text Generation ----------------
def text_fetcher_generation(link_ds):
    df = pd.read_csv(link_ds)
    
    idx = random.randint(0, df.shape[0]-1)
    while df.is_annotated.iloc[idx] != 0:
        idx = random.randint(0, df.shape[0]-1)
    return df.sentence.iloc[idx], idx
    

def save_dataset():
    pass


@app.route('/generation', methods=['GET', 'POST'])
def text_generation():
    project_data_link = os.path.join(app.root_path, 'static/datasets', 'sentiment_train.csv')
    text, idx = text_fetcher(project_data_link)
    form = TextGenerationForm()
    # form.label_type.choices = [('1', 'Positive'), ('2', 'Negative')]
    if form.validate_on_submit():
        df = pd.read_csv(project_data_link)
        df['response'] = None
        df['response'].iloc[idx] = form.response.data
        df.is_annotated.iloc[idx] = 1
        df.to_csv(project_data_link, index=False)
        #flash(f'Annotated at {idx} index. and {df.is_annotated.iloc[idx]}, Sentence: { df.sentence.iloc[idx] }, label: { df.label.iloc[idx] }', 'success')
        return render_template('text_generation.html', text=text, idx=idx, form=form)
    return render_template('text_generation.html', text=text, idx=idx, form=form)


# ---------------------- Q/A Generation ----------------
def text_fetcher_qa(link_ds):
    df = pd.read_csv(link_ds)
    idx = random.randint(0, df.shape[0]-1)
    while df.is_annotated.iloc[idx] != 0:
        idx = random.randint(0, df.shape[0]-1)
    return df.question.iloc[idx], df.context.iloc[idx], idx
    

def save_dataset():
    pass


@app.route('/qa', methods=['GET', 'POST'])
def QA():
    project_data_link = os.path.join(app.root_path, 'static/datasets', 'dataset.csv')
    text, context, idx = text_fetcher_qa(project_data_link)
    form = Q_A_Form()
    if form.validate_on_submit():
        df = pd.read_csv(project_data_link)
        df['answer'].iloc[idx] = form.answer.data
        df['explaination'].iloc[idx] = form.explaination.data
        df.is_annotated.iloc[idx] = 1
        df.to_csv(project_data_link, index=False)
        return render_template('qa.html', text=text, context = context,idx=idx, form=form)
    return render_template('qa.html', text=text, context = context, idx=idx, form=form)

# ---------------------- Text Entailment ----------------
def text_fetcher_entailment(link_ds):
    df = pd.read_csv(link_ds)
    
    idx = random.randint(0, df.shape[0]-1)
    while df.is_annotated.iloc[idx] != 0:
        idx = random.randint(0, df.shape[0]-1)
    return df.sentence.iloc[idx], idx
    

def save_dataset():
    pass


@app.route('/entailment', methods=['GET', 'POST'])
def text_entailment():
    project_data_link = os.path.join(app.root_path, 'static/datasets', 'sentiment_train.csv')
    text, idx = text_fetcher_entailment(project_data_link)
    form = TextEntailmentForm()
    form.label_type.choices = [('1', 'Positive'), ('2', 'Negative')]
    if form.validate_on_submit():
        df = pd.read_csv(project_data_link)
        df['hypothesis'].iloc[idx] = form.hypothesis.data
        df['label'].iloc[idx] = form.label.data
        df.is_annotated.iloc[idx] = 1
        df.to_csv(project_data_link, index=False)
        #flash(f'Annotated at {idx} index. and {df.is_annotated.iloc[idx]}, Sentence: { df.sentence.iloc[idx] }, label: { df.label.iloc[idx] }', 'success')
        return render_template('text_entailment.html', text=text, idx=idx, form=form)
    return render_template('text_entailment.html', text=text, idx=idx, form=form)


    
@app.route("/user_dashboard")
@login_required
def userDashboard():
    user = User.query.filter_by(username=current_user.username).first_or_404()
    projects = Project.query.filter_by(author=user).all()
    choice = [(_.id, _.title) for _ in projects]
    form = ProjectDashboardDropdown()
    form.projectType.choices = choice
    
    if form.validate_on_submit():
        pass
    
    return render_template('user_dashboard.html', title='About', form=form, legend='Annotators')



# --------------------------------- Exam ---------------------
@app.route("/exam/<int:user_id>", methods=['GET', 'POST'])
@login_required
def exam(user_id):
    form = ExamForm()
    #user = User.query.get_or_404(user_id)
    project_data_link = os.path.join(app.root_path, 'static/datasets', 'sentiment_train.csv')
    df = pd.read_csv(project_data_link)
    texts = df.sentence.iloc[:5].to_list()
    answer = [str(int(_)) for _ in df.label.iloc[:5].to_list()]
    answer = list(map(lambda x: x.replace('0', 'Positive'), answer))
    answer = list(map(lambda x: x.replace('1', 'Negative'), answer))
    corr = 0
    if form.validate_on_submit():
        if answer[0] == form.q1.data:
            corr+=1
        if answer[1] == form.q2.data:
            corr+=1
        if answer[2] == form.q3.data:
            corr+=1
        if answer[3] == form.q4.data:
            corr+=1
        if answer[4] == form.q5.data:
            corr+=1
        if corr > 0:
            print(corr)
            print("Passed")
            current_user.is_passed = True
            db.session.commit()
            flash('You have Passed', 'success') 
        else:
            flash('You have Failed', 'danger') 
        return redirect(url_for('home')) 
    
    return render_template('exam_page.html', texts=texts, form=form, title='EXAM')
