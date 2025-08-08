from flask import Flask

app = Flask(__name__)

from app import views  # this must come after app = Flask(...)

app.config['SECRET_KEY'] = 'your-secure-secret-key'  # 👈 required for CSRF protection

from app.routes import bp as main_bp
app.register_blueprint(main_bp, url_prefix="/")
