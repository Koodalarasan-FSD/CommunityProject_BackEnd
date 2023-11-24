from flask import Flask, jsonify, render_template, request, url_for, session, redirect,flash
import json
import urllib.parse
import mysql.connector
import os
from datetime import timedelta
import random
import string
import datetime
from flask_mail import Mail, Message
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import timedelta

#Run these Program in Terminal by including folder inorder to processes for saving(or)updating image files

app = Flask(__name__)

# You should use a strong, random secret key
app.secret_key = '170a7e7f0e5bcc675ce775da22e7ab99'

app.permanent_session_lifetime = timedelta(days=77)


@app.route('/')
def index():
    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')

    else:
        return redirect('user_dashboard')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    

    UserMailId = request.form['useremailid']
    UserPassword = request.form['userpassword']

    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
    )
    # Function to fetch data from the database
    try:
        
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT User_EMAILID from userattributes")
        data = mycursor.fetchall()


        #Below Method are used to compare input(User) with set of datas(ids and passwords) from database
        match_found = False  # A flag to indicate if a match is found
        
        # Iterate through the result and store values into separate lists
        for datas in data:
            user_ids=datas
            if UserMailId == user_ids[0] :
                #print(UserMailId)
                match_found = True
                break  # Exit the loop once a match is found
      
    
    except Exception as e:
        error_messageforuser = 'An error occurred: ' + str(e)
        flash(error_messageforuser, 'error')
        return render_template('loginpage.html', error_messageforuser=error_messageforuser)


    uniqueUserId=""
    PasswordOfUser=""
    User_ActiveStatus=""

    # Authentication logic here
    if match_found:
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT User_ID,User_Password,active_status from userattributes WHERE User_EMAILID=%s",(UserMailId,))
        dataforuserlogin = mycursor.fetchall()
       

        for rowuserdata in dataforuserlogin:
            
            uniqueUserId=rowuserdata[0]
            PasswordOfUser=rowuserdata[1]
            User_ActiveStatus=rowuserdata[2]
        
        print(uniqueUserId)
        
        if UserPassword == PasswordOfUser and User_ActiveStatus == 1:
            
            session.permanent = True
            session['userlogged_in'] = True
            session['uniqueUserId']=uniqueUserId# Storing uniqueUserId in the session inorder to get these value in another app.route
            session['UserMailId'] = UserMailId   # Storing UserMailId in the session inorder to get these value in another app.route
            return jsonify(status=200)
        
        else:
            alert_userlogin="Password is Wrong or Your're Not Authenticated"
            return jsonify(alert_userlogin=alert_userlogin)
    
    else:
        alert_userlogin='Email is Wrong'
        return jsonify(alert_userlogin=alert_userlogin)


@app.route('/vendor_login', methods=['GET', 'POST'])
def vendor_login():
    

    VendorMailId = request.form['vendoremail']
    VendorPassword = request.form['vendorpassword']

    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
    )
    # Function to fetch data from the database
    try:
        
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT Vendor_EMAILID from vendorattributes")
        data = mycursor.fetchall()


        #Below Method are used to compare input(User) with set of datas(ids and passwords) from database
        match_found = False  # A flag to indicate if a match is found
        
        # Iterate through the result and store values into separate lists
        for datas in data:
            vendor_ids=datas
            if VendorMailId == vendor_ids[0] :
                print(VendorMailId)
                match_found = True
                break  # Exit the loop once a match is found
      
    
    except Exception as e:
        error_messageforvendor = 'An error occurred: ' + str(e)
        flash(error_messageforvendor, 'error')
        return render_template('loginpage.html', error_messageforvendor=error_messageforvendor)

    uniqueVendorId=""
    vendorcategory=""
    PasswordOfVendor=""
    ActiveStatus=""

    # Authentication logic here
    if match_found:
        mycursor = mydb.cursor()
        mycursor.execute(
            "SELECT Vendor_ID,Vendor_Category,Vendor_Password,vendoractive_status from vendorattributes WHERE Vendor_EMAILID=%s",(VendorMailId,))
        dataforvendorlogin = mycursor.fetchall()
        

        for rowvendordata in dataforvendorlogin:
            uniqueVendorId=rowvendordata[0]
            vendorcategory=rowvendordata[1]
            PasswordOfVendor=rowvendordata[2]
            ActiveStatus=rowvendordata[3]
        
        
        
        if VendorPassword == PasswordOfVendor and ActiveStatus == 1:
            
            session.permanent = True
            session['vendorlogged_in'] = True
            session['uniqueVendorId']=uniqueVendorId
            session['vendorcategory']=vendorcategory
            session['VendorMailId'] = VendorMailId   # Storing VendorId in the session inorder to get these value in another app.route
            return jsonify(status=200)
        
        else:
            alert_vendorlogin="Password is Wrong or Your're Not Authenticated"
            return jsonify(alert_vendorlogin=alert_vendorlogin)
    
    else:
        alert_vendorlogin='Email is Wrong'
        return jsonify(alert_vendorlogin=alert_vendorlogin)

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    
    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    else:

        uniqueUserId=session.get('uniqueUserId')
        
        userid=""
        username=""
        useraddress=""
        userphoneno=""
        useremailid=""
        userpassword=""
        active_status=""

        
        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="communityproject"
        )
        # Function to fetch data from the database
        try:
            
            mycursor = mydb.cursor()
            mycursor.execute(
                "SELECT * from userattributes WHERE User_ID=%s",(uniqueUserId,))
            data = mycursor.fetchall()

            # Iterate through the result and store values into separate lists
            for rowuserdata in data:
                userid=rowuserdata[0]
                username=rowuserdata[1]
                useraddress=rowuserdata[2]
                userphoneno=rowuserdata[3]
                useremailid=rowuserdata[4]
                userpassword=rowuserdata[5]  #password and activestatus not needed to pass.
                active_status=rowuserdata[6]
        
        except Exception as e:
             print(f"Error: {e}")

        return render_template('userprofile.html',userid=userid,username=username,useraddress=useraddress,userphoneno=userphoneno,useremailid=useremailid)      


@app.route('/user_orders', methods=['GET', 'POST'])
def user_orders():
    
    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    else:

        uniqueUserId=session.get('uniqueUserId')
        
        orderid=[]
        productname=[]
        productprice=[]
        productquantity=[]
        producttotal=[]
        orderduration=[]
        cusfirstname=[]
        cuslastname=[]
        cusaddress=[]
        cuscity=[]
        cuscontact=[]
        cusemail=[]

        
        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="communityproject"
        )
        # Function to fetch data from the database
        try:
            
            mycursor = mydb.cursor()
            mycursor.execute(
                "SELECT Order_ID,Product_Name,Price,Quantity,Total,Order_Duration,Customer_FirstName,Customer_LastName,CustomerAddress,City,Contact_Number,EMail_ID from ordertable WHERE User_ID=%s",(uniqueUserId,))
            data = mycursor.fetchall()

            # Query the database to get the count of records
            mycursor.execute('SELECT COUNT(*) FROM ordertable WHERE User_ID=%s',(uniqueUserId,))
            countorder= mycursor.fetchone()[0]  # Get the count value

            

            # Iterate through the result and store values into separate lists
            for rowuserdata in data:
                orderid.append(rowuserdata[0])
                productname.append(rowuserdata[1])
                productprice.append(rowuserdata[2])
                productquantity.append(rowuserdata[3])
                producttotal.append(rowuserdata[4])
                orderduration.append(rowuserdata[5])
                cusfirstname.append(rowuserdata[6])
                cuslastname.append(rowuserdata[7])
                cusaddress.append(rowuserdata[8])
                cuscity.append(rowuserdata[9])
                cuscontact.append(rowuserdata[10])
                cusemail.append(rowuserdata[11])

            datauserorderlist = []

            # Iterate through the fetched records and generate HTML table rows
            for i in range(countorder):

                itemorderslist = {
                    "Order_id":orderid[i],
                    "ProductName":productname[i],
                    "ProductPrice":productprice[i],
                    "ProductQuantity":productquantity[i],
                    "ProductTotal":producttotal[i],
                    "OrderDuration":orderduration[i],
                    "CusFirstName":cusfirstname[i],
                    "CusLastName":cuslastname[i],
                    "CusAddress":cusaddress[i],
                    "CusCity":cuscity[i],
                    "CusContact":cuscontact[i],
                    "CusEmail":cusemail[i]
                        
                }
                datauserorderlist.append(itemorderslist)

        
        except Exception as e:
            print(f"Error: {e}")

        return render_template('userorders.html',datauserorderlist=datauserorderlist)      

        

        
@app.route('/get_new_content5', methods=['GET'])
def get_new_content5():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    else:

        #Getting Below Values from app.route('/vendor_login) by using session.get
        VendorMailId = session.get('VendorMailId')
        vendorcategory=session.get('vendorcategory')

        

        # Generate your dynamic HTML content here
        dynamic_content5 = ""
        dynamic_content5 += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_content5 += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
        dynamic_content5 += f'<div class="container-fluid w-100" >'

        dynamic_content5 += f'<div class="row">'
        dynamic_content5 += f'<div class="col-12">'
        dynamic_content5 += f'<div class="w-100">'
        dynamic_content5 += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-290px;">'
        dynamic_content5 += f'<h6 class="text-white text-capitalize ps-3">Vendor Profile</h6>'
        dynamic_content5 += f'</div>'
        dynamic_content5 += f'</div>'
        
        dynamic_content5 += f'<div class="card text-bg-light mb-3 col-12" style="margin-top:40px; width: 100%;">'
        dynamic_content5 += f'<div class="card-header">Vendor Details</div>'
        dynamic_content5 += f'<div class="card-body">'
        dynamic_content5 += f" Vendor_ID:  <label class='card-text'>{VendorMailId}</label><br>"
        dynamic_content5 += f' Category:  <label class="card-text">{vendorcategory}</label><br>'
        
        web_page_urlshowpersonalprofile = url_for('web_pagevendorpersonalprofile')
        dynamic_content5 += f'<a href="{web_page_urlshowpersonalprofile}" class="btn btn-primary">Create Personal Profile</a>'
        
        web_page_urlshowupdatepersonalprofile = url_for('web_pageupdatevendorpersonalprofile')
        dynamic_content5 += f'<a href="{web_page_urlshowupdatepersonalprofile}" class="btn btn-primary" style="margin-left:10px;">Update</a>'

            
        dynamic_content5 += f'</div>'
        dynamic_content5 += f'</div>'
        dynamic_content5 += f'</div>'
        dynamic_content5 += f'<h1 style="font-size:15px";>There are Three Categories of Users(Vendors) are allowed here!<h1>'
        dynamic_content5 += f'<center>'
        dynamic_content5 += f'<h2 style="font-size:12px";>1)Food Sales: Community Member can sales their Food Products and by publish(or)adding Product in Add Products in it.</h2>'
        dynamic_content5 += f'<h2 style="font-size:12px";>2)Education: Community Member can publish their teaching Courses and by adding courses in Add Courses in it.</h2>'
        dynamic_content5 += f'<h2 style="font-size:12px";>3)Business/Profession: Community Member can publish their Business/Professions like RealEstate Builders,Doctors by adding their Business/Profession Details in Add Businesss/Profession in it.</h2>'
        dynamic_content5 += f'</center>'
        dynamic_content5 += f'<h1 style="font-size:15px";>Important:All Category of Vendors must add their "Personal Profiles" First!!! in Personal Profile then do publish their other Stuffs.</h1>'
            
        dynamic_content5 += f'</div>'
        dynamic_content5 += f'</div>'

        
    return dynamic_content5


@app.route('/web_pagevendorpersonalprofile')
def web_pagevendorpersonalprofile():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        VendorMailId=session.get('VendorMailId')
        uniqueVendorId=session.get('uniqueVendorId')
        vendorcategory=session.get('vendorcategory')
        #print(uniqueVendorId)
        

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
        )
        # Function to fetch data from the database
        try:
            mycursor = mydb.cursor()
            mycursor.execute(
                "SELECT ContactMail from vendorpersonalprofileattributes")
            data = mycursor.fetchall()


            #Below Method are used to compare input(User) with set of datas(ids and passwords) from database
            match_found = False  # A flag to indicate if a match is found
            
            # Iterate through the result and store values into separate lists
            for datas in data:

                vendor_ids=datas
                if VendorMailId == vendor_ids[0] :         #[0] is used to eliminate unwanted characters
                    
                    match_found=True
                    break
        
        except Exception as e:
            print(f"Error:{e}") 
         
        if match_found:
            return redirect(url_for('web_pageupdatevendorpersonalprofile'))
        
        else:
            return render_template('personalprofileentry.html',VendorMailId=VendorMailId,uniqueVendorId=uniqueVendorId,vendorcategory=vendorcategory)
          

@app.route('/web_pageupdatevendorpersonalprofile', methods=['GET', 'POST'])
def web_pageupdatevendorpersonalprofile():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        #Getting Below Values from app.route('/vendor_login) by using session.get
        VendorMailId = session.get('VendorMailId')
        uniqueVendorId=session.get('uniqueVendorId')
        vendorcategory=session.get('vendorcategory')

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)
        
       
        connection = get_db_connection()
        cursor = connection.cursor()
        
        #  SQL query to fetch  records
        cursor.execute('SELECT ContactMail FROM vendorpersonalprofileattributes')
        data = cursor.fetchall()


        #Below Method are used to compare input(User) with set of datas(ids and passwords) from database
        match_found = False  # A flag to indicate if a match is found
            
        # Iterate through the result and store values into separate lists
        for datas in data:

            vendor_ids=datas
            if VendorMailId == vendor_ids[0] :
                match_found=True
                break
        
        
        if match_found:
            # Initialize empty lists to store values
            id = ""
            vprofilename = ""
            achieveinterestone = ""
            achieveinteresttwo = ""
            achieveinterestthree = ""
            coverphotoname = ""
            displaypicturename = ""
            dob = ""
            education = ""
            mobileno = ""
            website = ""
            city = ""
            contactmail = ""
            profession = ""
            maritalstatus = ""
            age = ""
            aboutus = ""

        

            #  SQL query to fetch  records
            cursor.execute(
                'SELECT Vendor_ID,Profile_Name,AchieveInterestOne,AchieveInterestTwo,AchieveInterestThree,CoverPhoto_Name,DisplayPicture_Name,DateOfBirth,Education,MobileNo,WebsiteLink,CityName,ContactMail,Profession,Marital_Status,Age,AboutUs FROM vendorpersonalprofileattributes WHERE ContactMail =%s',(VendorMailId,))
            myresultvendorpersonalprofile = cursor.fetchall()
    
                
            # Iterate through the result and append values to lists
            for rowpp in myresultvendorpersonalprofile:
                id = rowpp[0]
                vprofilename = rowpp[1]
                achieveinterestone = rowpp[2]
                achieveinteresttwo = rowpp[3]
                achieveinterestthree = rowpp[4]
                coverphotoname = rowpp[5]
                displaypicturename = rowpp[6]
                dob = rowpp[7]
                education = rowpp[8]
                mobileno = rowpp[9]
                website = rowpp[10]
                city = rowpp[11]
                contactmail = rowpp[12]
                profession = rowpp[13]
                maritalstatus = rowpp[14]
                age = rowpp[15]
                aboutus = rowpp[16]
        
            # Check if a flash message should be displayed
            flash_message = None
            if request.args.get('flash') == '1':
                flash_message = 'Data Updated Successfully!'
                return render_template('updatepersonalprofile.html',flash_message=flash_message)

            else:
                flash_message1="Update Your Personal Profile Correctly"
                return render_template('updatepersonalprofile.html',flash_message1=flash_message1,id=id,vprofilename=vprofilename,vendorcategory=vendorcategory,achieveinterestone=achieveinterestone,achieveinteresttwo=achieveinteresttwo,achieveinterestthree=achieveinterestthree,coverphotoname=coverphotoname,displaypicturename=displaypicturename,dob=dob,education=education,mobileno=mobileno,website=website,city=city,VendorMailId=VendorMailId,profession=profession,maritalstatus=maritalstatus,age=age,aboutus=aboutus)
 
        
        else:
            return render_template('personalprofileentry.html',VendorMailId=VendorMailId,uniqueVendorId=uniqueVendorId,vendorcategory=vendorcategory) 
    
        
       
            


@app.route('/insertvendorpersonalprofile', methods=['GET', 'POST'])
def insertvendorpersonalprofile():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        
       

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            try:
                # Moving Uploaded Picture(Cover Picture) to Particular Folder
                UPLOAD_FOLDER = "static/images/profileimages"
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png','avif','gif'}

                file = request.files['image']

                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image' not in request.files:
                    return "No file part"

                if file.filename == '':
                    return "No selected file"

                if not allowed_file(file.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                original_filenamecoverphoto = file.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)

                # Moving Uploaded Picture(Profile Picture) to Particular Folder
                file1 = request.files['image2']

                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image2' not in request.files:
                    return "No file part"

                if file1.filename == '':
                    return "No selected file"

                if not allowed_file(file1.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                original_filenamedisplaypic = file1.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
                file1.save(filename)


                Vendorid=request.form['Unique_Vendor_ID']
                Profilename = request.form['profilename']
                VendorCategory=request.form['vendorcategories']
                AchievementInterest1 = request.form['achievementinterest1']
                AchievementInterest2 = request.form['achievementinterest2']
                AchievementInterest3 = request.form['achievementinterest3']
                DateOfBirthentry = request.form['dob']
                Qualificationentry = request.form['qualification']
                ContactNumber = request.form['phonenumber']
                Link = request.form['link']
                CityName = request.form['cityname']
                Mail = request.form['contactmail']
                WorkingOccupation = request.form['occupation']
                Status = request.form['status']
                Age = request.form['age']
                About = request.form['abouthere']

                def get_db_connection():
                    return mysql.connector.connect(**db_config)

                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute('INSERT INTO vendorpersonalprofileattributes(Vendor_ID,Profile_Name,Vendor_Category,AchieveInterestOne,AchieveInterestTwo,AchieveInterestThree,CoverPhoto_Name,DisplayPicture_Name,DateOfBirth,Education,MobileNo,WebsiteLink,CityName,ContactMail,Profession,Marital_Status,Age,AboutUs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                    (Vendorid,Profilename,VendorCategory,AchievementInterest1, AchievementInterest2, AchievementInterest3, original_filenamecoverphoto, original_filenamedisplaypic, DateOfBirthentry, Qualificationentry, ContactNumber, Link, CityName, Mail, WorkingOccupation, Status, Age, About))
                connection.commit()
                cursor.close()
                connection.close()
                response_data = {'message': 'Data received successfully!'}
    

            except Exception as e:
                response_data = {'message': 'An Error Occurred!'}
                 

    return jsonify(response_data)




        
@app.route('/updationvendorpersonalprofile', methods=['GET', 'POST'])
def updationvendorpersonalprofile():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        if request.method == 'POST':
           

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }
            
            def get_db_connection():
                return mysql.connector.connect(**db_config)

            match_found = False  # A flag to indicate if a match is found
            match_found1 = False  # A flag to indicate if a match is found
            match_found2 = False  # A flag to indicate if a match is found
            #print("hello3")

            Vendor_Id=request.form['Unique_Vendor_ID']
            Profilename = request.form['profilename']
            VendorCategory=request.form['vendorcategories']
            AchievementInterest1 = request.form['achievementinterest1']
            AchievementInterest2 = request.form['achievementinterest2']
            AchievementInterest3 = request.form['achievementinterest3']
            DateOfBirthentry = request.form['dob']
            Qualificationentry = request.form['qualification']
            ContactNumber = request.form['phonenumber']
            Link = request.form['link']
            CityName = request.form['cityname']
            Mail = request.form['VendorMailId']
            WorkingOccupation = request.form['occupation']
            Status = request.form['status']
            Age = request.form['age']
            About = request.form['abouthere']
            #print(About)
            
            file = request.files['image']
            file1 = request.files['image2']
            #print("hello4")
            UPLOAD_FOLDER = "static/images/profileimages"
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            
            ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png','avif','gif'}
            
            

            if not file.filename=="": 
                #print("hello6")
                match_found=True
                
            if not file1.filename=="":
                #print("hello6")
                match_found1=True

            if not file.filename=="" and file1.filename=="":
                #print("hello6")
                match_found2=True
            
            if file.filename=="" and file1.filename=="":
                #print("hello6")
                match_found3=True
            #print("hello6")
            
            if match_found:  
                #print("hellomatchfound")

                # Moving Uploaded Picture(Cover Picture) to Particular Folder
                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image' not in request.files:
                    return "No file part"

                if file.filename == '':
                    return "No selected file"

                if not allowed_file(file.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                original_filenamecoverphoto = file.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)

                #print("hello7")
                connection = get_db_connection()
                cursor = connection.cursor()
                UPDATE_QUERY="""
                    
                    UPDATE vendorpersonalprofileattributes SET Profile_Name=%s,Vendor_Category=%s,AchieveInterestOne=%s,AchieveInterestTwo=%s,AchieveInterestThree=%s,CoverPhoto_Name=%s,DateOfBirth=%s,Education=%s,MobileNo=%s,WebsiteLink=%s,CityName=%s,ContactMail=%s,Profession=%s,Marital_Status=%s,Age=%s,AboutUs=%s WHERE Vendor_ID=%s;
                
                    """
                cursor.execute(UPDATE_QUERY,
                            (Profilename, VendorCategory,AchievementInterest1, AchievementInterest2, AchievementInterest3, original_filenamecoverphoto,  DateOfBirthentry, Qualificationentry, ContactNumber, Link, CityName, Mail, WorkingOccupation, Status, Age, About,Vendor_Id))
                connection.commit()
                cursor.close()
                connection.close()
                # After processing the form, set a flash message
                flash('Data Updated Successfully!', 'success')
                return redirect(url_for('web_pageupdatevendorpersonalprofile'))  # Redirect to the form pag

            if match_found1: 
                #print("hellomatchfound1")  

                # Moving Uploaded Picture(Profile Picture) to Particular Folder
                
                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image2' not in request.files:
                    return "No file part"


                if not allowed_file(file1.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                original_filenamedisplaypic = file1.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
                file1.save(filename)

                #print("hello8")

                connection = get_db_connection()
                cursor = connection.cursor()
                UPDATE_QUERY1="""
                    
                    UPDATE vendorpersonalprofileattributes SET Profile_Name=%s,Vendor_Category=%s,AchieveInterestOne=%s,AchieveInterestTwo=%s,AchieveInterestThree=%s,DisplayPicture_Name=%s,DateOfBirth=%s,Education=%s,MobileNo=%s,WebsiteLink=%s,CityName=%s,ContactMail=%s,Profession=%s,Marital_Status=%s,Age=%s,AboutUs=%s WHERE Vendor_ID=%s;
                    
                    """
                cursor.execute(UPDATE_QUERY1,
                            (Profilename, VendorCategory,AchievementInterest1, AchievementInterest2, AchievementInterest3, original_filenamedisplaypic, DateOfBirthentry, Qualificationentry, ContactNumber, Link, CityName, Mail, WorkingOccupation, Status, Age, About,Vendor_Id))
                connection.commit()
                cursor.close()
                connection.close()
                # After processing the form, set a flash message
                flash('Data Updated Successfully!', 'success')
                return redirect(url_for('web_pageupdatevendorpersonalprofile'))  # Redirect to the form pag


            if match_found2:
                #print("hellomatchfound2")

                # Moving Uploaded Picture(Cover Picture) to Particular Folder
                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image' not in request.files:
                    return "No file part"

                if file.filename == '':
                    return "No selected file"

                if not allowed_file(file.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                original_filenamecoverphoto = file.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)

                # Moving Uploaded Picture(Profile Picture) to Particular Folder
                
                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image2' not in request.files:
                    return "No file part"


                if not allowed_file(file1.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                original_filenamedisplaypic = file1.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
                file1.save(filename)
                #print("hello9")

                connection = get_db_connection()
                cursor = connection.cursor()

                UPDATE_QUERY2="""
                    
                    UPDATE vendorpersonalprofileattributes SET Profile_Name=%s,Vendor_Category=%s,AchieveInterestOne=%s,AchieveInterestTwo=%s,AchieveInterestThree=%s,CoverPhoto_Name=%s,DisplayPicture_Name=%s,DateOfBirth=%s,Education=%s,MobileNo=%s,WebsiteLink=%s,CityName=%s,ContactMail=%s,Profession=%s,Marital_Status=%s,Age=%s,AboutUs=%s WHERE Vendor_ID=%s;
                    
                    """

                cursor.execute(UPDATE_QUERY2,
                            (Profilename, VendorCategory,AchievementInterest1, AchievementInterest2, AchievementInterest3, original_filenamecoverphoto, original_filenamedisplaypic, DateOfBirthentry, Qualificationentry, ContactNumber, Link, CityName, Mail, WorkingOccupation, Status, Age, About,Vendor_Id))
                connection.commit()
                cursor.close()
                connection.close()
                # After processing the form, set a flash message
                flash('Data Updated Successfully!', 'success')
                return redirect(url_for('web_pageupdatevendorpersonalprofile'))  # Redirect to the form pag
            
            if match_found3:
                #print("hellomatchfound3")
                
                connection = get_db_connection()
                cursor = connection.cursor()

                UPDATE_QUERY3="""
                    
                    UPDATE vendorpersonalprofileattributes SET Profile_Name=%s,Vendor_Category=%s,AchieveInterestOne=%s,AchieveInterestTwo=%s,AchieveInterestThree=%s,DateOfBirth=%s,Education=%s,MobileNo=%s,WebsiteLink=%s,CityName=%s,ContactMail=%s,Profession=%s,Marital_Status=%s,Age=%s,AboutUs=%s WHERE Vendor_ID=%s;
                    
                    """
                
                cursor.execute(UPDATE_QUERY3,
                            (Profilename, VendorCategory,AchievementInterest1, AchievementInterest2, AchievementInterest3, DateOfBirthentry, Qualificationentry, ContactNumber, Link, CityName, Mail, WorkingOccupation, Status, Age, About,Vendor_Id))
                connection.commit()
                cursor.close()
                connection.close()
                # After processing the form, set a flash message
                flash('Data Updated Successfully!', 'success')
                return redirect(url_for('web_pageupdatevendorpersonalprofile',flash='1'))  # Redirect to the form page


@app.route('/changeuserpassword')
def changeuserpassword():
    flash_messageforuser="Enter G-Mail ID Below!"
    return render_template("passwordforgot.html",flash_messageforuser=flash_messageforuser)      
            
   
@app.route('/changevendorpassword')
def changevendorpassword():
    flash_messageforvendor="Enter G-Mail ID Below!"
    return render_template("passwordforgot.html",flash_messageforvendor=flash_messageforvendor)

@app.route('/vendor_sendotp',methods=['GET','POST'])
def vendor_sendotp():
    if request.method=="POST":
        Vendoremail=request.form['vendoremail']
        
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
        )
        
        # Function to fetch data from the database
        try:
            mycursor = mydb.cursor()
            mycursor.execute(
            "SELECT Vendor_EMAILID from vendorattributes")
            datav = mycursor.fetchall()

            
            #Below Method are used to compare input(User) with set of datas(ids and passwords) from database
            match_found = False  # A flag to indicate if a match is found

            # Initialize an empty list to store email addresses
            emails_in_db = []

            # Iterate through each record in datav
            for record in datav:
                # Extract the email address (the first element in each record)
                email = record[0]
                # Append the email address to the emails_in_db list
                emails_in_db.append(email)


            # Check if Vendoremail exists in the list of emails
            if Vendoremail in emails_in_db:
                # If Vendoremail exists in the database
                match_found = True
              
            else:
                error_messageforvendor="Check! Your EMail_ID is Wrong"
                return render_template('passwordforgot.html',error_messageforvendor=error_messageforvendor)
  
                    
        except Exception as e:
            error_messageforvendor = 'An error occurred: ' + str(e)
            flash(error_messageforvendor, 'error')
            return render_template('passwordforgot.html', error_messageforvendor=error_messageforvendor)
            
    
        
        if match_found:
            try:
                # Configure Flask-Mail to send email
                app.config['MAIL_SERVER'] = 'smtp.gmail.com'
                app.config['MAIL_PORT'] = 587
                app.config['MAIL_USE_TLS'] = True
                app.config['MAIL_USE_SSL'] = False
                app.config['MAIL_USERNAME'] = 'aasva.koodalarasan@gmail.com'  # Your Gmail email address
                app.config['MAIL_PASSWORD'] = 'mozs zzry opgs nfjc'         # Your Gmail password
                app.config['MAIL_DEFAULT_SENDER'] = 'aasva.koodalarasan@gmail.com'

                mail = Mail(app)

                # Secret key for session
                app.secret_key = secrets.token_hex(16)

                # Function to generate OTP
                def generate_otp():
                    characters = string.digits
                    return ''.join(secrets.choice(characters) for _ in range(6))
                
                otp = generate_otp()
                session['otp'] = otp
                session['Vendoremail'] = Vendoremail

                # Send the OTP via email
                msg = Message('OTP VERIFICATION to change Password', recipients=[Vendoremail])
                msg.body = f'Your OTP is: {otp}'
                mail.send(msg)

                
            except Exception as e:
                error_messageforvendor = 'An error occurred: ' + str(e)
                flash(error_messageforvendor, 'error')
                return render_template('passwordforgot.html', error_messageforvendor=error_messageforvendor)
    
    flash_messageforvendor="Enter OTP Correctly"       
    return render_template('vendorotp.html',Vendoremail=Vendoremail,flash_messageforvendor=flash_messageforvendor)



@app.route('/verify_vendorotp', methods=['GET', 'POST'])
def verify_vendorotp():
    if request.method == 'POST':
        v_email=request.form['vendoremailid']
        vendor_otp = request.form['vendorreceivedotp']

        #otp is receiving from /vendor_sendotp app.route and initialised in otp_received variable
        otp_received = session.get('otp', '')  # Get the 'otp' session variable with a default value of ''
        
        if vendor_otp == otp_received:
            flash_messageforvendor="OTP is Correct, Enter Password"
            return render_template('changingvendorpassword.html',v_email=v_email,flash_messageforvendor=flash_messageforvendor)
        
        else:
            
            error_messageforvendor= "OTP is not same"
            return render_template("vendorotp.html",error_messageforvendor=error_messageforvendor)
        
@app.route('/vendor_change_password',methods=['GET','POST'])
def vendor_change_password():

    if request.method=="POST":
        Vendor_email=request.form['vendoremailid']
        Vendor_password=request.form['vendorpassword']
        Vendor_confirmpassword=request.form['vendorconfirmpassword']

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
        )
        
        
        if Vendor_password == Vendor_confirmpassword:
            try:        
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE vendorattributes SET Vendor_Password= %s WHERE Vendor_EMAILID= %s",(Vendor_password,Vendor_email))
                mydb.commit()
                mydb.close()
                
            
            except Exception as e:
                error_message = 'An error occurred: ' + str(e)
                flash(error_message, 'error')
                return render_template('changingvendorpassword.html', error_message=error_message)
            
            # After processing the form, set a flash message
            flash_messageforvendor='Password Changed!, Login Now'
            return render_template('loginpage.html',flash_messageforvendor=flash_messageforvendor)

            
        else:
            error_message="Write Password and Confirm Password Correctly"
            return render_template('changingvendorpassword.html', error_message=error_message)
      
        
@app.route('/user_sendotp',methods=['GET','POST'])
def user_sendotp():
    if request.method=="POST":
        useremail=request.form['useremailid']
        
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
        )
        
        # Function to fetch data from the database
        try:
            mycursor = mydb.cursor()
            mycursor.execute(
            "SELECT User_EMAILID from userattributes")
            datauser = mycursor.fetchall()

            
            #Below Method are used to compare input(User) with set of datas(ids and passwords) from database
            match_found = False  # A flag to indicate if a match is found

            # Initialize an empty list to store email addresses
            useremails_in_db = []

            # Iterate through each record in datav
            for record in datauser:
                # Extract the email address (the first element in each record)
                email = record[0]
                # Append the email address to the emails_in_db list
                useremails_in_db.append(email)


            # Check if Vendoremail exists in the list of emails
            if useremail in useremails_in_db:
                # If Vendoremail exists in the database
                match_found = True
              
            else:
                error_messageforuser="Check! Your EMail_ID is Wrong"
                return render_template('passwordforgot.html',error_messageforuser=error_messageforuser)
  
                    
        except Exception as e:
            error_messageforuser = 'An error occurred: ' + str(e)
            flash(error_messageforuser, 'error')
            return render_template('passwordforgot.html', error_messageforuser=error_messageforuser)
    
        # Authentication logic here
        if match_found:
            try:
                # Configure Flask-Mail to send email
                app.config['MAIL_SERVER'] = 'smtp.gmail.com'
                app.config['MAIL_PORT'] = 587
                app.config['MAIL_USE_TLS'] = True
                app.config['MAIL_USE_SSL'] = False
                app.config['MAIL_USERNAME'] = 'aasva.koodalarasan@gmail.com'  # Your Gmail email address
                app.config['MAIL_PASSWORD'] = 'mozs zzry opgs nfjc'         # Your Gmail password
                app.config['MAIL_DEFAULT_SENDER'] = 'aasva.koodalarasan@gmail.com'

                mail = Mail(app)

                # Secret key for session
                app.secret_key = secrets.token_hex(16)

                # Function to generate OTP
                def generate_otp():
                    characters = string.digits
                    return ''.join(secrets.choice(characters) for _ in range(6))
                
                otp = generate_otp()
                session['otp'] = otp
                session['useremail'] = useremail

                # Send the OTP via email
                msg = Message('OTP VERIFICATION to change Password', recipients=[useremail])
                msg.body = f'Hey Respected,\n Your OTP is: {otp}'
                mail.send(msg)

                
            except Exception as e:
                error_messageforuser = 'An error occurred: ' + str(e)
                flash(error_messageforuser, 'error')
                return render_template('passwordforgot.html', error_messageforuser=error_messageforuser)
    
    flash_messageforuser="Enter OTP Correctly"
    return render_template('userotp.html',useremail=useremail,flash_messageforuser=flash_messageforuser)




@app.route('/verify_userotp', methods=['GET', 'POST'])
def verify_userotp():
    if request.method == 'POST':
        u_email=request.form['useremailid']
        user_otp = request.form['userreceivedotp']

        #otp is receiving from /vendor_sendotp app.route and initialised in otp_received variable
        otp_received = session.get('otp', '')  # Get the 'otp' session variable with a default value of ''
        
        if user_otp == otp_received:
            flash_messageforuser="OTP is Correct, Enter Password"
            return render_template('changinguserpassword.html',u_email=u_email,flash_messageforuser=flash_messageforuser)
        
        else:
            
            error_messageforuser= "OTP is not same"
            return render_template("userotp.html",error_messageforuser=error_messageforuser)





@app.route('/user_change_password',methods=['GET','POST'])
def user_change_password():

    if request.method=="POST":
        User_email=request.form['useremailid']
        User_password=request.form['userpassword']
        User_confirmpassword=request.form['userconfirmpassword']

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
        )
        
        
        if User_password == User_confirmpassword:
            try:        
                mycursor = mydb.cursor()
                mycursor.execute("UPDATE userattributes SET User_Password= %s WHERE User_EMAILID= %s",(User_password,User_email))
                mydb.commit()
                mydb.close()
                
            except Exception as e:
                error_messageforuser = 'An error occurred: ' + str(e)
                flash(error_messageforuser, 'error')
                return render_template('changinguserpassword.html', error_messageforuser=error_messageforuser)
            
            # After processing the form, set a flash message
            flash_messageforuser='Password Changed!, Login Now'
            return render_template('loginpage.html',flash_messageforuser=flash_messageforuser)
            
        else:
            error_messageforuser="Write Password and Confirm Password Correctly"
            return render_template('changinguserpassword.html',error_messageforuser=error_messageforuser)
                         
   

@app.route('/vendor_dashboard')
def vendor_dashboard():

    if session.get('vendorlogged_in', False):
        return render_template('vendorpanel.html')
    else:
        return render_template('loginpage.html')

@app.route('/user_dashboard')
def user_dashboard():

    if session.get('userlogged_in', False):
        return render_template('index.html')
    else:
        return render_template('loginpage.html')


@app.route('/vendor_logout')
def vendor_logout():
    session.pop('vendorlogged_in', None)
    return render_template('loginpage.html')

@app.route('/user_logout')
def user_logout():
    session.pop('userlogged_in', None)
    return render_template('loginpage.html')


@app.route('/vendorpersonalprofile/<int:vendorid>',methods=['GET','POST'])
def vendorpersonalprofile(vendorid):

    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    else:

        #Passed value(vendorid) initialised into uniqueVendorId variable
        uniqueVendorId=vendorid
        
        #getting value which is stored in session
        uniqueUserId=session.get('uniqueUserId')


        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        
        vprofilename = ""
        vendorcategory=""
        achieveinterestone = ""
        achieveinteresttwo = ""
        achieveinterestthree = ""
        coverphotoname = ""
        displaypicturename = ""
        dob = ""
        education = ""
        mobileno = ""
        website = ""
        city = ""
        contactmail = ""
        profession = ""
        maritalstatus = ""
        age = ""
        aboutus = ""

        
        connection = get_db_connection()
        cursor = connection.cursor()

        #  SQL query to fetch  records
        cursor.execute(
            'SELECT Profile_Name,Vendor_Category,AchieveInterestOne,AchieveInterestTwo,AchieveInterestThree,CoverPhoto_Name,DisplayPicture_Name,DateOfBirth,Education,MobileNo,WebsiteLink,CityName,ContactMail,Profession,Marital_Status,Age,AboutUs FROM vendorpersonalprofileattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
        myresultvendorpersonalprofile = cursor.fetchall()

        # Iterate through the result and append values to lists
        for rowpp in myresultvendorpersonalprofile:
            
            vprofilename = rowpp[0]
            vendorcategory=rowpp[1]
            achieveinterestone = rowpp[2]
            achieveinteresttwo = rowpp[3]
            achieveinterestthree = rowpp[4]
            coverphotoname = rowpp[5]
            displaypicturename = rowpp[6]
            dob = rowpp[7]
            education = rowpp[8]
            mobileno = rowpp[9]
            website = rowpp[10]
            city = rowpp[11]
            contactmail = rowpp[12]
            profession = rowpp[13]
            maritalstatus = rowpp[14]
            age = rowpp[15]
            aboutus = rowpp[16]

        if vendorcategory=="Food Sales":
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute(
                'SELECT Product_Name,ProductImage_Name,Price FROM productattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultvendorproduct = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM productattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            countproducts = cursor.fetchone()[0]  # Get the count value

            # Initialize empty lists to store values
            ProductName = []
            ProductImageName = []
            Product_Price = []

            # Iterate through the result and append values to lists
            for rowvendorproduct in myresultvendorproduct:
                ProductName.append(rowvendorproduct[0])
                ProductImageName.append(rowvendorproduct[1])
                Product_Price.append(rowvendorproduct[2])
            
            dataproductlist = []

            # Iterate through the fetched records and generate HTML table rows
            for i in range(countproducts):

                itemproductlist = {
                    "Product_Name":ProductName[i],
                    "Product_ImageName":ProductImageName[i],
                    "ProductPrice":Product_Price[i]
                    
                }
                dataproductlist.append(itemproductlist)

            return render_template('profilemain.html',uniqueVendorId=uniqueVendorId,uniqueUserId=uniqueUserId, vprofilename=vprofilename, achieveinterestone=achieveinterestone, achieveinteresttwo=achieveinteresttwo, achieveinterestthree=achieveinterestthree, coverphotoname=coverphotoname, displaypicturename=displaypicturename, dob=dob, education=education, mobileno=mobileno, website=website, city=city, contactmail=contactmail, profession=profession, maritalstatus=maritalstatus, age=age, aboutus=aboutus,dataproductlist=dataproductlist)

        elif vendorcategory=="Educational":
            db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            # Initialize empty lists to store values
            coursetuitionames = ''
            coursetuitionpaymentfees = ""
            coursetuitiondetails = ""
            languages = ""
            duration = ""
        
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT CourseTuitionName, PaymentFees, CourseTuition_Details,Languages,Duration FROM coursedetails WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultcoursedetails = cursor.fetchall()

            # Iterate through the result and append values to lists
            for rowcd  in myresultcoursedetails:
                coursetuitionames = rowcd[0]
                coursetuitionpaymentfees = rowcd[1]
                coursetuitiondetails = rowcd[2]
                languages = rowcd[3]
                duration = rowcd[4]
            
            return render_template('profilemaincourses.html', uniqueVendorId=uniqueVendorId, uniqueUserId=uniqueUserId,vprofilename=vprofilename, achieveinterestone=achieveinterestone, achieveinteresttwo=achieveinteresttwo, achieveinterestthree=achieveinterestthree, coverphotoname=coverphotoname, displaypicturename=displaypicturename, dob=dob, education=education, mobileno=mobileno, website=website, city=city, contactmail=contactmail, profession=profession, maritalstatus=maritalstatus, age=age, aboutus=aboutus, coursetuitionnames=coursetuitionames,coursetuitionpaymentfees=coursetuitionpaymentfees,coursetuitiondetails=coursetuitiondetails,languages=languages,duration=duration )
        
        else:
            db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            # Initialize empty lists to store values
            
            businessprofession_names = ""
            businessprofessionlogonames ="" 
            
            businessprofession_details=""
            experience=""
            enquiryfirstnumber=""
            enquirysecondnumber=""
            enquirymail=""
            websitelink=""
            address=""
            locationurl=""

            

            
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT BusinessProfession_Name,BusinessProfession_LogoName,BusinessProfession_Details,Experience,EnquiryFirstNumber,EnquirySecondNumber,EnquiryMail,WebsiteLink,Address,Location_URL FROM businessprofessionattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultbusinessprofessiondetails = cursor.fetchall()

            

            # Iterate through the result and append values to lists
            for rowbpdl in myresultbusinessprofessiondetails:
                
                businessprofession_names=rowbpdl[0]
                businessprofessionlogonames=rowbpdl[1]
                
                businessprofession_details=rowbpdl[2]
                experience=rowbpdl[3]
                enquiryfirstnumber=rowbpdl[4]
                enquirysecondnumber=rowbpdl[5]
                enquirymail=rowbpdl[6]
                websitelink=rowbpdl[7]
                address=rowbpdl[8]
                locationurl=rowbpdl[9]

            return render_template('profilemainbusiprofess.html',vprofilename=vprofilename,achieveinterestone=achieveinterestone,achieveinteresttwo=achieveinteresttwo,achieveinterestthree=achieveinterestthree,coverphotoname=coverphotoname,displaypicturename=displaypicturename,dob=dob,education=education,mobileno=mobileno,website=website,city=city,contactmail=contactmail,profession=profession,maritalstatus=maritalstatus,age=age,aboutus=aboutus,uniqueVendorId=uniqueVendorId,businessprofession_names=businessprofession_names,businessprofessionlogonames=businessprofessionlogonames,businessprofession_details=businessprofession_details,experience=experience,enquiryfirstnumber=enquiryfirstnumber,enquirysecondnumber=enquirysecondnumber,enquirymail=enquirymail,websitelink=websitelink,address=address,locationurl=locationurl)

    



@app.route('/vendorpersonalprofile3/<int:Vendor_ID>',methods=['GET','POST'])
def vendorpersonalprofile3(Vendor_ID):

    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    else:

        uniqueVendorId=Vendor_ID

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        
        vprofilename = ""
        achieveinterestone = ""
        achieveinteresttwo = ""
        achieveinterestthree = ""
        coverphotoname = ""
        displaypicturename = ""
        dob = ""
        education = ""
        mobileno = ""
        website = ""
        city = ""
        contactmail = ""
        profession = ""
        maritalstatus = ""
        age = ""
        aboutus = ""

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute(
                'SELECT Profile_Name,AchieveInterestOne,AchieveInterestTwo,AchieveInterestThree,CoverPhoto_Name,DisplayPicture_Name,DateOfBirth,Education,MobileNo,WebsiteLink,CityName,ContactMail,Profession,Marital_Status,Age,AboutUs FROM vendorpersonalprofileattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultvendorpersonalprofile = cursor.fetchall()

            # Iterate through the result and append values to lists
            for rowpp in myresultvendorpersonalprofile:
                
                vprofilename = rowpp[0]
                achieveinterestone = rowpp[1]
                achieveinteresttwo = rowpp[2]
                achieveinterestthree = rowpp[3]
                coverphotoname = rowpp[4]
                displaypicturename = rowpp[5]
                dob = rowpp[6]
                education = rowpp[7]
                mobileno = rowpp[8]
                website = rowpp[9]
                city = rowpp[10]
                contactmail = rowpp[11]
                profession = rowpp[12]
                maritalstatus = rowpp[13]
                age = rowpp[14]
                aboutus = rowpp[15]

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            # Initialize empty lists to store values
            coursetuitionames = ''
            coursetuitionpaymentfees = ""
            coursetuitiondetails = ""
            languages = ""
            duration = ""
        
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT CourseTuitionName, PaymentFees, CourseTuition_Details,Languages,Duration FROM coursedetails WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultcoursedetails = cursor.fetchall()

            # Iterate through the result and append values to lists
            for rowcd  in myresultcoursedetails:
                coursetuitionames = rowcd[0]
                coursetuitionpaymentfees = rowcd[1]
                coursetuitiondetails = rowcd[2]
                languages = rowcd[3]
                duration = rowcd[4]
                
        except Exception as e:
            print(f"Error: {e}")
        
        # Check if a flash message should be displayed
        flash_message = None
        if request.args.get('flash') == '1':
            flash_message = 'Enrolled Successfully!'
            return render_template('profilemaincourses.html',flash_message=flash_message,uniqueVendorId=uniqueVendorId, vprofilename=vprofilename, achieveinterestone=achieveinterestone, achieveinteresttwo=achieveinteresttwo, achieveinterestthree=achieveinterestthree, coverphotoname=coverphotoname, displaypicturename=displaypicturename, dob=dob, education=education, mobileno=mobileno, website=website, city=city, contactmail=contactmail, profession=profession, maritalstatus=maritalstatus, age=age, aboutus=aboutus, coursetuitionnames=coursetuitionames,coursetuitionpaymentfees=coursetuitionpaymentfees,coursetuitiondetails=coursetuitiondetails,languages=languages,duration=duration)
        else:
            return render_template('profilemaincourses.html', uniqueVendorId=uniqueVendorId, vprofilename=vprofilename, achieveinterestone=achieveinterestone, achieveinteresttwo=achieveinteresttwo, achieveinterestthree=achieveinterestthree, coverphotoname=coverphotoname, displaypicturename=displaypicturename, dob=dob, education=education, mobileno=mobileno, website=website, city=city, contactmail=contactmail, profession=profession, maritalstatus=maritalstatus, age=age, aboutus=aboutus, coursetuitionnames=coursetuitionames,coursetuitionpaymentfees=coursetuitionpaymentfees,coursetuitiondetails=coursetuitiondetails,languages=languages,duration=duration )


@app.route('/vendorpersonalprofile5/<int:VendorID>',methods=['GET','POST'])
def vendorpersonalprofile5(VendorID):

    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    else:

        uniqueVendorId=VendorID

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        
        vprofilename = ""
        achieveinterestone = ""
        achieveinteresttwo = ""
        achieveinterestthree = ""
        coverphotoname = ""
        displaypicturename = ""
        dob = ""
        education = ""
        mobileno = ""
        website = ""
        city = ""
        contactmail = ""
        profession = ""
        maritalstatus = ""
        age = ""
        aboutus = ""

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute(
                'SELECT Profile_Name,AchieveInterestOne,AchieveInterestTwo,AchieveInterestThree,CoverPhoto_Name,DisplayPicture_Name,DateOfBirth,Education,MobileNo,WebsiteLink,CityName,ContactMail,Profession,Marital_Status,Age,AboutUs FROM vendorpersonalprofileattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultvendorpersonalprofile = cursor.fetchall()

            # Iterate through the result and append values to lists
            for rowpp in myresultvendorpersonalprofile:
                
                vprofilename = rowpp[0]
                achieveinterestone = rowpp[1]
                achieveinteresttwo = rowpp[2]
                achieveinterestthree = rowpp[3]
                coverphotoname = rowpp[4]
                displaypicturename = rowpp[5]
                dob = rowpp[6]
                education = rowpp[7]
                mobileno = rowpp[8]
                website = rowpp[9]
                city = rowpp[10]
                contactmail = rowpp[11]
                profession = rowpp[12]
                maritalstatus = rowpp[13]
                age = rowpp[14]
                aboutus = rowpp[15]
            
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            # Initialize empty lists to store values
            
            businessprofession_names = ""
            businessprofessionlogonames ="" 
            
            businessprofession_details=""
            experience=""
            enquiryfirstnumber=""
            enquirysecondnumber=""
            enquirymail=""
            websitelink=""
            address=""
            locationurl=""

            

            
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT BusinessProfession_Name,BusinessProfession_LogoName,BusinessProfession_Details,Experience,EnquiryFirstNumber,EnquirySecondNumber,EnquiryMail,WebsiteLink,Address,Location_URL FROM businessprofessionattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultbusinessprofessiondetails = cursor.fetchall()

            

            # Iterate through the result and append values to lists
            for rowbpdl in myresultbusinessprofessiondetails:
                
                businessprofession_names=rowbpdl[0]
                businessprofessionlogonames=rowbpdl[1]
                
                businessprofession_details=rowbpdl[2]
                experience=rowbpdl[3]
                enquiryfirstnumber=rowbpdl[4]
                enquirysecondnumber=rowbpdl[5]
                enquirymail=rowbpdl[6]
                websitelink=rowbpdl[7]
                address=rowbpdl[8]
                locationurl=rowbpdl[9]

        except Exception as e:
                print(f"Error: {e}")
        # Check if a flash message should be displayed
        flash_message = None
        if request.args.get('flash') == '1':
            flash_message = 'Your Enquiry were Submitted!'
            return render_template('profilemainbusiprofess.html',flash_message=flash_message,vprofilename=vprofilename,achieveinterestone=achieveinterestone,achieveinteresttwo=achieveinteresttwo,achieveinterestthree=achieveinterestthree,coverphotoname=coverphotoname,displaypicturename=displaypicturename,dob=dob,education=education,mobileno=mobileno,website=website,city=city,contactmail=contactmail,profession=profession,maritalstatus=maritalstatus,age=age,aboutus=aboutus,uniqueVendorId=uniqueVendorId,businessprofession_names=businessprofession_names,businessprofessionlogonames=businessprofessionlogonames,businessprofession_details=businessprofession_details,experience=experience,enquiryfirstnumber=enquiryfirstnumber,enquirysecondnumber=enquirysecondnumber,enquirymail=enquirymail,websitelink=websitelink,address=address,locationurl=locationurl)
        
        else:
            return render_template('profilemainbusiprofess.html',vprofilename=vprofilename,achieveinterestone=achieveinterestone,achieveinteresttwo=achieveinteresttwo,achieveinterestthree=achieveinterestthree,coverphotoname=coverphotoname,displaypicturename=displaypicturename,dob=dob,education=education,mobileno=mobileno,website=website,city=city,contactmail=contactmail,profession=profession,maritalstatus=maritalstatus,age=age,aboutus=aboutus,uniqueVendorId=uniqueVendorId,businessprofession_names=businessprofession_names,businessprofessionlogonames=businessprofessionlogonames,businessprofession_details=businessprofession_details,experience=experience,enquiryfirstnumber=enquiryfirstnumber,enquirysecondnumber=enquirysecondnumber,enquirymail=enquirymail,websitelink=websitelink,address=address,locationurl=locationurl)
            
@app.route('/addenquiry',methods=['GET','POST'])
def addenquiry():
    if request.method=="POST":
        Name=request.form['name']
        Email=request.form['email']
        Phone=request.form['phone']
        Subject=request.form['subject']
        Message=request.form['message']
        VendorID=request.form['vendorid']

        
        Messaged_Duration = datetime.datetime.now()
        
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)
        
        try:
        
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('INSERT INTO businessenquirytable(Name,Email,Contact,Subject,Message,Message_ReceivedDuration,Vendor_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)',(Name,Email,Phone,Subject,Message,Messaged_Duration,VendorID))
            connection.commit()
            cursor.close()
            connection.close()
            flash('Your Enquiry Submitted!', 'success')
            return redirect(url_for('vendorpersonalprofile5',flash='1',VendorID=VendorID))  # Redirect to the form page

        except Exception as e:
            error_message = 'An error occurred: ' + str(e)
            flash(error_message, 'error')
            return render_template('profilemainbusiprofess.html', error_message=error_message)
        
    


@app.route('/student_register',methods=['GET','POST'])
def student_register():

    if request.method=="POST":
        StudentName=request.form['studentname']
        StudentEmail=request.form['studentemail']
        PhoneNumber=request.form['Phonenumber']
        Vendor_ID=request.form['vendorid']


        try:

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)
        
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('INSERT INTO studentdetails(Vendor_ID,Student_Name,EMail,Contact_Number) VALUES (%s,%s,%s,%s)',(Vendor_ID,StudentName,StudentEmail,PhoneNumber))

            connection.commit()
            cursor.close()
            connection.close()
            flash('Enrolled Successfully!', 'success')
            return redirect(url_for('vendorpersonalprofile3',flash='1',Vendor_ID=Vendor_ID))  # Redirect to the form page
        
        except Exception as e:
            error_message = 'An error occurred: ' + str(e)
            flash(error_message, 'error')
            return render_template('profilemaincourses.html', error_message=error_message)
                                  

    

@app.route('/get_new_contentcoursedetails',methods=['GET','POST'])
def get_new_contentcoursedetails():
     
    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        dynamic_contentcourselist = ""

        dynamic_contentcourselist += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentcourselist += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentcourselist += f'<div class="container-fluid w-100" >'
        dynamic_contentcourselist += f'<div class="row">'
        dynamic_contentcourselist += f'<div class="col-12">'
        dynamic_contentcourselist += f'<div class="w-100">'
        dynamic_contentcourselist += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentcourselist += f'<h6 class="text-white text-capitalize ps-3">Course Details</h6>'
        dynamic_contentcourselist += f'</div>'

        dynamic_contentcourselist += f'</div>'
        dynamic_contentcourselist += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentcourselist += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentcourselist += f'<table class="table table-bordered mb-0">'
        dynamic_contentcourselist += f'<thead>'
        dynamic_contentcourselist += f'<tr>'
        dynamic_contentcourselist += f'<th>Course/Tuition Name</th>'
        dynamic_contentcourselist += f'<th>Payment/Fees</th>'
        dynamic_contentcourselist += f'<th>Course/Tuition_Details</th>'
        dynamic_contentcourselist += f'<th>Languages</th>'
        dynamic_contentcourselist += f'<th>Duration</th>'
        
        dynamic_contentcourselist += f'</tr>'
        dynamic_contentcourselist += f'</thead>'
        dynamic_contentcourselist += f'<tbody>'

        dynamic_contentcourselist += f'</tbody>'
        dynamic_contentcourselist += f'</table>'

        dynamic_contentcourselist += f'</div>'

        web_page_urlshowcourselist = url_for('web_pagecourseslist')
        dynamic_contentcourselist += f'<center><a href="{web_page_urlshowcourselist}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentcourselist += f'</div>'

        dynamic_contentcourselist += f'</div>'
        dynamic_contentcourselist += f'</div>'

    return dynamic_contentcourselist

@app.route('/get_new_contentaddbusiness',methods=['GET','POST'])
def get_new_contentaddbusiness():
     
    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        dynamic_contentbusiness = ""

        dynamic_contentbusiness += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentbusiness += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentbusiness += f'<div class="container-fluid w-100" >'
        dynamic_contentbusiness += f'<div class="row">'
        dynamic_contentbusiness += f'<div class="col-12">'
        dynamic_contentbusiness += f'<div class="w-100">'
        dynamic_contentbusiness += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentbusiness += f'<h6 class="text-white text-capitalize ps-3">Add Business</h6>'
        dynamic_contentbusiness += f'</div>'

        dynamic_contentbusiness += f'</div>'
        dynamic_contentbusiness += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentbusiness += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentbusiness += f'<table class="table table-bordered mb-0">'
        dynamic_contentbusiness += f'<thead>'
        dynamic_contentbusiness += f'<tr>'
        dynamic_contentbusiness += f'<th>Business/Profession Name</th>'
        dynamic_contentbusiness += f'<th>Business/Profession Details</th>'
        dynamic_contentbusiness += f'<th> Enquiry</th>'
        
        dynamic_contentbusiness += f'</tr>'
        dynamic_contentbusiness += f'</thead>'
        dynamic_contentbusiness += f'<tbody>'

        dynamic_contentbusiness += f'</tbody>'
        dynamic_contentbusiness += f'</table>'

        dynamic_contentbusiness += f'</div>'

        web_page_urlshowaddbusiness = url_for('web_pageaddbusiness')
        dynamic_contentbusiness += f'<center><a href="{web_page_urlshowaddbusiness}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentbusiness += f'</div>'

        dynamic_contentbusiness += f'</div>'
        dynamic_contentbusiness += f'</div>'

    return dynamic_contentbusiness

@app.route('/get_new_contentEnquiry')
def get_new_contentEnquiry():
    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        dynamic_contentenquiry = ""

        dynamic_contentenquiry += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentenquiry += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentenquiry += f'<div class="container-fluid w-100" >'
        dynamic_contentenquiry += f'<div class="row">'
        dynamic_contentenquiry += f'<div class="col-12">'
        dynamic_contentenquiry += f'<div class="w-100">'
        dynamic_contentenquiry += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentenquiry += f'<h6 class="text-white text-capitalize ps-3">Enquiries</h6>'
        dynamic_contentenquiry += f'</div>'

        dynamic_contentenquiry += f'</div>'
        dynamic_contentenquiry += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentenquiry += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentenquiry += f'<table class="table table-bordered mb-0">'
        dynamic_contentenquiry += f'<thead>'
        dynamic_contentenquiry += f'<tr>'
        dynamic_contentenquiry += f'<th>Name</th>'
        dynamic_contentenquiry += f'<th>Contact</th>'
        dynamic_contentenquiry += f'<th>Enquiries</th>'
        
        dynamic_contentenquiry += f'</tr>'
        dynamic_contentenquiry += f'</thead>'
        dynamic_contentenquiry += f'<tbody>'

        dynamic_contentenquiry += f'</tbody>'
        dynamic_contentenquiry += f'</table>'

        dynamic_contentenquiry += f'</div>'

        web_page_urlshowenquiries = url_for('web_page_Enquiry')
        dynamic_contentenquiry += f'<center><a href="{web_page_urlshowenquiries}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentenquiry += f'</div>'

        dynamic_contentenquiry += f'</div>'
        dynamic_contentenquiry += f'</div>'

    return dynamic_contentenquiry

@app.route('/web_page_Enquiry')
def web_page_Enquiry():
    
    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')

    else:
        uniqueVendorId = session.get('uniqueVendorId')
        print(uniqueVendorId)
        
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        
        names = []
        enquirynumbers=[]
        enquirymail=[]
        subjects=[]
        messages=[]
        message_received_duration=[]
        

        countbusinessenquiries = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Name,Email,Contact,Subject,Message,Message_ReceivedDuration FROM businessenquirytable WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultbusinessenquirydetails = cursor.fetchall()
            
            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM businessenquirytable WHERE Vendor_ID=%s',(uniqueVendorId,))
            countbusinessenquiries = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for rowenquiry in myresultbusinessenquirydetails:
                names.append(rowenquiry[0])
                enquirynumbers.append(rowenquiry[1])
                enquirymail.append(rowenquiry[2])
                subjects.append(rowenquiry[3])
                messages.append(rowenquiry[4])
                message_received_duration.append(rowenquiry[5])
             
            databusinessprofessionenquirieslist = []

            # Iterate through the fetched records and generate HTML table rows
            for i in range(countbusinessenquiries):

                itembusinessprofessionenquirieslist = {
                    "Name":names[i],
                    "Enquiry_Number":enquirynumbers[i],
                    "Enquiry_Mail":enquirymail[i],
                    "Subject":subjects[i],
                    "Message":messages[i],
                    "Message_Received_Duration":message_received_duration[i]
                    
                }
                databusinessprofessionenquirieslist.append(itembusinessprofessionenquirieslist)
                
        except Exception as e:
            print(f"Error: {e}")

            

    return render_template('Enquiries_list.html', databusinessprofessionenquirieslist=databusinessprofessionenquirieslist)


@app.route('/about_us')
def about_us():
    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    else:
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        
        
        vendorid=[]
        vprofilename=[]
        displaypicturename = []
        

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute(
                'SELECT Vendor_ID,Profile_Name,DisplayPicture_Name FROM vendorpersonalprofileattributes')
            myresultvendorpersonalprofilewebpage = cursor.fetchall()

            print(myresultvendorpersonalprofilewebpage)

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM vendorpersonalprofileattributes')
            countvendors = cursor.fetchone()[0]  # Get the count value   
            


            # Iterate through the result and append values to lists
            for rowpp in myresultvendorpersonalprofilewebpage:
                vendorid.append(rowpp[0])
                vprofilename.append(rowpp[1])
                displaypicturename.append(rowpp[2])
            
            datavendorslist = []

            # Iterate through the fetched records and generate HTML table rows
            for i in range(countvendors):

                itemVendorslist = {
                    
                    "Vendor_ID":vendorid[i],
                    "DisplayPictureName":displaypicturename[i],
                    
                    "Vendor_Name":vprofilename[i]
                    
                }
                datavendorslist.append(itemVendorslist)
            
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            # Initialize empty lists to store values
            vendorids = []
            coursetuitionnames = []
            paymentfees = []
            languages = []
            duration = []

            countcourselist = 0  # Initialize count outside of the try block

            
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Vendor_ID,CourseTuitionName,PaymentFees,Languages,Duration FROM coursedetails ')
            myresultcoursedetails = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM coursedetails')
            countcourselist = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for rowcl in myresultcoursedetails:
                vendorids.append(rowcl[0])
                coursetuitionnames.append(rowcl[1])
                paymentfees.append(rowcl[2])
                languages.append(rowcl[3])
                duration.append(rowcl[4])
                
                
            
            datacourselist = []

            # Iterate through the fetched records and generate HTML table rows
            for i in range(countcourselist):

                itemcourselist = {

                    "Vendor_id": vendorids[i],
                    "CourseTuition_name": coursetuitionnames[i],
                    "Duration": duration[i],
                    "Language": languages[i],
                    "Payment_Fees": paymentfees[i]
                    
                }
                datacourselist.append(itemcourselist)
        
        except Exception as e:
            error_messageforuserwebpage = 'An error occurred: ' + str(e)
            flash(error_messageforuserwebpage, 'error')
            return render_template('aboutus.html', error_messageforuserwebpage=error_messageforuserwebpage)
        
        
                
        return render_template('aboutus.html',datavendorslist=datavendorslist,datacourselist=datacourselist)

@app.route("/Contact_Us")
def Contact_Us():
        
    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    else:

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        sno=[]
        location_name = []
        locationimagename=[]
        url = []
        

        countmap = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT * FROM map_attributes')
            myresultmapattributes = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM map_attributes')
            countmap = cursor.fetchone()[0]  # Get the count value



            # Iterate through the result and append values to lists
            for rowm in myresultmapattributes:
                sno.append(rowm[0])
                location_name.append(rowm[1])
                locationimagename.append(rowm[2])
                url.append(rowm[3])
                
            

        except Exception as e:
            error_messageforuserwebpagemap = 'An error occurred: ' + str(e)
            flash(error_messageforuserwebpagemap, 'error')
            return render_template('Contact_Us.html', error_messageforuserwebpagemap=error_messageforuserwebpagemap)
        
        
        datalocationlist=[]

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countmap):

            itemlocationlist={
                
                "S_No":sno[i],
                "Location_name":location_name[i],
                "LocationImage_name":locationimagename[i],
                "URL":url[i],
                
            }
            datalocationlist.append(itemlocationlist)

        return render_template('Contact_Us.html',datalocationlist=datalocationlist)

@app.route('/userenquiry',methods=['GET','POST'])
def userenquiry():
    Name=request.form['name']
    Mail=request.form['mail']
    Phone=request.form['phone']
    Query=request.form['query']

    userMessaged_Duration = datetime.datetime.now()

    try:

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)
    
        connection = get_db_connection()
        cursor = connection.cursor()

        #  SQL query to fetch  records
        cursor.execute('INSERT INTO userenquirytable(User_Name,UserEnquiryMail,UserEnquiryNumber,UserQuery,UserMessageDuration) VALUES (%s,%s,%s,%s,%s)',(Name,Mail,Phone,Query,userMessaged_Duration))

        connection.commit()
        cursor.close()
        connection.close()
        
    except Exception as e:
        error_messageforenquiringuser = 'An error occurred: ' + str(e)
        flash(error_messageforenquiringuser, 'error')
        return render_template('Contact_Us.html', error_messageforenquiringuser=error_messageforenquiringuser)
    
    flash_messageforenquiringuser='Your Enquiry Submitted!'
    return render_template('Contact_Us.html',flash_messageforenquiringuser=flash_messageforenquiringuser)  # Redirect to the form page
        

@app.route('/web_pageaddbusiness')
def web_pageaddbusiness():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        uniqueVendorId=session.get('uniqueVendorId')
        flash_message="Add Your Profession/Business Details If your other than Educational or Food Sales Category"
        return render_template('addbusiness.html',uniqueVendorId=uniqueVendorId,flash_message=flash_message)

@app.route('/insert_vendorbusinessprofession',methods=['GET','POST'])
def insert_vendorbusinessprofession():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        if request.method == "POST":

            

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            try:
                # Moving Uploaded Picture(Logo Picture) to Particular Folder
                UPLOAD_FOLDER = "static/images/businessprofessionimages"
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png','avif','gif'}

                file = request.files['image']

                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image' not in request.files:
                    return "No file part"

                if file.filename == '':
                    return "No selected file"

                if not allowed_file(file.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                original_filenamelogo = file.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)

                
                
                
                
                
                
                Vendor_id=request.form['vendorid']
                Business_Profession_Name = request.form['businessprofessionname']
                Business_Profession_Details = request.form['aboutbusinessprofession']
                Experience = request.form['experience']
                Enquirynumber1 = request.form['phonenumber1']
                Enquirynumber2= request.form['phonenumber2']
                EnquiryMail = request.form['enquirymail']
                BusinessProfessionLink = request.form['businessprofessionlink']
                Enquiry_address = request.form['enquiryaddress']
                Location_Link=request.form['locationlink']
                

                def get_db_connection():
                    return mysql.connector.connect(**db_config)

                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute('INSERT INTO businessprofessionattributes(Vendor_ID,BusinessProfession_Name,BusinessProfession_LogoName,BusinessProfession_Details,Experience,EnquiryFirstNumber,EnquirySecondNumber,EnquiryMail,WebsiteLink,Address,Location_URL) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (Vendor_id,Business_Profession_Name,original_filenamelogo,Business_Profession_Details,Experience,Enquirynumber1,Enquirynumber2,EnquiryMail,BusinessProfessionLink,Enquiry_address,Location_Link))
                connection.commit()
                cursor.close()
                connection.close()
                
                return redirect(url_for('web_pageshowbusinessprofessiondetails'))  # Redirect to the form page

            except Exception as e:
                error_messageforaddbusiness = 'An error occurred: ' + str(e)
                flash(error_messageforaddbusiness, 'error')
                return render_template('addbusiness.html', error_messageforaddbusiness=error_messageforaddbusiness)
                

    return render_template('addbusiness.html')

@app.route('/get_new_contentbusinessprofessiondetails')
def get_new_contentbusinessprofessiondetails():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')

    else:
        dynamic_contentbusiness = ""

        dynamic_contentbusiness += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentbusiness += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentbusiness += f'<div class="container-fluid w-100" >'
        dynamic_contentbusiness += f'<div class="row">'
        dynamic_contentbusiness += f'<div class="col-12">'
        dynamic_contentbusiness += f'<div class="w-100">'
        dynamic_contentbusiness += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentbusiness += f'<h6 class="text-white text-capitalize ps-3">Business Details</h6>'
        dynamic_contentbusiness += f'</div>'

        dynamic_contentbusiness += f'</div>'
        dynamic_contentbusiness += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentbusiness += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentbusiness += f'<table class="table table-bordered mb-0">'
        dynamic_contentbusiness += f'<thead>'
        dynamic_contentbusiness += f'<tr>'
        dynamic_contentbusiness += f'<th>Business/Profession Name</th>'
        dynamic_contentbusiness += f'<th>Business/Profession Details</th>'
        dynamic_contentbusiness += f'<th>Business Enquiry</th>'
        
        dynamic_contentbusiness += f'</tr>'
        dynamic_contentbusiness += f'</thead>'
        dynamic_contentbusiness += f'<tbody>'

        dynamic_contentbusiness += f'</tbody>'
        dynamic_contentbusiness += f'</table>'

        dynamic_contentbusiness += f'</div>'

        web_page_urlshowbusinessprofessiondetails = url_for('web_pageshowbusinessprofessiondetails')
        dynamic_contentbusiness += f'<center><a href="{web_page_urlshowbusinessprofessiondetails}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentbusiness += f'</div>'

        dynamic_contentbusiness += f'</div>'
        dynamic_contentbusiness += f'</div>'

    return dynamic_contentbusiness
        

@app.route('/web_pageshowbusinessprofessiondetails')
def web_pageshowbusinessprofessiondetails():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')

    else:
        uniqueVendorId=session.get('uniqueVendorId')
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        bpids = []
        businessprofession_names = []
        businessprofessionlogonames = []
        
        businessprofession_details=[]
        experience=[]
        enquiryfirstnumber=[]
        enquirysecondnumber=[]
        enquirymail=[]
        websitelink=[]
        address=[]
        Location_Link=[]

        countbusinessprofession = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT id,BusinessProfession_Name,BusinessProfession_LogoName,BusinessProfession_Details,Experience,EnquiryFirstNumber,EnquirySecondNumber,EnquiryMail,WebsiteLink,Address,Location_URL FROM businessprofessionattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultbusinessprofessiondetails = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM businessprofessionattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            countbusinessprofession = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for rowbpdl in myresultbusinessprofessiondetails:
                bpids.append(rowbpdl[0])
                businessprofession_names.append(rowbpdl[1])
                businessprofessionlogonames.append(rowbpdl[2])
                
                businessprofession_details.append(rowbpdl[3])
                experience.append(rowbpdl[4])
                enquiryfirstnumber.append(rowbpdl[5])
                enquirysecondnumber.append(rowbpdl[6])
                enquirymail.append(rowbpdl[7])
                websitelink.append(rowbpdl[8])
                address.append(rowbpdl[9])
                Location_Link.append(rowbpdl[10])

        except Exception as e:
            error_messageforbusinessprofessionlist = 'An error occurred: ' + str(e)
            flash(error_messageforbusinessprofessionlist, 'error')
            return render_template('BusinessProfession_list.html', error_messageforbusinessprofessionlist=error_messageforbusinessprofessionlist)

        databusinessprofessionlist = []

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countbusinessprofession):

            itembusinessprofessionlist = {

                "B_P_id": bpids[i],
                "BusinessProfessionName":businessprofession_names[i],
                "BusinessProfessionLogoName":businessprofessionlogonames[i],
                
                "BusinessProfessionDetails":businessprofession_details[i],
                "Experience":experience[i],
                "Enquiry_Firstnumber":enquiryfirstnumber[i],
                "Enquiry_Secondnumber":enquirysecondnumber[i],
                "Enquiry_Mail":enquirymail[i],
                "Website_Link":websitelink[i],
                "Address":address[i],
                "LocationLink":Location_Link[i]
            }
            databusinessprofessionlist.append(itembusinessprofessionlist)

    return render_template('BusinessProfession_list.html', databusinessprofessionlist=databusinessprofessionlist)


@app.route("/web_pageupdatebusinessprofessiondetails/<int:BP_Id>",methods=['GET','POST'])
def web_pageupdatebusinessprofessiondetails(BP_Id):

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        selectBP_id = BP_Id

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        bpids = []
        vendorids=[]
        businessprofession_names = []
        businessprofessionlogonames = []
        
        businessprofession_details=[]
        experience=[]
        enquiryfirstnumber=[]
        enquirysecondnumber=[]
        enquirymail=[]
        websitelink=[]
        address=[]
        Location_Link=[]

       

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT * FROM businessprofessionattributes WHERE id=%s',(selectBP_id,))
            myresultbusinessprofessiondetails = cursor.fetchall()

            

            # Iterate through the result and append values to lists
            for rowbpdl in myresultbusinessprofessiondetails:
                bpids.append(rowbpdl[0])
                vendorids.append(rowbpdl[1])
                businessprofession_names.append(rowbpdl[2])
                businessprofessionlogonames.append(rowbpdl[3])
                businessprofession_details.append(rowbpdl[4])
                experience.append(rowbpdl[5])
                enquiryfirstnumber.append(rowbpdl[6])
                enquirysecondnumber.append(rowbpdl[7])
                enquirymail.append(rowbpdl[8])
                websitelink.append(rowbpdl[9])
                address.append(rowbpdl[10])
                Location_Link.append(rowbpdl[11])

        except Exception as e:
            error_messageforupdatebusinessprofession = 'An error occurred: ' + str(e)
            flash(error_messageforupdatebusinessprofession, 'error')
            return render_template('UpdateBusinessProfession.html', error_messageforupdatebusinessprofession=error_messageforupdatebusinessprofession)

    return render_template('UpdateBusinessProfession.html', bpids=bpids,vendorids=vendorids,
        businessprofession_names=businessprofession_names,
        businessprofessionlogonames=businessprofessionlogonames,
        
        businessprofession_details=businessprofession_details,
        experience=experience,
        enquiryfirstnumber=enquiryfirstnumber,
        enquirysecondnumber=enquirysecondnumber,
        enquirymail=enquirymail,
        websitelink=websitelink,
        address=address,Location_Link=Location_Link)

@app.route('/web_pageupdationbusinessprofession',methods=['GET','POST'])
def web_pageupdationbusinessprofession():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        if request.method == 'POST':

            # Handle form submission here
            bpid=request.form['businessprofessionids']
            vendorids=request.form['vendorid']   
            Business_Profession_Name = request.form['businessprofessionname']
            Business_Profession_Details = request.form['aboutbusinessprofession']
            Experience = request.form['experience']
            Enquirynumber1 = request.form['phonenumber1']
            Enquirynumber2= request.form['phonenumber2']
            EnquiryMail = request.form['enquirymail']
            BusinessProfessionLink = request.form['businessprofessionlink']
            Enquiry_address = request.form['enquiryaddress']
            Location_Link=request.form['locationlink']
                
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            try:

                file = request.files['image']
                
                
                
                if file.filename == '' :

                    connection = get_db_connection()
                    cursor = connection.cursor()
                    update_query = """
                    
                        UPDATE businessprofessionattributes SET BusinessProfession_Name=%s,BusinessProfession_Details=%s,Experience=%s,EnquiryFirstNumber=%s,EnquirySecondNumber=%s,EnquiryMail=%s,WebsiteLink=%s,Address=%s,Location_URL=%s WHERE id=%s;
                    
                        """

                    cursor.execute(update_query, (Business_Profession_Name,Business_Profession_Details,Experience,Enquirynumber1,Enquirynumber2,EnquiryMail,BusinessProfessionLink,Enquiry_address,Location_Link,bpid))
                    connection.commit()
                    cursor.close()
                    connection.close()

                else:

                    UPLOAD_FOLDER = "static/images/businessprofessionimages/"
                    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'avif', 'gif'}

                    
            
                    if not file.filename =="":
                        
                        def allowed_file(filename):
                            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                        if 'image' not in request.files:
                            return "No file part"

                        if not allowed_file(file.filename):
                            return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                        # Get the original filename of the uploaded file inorder to save filename in the database
                        original_logofilename = file.filename

                        # Save the uploaded file to the destination folder
                        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                        file.save(filename)

                
                   
                    connection = get_db_connection()
                    cursor = connection.cursor()
                    update_query = """
                    
                        UPDATE businessprofessionattributes SET BusinessProfession_Name=%s,BusinessProfession_LogoName=%s,BusinessProfession_Details=%s,Experience=%s,EnquiryFirstNumber=%s,EnquirySecondNumber=%s,EnquiryMail=%s,WebsiteLink=%s,Address=%s,Location_URL=%s WHERE id=%s;
                    
                        """

                    cursor.execute(update_query, (Business_Profession_Name,original_logofilename,Business_Profession_Details,Experience,Enquirynumber1,Enquirynumber2,EnquiryMail,BusinessProfessionLink,Enquiry_address,Location_Link,bpid))
                    connection.commit()
                    cursor.close()
                    connection.close()
            
            except Exception as e:
                error_messageforupdatebusinessprofession = 'An error occurred: ' + str(e)
                flash(error_messageforupdatebusinessprofession, 'error')
                return render_template('UpdateBusinessProfession.html', error_messageforupdatebusinessprofession=error_messageforupdatebusinessprofession)

                
        #After Updation,Show Business/Profession List
        return redirect(url_for('web_pageshowbusinessprofessiondetails'))

@app.route("/web_pageremovebusinessprofessiondetails/<int:BP_Id>")
def web_pageremovebusinessprofessiondetails(BP_Id):

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        SelectedBPId = BP_Id

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            update_query = """
                DELETE FROM businessprofessionattributes WHERE id=%s;
                """

            cursor.execute(update_query, (SelectedBPId,))
            connection.commit()
            cursor.close()
            connection.close()


        except Exception as e:
            error_messageforupdatebusinessprofession = 'An error occurred: ' + str(e)
            flash(error_messageforupdatebusinessprofession, 'error')
            return render_template('UpdateBusinessProfession.html', error_messageforupdatebusinessprofession=error_messageforupdatebusinessprofession)

    #After Deletion,Show Business/Profession List
    return redirect(url_for('web_pageshowbusinessprofessiondetails'))   

@app.route('/user_signup',methods=['GET','POST'])
def user_signup():

    if request.method=="POST":

        UserName=request.form['username']
        UserAddress=request.form['useraddress']
        UserPhoneNO=request.form['userphonenumber']
        UserEmail=request.form['useremailid']
        UserPassword=request.form['userpassword']
        UserConfirmPassword=request.form['confirmuserpassword']

        db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)
    
    # Function to fetch data from the database
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if UserPassword in UserConfirmPassword:
           cursor.execute('INSERT INTO userattributes(User_Name,User_Address,User_PhoneNumber,User_EMAILID,User_Password) VALUES(%s,%s,%s,%s,%s)',(UserName,UserAddress,UserPhoneNO,UserEmail,UserPassword))
           connection.commit()
           cursor.close()
           connection.close()
           alert_message1 = "Registered Successfully"
        else:
            alert_message1 = "Check! Password and Confirm Password are not same"
    
    except Exception as e:
        error_messageforusersignup = 'An error occurred: ' + str(e)
        flash(error_messageforusersignup, 'error')
        return render_template('loginpage.html', error_messageforusersignup=error_messageforusersignup)

    return jsonify(alert_message2=alert_message1)

@app.route('/vendor_signup',methods=['GET','POST'])
def vendor_signup():

    if request.method=="POST":

        VendorName=request.form['vendorname']
        VendorCategory=request.form['selectedOption']
        VendorAddress=request.form['vendoraddress']
        VendorPhoneno=request.form['vendorphoneno']
        VendorEmail=request.form['vendoremail']
        VendorPassword=request.form['vendorpassword']
        VendorConfirmPassword=request.form['confirmvendorpassword']

        db_config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)
    
    # Function to fetch data from the database
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if VendorPassword in VendorConfirmPassword:
           cursor.execute('INSERT INTO vendorattributes(Vendor_Name,Vendor_Category,Vendor_Address,Vendor_PhoneNumber,Vendor_EMAILID,Vendor_Password) VALUES(%s,%s,%s,%s,%s,%s)',(VendorName,VendorCategory,VendorAddress,VendorPhoneno,VendorEmail,VendorPassword))
           connection.commit()
           cursor.close()
           connection.close()
           alert_message3 = "Registered Successfully"
        else:
            alert_message3 = "Check! Password and Confirm Password are not same"
    
    except Exception as e:
        error_messageforvendorsignup = 'An error occurred: ' + str(e)
        flash(error_messageforvendorsignup, 'error')
        return render_template('loginpage.html', error_messageforvendorsignup=error_messageforvendorsignup)

    return jsonify(alert_message4=alert_message3)


           

@app.route('/get_new_contentstudentdetails',methods=['GET','POST'])
def get_new_contentstudentdetails():
     
    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        dynamic_contentstudentlist = ""

        dynamic_contentstudentlist += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentstudentlist += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentstudentlist += f'<div class="container-fluid w-100" >'
        dynamic_contentstudentlist += f'<div class="row">'
        dynamic_contentstudentlist += f'<div class="col-12">'
        dynamic_contentstudentlist += f'<div class="w-100">'
        dynamic_contentstudentlist += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentstudentlist += f'<h6 class="text-white text-capitalize ps-3">Student Details</h6>'
        dynamic_contentstudentlist += f'</div>'

        dynamic_contentstudentlist += f'</div>'
        dynamic_contentstudentlist += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentstudentlist += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentstudentlist += f'<table class="table table-bordered mb-0">'
        dynamic_contentstudentlist += f'<thead>'
        dynamic_contentstudentlist += f'<tr>'
        dynamic_contentstudentlist += f'<th>Student Name</th>'
        dynamic_contentstudentlist += f'<th>EMAIL_ID</th>'
        dynamic_contentstudentlist += f'<th>Contact Number</th>'
        
        
        dynamic_contentstudentlist += f'</tr>'
        dynamic_contentstudentlist += f'</thead>'
        dynamic_contentstudentlist += f'<tbody>'

        dynamic_contentstudentlist += f'</tbody>'
        dynamic_contentstudentlist += f'</table>'

        dynamic_contentstudentlist += f'</div>'

        web_page_urlshowstudentlist = url_for('web_pageStudentlist')
        dynamic_contentstudentlist += f'<center><a href="{web_page_urlshowstudentlist}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentstudentlist += f'</div>'

        dynamic_contentstudentlist += f'</div>'
        dynamic_contentstudentlist += f'</div>'

    return dynamic_contentstudentlist

@app.route('/web_pageStudentlist',methods=['GET','POST'])
def web_pageStudentlist():
    
    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')

    else:
        uniqueVendorId=session.get('uniqueVendorId')
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        
        studentname = []
        studentemail = []
        studentcontactnumber = []
        

        countstudentlist = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Student_Name,EMail,Contact_Number FROM studentdetails WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultstudentlist = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM studentdetails WHERE Vendor_ID=%s',(uniqueVendorId,))
            countstudentlist = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for rowsl in myresultstudentlist:
                
                studentname.append(rowsl[0])
                studentemail.append(rowsl[1])
                studentcontactnumber.append(rowsl[2])
                

        except Exception as e:
            error_messageforstudent = 'An error occurred: ' + str(e)
            flash(error_messageforstudent, 'error')
            return render_template('Student_list.html', error_messageforstudent=error_messageforstudent)

        datastudentlist = []

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countstudentlist):

            itemstudentlist = {
                
                "Student_Name": studentname[i],
                "Student_Email": studentemail[i],
                "Student_Contactnumber": studentcontactnumber[i],
                
            }
            datastudentlist.append(itemstudentlist)

    return render_template('Student_list.html', datastudentlist=datastudentlist)

@app.route('/web_pagecourseslist',methods=['GET','POST'])
def web_pagecourseslist():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')

    else:
        uniqueVendorId=session.get('uniqueVendorId')
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        courseids = []
        coursetuitionnames = []
        paymentfees = []
        coursetuitiondetails = []
        languages = []
        duration = []

        countcourselist = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Course_id,CourseTuitionName,PaymentFees,CourseTuition_Details,Languages,Duration FROM coursedetails WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresultcoursedetails = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM coursedetails WHERE Vendor_ID=%s',(uniqueVendorId,))
            countcourselist = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for rowcl in myresultcoursedetails:
                courseids.append(rowcl[0])
                coursetuitionnames.append(rowcl[1])
                paymentfees.append(rowcl[2])
                coursetuitiondetails.append(rowcl[3])
                languages.append(rowcl[4])
                duration.append(rowcl[5])

        except Exception as e:
            error_messageforcourse = 'An error occurred: ' + str(e)
            flash(error_messageforcourse, 'error')
            return render_template('Course_list.html', error_messageforcourse=error_messageforcourse)

        datacourselist = []

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countcourselist):

            itemcourselist = {

                "Course_id": courseids[i],
                "CourseTuition_name": coursetuitionnames[i],
                "Payment_Fees": paymentfees[i],
                "CourseTuition_Details": coursetuitiondetails[i],
                "Language": languages[i],
                "Duration": duration[i]
            }
            datacourselist.append(itemcourselist)

    return render_template('Course_list.html', datacourselist=datacourselist)

    
@app.route('/web_pageupdatecourse/<int:Course_id>',methods=['GET','POST'])  
def web_pageupdatecourse(Course_id):

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        selectCourse_id = Course_id

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        courseids = []
        coursetuition_name = []
        paymentfees = []
        coursetuitiondetails = []
        languages = []
        duration = []
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute(
                'SELECT Course_id,CourseTuitionName,PaymentFees,CourseTuition_Details,Languages,Duration FROM coursedetails WHERE Course_id=%s', (selectCourse_id,))
            myresultcoursetoupdate = cursor.fetchall()

            # Iterate through the result and append values to lists
            for rowcourse in myresultcoursetoupdate:
                courseids.append(rowcourse[0])
                coursetuition_name.append(rowcourse[1])
                paymentfees.append(rowcourse[2])
                coursetuitiondetails.append(rowcourse[3])
                languages.append(rowcourse[4])
                duration.append(rowcourse[5])
                

        except Exception as e:
            error_messageforupdatecourse = 'An error occurred: ' + str(e)
            flash(error_messageforupdatecourse, 'error')
            return render_template('Updatecourse.html', error_messageforupdatecourse=error_messageforupdatecourse)

    return render_template('Updatecourse.html', courseids=courseids, coursetuition_name=coursetuition_name,  paymentfees=paymentfees, coursetuitiondetails=coursetuitiondetails, languages=languages,duration=duration)

@app.route('/web_pageupdationcourse', methods=['GET', 'POST'])
def web_pageupdationcourse():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        if request.method == 'POST':

            # Handle form submission here
            CIDs = request.form['courseids']
            CourseTuitionName = request.form['coursetuitionname']
            PaymentTuitionFees = request.form['paymenttuitionfees']
            TuitionCourseDetails = request.form['tuitioncoursedetails']
            Language = request.form['language']
            Duration = request.form['duration']

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            try:
            
                connection = get_db_connection()
                cursor = connection.cursor()
                update_query = """
                    
                    UPDATE coursedetails SET CourseTuitionName=%s,PaymentFees=%s,CourseTuition_Details=%s,Languages=%s,Duration=%s WHERE Course_id=%s;
                    
                    """

                cursor.execute(update_query, (CourseTuitionName,PaymentTuitionFees,TuitionCourseDetails,Language,Duration,CIDs))
                connection.commit()
                cursor.close()
                connection.close()
            
            except Exception as e:
                error_messageforupdatecourse = 'An error occurred: ' + str(e)
                flash(error_messageforupdatecourse, 'error')
                return render_template('Updatecourse.html', error_messageforupdatecourse=error_messageforupdatecourse)
                

    # After Updation, Show Product List
    return redirect(url_for('web_pagecourseslist'))

@app.route("/web_pageremovecourse/<int:Course_id>")
def web_pageremovecourse(Course_id):

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        SelectedCourseId = Course_id
        
        try:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            connection = get_db_connection()
            cursor = connection.cursor()

            update_query = """
                DELETE FROM coursedetails WHERE Course_id=%s;
                """

            cursor.execute(update_query, (SelectedCourseId,))
            connection.commit()
            cursor.close()
            connection.close()
        
        except Exception as e:
            error_messageforcourse = 'An error occurred: ' + str(e)
            flash(error_messageforcourse, 'error')
            return render_template('Course_list.html', error_messageforcourse=error_messageforcourse)

    # After Deletion of record, Show Course List
    return redirect(url_for('web_pagecourseslist'))


@app.route('/checkout')
def checkout():
    if not session.get('userlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        data_string = request.args.get('data')

        uniqueUserId=session.get('uniqueUserId')

        if not data_string:
            return jsonify({"error": "No JSON data provided in the URL"}), 400
        
        try:
            decoded_data = urllib.parse.unquote(data_string)
            cart_data = json.loads(urllib.parse.unquote(decoded_data))
            return render_template('checkoutpage.html', cart_data=cart_data,uniqueUserId=uniqueUserId)

        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            error_message = f"Invalid JSON data in the URL: {str(e)}"
            return jsonify({"error": error_message}), 400
    

@app.route('/placeorder',methods=['GET','POST'])
def placeorder():
    if request.method=="POST":
        Userfirstname=request.form['firstname']
        Userlastname=request.form['lastname']
        Address=request.form['address']
        City=request.form['city']
        State=request.form['statename']
        Country=request.form['countryname']
        Zipcode=request.form['postalcode']
        Phonenumber=request.form['phoneno']
        Email=request.form['emailid']
        UserID=request.form['userid']


        #Getting list of names inorder to save multiple values(records) under single header(column)
        #forex: In Product_Name, Pizza,Banana,Lemon are stored in single row not as separate
        #       In Price, 22,5,10 are stored in single row not as separate     
        ordereditem_names = request.form.getlist('ordereditem_name[]')
        
        delimiter=","
        Resultnames=delimiter.join(ordereditem_names)
        #print(Resultnames)
        
        ordereditem_prices = request.form.getlist('ordereditem_price[]')
        Resultprices=delimiter.join(ordereditem_prices)
        #print(Resultprices)

        ordereditem_counts = request.form.getlist('ordereditem_count[]')
        Resultcounts=delimiter.join(ordereditem_counts)

        
        total=request.form.get('grandtotal')


        #Generating Order_Id
        def generate_order_id():
            # Define the characters you want to use in the order ID
            characters = string.ascii_letters + string.digits

            # Generate a random order ID with a length of 7 characters
            order_id = ''.join(random.choice(characters) for _ in range(7))

            return order_id

        order_id = generate_order_id()

        orderedduration = datetime.datetime.now()

        uniqueVendorId=session.get('uniqueVendorId')
       
        db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)
        

        try:

            connection = get_db_connection()
            cursor = connection.cursor()

            
            # SQL query to fetch  records
            cursor.execute("INSERT INTO ordertable(Order_ID,Vendor_ID,User_ID,Product_Name,Price,Quantity,Total,Order_Duration,Customer_FirstName,Customer_LastName,CustomerAddress,City,State,Country,PostalCode,Contact_Number,EMail_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(order_id,uniqueVendorId,UserID,Resultnames,Resultprices,Resultcounts,total,orderedduration,Userfirstname,Userlastname,Address,City,State,Country,Zipcode,Phonenumber,Email))
                
            connection.commit()
            cursor.close()
            connection.close()
        
        except Exception as e:
            error_messageforcheckout = 'An error occurred: ' + str(e)
            flash(error_messageforcheckout, 'error')
            return render_template('checkoutpage.html', error_messageforcheckout=error_messageforcheckout)
                                  
    flash_messageforuser="Your Order Is Placed"
    return render_template('checkoutpage.html',flash_messageforuser=flash_messageforuser)
    
        
    
    

    





@app.route('/get_new_content6', methods=['GET'])
def get_new_content6():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        dynamic_contentproductlist = ""

        dynamic_contentproductlist += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentproductlist += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentproductlist += f'<div class="container-fluid w-100" >'
        dynamic_contentproductlist += f'<div class="row">'
        dynamic_contentproductlist += f'<div class="col-12">'
        dynamic_contentproductlist += f'<div class="w-100">'
        dynamic_contentproductlist += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentproductlist += f'<h6 class="text-white text-capitalize ps-3">Product List</h6>'
        dynamic_contentproductlist += f'</div>'

        dynamic_contentproductlist += f'</div>'
        dynamic_contentproductlist += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentproductlist += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentproductlist += f'<table class="table table-bordered mb-0">'
        dynamic_contentproductlist += f'<thead>'
        dynamic_contentproductlist += f'<tr>'
        dynamic_contentproductlist += f'<th>Product ID</th>'
        dynamic_contentproductlist += f'<th>Product Name</th>'
        dynamic_contentproductlist += f'<th>Product Images</th>'
        dynamic_contentproductlist += f'<th>Product Category'
        dynamic_contentproductlist += f'<th>Product Details</th>'
        dynamic_contentproductlist += f'<th>Price</th>'
        dynamic_contentproductlist += f'<th>Updation</th>'

        dynamic_contentproductlist += f'</tr>'
        dynamic_contentproductlist += f'</thead>'
        dynamic_contentproductlist += f'<tbody>'

        dynamic_contentproductlist += f'</tbody>'
        dynamic_contentproductlist += f'</table>'

        dynamic_contentproductlist += f'</div>'

        web_page_urlshowproductlist = url_for('web_pageproductlist')
        dynamic_contentproductlist += f'<center><a href="{web_page_urlshowproductlist}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentproductlist += f'</div>'

        dynamic_contentproductlist += f'</div>'
        dynamic_contentproductlist += f'</div>'

    return dynamic_contentproductlist


@app.route('/web_pageproductlist')
def web_pageproductlist():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')

    else:
        uniqueVendorId=session.get('uniqueVendorId')
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        productids = []
        productnames = []
        productimagenames = []
        productcategories = []
       
        productdetails = []
        prices = []

        count2 = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Product_ID,Product_Name,ProductImage_Name,Product_category,Product_Details,Price FROM productattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresult1 = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM productattributes WHERE Vendor_ID=%s',(uniqueVendorId,))
            count2 = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for row2 in myresult1:
                productids.append(row2[0])
                
                productnames.append(row2[1])
                productimagenames.append(row2[2])
                productcategories.append(row2[3])
               
                productdetails.append(row2[4])
                prices.append(row2[5])

        except Exception as e:
            error_messageforproduct = 'An error occurred: ' + str(e)
            flash(error_messageforproduct, 'error')
            return render_template('Product_list.html', error_messageforproduct=error_messageforproduct)

        dataproductlist = []

        # Iterate through the fetched records and generate HTML table rows
        for i in range(count2):

            itemproductlist = {

                "Product_id": productids[i],
                "Product_name": productnames[i],
                "Productimage_name": productimagenames[i],
                "Product_category": productcategories[i],
                
                "Product_details": productdetails[i],
                "Price": prices[i]
            }
            dataproductlist.append(itemproductlist)

    return render_template('Product_list.html', dataproductlist=dataproductlist)


@app.route('/web_pageupdateproduct/<int:Product_id>', methods=['GET', 'POST'])
def web_pageupdateproduct(Product_id):

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        selectProduct_id = Product_id

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        productids = []
        productvendorids = []
        productnames = []
        productimagenames = []
        productcategories = []
        
        productdetails = []
        prices = []

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute(
                'SELECT Product_ID,Vendor_ID,Product_Name,ProductImage_Name,Product_category,Product_Details,Price FROM productattributes WHERE Product_ID=%s', (selectProduct_id,))
            myresultvproduct = cursor.fetchall()

            # Iterate through the result and append values to lists
            for rowvproduct in myresultvproduct:
                productids.append(rowvproduct[0])
                productvendorids.append(rowvproduct[1])
                productnames.append(rowvproduct[2])
                productimagenames.append(rowvproduct[3])
                productcategories.append(rowvproduct[4])
                
                productdetails.append(rowvproduct[5])
                prices.append(rowvproduct[6])

        except Exception as e:
            error_messageforupdateproduct = 'An error occurred: ' + str(e)
            flash(error_messageforupdateproduct, 'error')
            return render_template('Updateproduct.html', error_messageforupdateproduct=error_messageforupdateproduct)

    return render_template('Updateproduct.html', productids=productids,productvendorids=productvendorids, productnames=productnames,productimagenames=productimagenames,productcategories=productcategories,  productdetails=productdetails, prices=prices)


@app.route("/web_pageremoveproduct/<int:Product_id>")
def web_pageremoveproduct(Product_id):

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        SelectedProductId = Product_id

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)
        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            update_query = """
                DELETE FROM productattributes WHERE Product_ID=%s;
                """

            cursor.execute(update_query, (SelectedProductId,))
            connection.commit()
            cursor.close()
            connection.close()
        
        except Exception as e:
            error_messageforproduct = 'An error occurred: ' + str(e)
            flash(error_messageforproduct, 'error')
            return render_template('Product_list.html', error_messageforproduct=error_messageforproduct)

        # After Deletion of record, Show Product List
        return redirect(url_for('web_pageproductlist'))

@app.route('/web_pageupdationproduct', methods=['GET', 'POST'])
def web_pageupdationproduct():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        if request.method == 'POST':

            # Handle form submission here
            PIDs = request.form['productids']
            PName = request.form['productname']
            selectoption = request.form['selectedOption']
            
            Comment = request.form['details']
            Price = request.form['price']

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            file = request.files['image']

            try:

                if file.filename == '':

                    connection = get_db_connection()
                    cursor = connection.cursor()
                    update_query = """
                        
                        UPDATE productattributes SET Product_Name=%s,Product_category=%s,Product_Details=%s,Price=%s WHERE Product_ID=%s;
                        
                        """

                    cursor.execute(update_query, (PName, selectoption,
                                Comment, Price, PIDs))
                    connection.commit()
                    cursor.close()
                    connection.close()

                else:

                    UPLOAD_FOLDER = "static/images/productimages/"
                    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'avif', 'gif'}

                    def allowed_file(filename):
                        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                    if 'image' not in request.files:
                        return "No file part"

                    if not allowed_file(file.filename):
                        return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                    # Get the original filename of the uploaded file inorder to save filename in the database
                    original_newfilename = file.filename

                    # Save the uploaded file to the destination folder
                    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                    file.save(filename)

                    connection = get_db_connection()
                    cursor = connection.cursor()
                    update_query = """
                        
                        UPDATE productattributes SET Product_Name=%s,ProductImage_Name=%s,Product_category=%s,Product_Details=%s,Price=%s WHERE Product_ID=%s;
                        
                        """

                    cursor.execute(update_query, (PName, original_newfilename,
                                selectoption,  Comment, Price, PIDs))
                    connection.commit()
                    cursor.close()
                    connection.close()
            
            except Exception as e:
                error_messageforupdateproduct = 'An error occurred: ' + str(e)
                flash(error_messageforupdateproduct, 'error')
                return render_template('Updateproduct.html', error_messageforupdateproduct=error_messageforupdateproduct)

            # After Updation, Show Product List
            return redirect(url_for('web_pageproductlist'))
            

@app.route('/get_new_content7', methods=['GET', 'POST'])
def get_new_content7():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        # Generate your dynamic HTML content here
        dynamic_content7 = ""
        
        
        dynamic_content7 += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_content7 += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
        
        dynamic_content7 += f'<div class="container">'
        dynamic_content7 += f'<div class="row">'
        dynamic_content7 += f'<div class="w-100">'
        dynamic_content7 += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-342px;">'
        dynamic_content7 += f'<h6 class="text-white text-capitalize ps-3">Add Products</h6>'
        dynamic_content7 += f'</div>'
        dynamic_content7 += f'</div>'

        web_page_urladdproduct = url_for('web_pageaddproduct')
        dynamic_content7 += f'<center><a href="{web_page_urladdproduct}" class="btn btn-success" style="margin-top:-275px;">Click Here!</a></center>'

        
    
    return dynamic_content7



@app.route('/web_pageaddproduct')
def web_pageaddproduct():
    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        uniqueVendorId=session.get('uniqueVendorId')
        flash_message='Add Your Products Here If your other than "Education" or "Business/Profession" Category'
        return render_template('addproduct.html',flash_message=flash_message,uniqueVendorId=uniqueVendorId)


@app.route('/insertproducts',methods=['GET','POST'])
def insertproducts():
    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        if request.method == 'POST':

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            # Insert data into the MySQL database
            try:

                UPLOAD_FOLDER = "static/images/productimages/"
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png','avif','gif'}

                file = request.files['image']

                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image' not in request.files:
                    return "No file part"

                if file.filename == '':
                    return "No selected file"

                if not allowed_file(file.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                original_filename1 = file.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)

                # Handle form submission here
                Vendorid=request.form['vendorid']
                PName = request.form['productname']
                selectoption = request.form['selectedOption']
               
                Comment = request.form['commenthere']
                Price = request.form['price']

                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute('INSERT INTO productattributes (Vendor_ID,Product_Name,ProductImage_Name,Product_category,Product_Details,Price) VALUES (%s, %s,%s,%s,%s,%s)',
                            (Vendorid,PName, original_filename1, selectoption,  Comment, Price))
                connection.commit()
                cursor.close()
                connection.close()

                
                return redirect(url_for('web_pageproductlist'))
            except Exception as e:
                error_messageforaddproduct = 'An error occurred: ' + str(e)
                flash(error_messageforaddproduct, 'error')
                return render_template('addproduct.html', error_messageforaddproduct=error_messageforaddproduct)


@app.route('/get_new_contentprofile', methods=['GET', 'POST'])
def get_new_contentprofile():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        # Generate your dynamic HTML content here
        dynamic_contentuserprofile = ""

        dynamic_contentuserprofile += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentuserprofile += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentuserprofile += f'<div class="container">'
        dynamic_contentuserprofile += f'<div class="row">'
        dynamic_contentuserprofile += f'<div class="w-100">'
        dynamic_contentuserprofile += f'<div class="shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;  margin-top:-340px;">'
        dynamic_contentuserprofile += f'<center><h6 class="text-white text-capitalize ps-3">Add Your Personal Profile</h6></center>'
        dynamic_contentuserprofile += f"</div>"
        dynamic_contentuserprofile += f"</div>"

        web_page_urlpersonalprofile = url_for('web_pagevendorpersonalprofile')
        dynamic_contentuserprofile += f'<center><a href="{web_page_urlpersonalprofile}" class="btn btn-success" style="margin-top:-402px;">Click Here!</a></center>'
        dynamic_contentuserprofile += f'</div>'
        dynamic_contentuserprofile += f'</div>'

    return dynamic_contentuserprofile

@app.route('/get_new_contentaddcourses', methods=['GET', 'POST'])
def get_new_contentaddcourses():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        # Generate your dynamic HTML content here
        dynamic_contentaddcourses = ""

        dynamic_contentaddcourses += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentaddcourses += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentaddcourses += f'<div class="container">'
        dynamic_contentaddcourses += f'<div class="row">'
        dynamic_contentaddcourses += f'<div class="w-100">'
        dynamic_contentaddcourses += f'<div class="shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;  margin-top:-340px;">'
        dynamic_contentaddcourses += f'<center><h6 class="text-white text-capitalize ps-3">Add Your Courses</h6></center>'
        dynamic_contentaddcourses += f"</div>"
        dynamic_contentaddcourses += f"</div>"

        web_page_urladdcourses = url_for('web_pageaddcourses')
        dynamic_contentaddcourses += f'<center><a href="{web_page_urladdcourses}" class="btn btn-success" style="margin-top:-402px;">Click Here!</a></center>'
        dynamic_contentaddcourses += f'</div>'
        dynamic_contentaddcourses += f'</div>'

    return dynamic_contentaddcourses

@app.route('/web_pageaddcourses')
def web_pageaddcourses():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        uniqueVendorId=session.get('uniqueVendorId')
        return render_template('addcoursesentry.html',uniqueVendorId=uniqueVendorId)






@app.route('/insertcoursesdetails', methods=['GET', 'POST'])
def insertcoursedetails():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:
        if request.method == "POST":

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            try:
                
                Vendor_id=request.form['vendorid']
                coursetuition= request.form['coursetuitionname']
                payment_tuitionfees = request.form['paymenttuitionfees']
                tuitioncourse_details = request.form['tuitioncoursedetails']
                Language = request.form['language']
                durations = request.form['duration']
                
                def get_db_connection():
                    return mysql.connector.connect(**db_config)

                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute('INSERT INTO coursedetails(Vendor_ID,CourseTuitionName,PaymentFees,CourseTuition_Details,Languages,Duration) VALUES (%s,%s,%s,%s,%s,%s)',
                            (Vendor_id,coursetuition,payment_tuitionfees,tuitioncourse_details,Language,durations))
                connection.commit()
                cursor.close()
                connection.close()

            except Exception as e:
                error_messageforcourse = 'An error occurred: ' + str(e)
                flash(error_messageforcourse, 'error')
                return render_template('addcoursesentry.html', error_messageforcourse=error_messageforcourse)

    return redirect(url_for('web_pagecourseslist'))



@app.route('/get_new_content8', methods=['GET'])
def get_new_content8():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        dynamic_contentindexoforderlist = ""

        dynamic_contentindexoforderlist += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentindexoforderlist += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
        dynamic_contentindexoforderlist += f'<div class="container-fluid w-100" >'
        dynamic_contentindexoforderlist += f'<div class="row">'
        dynamic_contentindexoforderlist += f'<div class="col-12">'
        dynamic_contentindexoforderlist += f'<div class="w-100">'
        dynamic_contentindexoforderlist += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;margin-top:-346px;">'
        dynamic_contentindexoforderlist += f'<h6 class="text-white text-capitalize ps-3">Ordered Product List</h6>'
        dynamic_contentindexoforderlist += f'</div>'

        dynamic_contentindexoforderlist += f'</div>'
        dynamic_contentindexoforderlist += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentindexoforderlist += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentindexoforderlist += f'<table class="table table-bordered mb-0">'
        dynamic_contentindexoforderlist += f'<thead>'
        dynamic_contentindexoforderlist += f'<tr>'
        dynamic_contentindexoforderlist += f'<th>S.No</th>'
        dynamic_contentindexoforderlist += f'<th>Order_ID</th>'
        dynamic_contentindexoforderlist += f'<th>Vendor_ID</th>'
        dynamic_contentindexoforderlist += f'<th>Product_ID</th>'
        dynamic_contentindexoforderlist += f'<th>Product_Name</th>'
        dynamic_contentindexoforderlist += f'<th>Product_Image</th>'
        dynamic_contentindexoforderlist += f'<th>Product_Category</th>'
        dynamic_contentindexoforderlist += f'<th>Product_Details</th>'
        dynamic_contentindexoforderlist += f'<th>Quantity</th>'
        dynamic_contentindexoforderlist += f'<th>Price</th>'
        dynamic_contentindexoforderlist += f'<th>Further</th>'

        dynamic_contentindexoforderlist += f'</tr>'
        dynamic_contentindexoforderlist += f'</thead>'
        dynamic_contentindexoforderlist += f'<tbody>'

        dynamic_contentindexoforderlist += f'</tbody>'
        dynamic_contentindexoforderlist += f'</table>'
        dynamic_contentindexoforderlist += f'</div>'

        web_page_urlshoworderlist = url_for('web_pageorderlist')
        dynamic_contentindexoforderlist += f'<center><a href="{web_page_urlshoworderlist}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentindexoforderlist += f'</div>'
        dynamic_contentindexoforderlist += f'</div>'
        dynamic_contentindexoforderlist += f'</div>'
        dynamic_contentindexoforderlist += f'</div>'

    return dynamic_contentindexoforderlist


@app.route('/web_pageorderlist')
def web_pageorderlist():

    if not session.get('vendorlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        uniqueVendorId=session.get('uniqueVendorId')

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
       
        orderids = []
        
        productnames = []
        prices = []
        total = []
        productorderedduration = []
        customerfirstname=[]
        customerlastname=[]
        customeraddress=[]
        city=[]
        contactnumber=[]
        emailid = []
        

        count3 = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Order_ID,Product_Name,Price,Total,Order_Duration,Customer_FirstName,Customer_LastName,CustomerAddress,City,Contact_Number,EMail_ID FROM ordertable WHERE Vendor_ID=%s',(uniqueVendorId,))
            myresult3 = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM ordertable WHERE Vendor_ID=%s',(uniqueVendorId,))
            count3 = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for row3 in myresult3:
                orderids.append(row3[0])
                
                productnames.append(row3[1])
                prices.append(row3[2])
                total.append(row3[3])
                productorderedduration.append(row3[4])
                customerfirstname.append(row3[5])
                customerlastname.append(row3[6])
                customeraddress.append(row3[7])
                city.append(row3[8])
                contactnumber.append(row3[9])
                emailid.append(row3[10])
                

        except Exception as e:
            error_messagefororder = 'An error occurred: ' + str(e)
            flash(error_messagefororder, 'error')
            return render_template('orderlist.html', error_messagefororder=error_messagefororder)

        dataorderlist = []

        # Iterate through the fetched records and generate HTML table rows
        for i in range(count3):
            item = {
                
                "order_id": orderids[i],
                
                "product_name": productnames[i],
                "price": prices[i],
                "Total": total[i],
                "productordered_duration": productorderedduration[i],
                "customer_firstname": customerfirstname[i],
                "customer_lastname": customerlastname[i],
                "customer_address":customeraddress[i],
                "City": city[i],
                "Contact_number":contactnumber[i],
                "Email_ID":emailid[i]
                
            }
            dataorderlist.append(item)

    return render_template('orderlist.html', dataorderlist=dataorderlist)


@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    
    AdminId=request.form['adminid']
    AdminPassword=request.form['adminpassword']

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
    )
    # Function to fetch data from the database
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT admin_id,adminpassword from adminattributes")
        admin_data = mycursor.fetchall()


        #Below Method are used to compare input(User) with set of datas(ids and passwords) from database
        match_found = False  # A flag to indicate if a match is found
        
        # Iterate through the result and store values into separate lists
        for admindatas in admin_data:

            adminid,admin_password=admindatas
            if AdminId == adminid and AdminPassword == admin_password:
                match_found = True
                break  # Exit the loop once a match is found
    
    except Exception as e:
        alert_messageforadmin="An Error Occurred:" +str(e)
        return jsonify(alert_messageforadmin=alert_messageforadmin)
        

    # Authentication logic here
    if match_found:
        session.permanent=True
        session['AdminId']=AdminId
        session['adminlogged_in']=True
        return jsonify(status=200)
    
    else:
        alert_messageforadmin="Check ID and Password"
        return jsonify(alert_messageforadmin=alert_messageforadmin)

    
      
    

    
@app.route('/admin_dashboard')
def admin_dashboard():

    if session.get('adminlogged_in',False):
        return render_template('adminpanel.html')
    else:
        return render_template('adminlogin.html')
    

@app.route('/adminlogout')
def adminlogout():

    session.pop('adminlogged_in',None)
    return render_template('adminlogin.html')




@app.route('/changeadminpassword',methods=['GET','POST'])
def changeadminpassword():

    
    CheckAdminId=request.form['adminidforcheck']
    NewPassword=request.form['newpassword']
    AgainNewPassword=request.form['againnewpassword']

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
    )
    # Function to fetch data from the database
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT admin_id,adminpassword from adminattributes")
        data = mycursor.fetchall()
        # Initialize empty lists to store values
        admin_ids = []
        admin_passwords = []

        # Iterate through the result and store values into separate lists
        for adminid, admin_password in data:

            admin_ids.append(adminid)
            admin_passwords.append(admin_password)

        if CheckAdminId in admin_ids and NewPassword == AgainNewPassword:
           mycursor.execute("UPDATE adminattributes SET adminpassword= %s  WHERE admin_id= %s",(NewPassword,CheckAdminId))
           mydb.commit()
           alert_message = "Password Updated"
        else:
            alert_message = "Password not updated!,Try Again"
    
    except Exception as e:
        alert_message = "An error occurred:" +str(e)
        return jsonify(alert_message=alert_message)

        


    return jsonify(alert_message=alert_message)




# Dynamic Page Without Refreshing Whole Page in Flask Module
@app.route('/get_new_content', methods=['GET'])
def get_new_content():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')
    
    else:
        
        #Getting Below Values from app.route('/adminlogin) by using session.get
        AdminId=session.get('AdminId')

        # Generate your dynamic HTML content here
        dynamic_content = f"""
        
            
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
        
            <div class="container-fluid w-100 style="padding-inline-start:10px;"  >
            <div class="row">
            <div class="col-12">
            <div class="w-100">
            <div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;  margin-top:-315px;">
            <h6 class="text-white text-capitalize ps-3">Admin Profile</h6>
            </div>
            </div>
            
            <div class="card text-bg-light mb-3 col-12" style="margin-top:40px;  width: 100%;">
            <div class="card-header">Admin Details</div>
            <div class="card-body">
            Admin_ID:  <label class='card-text'>{AdminId}</label><br>
            
                
            </div>
            </div>
            </div 
            </div>
            </div>
            """

    return dynamic_content




@app.route('/get_new_content2', methods=['GET', 'POST'])
def get_new_content2():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')
    
    else:

        dynamic_contentvendorauth=""

        dynamic_contentvendorauth +=f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentvendorauth+=f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
            
        dynamic_contentvendorauth+=f'<div class="container-fluid w-100" >'
        dynamic_contentvendorauth+=f'<div class="row">'
        dynamic_contentvendorauth+=f'<div class="col-12">'
        dynamic_contentvendorauth+=f'<div class="w-100">'
        dynamic_contentvendorauth+=f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentvendorauth+=f'<h6 class="text-white text-capitalize ps-3">Vendors For Authentication</h6>'
        dynamic_contentvendorauth+=f'</div>'

        dynamic_contentvendorauth+=f'</div>'
        dynamic_contentvendorauth+=f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentvendorauth+=f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentvendorauth+=f'<table class="table table-bordered mb-0">'
        dynamic_contentvendorauth+=f'<thead>'
        dynamic_contentvendorauth+=f'<tr>'
        
        
        dynamic_contentvendorauth+=f'<th>Vendor Name</th>'
        dynamic_contentvendorauth+=f'<th>Details</th>'
        dynamic_contentvendorauth+=f'<th>Authentication</th>'
        
                        
        dynamic_contentvendorauth+=f'</tr>'
        dynamic_contentvendorauth+=f'</thead>'
        dynamic_contentvendorauth+=f'<tbody>'
                        
        dynamic_contentvendorauth+=f'</tbody>'
        dynamic_contentvendorauth+=f'</table>'
            

        dynamic_contentvendorauth+=f'</div>'

        web_page_urlshowauthvendorauthlist = url_for('web_pageauthvendorlist')
        dynamic_contentvendorauth+=f'<center><a href="{web_page_urlshowauthvendorauthlist}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'
    
        dynamic_contentvendorauth+=f'</div>'
        
        dynamic_contentvendorauth+=f'</div>'
        dynamic_contentvendorauth+=f'</div>'
        
    return dynamic_contentvendorauth

@app.route('/get_new_contentvendorlist')
def get_new_contentvendorlist():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')
    
    else:

        dynamic_contentvendorlist=""

        dynamic_contentvendorlist+=f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentvendorlist+=f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
            
        dynamic_contentvendorlist+=f'<div class="container-fluid w-100" >'
        dynamic_contentvendorlist+=f'<div class="row">'
        dynamic_contentvendorlist+=f'<div class="col-12">'
        dynamic_contentvendorlist+=f'<div class="w-100">'
        dynamic_contentvendorlist+=f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentvendorlist+=f'<h6 class="text-white text-capitalize ps-3">Vendor List</h6>'
        dynamic_contentvendorlist+=f'</div>'

        dynamic_contentvendorlist+=f'</div>'
        dynamic_contentvendorlist+=f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentvendorlist+=f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentvendorlist+=f'<table class="table table-bordered mb-0">'
        dynamic_contentvendorlist+=f'<thead>'
        dynamic_contentvendorlist+=f'<tr>'
        
        
        dynamic_contentvendorlist+=f'<th>Vendor Name</th>'
        dynamic_contentvendorlist+=f'<th>Details</th>'
        dynamic_contentvendorlist+=f'<th>Authentication</th>'
        
                        
        dynamic_contentvendorlist+=f'</tr>'
        dynamic_contentvendorlist+=f'</thead>'
        dynamic_contentvendorlist+=f'<tbody>'
                        
        dynamic_contentvendorlist+=f'</tbody>'
        dynamic_contentvendorlist+=f'</table>'
            

        dynamic_contentvendorlist+=f'</div>'

        web_page_urlshowvendorlist = url_for('web_pagevendorlist')
        dynamic_contentvendorlist+=f'<center><a href="{web_page_urlshowvendorlist}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'
    
        dynamic_contentvendorlist+=f'</div>'
        
        dynamic_contentvendorlist+=f'</div>'
        dynamic_contentvendorlist+=f'</div>'
        
    return dynamic_contentvendorlist
    
@app.route('/get_new_contentlocationlist') 
def get_new_contentlocationlist():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:   
        dynamic_contentforlocation=""

        dynamic_contentforlocation +=f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentforlocation +=f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
            
        dynamic_contentforlocation +=f'<div class="container-fluid w-100" >'
        dynamic_contentforlocation +=f'<div class="row">'
        dynamic_contentforlocation +=f'<div class="col-12">'
        dynamic_contentforlocation +=f'<div class="w-100">'
        dynamic_contentforlocation +=f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentforlocation +=f'<h6 class="text-white text-capitalize ps-3">Location</h6>'
        dynamic_contentforlocation +=f'</div>'

        web_page_urlforlocation = url_for('web_pageforlocation')
        dynamic_contentforlocation+=f'<center><a href="{web_page_urlforlocation}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'
        dynamic_contentforlocation +=f'</div>'
        dynamic_contentforlocation +=f'</div>'
        dynamic_contentforlocation +=f'</div>'
        dynamic_contentforlocation +=f'</div>'
    
    return dynamic_contentforlocation

@app.route('/get_new_contentorderlistforadmin', methods=['GET'])
def get_new_contentorderlistforadmin():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        dynamic_contentindexoforderlistforadmin = ""

        dynamic_contentindexoforderlistforadmin += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentindexoforderlistforadmin += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
        dynamic_contentindexoforderlistforadmin += f'<div class="container-fluid w-100" >'
        dynamic_contentindexoforderlistforadmin += f'<div class="row">'
        dynamic_contentindexoforderlistforadmin += f'<div class="col-12">'
        dynamic_contentindexoforderlistforadmin += f'<div class="w-100">'
        dynamic_contentindexoforderlistforadmin += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;margin-top:-346px;">'
        dynamic_contentindexoforderlistforadmin += f'<h6 class="text-white text-capitalize ps-3">Ordered Product List</h6>'
        dynamic_contentindexoforderlistforadmin += f'</div>'

        dynamic_contentindexoforderlistforadmin += f'</div>'
        dynamic_contentindexoforderlistforadmin += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentindexoforderlistforadmin += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentindexoforderlistforadmin += f'<table class="table table-bordered mb-0">'
        dynamic_contentindexoforderlistforadmin += f'<thead>'
        dynamic_contentindexoforderlistforadmin += f'<tr>'
        dynamic_contentindexoforderlistforadmin += f'<th>S.No</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Order_ID</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Vendor_ID</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Product_ID</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Product_Name</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Product_Image</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Product_Category</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Product_Details</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Quantity</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Price</th>'
        dynamic_contentindexoforderlistforadmin += f'<th>Further</th>'

        dynamic_contentindexoforderlistforadmin += f'</tr>'
        dynamic_contentindexoforderlistforadmin += f'</thead>'
        dynamic_contentindexoforderlistforadmin += f'<tbody>'

        dynamic_contentindexoforderlistforadmin += f'</tbody>'
        dynamic_contentindexoforderlistforadmin += f'</table>'
        dynamic_contentindexoforderlistforadmin += f'</div>'

        web_page_urlshoworderlistforadmin = url_for('web_pageorderlistforadmin')
        dynamic_contentindexoforderlistforadmin += f'<center><a href="{web_page_urlshoworderlistforadmin}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentindexoforderlistforadmin += f'</div>'
        dynamic_contentindexoforderlistforadmin += f'</div>'
        dynamic_contentindexoforderlistforadmin += f'</div>'
        dynamic_contentindexoforderlistforadmin += f'</div>'

    return dynamic_contentindexoforderlistforadmin

@app.route('/web_pageorderlistforadmin')
def web_pageorderlistforadmin():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('loginpage.html')
    
    else:

        

        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
       
        orderids = []
        vendorids=[]
        productnames = []
        prices = []
        total = []
        productorderedduration = []
        customerfirstname=[]
        customerlastname=[]
        customeraddress=[]
        city=[]
        contactnumber=[]
        emailid = []
        

        count3 = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Order_ID,Vendor_ID,Product_Name,Price,Total,Order_Duration,Customer_FirstName,Customer_LastName,CustomerAddress,City,Contact_Number,EMail_ID FROM ordertable ')
            myresult3 = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM ordertable ')
            count3 = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for row3 in myresult3:
                orderids.append(row3[0])
                vendorids.append(row3[1])
                productnames.append(row3[2])
                prices.append(row3[3])
                total.append(row3[4])
                productorderedduration.append(row3[5])
                customerfirstname.append(row3[6])
                customerlastname.append(row3[7])
                customeraddress.append(row3[8])
                city.append(row3[9])
                contactnumber.append(row3[10])
                emailid.append(row3[11])
                

        except Exception as e:
            error_messageorderlistforadmin = 'An error occurred: ' + str(e)
            flash(error_messageorderlistforadmin, 'error')
            return render_template('orderlistforadmin.html', error_messageorderlistforadmin=error_messageorderlistforadmin)

        dataorderlist = []

        # Iterate through the fetched records and generate HTML table rows
        for i in range(count3):
            item = {
                
                "order_id": orderids[i],
                "vendor_id":vendorids[i],
                "product_name": productnames[i],
                "price": prices[i],
                "Total": total[i],
                "productordered_duration": productorderedduration[i],
                "customer_firstname": customerfirstname[i],
                "customer_lastname": customerlastname[i],
                "customer_address":customeraddress[i],
                "City": city[i],
                "Contact_number":contactnumber[i],
                "Email_ID":emailid[i]
                
            }
            dataorderlist.append(item)

    return render_template('orderlistforadmin.html', dataorderlist=dataorderlist)


@app.route('/web_pageforlocation')
def web_pageforlocation():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:  
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        sno=[]
        location_name = []
        locationimagename=[]
        url = []
        

        countmapattributes = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT * FROM map_attributes')
            myresultmap = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM map_attributes')
            countmapattributes = cursor.fetchone()[0]  # Get the count value



            # Iterate through the result and append values to lists
            for rowm in myresultmap:
                sno.append(rowm[0])
                location_name.append(rowm[1])
                locationimagename.append(rowm[2])
                url.append(rowm[3])
                
            

        except Exception as e:
            error_messagelocationforadmin = 'An error occurred: ' + str(e)
            flash(error_messagelocationforadmin, 'error')
            return render_template('Location_list.html', error_messagelocationforadmin=error_messagelocationforadmin)


        datalocationlist=[]

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countmapattributes):

            itemlocationlist={
                
                "S_No":sno[i],
                "Location_name":location_name[i],
                "LocationImage_name":locationimagename[i],
                "URL":url[i],
                
            }
            datalocationlist.append(itemlocationlist)

        
    return render_template('Location_list.html',datalocationlist=datalocationlist)

@app.route('/get_new_contentUserEnquiry')
def get_new_contentUserEnquiry():
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')
    
    else:

        dynamic_contentuserenquiry = ""

        dynamic_contentuserenquiry += f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentuserenquiry += f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'

        dynamic_contentuserenquiry += f'<div class="container-fluid w-100" >'
        dynamic_contentuserenquiry += f'<div class="row">'
        dynamic_contentuserenquiry += f'<div class="col-12">'
        dynamic_contentuserenquiry += f'<div class="w-100">'
        dynamic_contentuserenquiry += f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4; margin-top:-350px;">'
        dynamic_contentuserenquiry += f'<h6 class="text-white text-capitalize ps-3">User_Enquiries</h6>'
        dynamic_contentuserenquiry += f'</div>'

        dynamic_contentuserenquiry += f'</div>'
        dynamic_contentuserenquiry += f'<div class="col-12" style="margin-top:40px;">'
        dynamic_contentuserenquiry += f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_contentuserenquiry += f'<table class="table table-bordered mb-0">'
        dynamic_contentuserenquiry += f'<thead>'
        dynamic_contentuserenquiry += f'<tr>'
        dynamic_contentuserenquiry += f'<th>Name</th>'
        dynamic_contentuserenquiry += f'<th>Contact</th>'
        dynamic_contentuserenquiry += f'<th>Enquiries</th>'
        
        dynamic_contentuserenquiry += f'</tr>'
        dynamic_contentuserenquiry += f'</thead>'
        dynamic_contentuserenquiry += f'<tbody>'

        dynamic_contentuserenquiry += f'</tbody>'
        dynamic_contentuserenquiry += f'</table>'

        dynamic_contentuserenquiry += f'</div>'

        web_page_urlshowuserenquiries = url_for('web_page_UserEnquiry')
        dynamic_contentuserenquiry += f'<center><a href="{web_page_urlshowuserenquiries}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'

        dynamic_contentuserenquiry += f'</div>'

        dynamic_contentuserenquiry += f'</div>'
        dynamic_contentuserenquiry += f'</div>'

        return dynamic_contentuserenquiry

@app.route('/web_page_UserEnquiry')
def web_page_UserEnquiry():
    
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:
        
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        # Initialize empty lists to store values
        
        usernames = []
        userenquirymail=[]
        userenquirynumbers=[]
        userqueries=[]
        message_received_durationfromuser=[]
        

        countuserenquiries = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT User_Name,UserEnquiryMail,UserEnquiryNumber,UserQuery,UserMessageDuration FROM userenquirytable')
            myresultuserenquirydetails = cursor.fetchall()
            
            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM userenquirytable')
            countuserenquiries = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for rowuserenquiry in myresultuserenquirydetails:
                usernames.append(rowuserenquiry[0])
                userenquirymail.append(rowuserenquiry[1])
                userenquirynumbers.append(rowuserenquiry[2])
                userqueries.append(rowuserenquiry[3])
                message_received_durationfromuser.append(rowuserenquiry[4])
             
            datauserenquirieslist = []

            # Iterate through the fetched records and generate HTML table rows
            for i in range(countuserenquiries):

                itemuserenquirieslist = {
                    "UserName":usernames[i],
                    "UserEnquiry_Mail":userenquirymail[i],
                    "UserEnquiry_Number":userenquirynumbers[i],
                    "UserQueries":userqueries[i],
                    "UserMessage_Received_Duration":message_received_durationfromuser[i]
                    
                }
                datauserenquirieslist.append(itemuserenquirieslist)
                
        except Exception as e:
            error_messageforuserenquiry = 'An error occurred: ' + str(e)
            flash(error_messageforuserenquiry, 'error')
            return render_template('UserEnquiries_list.html', error_messageforuserenquiry=error_messageforuserenquiry)


            

    return render_template('UserEnquiries_list.html', datauserenquirieslist=datauserenquirieslist)


        
@app.route('/web_pageremovelocation/<int:sno>',methods=['GET','POST'])
def web_pageremovelocation(sno):
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:  
        Selected_sno=sno

        db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }
        
        def get_db_connection():
            return mysql.connector.connect(**db_config)

        
        try:

            connection = get_db_connection()
            cursor = connection.cursor()

            update_query = """
                DELETE FROM map_attributes WHERE S_No=%s;
                """

            cursor.execute(update_query, (Selected_sno,))
            connection.commit()
            cursor.close()
            connection.close()

            # After Deletion of record, Show Product List
            db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)


            # Initialize empty lists to store values
            sno=[]
            location_name = []
            locationimagename=[]
            url = []
        

            countmapattributes = 0  # Initialize count outside of the try block

        
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT * FROM map_attributes')
            myresultmap = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM map_attributes')
            countmapattributes = cursor.fetchone()[0]  # Get the count value



            # Iterate through the result and append values to lists
            for rowm in myresultmap:
                sno.append(rowm[0])
                location_name.append(rowm[1])
                locationimagename.append(rowm[2])
                url.append(rowm[3])
                
            

        except Exception as e:
            error_messagelocationforadmin = 'An error occurred: ' + str(e)
            flash(error_messagelocationforadmin, 'error')
            return render_template('Location_list.html', error_messagelocationforadmin=error_messagelocationforadmin)


        datalocationlist=[]

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countmapattributes):

            itemlocationlist={
                
                "S_No":sno[i],
                "Location_name":location_name[i],
                "LocationImage_name":locationimagename[i],
                "URL":url[i],
                
            }
            datalocationlist.append(itemlocationlist)

        
    return render_template('Location_list.html',datalocationlist=datalocationlist)

@app.route('/add_location')
def add_location():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:
        return render_template('addlocation.html')

@app.route('/insert_location',methods=['GET','POST']) 
def insert_location():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:  
        if request.method == 'POST':
            
            Location_name = request.form['location_name']
            Map_URL = request.form['mapurl']

            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            try:
                # Moving Uploaded Picture(Cover Picture) to Particular Folder
                UPLOAD_FOLDER = "static/images/mapimages"
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

                ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'avif', 'gif'}

                file = request.files['image']

                def allowed_file(filename):
                    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                if 'image' not in request.files:
                    return "No file part"

                if file.filename == '':
                    return "No selected file"

                if not allowed_file(file.filename):
                    return "Invalid file format. Only JPG, JPEG, PNG, and GIF are allowed."

                # Get the original filename of the uploaded file inorder to save filename in the database
                originaluploadedimagefile_name = file.filename

                # Save the uploaded file to the destination folder
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)

                
                def get_db_connection():
                    return mysql.connector.connect(**db_config)

                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute('INSERT INTO map_attributes(Location_Name,Image_Name,URL) VALUES (%s,%s,%s)',
                            (Location_name, originaluploadedimagefile_name,Map_URL))
                connection.commit()
                cursor.close()
                connection.close()

            except Exception as e:
                error_messageforaddlocation = 'An error occurred: ' + str(e)
                flash(error_messageforaddlocation, 'error')
                return render_template('addlocation.html', error_messageforaddlocation=error_messageforaddlocation)


    return redirect(url_for('web_pageforlocation'))



    
@app.route('/web_pageauthvendorlist')
def web_pageauthvendorlist(): 

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:   
        
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        vendorids=[]
        vendornames = []
        vendorcategories=[]
        vendoraddress = []
        vendoremails=[]
        phones = []
        

        countauth = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT Vendor_ID,Vendor_Name,Vendor_Category,Vendor_Address,Vendor_EMAILID,Vendor_PhoneNumber FROM vendorattributes WHERE vendoractive_status=0 ')
            myresultauthvendor = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM vendorattributes WHERE vendoractive_status=0')
            countauth = cursor.fetchone()[0]  # Get the count value



            # Iterate through the result and append values to lists
            for row in myresultauthvendor:
                vendorids.append(row[0])
                vendornames.append(row[1])
                vendorcategories.append(row[2])
                vendoraddress.append(row[3])
                vendoremails.append(row[4])
                phones.append(row[5])
                

            

        except Exception as e:
            print(f"Error: {e}")

        dataauthvendorlist=[]

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countauth):

            itemauthvendorlist={
                
                "Vendor_id":vendorids[i],
                "Vendor_name":vendornames[i],
                "Vendor_category":vendorcategories[i],
                "Vendor_Address":vendoraddress[i],
                "Vendor_Email":vendoremails[i],
                "Phonenumber":phones[i],
                

            }
            dataauthvendorlist.append(itemauthvendorlist)

        
    return render_template('vendorlistauthentication.html',dataauthvendorlist=dataauthvendorlist)

@app.route('/web_pagevendorlist')
def web_pagevendorlist(): 

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:   
        
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        vendorids=[]
        vendornames = []
        vendorcategories=[]
        vendoraddress = []
        vendoremails=[]
        phones = []
        vendoractivestatus=[]

        count = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT Vendor_ID,Vendor_Name,Vendor_Category,Vendor_Address,Vendor_EMAILID,Vendor_PhoneNumber,vendoractive_status FROM vendorattributes')
            myresult = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM vendorattributes')
            count = cursor.fetchone()[0]  # Get the count value



            # Iterate through the result and append values to lists
            for row in myresult:
                vendorids.append(row[0])
                vendornames.append(row[1])
                vendorcategories.append(row[2])
                vendoraddress.append(row[3])
                vendoremails.append(row[4])
                phones.append(row[5])
                vendoractivestatus.append(row[6])

            

        except Exception as e:
            print(f"Error: {e}")

        datavendorlist=[]

        # Iterate through the fetched records and generate HTML table rows
        for i in range(count):

            itemvendorlist={
                
                "Vendor_id":vendorids[i],
                "Vendor_name":vendornames[i],
                "Vendor_category":vendorcategories[i],
                "Vendor_Address":vendoraddress[i],
                "Vendor_Email":vendoremails[i],
                "Phonenumber":phones[i],
                "Vendor_activestatus":vendoractivestatus[i]

            }
            datavendorlist.append(itemvendorlist)

        
    return render_template('vendorlist.html',datavendorlist=datavendorlist)       
        
      
   

@app.route('/web_pagevendorlistwithproduct/<int:Vendor_id>',methods=['GET','POST'])
def web_pagevendorlistwithproduct(Vendor_id):

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
        select_vendorid=Vendor_id
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }
        
        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        vendorid=""
        vendorname = ""
        vendorcategory=""
        vendoraddress=""
        vendorphone = ""
        vendoremailid=""
        

        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT Vendor_ID,Vendor_Name,Vendor_Category,Vendor_Address,Vendor_PhoneNumber,Vendor_EMAILID FROM vendorattributes WHERE Vendor_ID=%s',(select_vendorid,))
            myresultvendorlist = cursor.fetchall()

            

            # Iterate through the result and append values to lists
            for row in myresultvendorlist:
                vendorid=row[0]
                vendorname=row[1]
                vendorcategory=row[2]
                vendoraddress=row[3]
                vendorphone=row[4]
                vendoremailid=row[5]
                
            
            
            db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

        

            # Initialize empty lists to store values
            productids=[]
            productnames=[]
            productimagenames=[]
            productcategories=[]
            productdetails=[]
            prices=[]

            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Product_ID,Product_Name,ProductImage_Name,Product_category,Product_Details,Price FROM productattributes WHERE Vendor_ID=%s',(select_vendorid,))
            myresultproduct = cursor.fetchall()
    
            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM productattributes WHERE Vendor_ID=%s',(select_vendorid,))
            countproduct = cursor.fetchone()[0]  # Get the count value
            
            
            # Iterate through the result and append values to lists
            for row1 in myresultproduct:
                productids.append(row1[0])
                productnames.append(row1[1])
                productimagenames.append(row1[2])
                productcategories.append(row1[3])
                productdetails.append(row1[4])
                prices.append(row1[5])
                
        
        except Exception as e:
            print(f"Error: {e}")


        datasofparticularvendorproductdetail=[]
        # Iterate through the fetched records and generate HTML table rows
        for i in range(countproduct):
            itemparticularvendordetail={
                "Product_Id":productids[i],
                "Product_Name":productnames[i],
                "Product_Imagename":productimagenames[i],
                "Product_Categories":productcategories[i],
                "Product_Details":productdetails[i],
                "Prices":prices[i]
            }
            datasofparticularvendorproductdetail.append(itemparticularvendordetail)
                
               


            
        
    return render_template('particularvendorproductdetail.html',datasofparticularvendorproductdetail=datasofparticularvendorproductdetail,vendorid=vendorid,vendorname=vendorname,vendorcategory=vendorcategory,vendoraddress=vendoraddress,vendoremailid=vendoremailid,vendorphone=vendorphone)

@app.route('/web_pagevendorlistwithcourse/<int:Vendor_id>',methods=['GET','POST'])
def web_pagevendorlistwithcourse(Vendor_id):

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
        select_vendorid=Vendor_id
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }
        
        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        vendorid=""
        vendorname = ""
        vendorcategory=""
        vendoraddress=""
        vendorphone = ""
        vendoremailid=""
        

        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT Vendor_ID,Vendor_Name,Vendor_Category,Vendor_Address,Vendor_PhoneNumber,Vendor_EMAILID FROM vendorattributes WHERE Vendor_ID=%s',(select_vendorid,))
            myresultvendorlist = cursor.fetchall()

            

            # Iterate through the result and append values to lists
            for row in myresultvendorlist:
                vendorid=row[0]
                vendorname=row[1]
                vendorcategory=row[2]
                vendoraddress=row[3]
                vendorphone=row[4]
                vendoremailid=row[5]
                
            
            
            db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            # Initialize empty lists to store values
            courseids = []
            coursetuitionnames = []
            paymentfees = []
            coursetuitiondetails = []
            languages = []
            duration = []

            countparticularvendorcourselist = 0  # Initialize count outside of the try block

        
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Course_id,CourseTuitionName,PaymentFees,CourseTuition_Details,Languages,Duration FROM coursedetails WHERE Vendor_ID=%s',(select_vendorid,))
            myresultparticularvendorcoursedetails = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM coursedetails WHERE Vendor_ID=%s',(select_vendorid,))
            countparticularvendorcourselist = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for rowcl in myresultparticularvendorcoursedetails:
                courseids.append(rowcl[0])
                coursetuitionnames.append(rowcl[1])
                paymentfees.append(rowcl[2])
                coursetuitiondetails.append(rowcl[3])
                languages.append(rowcl[4])
                duration.append(rowcl[5])

        except Exception as e:
            error_messageforparticularcourse = 'An error occurred: ' + str(e)
            flash(error_messageforparticularcourse, 'error')
            return render_template('particularvendorcoursedetail.html', error_messageforparticularcourse=error_messageforparticularcourse)

        dataparticularvendorcourselist = []

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countparticularvendorcourselist):

            itemparticularvendorcourselist = {

                "Course_id": courseids[i],
                "CourseTuition_name": coursetuitionnames[i],
                "Payment_Fees": paymentfees[i],
                "CourseTuition_Details": coursetuitiondetails[i],
                "Language": languages[i],
                "Duration": duration[i]
            }
            dataparticularvendorcourselist.append(itemparticularvendorcourselist)
                
               


            
        
    return render_template('particularvendorcoursedetail.html',dataparticularvendorcourselist=dataparticularvendorcourselist,vendorid=vendorid,vendorname=vendorname,vendorcategory=vendorcategory,vendoraddress=vendoraddress,vendoremailid=vendoremailid,vendorphone=vendorphone)

@app.route('/web_pagevendorlistwithbusinessprofession/<int:Vendor_id>',methods=['GET','POST'])
def web_pagevendorlistwithbusinessprofession(Vendor_id):

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
        select_vendorid=Vendor_id
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }
        
        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        vendorid=""
        vendorname = ""
        vendorcategory=""
        vendoraddress=""
        vendorphone = ""
        vendoremailid=""
        

        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT Vendor_ID,Vendor_Name,Vendor_Category,Vendor_Address,Vendor_PhoneNumber,Vendor_EMAILID FROM vendorattributes WHERE Vendor_ID=%s',(select_vendorid,))
            myresultvendorlist = cursor.fetchall()

            

            # Iterate through the result and append values to lists
            for row in myresultvendorlist:
                vendorid=row[0]
                vendorname=row[1]
                vendorcategory=row[2]
                vendoraddress=row[3]
                vendorphone=row[4]
                vendoremailid=row[5]
                
            
            
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

            # Initialize empty lists to store values
            bpids = []
            businessprofession_names = []
            businessprofessionlogonames = []
            
            businessprofession_details=[]
            experience=[]
            enquiryfirstnumber=[]
            enquirysecondnumber=[]
            enquirymail=[]
            websitelink=[]
            address=[]
            Location_Link=[]

            countparticularvendorbusinessprofession = 0  # Initialize count outside of the try block

        
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT id,BusinessProfession_Name,BusinessProfession_LogoName,BusinessProfession_Details,Experience,EnquiryFirstNumber,EnquirySecondNumber,EnquiryMail,WebsiteLink,Address,Location_URL FROM businessprofessionattributes WHERE Vendor_ID=%s',(select_vendorid,))
            myresultparticularvendorbusinessprofessiondetails = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM businessprofessionattributes WHERE Vendor_ID=%s',(select_vendorid,))
            countparticularvendorbusinessprofession = cursor.fetchone()[0]  # Get the count value

            # Iterate through the result and append values to lists
            for rowbpdl in myresultparticularvendorbusinessprofessiondetails:
                bpids.append(rowbpdl[0])
                businessprofession_names.append(rowbpdl[1])
                businessprofessionlogonames.append(rowbpdl[2])
                
                businessprofession_details.append(rowbpdl[3])
                experience.append(rowbpdl[4])
                enquiryfirstnumber.append(rowbpdl[5])
                enquirysecondnumber.append(rowbpdl[6])
                enquirymail.append(rowbpdl[7])
                websitelink.append(rowbpdl[8])
                address.append(rowbpdl[9])
                Location_Link.append(rowbpdl[10])

        except Exception as e:
            error_messageforparticularvendorbp = 'An error occurred: ' + str(e)
            flash(error_messageforparticularvendorbp, 'error')
            return render_template('particularvendorbusinessprofessiondetail.html', error_messageforparticularvendorbp=error_messageforparticularvendorbp)

        dataparticularvendorbusinessprofessiondetail = []

        # Iterate through the fetched records and generate HTML table rows
        for i in range(countparticularvendorbusinessprofession):

            itemparticularvendorbusinessprofessionlist = {

                "B_P_id": bpids[i],
                "BusinessProfessionName":businessprofession_names[i],
                "BusinessProfessionLogoName":businessprofessionlogonames[i],
                
                "BusinessProfessionDetails":businessprofession_details[i],
                "Experience":experience[i],
                "Enquiry_Firstnumber":enquiryfirstnumber[i],
                "Enquiry_Secondnumber":enquirysecondnumber[i],
                "Enquiry_Mail":enquirymail[i],
                "Website_Link":websitelink[i],
                "Address":address[i],
                "LocationLink":Location_Link[i]
            }
            dataparticularvendorbusinessprofessiondetail.append(itemparticularvendorbusinessprofessionlist)
               


            
        
    return render_template('particularvendorbusinessprofessiondetail.html',dataparticularvendorbusinessprofessiondetail=dataparticularvendorbusinessprofessiondetail,vendorid=vendorid,vendorname=vendorname,vendorcategory=vendorcategory,vendoraddress=vendoraddress,vendoremailid=vendoremailid,vendorphone=vendorphone)



@app.route('/web_pagevendorauth/<int:Vendor_id>',methods=['GET','POST'])
def web_pagevendorauth(Vendor_id):

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
        select_id=Vendor_id
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        vendorids=""
        vendornames = ""
        vendorcategories=""
        
        phones = ""
        


        

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT Vendor_ID,Vendor_Name,Vendor_Category,Vendor_PhoneNumber FROM vendorattributes WHERE Vendor_ID=%s',(select_id,))
            myresult2 = cursor.fetchall()

            


            # Iterate through the result and append values to lists
            for row in myresult2:
                vendorids=row[0]
                vendornames=row[1]
                vendorcategories=row[2]
                phones=row[3]
                

            

        except Exception as e:
            print(f"Error: {e}")

        # Initialize an empty string to store the dynamic HTML content
        dynamic_content9 = ""
            
        dynamic_content9 +=f"<tr>\n"
        dynamic_content9 +=f"<td>{vendorids}</td>\n"
        dynamic_content9 +=f"<td>{vendornames}</td>\n"
        dynamic_content9 +=f"<td>{vendorcategories}</td>\n"
        dynamic_content9 +=f"<td>{phones}</td>\n"
        dynamic_content9 +=f"<td>\n"
        
        web_page_url = url_for('accept_request',passingvendorsid1=vendorids)
        dynamic_content9 += f'<a href="{web_page_url}" class="btn btn-info" value="{vendorids}" >Accept</a>\n'
        web_page_url_1 = url_for('decline_request',passingvendorsid_1=vendorids)
        dynamic_content9 += f'<a href="{web_page_url_1}" class="btn btn-info" value="{vendorids}" >Decline</a>\n'
        

        dynamic_content9 +=f"</td>\n"
        dynamic_content9 +=f"</tr>\n"
        
        
        # Complete the HTML structure
        dynamic_content9 = f"""
        
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
            <div class="container-fluid w-100" >
                <div class="row">
                    <div class="col-12">
                        <div class="w-100">
                            <div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;margin-top:3px;">
                                <h6 class="text-white text-capitalize ps-3">List of Vendors</h6>
                            </div>
                        </div>
                    
                    <div class="col-12" style="margin-top:7px;">
                        
                        <div class="table-responsive border border-3 p-3 bg-white">
                            <table id="table_id" class="table table-bordered mb-0">
                                <thead>
                                    <tr>
                                        <th>Vendor-ID</th>
                                        <th>Name</th>
                                        <th>Vendor Category</th>
                                        <th>Phone-No</th>
                                        <th>Authentication</th>
                                        
                                    </tr>
                                </thead>
                                <tbody>
                                    {dynamic_content9}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
            
            
        """
    return dynamic_content9


    


    
@app.route('/accept_request<int:passingvendorsid1>',methods=['GET','POST'])
def accept_request(passingvendorsid1):
        
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
    
        v_id = passingvendorsid1
        
    
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="communityproject"
        )
        # Function to fetch data from the database
        try:
            mycursor = mydb.cursor()
            
            # Update the vendoractivestatus for the specified vendor ID
            update_query = "UPDATE vendorattributes SET vendoractive_status = 1 WHERE Vendor_ID = %s"
            mycursor.execute(update_query, (v_id,))
            mydb.commit()

            
        
            
            
        except Exception as e:
            print(f"Error: {e}")
            
        finally:

            #Retrieving emailid from database inorder to send Authentication email
            mycursor.execute("SELECT Vendor_EMAILID,Vendor_Password from vendorattributes WHERE Vendor_ID=%s",(v_id,)) 
            dataattributes=mycursor.fetchall()

            emailidfromdb=""
            vendorpasswordfromdb=""

            for email, vpassword in dataattributes:
                emailidfromdb=email
                vendorpasswordfromdb=vpassword

            #EMAIL CONFIGURATION
            smtp_server="smtp.gmail.com"
            smtp_port=587 # Port number may vary depending on the SMTP server
            sender_email="aasva.koodalarasan@gmail.com"
            password="mozs zzry opgs nfjc"     #password was generated in GMAIL->MANAGE ACCOUNT->SECURITY-> 2 STEP..
                                            #....VERIFICATION and ENABLE it AND THEN AGAIN GO TO 2 STEP VERIFICATION then in there to App Password...
                                            #...type smtp in App Name and to click generate password.....
                                            #....don't app name which is saved and showing there.

            # Recipient email address stored in a variable
            recipient_email =emailidfromdb
            

            # Create the email message
            subject="Authentication Message"
            message=f"Hey Respected,\n Thank You So Much for desired to join with Our Community\n.Now itself Your Authenticated Member of Our Community and Here is Your Authenticated Account,\n  Email:{emailidfromdb}\n Password:{vendorpasswordfromdb}\nAgain Thank You a lot and Blessed With Happiness from God"

            msg=MIMEMultipart()
            msg['From']=sender_email
            msg['To']=recipient_email
            msg['Subject']=subject

            msg.attach(MIMEText(message,'plain'))

            #Establish an SMTP connection and send the email
            try:
                server=smtplib.SMTP(smtp_server,smtp_port)
                server.starttls() # Use TLS encryption
                server.login(sender_email,password)
                server.sendmail(sender_email,recipient_email,msg.as_string())
                print('Email sent successfully')
            except Exception as e:
                print(f'An error occurred: {e}')
            return redirect(url_for('web_pagevendorlist'))
@app.route('/decline_request<int:passingvendorsid_1>',methods=['GET','POST'])
def decline_request(passingvendorsid_1):
    
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
        v_id_1 = passingvendorsid_1
        
    
        mydb = mysql.connector.connect(
           host="localhost",
           user="root",
           password="",
           database="communityproject"
        )
        # Function to fetch data from the database
        try:
            mycursor = mydb.cursor()

            #Retrieving emailid from database inorder to send Authentication email
            mycursor.execute("SELECT Vendor_EMAILID from vendorattributes WHERE Vendor_ID=%s",(v_id_1,)) 
            dataattributes01=mycursor.fetchone()

            mycursor.execute("DELETE from vendorattributes WHERE Vendor_ID=%s",(v_id_1,)) 
            mydb.commit()

            emailidfromdbtodecline=""
            

            for email01 in dataattributes01:
                emailidfromdbtodecline=email01
                

            
            
        except Exception as e:
            print(f"Error: {e}")
            
        finally:

            
            #EMAIL CONFIGURATION
            smtp_server="smtp.gmail.com"
            smtp_port=587 # Port number may vary depending on the SMTP server
            sender_email="aasva.koodalarasan@gmail.com"
            password="mozs zzry opgs nfjc"     #password was generated in GMAIL->MANAGE ACCOUNT->SECURITY-> 2 STEP..
                                               #....VERIFICATION and ENABLE it AND THEN AGAIN GO TO 2 STEP VERIFICATION then in there to App Password...
                                               #...type smtp in App Name and to click generate password.....
                                               #....don't app name which is saved and showing there.

            # Recipient email address stored in a variable
            recipient_email =emailidfromdbtodecline
             

            # Create the email message
            subject="Authentication Message"
            message=f"Hey Respected,\n Thank You So Much for desired to join with Our Community\n.But Unluckily you'are not Authenticated Person of Our Beloved Community\nSorry for Inconvenience and Thanks a lot and Blessed With Happiness from God"

            msg=MIMEMultipart()
            msg['From']=sender_email
            msg['To']=recipient_email
            msg['Subject']=subject

            msg.attach(MIMEText(message,'plain'))

            #Establish an SMTP connection and send the email
            try:
                server=smtplib.SMTP(smtp_server,smtp_port)
                server.starttls() # Use TLS encryption
                server.login(sender_email,password)
                server.sendmail(sender_email,recipient_email,msg.as_string())
                print('Email sent successfully')
            except Exception as e:
                print(f'An error occurred: {e}')
            return redirect(url_for('web_pagevendorlist'))
            
    









@app.route('/get_new_content4', methods=['GET'])
def get_new_content4():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
        dynamic_content4 = ""

        dynamic_content4 +=f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_content4 +=f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
        
        dynamic_content4 +=f'<div class="container-fluid w-100" >'
        dynamic_content4 +=f'<div class="row">'
        dynamic_content4 +=f'<div class="col-12">'
        dynamic_content4 +=f'<div class="w-100">'
        dynamic_content4 +=f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;margin-top:-350px;">'
        dynamic_content4 +=f' <h6 class="text-white text-capitalize ps-3">Product List</h6>'
        dynamic_content4 +=f'</div>'

        dynamic_content4 +=f'</div>'
        dynamic_content4 +=f'<div class="col-12" style="margin-top:40px;">'
        dynamic_content4 +=f'<div class="table-responsive border border-3 p-3 bg-white">'

        dynamic_content4 +=f'<table class="table table-bordered mb-0">'
        dynamic_content4 +=f'<thead>'
        dynamic_content4 +=f'<tr>'
        dynamic_content4 +=f'<th>Product ID</th>'
        dynamic_content4 +=f'<th>Product Name</th>'
        dynamic_content4 +=f'<th>Product Images</th>'
        dynamic_content4 +=f'<th>Product Category</th>'
        dynamic_content4 +=f'<th>Product Details</th>'
        dynamic_content4 +=f'<th>Price</th>'
                        
        dynamic_content4 +=f'</tr>'
        dynamic_content4 +=f'</thead>'
        dynamic_content4 +=f'<tbody>'
                        
    
        dynamic_content4 +=f'</tbody>'
        dynamic_content4 +=f'</table>'
        dynamic_content4 +=f'</div>'
        web_page_urlshowwholeproductlist = url_for('web_pagewholeproductlist')
        dynamic_content4 +=f'<center><a href="{web_page_urlshowwholeproductlist}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'
    
        dynamic_content4 +=f'</div>'
        dynamic_content4 +=f'</div>'
        dynamic_content4 +=f'</div>'

    return dynamic_content4


@app.route('/web_pagewholeproductlist')
def web_pagewholeproductlist():

    
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
    
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        productids=[]
        vendorids=[]
        productnames=[]
        productimagenames=[]
        productcategories=[]
        productdetails=[]
        prices=[]

        count1 = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Product_ID,Vendor_ID,Product_Name,ProductImage_Name,Product_category,Product_Details,Price FROM productattributes')
            myresult1 = cursor.fetchall()
    
            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM productattributes')
            count1 = cursor.fetchone()[0]  # Get the count value
            
            
            # Iterate through the result and append values to lists
            for row1 in myresult1:
                productids.append(row1[0])
                vendorids.append(row1[1])
                productnames.append(row1[2])
                productimagenames.append(row1[3])
                productcategories.append(row1[4])
                productdetails.append(row1[5])
                prices.append(row1[6])

            
        except Exception as e:
            print(f"Error: {e}")

        datainwholeproductlist=[]

        # Iterate through the fetched records and generate HTML table rows
        for i in range(count1):

            itemsinwholeproductlist={
            
                "Product_IDs":productids[i],
                "Product_Names":productnames[i],
                "ProductImage_Names":productimagenames[i],
                "Product_categories":productcategories[i],
                "Product_details":productdetails[i],
                "Prices":prices[i],
                "Vendor_IDs":vendorids[i]
            }
            datainwholeproductlist.append(itemsinwholeproductlist)
                    
            
    return render_template('wholeproductlist.html',datainwholeproductlist=datainwholeproductlist)

@app.route('/web_pagevendorlistwiththeirproduct',methods=['GET','POST'])
def web_pagevendorlistwiththeirproduct():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
          
    
        select_vendorid=request.args.get('vendor_id')
        select_productid = request.args.get('product_id')
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }
        
        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        vendorid=""
        vendorname = ""
        vendorcategory=""
        vendoraddress=""
        vendorphone = ""
        vendoremailid=""
        

        
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT Vendor_ID,Vendor_Name,Vendor_Category,Vendor_Address,Vendor_PhoneNumber,Vendor_EMAILID FROM vendorattributes WHERE Vendor_ID=%s',(select_vendorid,))
            myresultvendorlist = cursor.fetchall()

            

            # Iterate through the result and append values to lists
            for row in myresultvendorlist:
                vendorid=row[0]
                vendorname=row[1]
                vendorcategory=row[2]
                vendoraddress=row[3]
                vendorphone=row[4]
                vendoremailid=row[5]
                
            
            
            db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
            }

            def get_db_connection():
                return mysql.connector.connect(**db_config)

        

            # Initialize empty lists to store values
            productids=[]
            productnames=[]
            productimagenames=[]
            productcategories=[]
            productdetails=[]
            prices=[]

            connection = get_db_connection()
            cursor = connection.cursor()

            #  SQL query to fetch  records
            cursor.execute('SELECT Product_ID,Product_Name,ProductImage_Name,Product_category,Product_Details,Price FROM productattributes WHERE Product_ID=%s',(select_productid,))
            myresultproduct = cursor.fetchall()
    
            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM productattributes WHERE Product_ID=%s',(select_productid,))
            countproduct = cursor.fetchone()[0]  # Get the count value
            
            
            # Iterate through the result and append values to lists
            for row1 in myresultproduct:
                productids.append(row1[0])
                productnames.append(row1[1])
                productimagenames.append(row1[2])
                productcategories.append(row1[3])
                productdetails.append(row1[4])
                prices.append(row1[5])
                
        
        except Exception as e:
            print(f"Error: {e}")


        datasofvendorparticularproductdetail=[]
        # Iterate through the fetched records and generate HTML table rows
        for i in range(countproduct):
            itemvendorparticulardetail={
                "Product_Id":productids[i],
                "Product_Name":productnames[i],
                "Product_Imagename":productimagenames[i],
                "Product_Categories":productcategories[i],
                "Product_Details":productdetails[i],
                "Prices":prices[i]
            }
            datasofvendorparticularproductdetail.append(itemvendorparticulardetail)
                
               


            
        
    return render_template('vendordetailparticularproduct.html',datasofvendorparticularproductdetail=datasofvendorparticularproductdetail,vendorid=vendorid,vendorname=vendorname,vendorcategory=vendorcategory,vendoraddress=vendoraddress,vendoremailid=vendoremailid,vendorphone=vendorphone)


@app.route('/get_new_contentuserlist', methods=['GET', 'POST'])
def get_new_contentuserlist():

    
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else: 
    
        dynamic_contentuserindex = ""


        dynamic_contentuserindex +=f'<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
        dynamic_contentuserindex +=f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>'
        dynamic_contentuserindex +=f'<div class="container-fluid w-100" >'
        dynamic_contentuserindex +=f'<div class="row">'
        dynamic_contentuserindex +=f'<div class="col-12">'
        dynamic_contentuserindex +=f'<div class="w-100">'
        dynamic_contentuserindex +=f'<div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;margin-top:-328px;">'
        dynamic_contentuserindex +=f'<h6 class="text-white text-capitalize ps-3">List of Users</h6>'
        dynamic_contentuserindex +=f'</div>'
        dynamic_contentuserindex +=f'</div>'
                    
        dynamic_contentuserindex +=f'<div class="col-12" style="margin-top:12px;">'
                        
        dynamic_contentuserindex +=f'<div class="table-responsive border border-3 p-3 bg-white">'
        dynamic_contentuserindex +=f'<table id="table_id" class="table table-bordered mb-0">'
        dynamic_contentuserindex +=f'<thead>'
        dynamic_contentuserindex +=f'<tr>'
        dynamic_contentuserindex +=f'<th>User-ID</th>'
        dynamic_contentuserindex +=f'<th>Name</th>'
        dynamic_contentuserindex +=f'<th>Address</th>'
        dynamic_contentuserindex +=f'<th>Phone-No</th>'
        dynamic_contentuserindex +=f'<th>Email_ID</th>'
        dynamic_contentuserindex +=f'<th>Authentication</th>'
        dynamic_contentuserindex +=f'<th>Details</th>'
        dynamic_contentuserindex +=f'</tr>'
        dynamic_contentuserindex +=f'</thead>'
        dynamic_contentuserindex +=f'<tbody>'
                                    
        dynamic_contentuserindex +=f'</tbody>'
        dynamic_contentuserindex +=f'</table>'
        dynamic_contentuserindex +=f'</div>'
        web_page_urlshowuserlist = url_for('web_pageuserlist')
        dynamic_contentuserindex+=f'<center><a href="{web_page_urlshowuserlist}" class="btn btn-success" style="margin-top:72px;">Click Here!</a></center>'
    
        dynamic_contentuserindex +=f'</div>'
        dynamic_contentuserindex +=f'</div>'
        dynamic_contentuserindex +=f'</div>'
        dynamic_contentuserindex +=f'</div>'
            
            
    
    return dynamic_contentuserindex

@app.route('/web_pageuserlist')
def web_pageuserlist():

    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        userids=[]
        usernames = []
        useraddress=[]
        userphones = []
        useremailids=[]
        useractive_status=[]

        count2 = 0  # Initialize count outside of the try block

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT User_Id,User_Name,User_Address,User_PhoneNumber,User_EMAILID,active_status FROM userattributes')
            myresult4 = cursor.fetchall()

            # Query the database to get the count of records
            cursor.execute('SELECT COUNT(*) FROM userattributes')
            count2 = cursor.fetchone()[0]  # Get the count value



            # Iterate through the result and append values to lists
            for row in myresult4:
                userids.append(row[0])
                usernames.append(row[1])
                useraddress.append(row[2])
                userphones.append(row[3])
                useremailids.append(row[4])
                useractive_status.append(row[5])

            

        except Exception as e:
            print(f"Error: {e}")

        datauserlist=[]
        # Iterate through the fetched records and generate HTML table rows
        for i in range(count2):

            itemsinuserlist={
                "user_id":userids[i],
                "user_name":usernames[i],
                "user_address":useraddress[i],
                "user_phone":userphones[i],
                "user_emailid":useremailids[i],
                "useractivestatus":useractive_status[i]

            }
            datauserlist.append(itemsinuserlist)
                
    return render_template('userlist.html',datauserlist=datauserlist)




@app.route('/web_pageuserauth/<int:user_id>',methods=['GET','POST'])
def web_pageuserauth(user_id):
    
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:
        select_userid=user_id
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "communityproject"
        }

        def get_db_connection():
            return mysql.connector.connect(**db_config)

        

        # Initialize empty lists to store values
        userids=""
        usernames = ""
        useraddress=""
        userphones = ""
        useremailids=""
        useractivestatus1=""

        

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # your SQL query to fetch the records
            cursor.execute('SELECT User_ID,User_Name,User_Address,User_PhoneNumber,User_EMAILID,active_status FROM userattributes WHERE User_ID=%s',(select_userid,))
            myresult5 = cursor.fetchall()

            


            # Iterate through the result and append values to lists
            for row in myresult5:
                userids=row[0]
                usernames=row[1]
                useraddress=row[2]
                useremailids=row[3]
                userphones=row[4]
                useractivestatus1=row[5]

            

        except Exception as e:
            print(f"Error: {e}")

        # Initialize an empty string to store the dynamic HTML content
        dynamic_content12 = ""
            
        dynamic_content12 +=f"<tr>\n"
        dynamic_content12 +=f"<td>{userids}</td>\n"
        dynamic_content12 +=f"<td>{usernames}</td>\n"
        dynamic_content12 +=f"<td>{useraddress}</td>\n"
        dynamic_content12 +=f"<td>{useremailids}</td>\n"
        dynamic_content12 +=f"<td>{userphones}</td>\n"
        dynamic_content12 +=f"<td>\n"
        if useractivestatus1 == 0:
            web_page_url2 = url_for('accept_userrequest',passinguserid_1=userids)
            dynamic_content12 += f'<a href="{web_page_url2}" class="btn btn-info" value="{userids}" >Accept</a>\n'
            web_page_url02 = url_for('decline_userrequest',passingusersids1=userids)
            dynamic_content12 += f'<a href="{web_page_url02}" class="btn btn-info" value="{userids}" >Decline</a>\n'
        else:
            dynamic_content12 += f'<a href="#" class="btn btn-info" value="{userids}" id="more">More</a>'

        dynamic_content12 +=f"</td>\n"
        dynamic_content12 +=f"</tr>\n"
        
        
        # Complete the HTML structure
        dynamic_content12 = f"""
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
            <div class="container-fluid w-100" >
                <div class="row">
                    <div class="col-12">
                        <div class="w-100">
                            <div class=" shadow-primary border-radius-lg pt-4 pb-3" style="background-color: #4070f4;margin-top:3px;">
                                <h6 class="text-white text-capitalize ps-3">Authenticate Users</h6>
                            </div>
                        </div>
                    
                    <div class="col-12" style="margin-top:7px;">
                        
                        <div class="table-responsive border border-3 p-3 bg-white">
                            <table id="table_id" class="table table-bordered mb-0">
                                <thead>
                                    <tr>
                                        <th>User-ID</th>
                                        <th>Name</th>
                                        <th>Address</th>
                                        <th>Phone-No</th>
                                        <th>EMAIL_ID</th>
                                        <th>Authentication</th>
                                        <th>Details</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {dynamic_content12}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
            
            
        """
    return dynamic_content12
            

@app.route('/accept_userrequest/<int:passinguserid_1>',methods=['GET','POST'])
def accept_userrequest(passinguserid_1):
    
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:
        
        users_id =passinguserid_1
        
    
        mydb = mysql.connector.connect(
           host="localhost",
           user="root",
           password="",
           database="communityproject"
        )
        # Function to fetch data from the database
        try:
            mycursor = mydb.cursor()
            
            # Update the vendoractivestatus for the specified vendor ID
            update_query1 = "UPDATE userattributes SET active_status = 1 WHERE User_ID = %s"
            mycursor.execute(update_query1, (users_id,))
            mydb.commit()

            
        
            
            
        except Exception as e:
            print(f"Error: {e}")
            
        finally:

            #Retrieving emailid from database inorder to send Authentication email
            mycursor.execute("SELECT User_EMAILID,User_Password from userattributes WHERE User_ID=%s",(users_id,)) 
            userdataattributes=mycursor.fetchall()

            useremailidfromdb=""
            userpasswordfromdb=""

            for usersemail, upassword in userdataattributes:
                useremailidfromdb=usersemail
                userpasswordfromdb=upassword

            #EMAIL CONFIGURATION
            smtp_server="smtp.gmail.com"
            smtp_port=587 # Port number may vary depending on the SMTP server
            sender_email="aasva.koodalarasan@gmail.com"
            password="mozs zzry opgs nfjc"     #password was generated in GMAIL->MANAGE ACCOUNT->SECURITY-> 2 STEP..
                                               #....VERIFICATION and Enable it AND THEN AGAIN GO TO 2 STEP VERIFICATION then in there to App Password...
                                               #...type smtp in App Name and to click generate password.....
                                               #....don't app name which is saved and showing there.

            # Recipient email address stored in a variable
            recipient_email =useremailidfromdb
             

            # Create the email message
            subject="Authentication Message"
            message=f"Hey Respected,\n Thank You So Much for desired to join with Our Community\n.Now itself Your Authenticated Member of Our Community and Here is Your Authenticated Account,\n  Email:{useremailidfromdb}\n Password:{userpasswordfromdb}\nAgain Thank You a lot and Blessed With Happiness from God"

            msg=MIMEMultipart()
            msg['From']=sender_email
            msg['To']=recipient_email
            msg['Subject']=subject

            msg.attach(MIMEText(message,'plain'))

            #Establish an SMTP connection and send the email
            try:
                server=smtplib.SMTP(smtp_server,smtp_port)
                server.starttls() # Use TLS encryption
                server.login(sender_email,password)
                server.sendmail(sender_email,recipient_email,msg.as_string())
                print('Email sent successfully')
            except Exception as e:
                print(f'An error occurred: {e}')
            return redirect(url_for('web_pageuserlist'))

@app.route('/decline_userrequest<int:passingusersids1>',methods=['GET','POST'])
def decline_userrequest(passingusersids1):
    
    if not session.get('adminlogged_in') and request.endpoint not in ('login', 'static'):
        return render_template('adminlogin.html')

    else:
        v_id_01 = passingusersids1
        
    
        mydb = mysql.connector.connect(
           host="localhost",
           user="root",
           password="",
           database="communityproject"
        )
        # Function to fetch data from the database
        try:
            mycursor = mydb.cursor()

            #Retrieving emailid from database inorder to send Authentication email
            mycursor.execute("SELECT User_EMAILID from userattributes WHERE User_ID=%s",(v_id_01,)) 
            dataattributes001=mycursor.fetchone()

            useremailidfromdbtodecline=""
            

            for email001 in dataattributes001:
                useremailidfromdbtodecline=email001

            # Update the vendoractivestatus for the specified vendor ID
            update_query001 = "DELETE FROM userattributes WHERE User_ID = %s"
            mycursor.execute(update_query001, (v_id_01,))
            mydb.commit()
                

            
            
        except Exception as e:
            print(f"Error: {e}")
            
        finally:

            
            #EMAIL CONFIGURATION
            smtp_server="smtp.gmail.com"
            smtp_port=587 # Port number may vary depending on the SMTP server
            sender_email="aasva.koodalarasan@gmail.com"
            password="mozs zzry opgs nfjc"     #password was generated in GMAIL->MANAGE ACCOUNT->SECURITY-> 2 STEP..
                                               #....VERIFICATION and ENABLE it AND THEN AGAIN GO TO 2 STEP VERIFICATION then in there to App Password...
                                               #...type smtp in App Name and to click generate password.....
                                               #....don't app name which is saved and showing there.

            # Recipient email address stored in a variable
            recipient_email =useremailidfromdbtodecline
             

            # Create the email message
            subject="Authentication Message"
            message=f"Hey Respected,\n Thank You So Much for desired to join with Our Community\n.But Unluckily you'are not Authenticated Person of Our Beloved Community\nSorry for Inconvenience and Thanks a lot and Blessed With Happiness from God"

            msg=MIMEMultipart()
            msg['From']=sender_email
            msg['To']=recipient_email
            msg['Subject']=subject

            msg.attach(MIMEText(message,'plain'))

            #Establish an SMTP connection and send the email
            try:
                server=smtplib.SMTP(smtp_server,smtp_port)
                server.starttls() # Use TLS encryption
                server.login(sender_email,password)
                server.sendmail(sender_email,recipient_email,msg.as_string())
                print('Email sent successfully')
            except Exception as e:
                print(f'An error occurred: {e}')
            return redirect(url_for('web_pageuserlist'))





if __name__ == '__main__':
    app.run()
