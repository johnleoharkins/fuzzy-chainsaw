
from flask import jsonify, render_template
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from src.models import RedditDataModel
from src.schemas import RedditDataSchema

blp = Blueprint("Reddit", __name__, "Operations on reddit")

@blp.route("/reddit")
class Reddit(MethodView):
    @blp.response(200, RedditDataSchema(many=True))
    def get(self):
        try:
            return RedditDataModel.query.all()
        except SQLAlchemyError:
            abort(500, message="SQLAlchemyError during game lookup.")
