import flask
from flask_sqlalchemy import SQLAlchemy
import validators

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profiles.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), nullable=False)
    link = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
@app.route('/', methods=['GET'])
def hello():
    return flask.render_template('index.html', projects = Project.query.all())

@app.route('/add_project', methods=['POST'])
def add_project():
    title = flask.request.form['title']
    link = flask.request.form['link']
    # if not link.startswith("https://"):
    #     link = "https://" + link

    if validators.url(link):
        print(title, link)
        db.session.add(Project(title = title, link = link))
        db.session.commit()
    
    return flask.redirect(flask.url_for('hello'))

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add(Project(title='Video-to-audio-telegram', link='https://github.com/CYBER-NVORON/Video-to-audio-telegram'))
    db.session.add(Project(title='TelePrinter', link='https://github.com/CYBER-NVORON/TelePrinter'))
    db.session.add(Project(title='Music-Player', link='https://github.com/CYBER-NVORON/Music-Player'))
    db.session.commit()

if __name__ == "__main__":
    print("Пример ввода: Название - itmo-labs-python  Ссылка - https://github.com/CYBER-NVORON/itmo-labs-python")
    app.run(host="0.0.0.0")