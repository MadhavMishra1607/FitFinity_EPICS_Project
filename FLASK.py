from flask import Flask , render_template , request
import mysql.connector

# function to calculate BMI
def calculate_bmi(weight, height):
    bmi = weight / ((height/100)**2)
    return round(bmi, 2)

app = Flask(__name__)

@app.route('/')
def styling():
    return render_template("Landingpage.html")
@app.route('/Analysis')
def analysis():
    return render_template("analytics.html")
@app.route('/About us')
def about():
    return render_template("about.html")
@app.route('/Contact us')
def contact():
    return render_template("contact.html")
@app.route('/Get Started')
def getstarted():
    return render_template("form1.html")

# route to handle the form 1 submission
@app.route('/NEXT', methods=['GET','POST'])
def submit():
    if (request.method=='POST'):
       name = request.form.get['name']
       age = request.form.get['age']
       height = request.form.get['height']
       weight = request.form.get['weight']
       gender = request.form.get['gender']
    bmi = calculate_bmi(float(weight), float(height))
    # Database connection
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="user_info") 
                        
    #Create cursor
    cursor = mydb.cursor()

    # Insert user details into the database
    query = "INSERT INTO users (name, age, height, weight, gender, bmi) VALUES (%s, %s, %s, %s, %s)"
    values = (name, age, height, weight, gender, bmi)
    cursor.execute(query, values)
    mydb.commit()

    return "Data inserted successfully!"

   # return the user's details from the database
    cursor.execute("SELECT * FROM users WHERE id=%s", (cursor.lastrowid,))
    result = cursor.fetchone()
    return render_template('form2.html', result=result)

# route to handle the form 2 submission
@app.route('/GET YOUR RESULTS', methods=['GET','POST'])
def submit1():
    if (request.method=='POST'):
       stress_level = request.form.get['stress_level']
       activity_level = request.form.get['activity_level']

    
    # return the user's details from the database
    return render_template('report.html',  stress_level=stress_level, activity_level=activity_level)

# route to handle the form submission and match the entered values with the database
@app.route('/GET YOUR RESULTS', methods=['GET','POST'])
def yoga_diet():
    if (request.method=='POST'):
       # get the medical complications entered by the user
       medical_complications = request.form.getlist('medical_complications')

    # create a connection to the database
    mydb1 = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="yoga_diet")
    
    # create a cursor object to execute SQL queries
    cursor = mydb1.cursor()

    # create an empty list to store the matching yoga asanas and dietary habits
    matching_results = []
    
    # iterate over each medical complication entered by the user
    for medical_complication in medical_complications:
        # execute a SQL query to get the matching yoga asanas and dietary habits
        cursor.execute("SELECT yoga_asanas, dietary_habits FROM yoga_asanas WHERE medical_complication=?", (medical_complication,))
        
        # fetch all the matching results
        results = cursor.fetchall()
         # append the matching results to the list
        matching_results.extend(results)
    
    # close the connection to the database
    mydb1.close()
    
    # render the results template with the matching yoga asanas and dietary habits
    return render_template('report.html', matching_results=matching_results)
    
if __name__== '_main_':
    app.run(debug=True)