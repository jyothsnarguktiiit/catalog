from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin

engine=create_engine('sqlite:///iii.db')
engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

app=Flask(__name__)


login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'


app.config['MAIL_SERVER']="smtp.gmail.com"
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']="jyothsnajonnadula123@gmail.com"
app.config['MAIL_PASSWORD']='jyothsna@123'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.secret_key='abc'

mail=Mail(app)
otp=randint(000000,999999)


@app.route("/sample")
def demo ():
    return "hello world welcome iiit"

@app.route("/demo")
def d():
    return "<h1>Hello demo page</h1>"

@app.route("/info/details")
def f():
    return "hello details"

@app.route("/details/<name>")
def info(name):
    return "hello {}".format(name)

@app.route("/det/<name>/<int:age>/<float:salary>")
def ik(name,age,salary):
    return "hello {} age is {} and salary {}".format(name,age,salary)

@app.route("/admin")
def admin():
    return "Hello Admin"

@app.route("/student")
def student():
    return "Hello student"

@app.route("/staff")
def staff():
    return "Hello staff"

@app.route("/info/<name>")
def admin_info(name):
    if name=='admin':
        return redirect(url_for('admin'))
    elif name=='staff':
        return redirect(url_for('staff'))
    elif name=='student':
        return redirect(url_for('student'))
    else:
        return "no url"
    
@app.route("/data/<name>/<int:age>/<float:salary>")
def demo_html(name,age,salary):
    return render_template('sample.html',n=name,a=age,s=salary)

@app.route("/tabl")
def tj():
    sno=29
    name='jyothsna'
    branch='cse'
    dept='Trainer'
    return render_template('tablee.html',s_no=sno,n=name,b=branch,d=dept,)

data=[{'sno':1,'name':'jyothsna','branch':'cse','dept':'cse dept'},
      {'sno':2,'name':'lakshmi','branch':'ece','dept':'ece dept'},
      {'sno':3,'name':'sushmitha','branch':'cse','dept':'cse dept'}]
@app.route("/dummy_data")
def dummy():
      return render_template("data.html",dummy_data=data)

@app.route("/tablee/<int:number>")
def tablee(number):
    return render_template("tem.html",n=number)

@app.route("/file_upload",methods=['GET','POST'])
def file_upload():
    return render_template("file_upload.html")

@app.route("/success",methods=['GET','POST'])
def success():
    if request.method=='POST':
        f=request.files['file']
        f.save(f.filename)
        
        return render_template("success.html",f_name=f.filename)

@app.route("/email")
def email_send():
    return render_template("email.html")

@app.route("/email_verify",methods=['POST','GET'])
def verify_email():
    email=request.form['email']
    msg=Message("one time password",sender="n151208@rguktn.ac.in",recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template("v_email.html")

@app.route("/email_success",methods=['POST','GET'])
def success_email():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return render_template("email_success.html")
    return "Invalid otp"

@app.route("/")
def index1():
    return render_template('index.html')

@app.route("/show")
@login_required
def showData():
    register=session.query(Register).all()
    
    return render_template('show.html',reg=register)

@app.route("/new",methods=['POST','GET'])
def addData():
    if request.method=='POST':
        newData=Register(name=request.form['name'],
                         surname=request.form['surname'],
                         mobile=request.form['mobile'],
                         email=request.form['email'],
                         branch=request.form['branch'],
                         role=request.form['role'])
        session.add(newData)
        session.commit()
        flash("new Data Addeded...")
        return redirect(url_for('showData'))
    else:
        return render_template('new.html')
    return render_template('new.html')

@app.route("/account",methods=['POST','GET'])
@login_required
def account():
    return render_template("account.html")

@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=='POST':
        userData=User(name=request.form['name'],
                      email=request.form['email'],
                      password=request.form['password'])
        session.add(userData)
        session.commit()
        return render_template('index')
    else:
        return render_template('register.html')

@login_required
@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('showData'))
    
    try:
        if request.method=='POST':
            user=session.query(User).filter_by(email=request.form['email'],password=request.form['password'].first())
            
            if user:
                login_user(user)
                return redirect(url_for('ShowData'))
            else:
                flash("Invalid Login...")
        else:
            return render_template('login.html',title="login")
    except Exception as e:
        flash("login Failed..")
    else:
        return render_template('login.html',title='login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/register_new")
def reg():
    return render_template('register.html')

@app.route("/login_new")
def lo():
    return render_template('login.html')
    
@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
    editedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        editedData.name=request.form['name']
        editedData.surname=request.form['surname']
        editedData.mobile=request.form['mobile']
        editedData.email=request.form['email']
        editedData.branch=request.form['branch']
        editedData.role=request.form['role']
        
        
        session.add(editedData)
        session.commit()
        flash("successfully edit the data.....{}".format(editedData.name))
        return redirect(url_for('showData'))
    else:
        return render_template('edit.html',register=editedData)

@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
    deletedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        session.delete(deletedData)
        session.commit()
        flash("deleted thesuccessfully.....{}".format(deletedData.name))
        return redirect(url_for('showData'))
    else:
        return render_template('delete.html',register=deletedData)

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))


if __name__=='__main__':
    app.run(debug=True)