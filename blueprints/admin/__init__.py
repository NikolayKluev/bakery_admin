from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

admin_bp = Blueprint("admin", __name__, template_folder="../../templates/admin")
db = SQLAlchemy()
