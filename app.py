from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine, text
from models.models import *
import hashlib

app = Flask(__name__)
app.secret_key="somesupersecretkey"
#Please return to your default port 3306
app.config['SQLALCHEMY_DATABASE_URI']='mysql+mysqlconnector://robertsru:SOPcourse123@localhost:13306/sti_data'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')

@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['username'].lower()
        password_entered = request.form['password']
        #decrypt the password
        hash = password_entered + app.secret_key
        hash = hashlib.sha256(hash.encode())
        password = hash.hexdigest()
        #check if the user exists in the database
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}' and password = '{password}'"))
            account = result.fetchone()
            con.commit()

        if account:
            session['loggedin'] = True
            session['id'] = account.id
            session['username'] = account.username
            msg = "Logged in successfully"
            return redirect(url_for('home', msg=msg))
        else:
            msg = "Incorrect username/password"
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg =""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #get the form values
        username = request.form['username'].lower()
        cusername = request.form['cusername'].lower()
        password = request.form['password']
        cpassword = request.form['cpassword']
        if username!=cusername:
            msg = "Usernames do not match"
            return render_template('register.html', msg=msg)
        if password!=cpassword:
            msg = "Passwords do not match"
            return render_template('register.html', msg=msg)
        with engine.connect() as con:
            result = con.execute(text(f"Select * from user where username = '{username}'"))
            account = result.fetchone()
            con.commit()
        if account:
            msg = "Account already exists"
            return render_template('register.html', msg=msg)
        
        if not username or not password or not cusername or not cpassword:
                msg = "Please fill out the form"
                return render_template('register.html', msg=msg)
        else:
            #encrypt the password
            hash = password + app.secret_key
            hash = hashlib.sha256(hash.encode())
            password = hash.hexdigest()
            #insert the user into the database
            with engine.connect() as con:
                con.execute(text(f"Insert into user (username, password) values ('{username}', '{password}')"))
                con.commit()
            msg = "Account created successfully"
            return redirect(url_for('login', msg=msg))
    return render_template('register.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

       
  
@app.route('/congenital_syphilis')
def congenital_syphilis():
    return render_template('congenital_syphilis.html')

@app.route('/hepatitis')
def hepatitis():
    return render_template('hepatitis.html')

@app.route('/sti')
def sti():
    return render_template('sti.html')


#The page for the client registration
@app.route('/register_client', methods=['POST'])
def register_client():
    #get the data from the form
    if request.method=='POST' and 'unique_id' in request.form:
        unique_id = request.form['unique_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        date_of_birth = request.form['dob']
        country_of_birth = request.form['country_of_birth']
        sex = request.form['gender']
        marital_status = request.form['marital-status']
        occupation = request.form['occupation']
        gender_identity = request.form['gender-identity']
        sexual_orientation = request.form['sexual-orientation']
        phone_number = request.form['phone']
        address = request.form['line1']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip-code']
        country = request.form['country']
        email = request.form['email']
        ethnicity = request.form['ethnicity']
        race = request.form['race']
        #check if the unique_id is already in the database
        with engine.connect() as con:
            result = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{unique_id}'"))
            client = result.fetchone()
            if client:
                msg = 'The client already exists.'
                return redirect(url_for('home', msg = msg))
        #check if all the required fields are filled
        
        #insert the values in the database
        created_at = datetime.now()
        updated_at = datetime.now()
        created_by = session['username']
        updated_by = session['username']
        with engine.connect() as con:
            con.execute(text(f"INSERT INTO client_profile(created_by, created_at, updated_at, updated_by, unique_id, first_name, last_name, middle_name, date_of_birth,\
                                      country_of_birth, gender, marital_status, occupation, gender_identity,\
                                      sexual_orientation, phone_number, address, city, state, zip_code, country,\
                                      email, ethnicity, race)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}', '{first_name}', '{last_name}', '{middle_name}',\
                                      '{date_of_birth}', '{country_of_birth}', '{sex}', '{marital_status}',\
                                      '{occupation}', '{gender_identity}','{sexual_orientation}', '{phone_number}',\
                                      '{address}', '{city}', '{state}', '{zip_code}', '{country}', '{email}',\
                                      '{ethnicity}', '{race}'\
                                    )"))
            
            con.execute(text(f"INSERT INTO client_screening_sti(created_by, created_at, updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
        
            con.execute(text(f"INSERT INTO client_treatment_sti(created_by, created_at, updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
            con.execute(text(f"INSERT INTO congenital_syphilis_mothers(created_by, created_at,updated_at, updated_by, unique_id, infant_unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}', '{unique_id}+infant')"))
            con.execute(text(f"INSERT INTO congenital_syphilis_infant(created_by, created_at,updated_at, updated_by, infant_unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}+infant')"))
            
            con.execute(text(f"INSERT INTO hepatitis_b_mothers(created_by, created_at, updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
            con.execute(text(f"INSERT INTO partner_management_sti(created_by, created_at, updated_at, updated_by, unique_id)\
                                      VALUES('{created_by}','{created_at}', '{updated_at}', '{updated_by}','{unique_id}')"))
        
            con.commit()
        msg = 'You have successfully registered the client.';
        # redirect the user to the home page
        return redirect(url_for('home', msg = msg))
    return render_template('home.html')

#The retieve client page based on passed client_id
@app.route('/retrieve_client', methods=['POST'])
def retrieve_client():
    msg = ''
    #get the client_id from the urlß
    client_id = request.form['client_id']
    #validate the client_id
    #if the client_id is not valid, redirect to the home page
    #if the client_id is valid, continue
    if 'loggedin' in session:
        if client_id:
            #get the client data from the database
            with engine.connect() as con:
                result_profile = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{client_id}'"))
                result_hepatitis = con.execute(text(f"SELECT * FROM hepatitis_b_mothers WHERE unique_id = '{client_id}'"))
                result_screening_sti = con.execute(text(f"SELECT * FROM client_screening_sti WHERE unique_id = '{client_id}'"))
                result_treatment_sti = con.execute(text(f"SELECT * FROM client_treatment_sti WHERE unique_id = '{client_id}'"))
                result_congenital_syphilis_mothers = con.execute(text(f"SELECT * FROM congenital_syphilis_mothers WHERE unique_id = '{client_id}'"))
                result_congenital_syphilis_infant = con.execute(text(f"SELECT * FROM congenital_syphilis_infant WHERE infant_unique_id = '{client_id}+infant'"))
                result_partner_management_sti = con.execute(text(f"SELECT * FROM partner_management_sti WHERE unique_id = '{client_id}'"))

                client_profile = result_profile.fetchone()
                client_hepatitis = result_hepatitis.fetchone()
                client_screening_sti = result_screening_sti.fetchone()
                client_treatment_sti = result_treatment_sti.fetchone()
                client_congenital_syphilis_mothers = result_congenital_syphilis_mothers.fetchone()
                client_congenital_syphilis_infant = result_congenital_syphilis_infant.fetchone()
                client_partner_management_sti = result_partner_management_sti.fetchone()

                con.commit()
            if client_profile and client_hepatitis and client_screening_sti and client_treatment_sti and client_congenital_syphilis_mothers and client_congenital_syphilis_infant and client_partner_management_sti:
                #display the client data
                return render_template('profile.html', client = client_profile, hepatitis = client_hepatitis, screening_sti = client_screening_sti, treatment_sti = client_treatment_sti, congenital_syphilis_mothers = client_congenital_syphilis_mothers, congenital_syphilis_infant = client_congenital_syphilis_infant, partner_management_sti = client_partner_management_sti)
                                     
            else:
                #redirect to the home page
                msg = 'The client does not exist.'
                return redirect(url_for('home', msg = msg))
    return redirect(url_for('login'))
    
@app.route('/update_profile', methods=['POST'])
def update_profile():
    msg=""
    client_id = request.form['unique_id']
    if 'loggedin' in session:
        if client_id:
            #get the client data from the database
            with engine.connect() as con:
                result_profile = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{client_id}'"))
                client_profile = result_profile.fetchone()
                con.commit()
            if client_profile:
                update_at = datetime.now()
                updated_by = session['username']
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                middle_name = request.form['middle_name']
                date_of_birth = request.form['dob']
                country_of_birth = request.form['country_of_birth']
                gender = request.form['gender']
                marital_status = request.form['marital-status']
                occupation = request.form['occupation']
                gender_identity = request.form['gender-identity']
                sexual_orientation = request.form['sexual-orientation']
                phone_number = request.form['phone']
                address = request.form['line1']
                city = request.form['city']
                state = request.form['state']
                zip_code = request.form['zip-code']
                country = request.form['country']
                email = request.form['email']
                ethnicity = request.form['ethnicity']
                race = request.form['race']
                with engine.connect() as con:
                    result = con.execute(text(f"UPDATE client_profile SET updated_at = '{update_at}', updated_by = '{updated_by}',\
                                              first_name = '{first_name}', last_name = '{last_name}',\
                                                middle_name = '{middle_name}', date_of_birth = '{date_of_birth}',\
                                                country_of_birth = '{country_of_birth}', gender = '{gender}',\
                                                marital_status = '{marital_status}', occupation = '{occupation}',\
                                                gender_identity ='{gender_identity}', sexual_orientation = '{sexual_orientation}',\
                                                phone_number = '{phone_number}', address = '{address}', city = '{city}',\
                                                state = '{state}', zip_code = '{zip_code}', country = '{country}',\
                                                email = '{email}', ethnicity = '{ethnicity}', race ='{race}' WHERE unique_id = '{client_id}'"))
                    con.commit()
                msg = "Client profile updated successfully"
                return render_template('home.html', msg=msg)
                
            else:
                #redirect to the home page
                msg = 'The client does not exist.'
                return redirect(url_for('home', msg = msg))

@app.route('/update_chlagon',methods=['POST'])
def update_chlagon():
    msg = ''
    #get the client_id from the urlß
    client_id = request.form['unique_id']
    #validate the client_id
    #if the client_id is valid, continue
    if 'loggedin' in session:
        if client_id:
             #get the client data from the database
            with engine.connect() as con:
              
                result_profile = con.execute(text(f"SELECT * FROM client_profile WHERE unique_id = '{client_id}'"))
                result_hepatitis = con.execute(text(f"SELECT * FROM hepatitis_b_mothers WHERE unique_id = '{client_id}'"))
                result_screening_sti = con.execute(text(f"SELECT * FROM client_screening_sti WHERE unique_id = '{client_id}'"))
                result_treatment_sti = con.execute(text(f"SELECT * FROM client_treatment_sti WHERE unique_id = '{client_id}'"))
                result_congenital_syphilis_mothers = con.execute(text(f"SELECT * FROM congenital_syphilis_mothers WHERE unique_id = '{client_id}'"))
                result_congenital_syphilis_infant = con.execute(text(f"SELECT * FROM congenital_syphilis_infant WHERE infant_unique_id = '{client_id}+infant'"))
                result_partner_management_sti = con.execute(text(f"SELECT * FROM partner_management_sti WHERE unique_id = '{client_id}'"))
                
                client_profile = result_profile.fetchone()
                client_screening_sti = result_screening_sti.fetchone()
                client_treatment_sti = result_treatment_sti.fetchone()
                client_partner_management_sti = result_partner_management_sti.fetchone()

                client_profile = result_profile.fetchone()
                client_hepatitis = result_hepatitis.fetchone()
                client_screening_sti = result_screening_sti.fetchone()
                client_treatment_sti = result_treatment_sti.fetchone()
                client_congenital_syphilis_mothers = result_congenital_syphilis_mothers.fetchone()
                client_congenital_syphilis_infant = result_congenital_syphilis_infant.fetchone()
                client_partner_management_sti = result_partner_management_sti.fetchone()

                con.commit()
           
            #replace with the updated data from the form
                
            #screening info
            if client_screening_sti:
                updated_at = datetime.now()
                updated_by = session['username']
                date_of_screening=request.form["date_of_screening"]
                if date_of_screening is '':
                    date_of_screening='1900-01-01'
                health_care_provider = request.form["health_care_provider"]
                reporter_name=request.form["reporter_name"]
                reporter_contact=request.form["reporter_contact"]
                sexual_partner_gender = request.form["sexual_partner_gender"]
                sexual_partner_gender_identity=request.form["sexual_partner_gender_identity"]
                previous_HIV_screening=request.form["previous_HIV_screening"]
                previous_HIV_screening_date=request.form["previous_HIV_screening_date"]
                if previous_HIV_screening_date is '':
                    previous_HIV_screening_date='1900-01-01'
                previous_HIV_screening_result=request.form["previous_HIV_screening_result"]
                reason_for_testing=request.form["reason_for_testing"]
                screening_type=request.form["screening_type"]
                site_of_sample_collection=request.form["site_of_sample_collection"]
                sample_collection_date=request.form["sample_collection_date"]
                if sample_collection_date is '':
                    sample_collection_date='1900-01-01'
                screening_result=request.form["screening_result"]
                screening_notes=request.form["screening_notes"]
                diagnosis=request.form["diagnosis"]
            
            #get updated treatment info
            if client_treatment_sti:
                 updated_at = datetime.now()
                 updated_by = session['username']
                 date_of_treatment=request.form["cts_date_of_treatment"]
                 if date_of_treatment is '':
                     date_of_treatment='1900-01-01'
                 health_care_provider=request.form["cts_health_care_provider"]
                 reporter_name=request.form["cts_reporter_name"]
                 reporter_contact=request.form["cts_reporter_contact"]
                 treatment_type=request.form["treatment_type"]
                 treatment_plan=request.form["treatment_plan"]
                 treatment_notes=request.form["treatment_notes"]
                 treatment_result=request.form["treatment_result"]

            #get partner information
            if client_partner_management_sti:
                 updated_at = datetime.now()
                 updated_by = session['username']
                 date_of_treatment=request.form["date_of_partner_management"]
                 if date_of_treatment is '':
                     date_of_treatment='1900-01-01'
                 health_care_provider=request.form["cpms_health_care_provider"]
                 reporter_name=request.form["cpms_reporter_name"]
                 reporter_contact=request.form["cpms_reporter_contact"]
                 partner_management_type=request.form["partner_management_type"]
                 partner_management_plan=request.form["partner_management_plan"]
                 partner_management_notes=request.form["partner_management_notes"]
                 partner_management_result=request.form["partner_management_result"]

            #perform additional non-enduser validation checks here... 

            with engine.connect() as con:
                    css_result = con.execute(text(f"UPDATE client_screening_sti set updated_at ='{updated_at}' , updated_by = '{updated_by}', \
                                            date_of_screening='{date_of_screening}',health_care_provider = '{health_care_provider}',\
                reporter_name='{reporter_name}',\
                reporter_contact='{reporter_contact}',\
                sexual_partner_gender = '{sexual_partner_gender}',\
                sexual_partner_gender_identity='{sexual_partner_gender_identity}',\
                previous_HIV_screening='{previous_HIV_screening}',\
                previous_HIV_screening_date='{previous_HIV_screening_date}',\
                previous_HIV_screening_result='{previous_HIV_screening_result}',\
                reason_for_testing='{reason_for_testing}',\
                screening_type='{screening_type}',\
                site_of_sample_collection='{site_of_sample_collection}',\
                sample_collection_date='{sample_collection_date}',\
                screening_result='{screening_result}',\
                screening_notes='{screening_notes}',\
                diagnosis='{diagnosis}'"))
                    
                    cts_result = con.execute(text(f"UPDATE client_treatment_sti set \
                                              updated_at = '{updated_at}', \
                 updated_by = '{updated_by}',date_of_treatment='{date_of_treatment}',\
                 health_care_provider='{health_care_provider}',\
                 reporter_name='{reporter_name}',\
                 reporter_contact='{reporter_contact}',\
                 treatment_type='{treatment_type}',\
                 treatment_plan='{treatment_plan}',\
                 treatment_notes='{treatment_notes}',\
                 treatment_result='{treatment_result}'"))
                    
                    cpms_result = con.execute(text(f"UPDATE partner_management_sti set \
                                           updated_at ='{updated_at}',\
                 updated_by = '{updated_by}',date_of_partner_management='{date_of_treatment}',\
                 health_care_provider='{health_care_provider}',reporter_name='{reporter_name}',\
                 reporter_contact='{reporter_contact}',partner_management_type='{partner_management_type}',\
                 partner_management_plan='{partner_management_plan}',partner_management_notes='{partner_management_notes}',\
                 partner_management_result='{partner_management_result}'"))
            con.commit()
            msg=""
            if css_result:
                msg+="Failed to update client screening sti section"
            elif cts_result:
                msg+="Failed to update client treatment sti section"
            elif cpms_result:
                msg+="Failed to update client partner Management Section"
            else:
                msg = "Client Chlamydia and Gonnorrhea Sections updated successfully"
           # return render_template('profile.html',msg=msg, client = client_profile, screening_sti = client_screening_sti, treatment_sti = client_treatment_sti, partner_management_sti = client_partner_management_sti)
            return render_template('profile.html',msg=msg, client = client_profile, hepatitis = client_hepatitis, screening_sti = client_screening_sti, treatment_sti = client_treatment_sti, congenital_syphilis_mothers = client_congenital_syphilis_mothers, congenital_syphilis_infant = client_congenital_syphilis_infant, partner_management_sti = client_partner_management_sti)
        else:
            #redirect to the home page
            msg = 'The client does not exist.'
            return redirect(url_for('home', msg = msg))
