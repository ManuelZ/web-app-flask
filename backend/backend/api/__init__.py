from flask import Blueprint

bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")

from backend.api import views
