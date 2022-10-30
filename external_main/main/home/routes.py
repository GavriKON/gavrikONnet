from flask import request, render_template, Blueprint
from main.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    PAGE = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.data_posted.desc()).paginate(per_page=4,
                                                                  page=PAGE)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title='About')
