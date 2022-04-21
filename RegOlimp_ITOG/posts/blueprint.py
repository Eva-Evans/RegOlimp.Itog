from flask import Blueprint, render_template
from flask_login import login_required


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
@login_required
def index():
    return render_template('posts/index.html')
