from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import joblib 
from django.http import HttpResponse


# Home Page View
def index_view(request):
    return render(request, 'index.html')

# About Page View
def about_view(request):
    return render(request, 'about.html')

import mysql.connector as sql
from django.contrib import messages
from django.shortcuts import render, redirect

# Signup View
import mysql.connector as sql
from django.contrib import messages
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == "POST":
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        contactnumber = request.POST.get('contactnumber')  # New field
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = {}

        # Validate password match
        if password != confirm_password:
            errors['password_error'] = "Passwords do not match."
            return render(request, 'signup.html', {'errors': errors})

        try:
            # Connect to MySQL database
            conn = sql.connect(
                host="localhost",
                user="root",
                password="Abhi@15112000",
                database="humanstress"
            )
            cursor = conn.cursor()

            # Check if username or email already exists
            cursor.execute("SELECT COUNT(*) FROM signup WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone()[0] > 0:
                errors['duplicate_error'] = "Username or email already exists."
                return render(request, 'signup.html', {'errors': errors})

            # Insert user into the database
            cursor.execute(
                "INSERT INTO signup (username, email, contactnumber, password, cpassword) VALUES (%s, %s, %s, %s, %s)",
                (username, email, contactnumber, password, confirm_password)
            )
            conn.commit()
            messages.success(request, "Account created successfully!")
            return redirect('login')

        except sql.Error as e:
            messages.error(request, f"Database error: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render(request, 'signup.html')


# Login View
def login_view(request):
    if request.method == "POST":
        # Get login form data
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Connect to MySQL database
            conn = sql.connect(
                host="localhost",
                user="root",
                password="Abhi@15112000",
                database="humanstress"
            )
            cursor = conn.cursor()

            # Query for user authentication
            cursor.execute("SELECT * FROM signup WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                # Successful login
                # Insert user login details into the 'user_logins' table
                cursor.execute(
                    "INSERT INTO user_logins (username, password, login_time) VALUES (%s, %s, %s)",
                    (username, password, datetime.now())
                )
                conn.commit()

                # Django's authenticate and login method
                user_obj = authenticate(request, username=username, password=password)
                if user_obj is not None:
                    login(request, user_obj)

                messages.success(request, "Successfully logged in!")
                return redirect('dataentry')  # Redirect to data entry page after successful login
            else:
                # Invalid credentials
                messages.error(request, "Invalid username or password.")
                return render(request, 'login.html')

        except sql.Error as e:
            messages.error(request, f"Database error: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render(request, 'login.html')


# Data Entry View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import mysql.connector as sql
from datetime import datetime

@login_required
def data_entry_view(request):
    if request.method == "POST":
        try:
            # Fetch data from the form
            snoring_rate = float(request.POST.get("snoring_rate", 0))
            respiratory_rate = float(request.POST.get("respiratory_rate", 0))
            body_temperature = float(request.POST.get("body_temperature", 0))
            limb_movement = float(request.POST.get("limb_movement", 0))
            blood_oxygen = float(request.POST.get("blood_oxygen", 0))
            eye_movements = float(request.POST.get("eye_movements", 0))
            sleep_hours = float(request.POST.get("sleep_hours", 0))
            heart_rate = float(request.POST.get("heart_rate", 0))

            # Determine stress status
            is_stressed = (
                snoring_rate < 46 or snoring_rate > 98 or
                respiratory_rate < 15 or respiratory_rate > 30 or
                body_temperature < 86 or body_temperature > 98 or
                limb_movement < 5 or limb_movement > 18 or
                blood_oxygen < 84 or blood_oxygen > 96 or
                eye_movements < 60 or eye_movements > 105 or
                sleep_hours < 0 or sleep_hours > 9 or
                heart_rate < 52 or heart_rate > 84
            )
            # Convert boolean to string
            is_stressed = "Stressed" if is_stressed else "Not Stressed"

            # Connect to MySQL database
            conn = sql.connect(
                host="localhost",
                user="root",
                password="Abhi@15112000",
                database="humanstress"
            )
            cursor = conn.cursor()

            # Insert data into the database
            query = """
                INSERT INTO health_data (snoring_rate, respiratory_rate, body_temperature, 
                                         limb_movement, blood_oxygen, eye_movements, sleep_hours, 
                                         heart_rate, is_stressed)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                snoring_rate, respiratory_rate, body_temperature, 
                limb_movement, blood_oxygen, eye_movements, sleep_hours, 
                heart_rate, is_stressed
            )
            cursor.execute(query, values)
            conn.commit()

            # Debugging Logs
            print(f"Query: {query}")
            print(f"Values: {values}")

            # Show success message
            messages.success(request, "Health data submitted successfully!")
            return redirect("result")

        except sql.Error as e:
            messages.error(request, f"Database error: {e}")
            print(f"Database error: {e}")  # Debugging
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render(request, "dataentry.html")


# Result View 

@login_required
def result(request):
    try:
        # Connect to MySQL database
        conn = sql.connect(
            host="localhost",
            user="root",
            password="Abhi@15112000",
            database="humanstress"
        )
        cursor = conn.cursor(dictionary=True)

        # Fetch the most recent entry
        query = "SELECT is_stressed FROM health_data ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()

        # Pass the result to the template
        context = {"is_stressed": result["is_stressed"]} if result else {"is_stressed": "Not Stressed"}

    except sql.Error as e:
        messages.error(request, f"Database error: {e}")
        context = {"is_stressed": "Not Stressed"}
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render(request, 'result.html', context)







