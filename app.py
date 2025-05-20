from flask import Flask, session, render_template
from config import Config

app = Flask(__name__,)
app.config.from_object(Config)

from controllers.admin_controller import admin_bp
from controllers.student_controller import student_bp

app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)