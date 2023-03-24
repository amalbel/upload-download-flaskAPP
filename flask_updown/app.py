from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from flask import make_response


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    data = db.Column(db.LargeBinary)

@app.route('/')
def index():
    files = File.query.all()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    new_file = File(name=file.filename, data=file.read())
    db.session.add(new_file)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/download/<int:id>')
def download(id):
    file_data = File.query.filter_by(id=id).first()
    response = make_response(file_data.data)
    response.headers.set('Content-Type', 'application/octet-stream')
    response.headers.set('Content-Disposition', 'attachment', filename=file_data.name)
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
