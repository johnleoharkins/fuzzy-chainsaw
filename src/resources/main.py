from flask import jsonify, render_template
from flask_smorest import Blueprint, abort
from flask.views import MethodView

blp = Blueprint("Main", __name__, description="Operations on main")


@blp.route("/home")
class Home(MethodView):
    @blp.response(200)
    def get(self):
        home_data = jsonify(data="home data")
        return home_data


@blp.route("/")
class MainIndex(MethodView):
    def get(self):
        return render_template('index.html')


@blp.route("/hello-world")
class HelloWorld(MethodView):
    def get(self):
        return """
        <p>Hello, World!</p>
        <ul>
            <li>
                <a href="/">Home</a>
            </li>
        </ul>"""

