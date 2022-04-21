from app import app
from posts.blueprint import posts
import view

app.register_blueprint(posts, url_prefix='/account')

if __name__ == '__main__':
    app.run()
