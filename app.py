from flask import Flask,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy

#Flask object instantiation
app=Flask(__name__)

# URI def format :'postgresql://DB_USER:PASSWORD@HOST/DATABASE'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:RK@localhost/db1'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True)
    email=db.Column(db.String(50),unique=True)

    def __init__(self,username,email):
        self.username=username
        self.email=email

    def __rep__(self):
        return '<User %r>' % self.username

#decorator to map URL function
@app.route('/')
def home():
    #render_template() renders the template
    return render_template('add_user.html')

@app.route('/post_user',methods=['POST'])
def post_user():
    if request.method == 'POST':
        email = request.form['email']
        username=request.form['username']
        # Check that email does not already exist
        if not db.session.query(User).filter(User.email == email).count() and not db.session.query(User).filter(User.username == username).count():

            #creating the User object
            user=User(username,email)
            #adding to database
            db.session.add(user)
            db.session.commit()
        else:
            #flash('Email already taken!')
            return render_template('add_user.html')
    return render_template('index.html')
    
    
#run() makes sure to run only app.py on the server when this script is executed by the Python interpreter
if __name__=='__main__':

    #debug==True activates the Flask debugger and provides detailed error messages

    app.run(debug=True)

