from flask import Flask, render_template
from config import Config
from blueprints.admin import admin_bp, db
from blueprints.admin.routes import login_manager
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "admin.login"
CSRFProtect().init_app(app)

app.register_blueprint(admin_bp, url_prefix="/admin")

@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404

if __name__ == "__main__":
    # with app.app_context(): 
    #     db.create_all()
    app.run(debug=True)
