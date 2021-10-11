
from flask import Flask, render_template, request, redirect, url_for ,flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.secret_key = "Secret Key"

mydb=app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sikandar123$@localhost:3306/python_for_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    d_name = db.Column(db.String(80), nullable=False)
    d_description = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)



#doctor class

class Doctr(db.Model):
    __tablename__="doctor"
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    depart_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phon_no = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)

#Nurse class
class Nurse(db.Model):
    __tablename__="nurse"
    id = db.Column(db.Integer, primary_key=True)
    Nurse_Name = db.Column(db.String(100), nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    Phon_No = db.Column(db.String(14), nullable=False)
    date = db.Column(db.String(12), nullable=True)

#Patients class

class Patient(db.Model):
    __tablename__="patient"
    id = db.Column(db.Integer, primary_key=True)
    P_Name = db.Column(db.String(100), nullable=False)
    P_Address = db.Column(db.String(100), nullable=False)
    Phone_no = db.Column(db.String(14), nullable=False)
    Sex = db.Column(db.String(14), nullable=False)
    Age = db.Column(db.String(14), nullable=False)
    Blood_Group = db.Column(db.String(3), nullable=False)
    date = db.Column(db.String(12), nullable=True)
#login class

class Registr(db.Model):
    __tablename__="register"
    user = db.Column(db.String(100) ,  primary_key=True)
    email = db.Column(db.String(100))
    u_pass=db.Column(db.String(14))
    rpass = db.Column(db.String(14))


#index page
@app.route('/', methods = ['GET','POST'])
def index():
    return render_template("index.html")

#login
@app.route('/form_login', methods=['POST', 'GET'])
def login():
        if "username" in session:
            return redirect(url_for("department"))
        else:
            name1 = request.form['username']
            pwd = request.form['password']
            data = Registr.query.filter_by(user=name1, u_pass=pwd).first()
            if not data:
                flash("Incorrect use rand Password")
                return render_template("index.html")
            else:
                session["username"] = name1
                return render_template("department.html")
#logout
@app.route('/logout' , methods=['GET','POST'])
def logout():
    session.pop('username', None)

    return render_template("index.html")




#department
@app.route('/department', methods = ['GET','POST'])
def department():
    if "username" in session:
        entry = Department.query.all()
        return render_template("department.html", edit = entry)
    else:
        return render_template("index.html")

# Add page

@app.route('/insert', methods = ['GET','POST'])
def insert():
    if  request.method=='POST':
        '''Add enter database'''
        deptName=request.form['deptName']
        deptDesc=request.form['deptDesc']

        '''
           sno, d_name ,d_description,date
           '''
        entry = Department(d_name=deptName, d_description=deptDesc ,date= datetime.now())
        db.session.add(entry)
        db.session.commit()
        flash("Department Add Successfully")

    return redirect(url_for('department'))

#update
@app.route("/update/",methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        up_d = Department.query.filter_by(id=id).first()

        up_d.d_name = request.form['deptName']
        up_d.d_description = request.form['deptDesc']

        db.session.commit()
        flash("Department Updated Successfully")

        return redirect(url_for('department'))

# This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    entry = Department.query.filter_by(id=id).first()
    db.session.delete(entry)
    db.session.commit()
    flash("Department Deleted Successfully")

    return redirect(url_for('department'))



#doctor

@app.route('/doctor', methods = ['GET','POST'])
def doctor():
    if "username" in session:
        entr = Doctr.query.all()
        entr1 = Department.query.all()
        return render_template("doctor.html", doc = entr, department=entr1)
    else:
        return render_template("index.html")
#add doctor
@app.route('/docadd', methods=['GET','POST'])
def docadd():
    if request.method == 'POST':
        doctname = request.form['doctname']
        dept = request.form['dept']
        add = request.form['add']
        phon = request.form['phon']

        entr = Doctr(doctor_name=doctname, depart_name=dept, address=add,phon_no=phon,date=datetime.now())
        db.session.add(entr)
        db.session.commit()

        flash("Doctor Details Add Successfully")



        return redirect(url_for('doctor'))

#docter edit
@app.route("/doctrupdate", methods = ['GET', 'POST'])
def doctrupdate():
    if "username" in session:
     if request.method == 'POST':
        id = request.form['doctid']
        entr = Doctr.query.filter_by(id=id).first()
        entr.doctor_name = request.form['doctname']
        entr.depart_name = request.form['dept']
        entr.address = request.form['add']
        entr.phon_no = request.form['phon']

        db.session.commit()
        flash("Doctor Details Updated Successfully")

        return redirect(url_for('doctor'))
    else:
        return render_template("index.html")


#doctor delete
@app.route('/docdelete/<id>/', methods=['GET', 'POST'])
def docdelete(id):
    entr = Doctr.query.filter_by(id=id).first()
    db.session.delete(entr)
    db.session.commit()
    flash("Doctor Detail Deleted Successfully")

    return redirect(url_for('doctor'))

#Nurse----------

@app.route('/nurse', methods = ['GET','POST'])
def nurse():
    if "username" in session:

        nentr = Nurse.query.all()

        return render_template("nurse.html" , nus = nentr)
    else:
        return render_template("index.html")

#Add Nurse

@app.route('/nusadd', methods=['GET','POST'])
def nusadd():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']

        nentr = Nurse(Nurse_Name=name, Address=address, Phon_No=phone,date=datetime.now())
        db.session.add(nentr)
        db.session.commit()

        flash("Nurse Details Add Successfully")



        return redirect(url_for('nurse'))

#Nurse edit
@app.route("/nsupdate", methods = ['GET', 'POST'])
def nsupdate():
    if request.method == 'POST':
        id = request.form['nid']
        nentr = Nurse.query.filter_by(id=id).first()

        nentr.Nurse_Name = request.form['name']
        nentr.Address = request.form['address']
        nentr.Phon_No = request.form['phone']

        db.session.commit()
        flash("Nurse info Updated Successfully")

        return redirect(url_for('nurse'))


#Nurse Delete

@app.route('/nusdelete/<id>/', methods=['GET', 'POST'])
def nusdelete(id):
    nentr = Nurse.query.filter_by(id=id).first()
    db.session.delete(nentr)
    db.session.commit()
    flash("Nurse info Deleted Successfully")

    return redirect(url_for('nurse'))

#patients-------------
@app.route('/patients' , methods = ['GET' , 'POST'])
def patients():
    if "username" in session:
        pentr = Patient.query.all()

        return render_template('patients.html', pnt = pentr)
    else:
        return render_template("index.html")
#Patients Add

@app.route('/ptadd', methods=['GET','POST'])
def ptadd():
    if request.method == 'POST':
        patientname = request.form['patientname']
        addres = request.form['addres']
        phn = request.form['phn']
        sex = request.form['sex']
        age = request.form['age']
        bdgrp = request.form['bdgrp']

        pentr = Patient(P_Name=patientname, P_Address=addres, Phone_no=phn, Sex=sex, Age=age , Blood_Group=bdgrp ,date=datetime.now())
        db.session.add(pentr)
        db.session.commit()

        flash("Patient Details Add Successfully")

        return redirect(url_for('patients'))

#patients Edit
@app.route("/pupdate", methods = ['GET', 'POST'])
def pupdate():
    if request.method == 'POST':
        id = request.form['pid']
        pentr = Patient.query.filter_by(id=id).first()

        pentr.P_Name = request.form['patientname']
        pentr.P_Address = request.form['addres']
        pentr.Phone_no = request.form['phn']
        pentr.Sex = request.form['sex']
        pentr.Age = request.form['age']
        pentr.Blood_Group = request.form['bdgrp']

        db.session.commit()
        flash("Patient info Updated Successfully")

    return redirect(url_for('patients'))

#Patient Delete

@app.route('/pdelete/<id>/', methods=['GET', 'POST'])
def pdelete(id):
    pentr = Patient.query.filter_by(id=id).first()
    db.session.delete(pentr)
    db.session.commit()
    flash("Patient info Deleted Successfully")

    return redirect(url_for('patients'))

#profile----------

@app.route('/profile' , methods = ['GET','POST'])
def profile():
    if "username" in session:
        return render_template('profile.html')
    else:
        return render_template("index.html")

#change
@app.route('/updatepwd' , methods=['GET', 'POST'])
def updatepwd():
    if "username" in session:
        name1 = session["username"]
        pwd = request.form['password']
        data = Registr.query.filter_by(user=name1, u_pass=pwd).first()
        if not data:
            msg = "Incorrect Password"
            return render_template("profile.html",msg = msg)
        else:
            newpwd = request.form['newpwd']
            conpwd = request.form['conpwd']
            if newpwd != conpwd:
                msg = "Password Not Matched"
                return render_template("profile.html", msg1 = msg)
            else:
                update = Registr.query.filter_by(user=name1).first()
                update.u_pass = newpwd
                db.session.commit()
                flash('password updated secessfully')
                return render_template("profile.html")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
