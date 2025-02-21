from flask import Flask
from api_user import user_blueprint
from api_validate_quiz import quiz_blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(quiz_blueprint)

if __name__ == '__main__':
    app.run(debug=True)