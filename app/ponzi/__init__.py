from flask import Blueprint

ponzibp = Blueprint('ponzi', __name__)

from . import views