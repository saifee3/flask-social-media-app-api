from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from models import db
from routes import bp as main_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "your-secret-key"  
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=72) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///My_Database_user_22.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(main_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
