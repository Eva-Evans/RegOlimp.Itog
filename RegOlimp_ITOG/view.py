from flask_login import current_user, login_user, logout_user
from app import app, db, babel
from flask import render_template, request, flash, redirect, url_for
from models import Users, Olimp, Grade
from forms import LoginForm, RegFormOrg, RegFormTeach, RegFormStud, CreateOlimp, EditOlimp, RecordStud, FormGrade
from flask_login import login_required


@app.route('/')
def index():
    q = request.args.get('q')

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        posts = Olimp.query.filter(Olimp.title.contains(q) | Olimp.body.contains(q))#.all()
    else:
        posts = Olimp.query.order_by(Olimp.created.desc())

    pages = posts.paginate(page=page, per_page=8)

    return render_template('index.html', posts=posts, pages=pages)


@app.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Olimp.query.filter(Olimp.slug == slug).first()
    if request.method == 'POST':
        form = EditOlimp(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('post_detail', slug=post.slug))
    form = EditOlimp(obj=post)
    return render_template('edit_post.html', post=post, form=form)


@app.route('/<slug>/edit_grade', methods=['POST', 'GET'])
@login_required
def edit_grade(slug):
    print(slug)
    param = slug.split("|")
    print(param)
    grade = Grade.query.filter(Grade.id == param[0]).first()
    if request.method == 'POST':
        form = FormGrade(formdata=request.form, obj=grade)
        form.populate_obj(grade)
        db.session.commit()
        return redirect(url_for('post_detail', slug=param[1]))
    form = FormGrade(obj=grade)
    return render_template('edit_grade.html', post=grade, form=form)


@app.route('/olimps_user/<slug>')
@login_required
def user_detail(slug):
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    usertag = Users.query.filter(Users.email == slug).first()
    posts = usertag.olimps#.all()
    pages = posts.paginate(page=page, per_page=8)
    return render_template('olimps_user.html', posts=posts, pages=pages)


@app.route('/<slug>', methods=['POST', 'GET'])
def post_detail(slug):
    post = Olimp.query.filter(Olimp.slug == slug).first()
    form = RecordStud()
    if form.validate_on_submit():
        grade = Grade(user_id=current_user.id, olimp_id=post.id, grade=0)
        db.session.add(grade)
        u = Users.query.filter(Users.id == current_user.id).first()
        post.users.append(u)
        db.session.commit()
    if current_user.is_authenticated:
        grade_user = Grade.query.filter((Grade.user_id == current_user.id) & (Grade.olimp_id == post.id)).first()
        grade_list = Grade.query.filter(Grade.olimp_id == post.id).all()
        return render_template('post_detail.html', post=post, form=form, grade_user=grade_user, grade_list=grade_list)
    return render_template('post_detail.html', post=post)


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = CreateOlimp()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        new_post = Olimp(title=title, body=body)
        db.session.add(new_post)
        db.session.commit()
        usertag = Users.query.filter(Users.email == current_user.get_email()).first()
        new_post1 = Olimp.query.filter(Olimp.title == title).first()
        new_post1.users.append(usertag)
        db.session.commit()
        flash("Данные успешно добавлены в базу")
        return redirect('/create')
    return render_template('create.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/account')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/register_student/', methods=['POST', 'GET'])
def register_student():
    if current_user.is_authenticated:
        return redirect('/blog')

    form_reg_stud = RegFormStud()
    if form_reg_stud.validate_on_submit():
        email = form_reg_stud.email.data
        fio = form_reg_stud.fio.data
        school = str(form_reg_stud.school.data)
        klass = str(form_reg_stud.klass.data)
        password = form_reg_stud.password.data
        if Users.query.filter_by(email=email).first():
            flash("Такой адрес уже присутствует в базе")
            return redirect('/register_student')

        user = Users(email=email, fio=fio, school=school, klass=klass, role=4, active=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Успешная регистрация.")
        flash("Теперь можно авторизоваться на сайте.")
        return redirect('/login')
    return render_template('register_student.html', form=form_reg_stud)


@app.route('/register_teacher/', methods=['POST', 'GET'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect('/blog')

    form_reg_teach = RegFormTeach()
    if form_reg_teach.validate_on_submit():
        school = str(form_reg_teach.school.data)
        email = form_reg_teach.email.data
        fio = form_reg_teach.fio.data
        password = form_reg_teach.password.data
        if Users.query.filter_by(email=email).first():
            flash("Такой адрес уже присутствует в базе")
            return redirect('/register_teacher')

        user = Users(email=email, fio=fio, school=school, role=3, active=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Успешная регистрация.")
        flash("Дождитесь пока администратор подтвердит ваши данные.")
        return redirect('/login')
    return render_template('register_teacher.html', form=form_reg_teach)


@app.route('/register_organizer/', methods=['POST', 'GET'])
def register_organizer():
    if current_user.is_authenticated:
        return redirect('/blog')

    form_reg_org = RegFormOrg()
    if form_reg_org.validate_on_submit():
        email = form_reg_org.email.data
        fio = form_reg_org.fio.data
        password = form_reg_org.password.data
        if Users.query.filter_by(email=email).first():
            flash("Такой адрес уже присутствует в базе")
            return redirect('/register_organizer')

        user = Users(email=email, fio=fio, role=2, active=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Успешная регистрация.")
        flash("Дождитесь пока администратор подтвердит ваши данные.")
        return redirect('/login')
    return render_template('register_organizer.html', form=form_reg_org)


@app.route('/login/', methods=('POST', 'GET'))
def login():
    if current_user.is_authenticated:
        return redirect('/account')

    form_login = LoginForm()
    if form_login.validate_on_submit():
        email = form_login.email.data
        user = Users.query.filter_by(email=email).first()
        if user is not None and user.active == 0:
            flash('Ваша учетная запись не активна. Обратитесь к системному администратору.')
            return render_template("login.html", form=form_login)
        if user is not None and user.check_password(form_login.password.data):
            login_user(user)
            return redirect('/account')
    return render_template("login.html", form=form_login)


@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'ru'


