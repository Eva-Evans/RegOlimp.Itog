from flask import Flask, redirect, render_template
from config import Configuration
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_babelex import Babel
from flask_admin.contrib.sqla import ModelView


login = LoginManager()

app = Flask(__name__)
app.config.from_object(Configuration)


db = SQLAlchemy(app)

login.init_app(app)
login.login_view = 'login'

babel = Babel(app)



#Admin Panel

from models import *


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.role == 1:
            return current_user

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/login')


admin = Admin(app, index_view=MyAdminIndexView())


admin.add_view(ModelView(Olimp, db.session))
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(School, db.session))
admin.add_view(ModelView(Klass, db.session))
admin.add_view(ModelView(Grade, db.session))
