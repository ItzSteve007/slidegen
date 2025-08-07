from django.shortcuts import render, redirect
import random
import smtplib
from email.mime.text import MIMEText
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth import login

def otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        action = request.POST.get('action')  # login or signup

        if not email or not password or action not in ['login', 'signup']:
            return render(request, 'error.html', {'message': 'Invalid form submission'})

        if action == 'signup':
            # If user already exists, stop and show error
            if User.objects.filter(username=email).exists():
                return render(request, 'login.html', {
                    'signup_error': 'Account already exists. Try logging in.',
                    'email': email
                })

        elif action == 'login':
            # Check if credentials are correct before sending OTP
            user = authenticate(request, username=email, password=password)
            if user is None:
                return render(request, 'login.html', {
                    'login_error': 'Invalid email or password.',
                    'email': email
                })

        # Proceed with sending OTP
        otp = random.randint(100000, 999999)

        # Send OTP Email
        subject = 'SlideGen OTP Code'
        body = f'Your OTP code for logging in SlideGen is: {otp}'
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = email

        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, [email], msg.as_string())
            server.quit()
        except Exception as e:
            return render(request, 'error.html', {'message': f'Error sending email: {str(e)}'})

        # Store details in session
        request.session['email'] = email
        request.session['password'] = password
        request.session['action'] = action
        request.session['otp'] = str(otp)

        return render(request, 'otp.html', {'email': email, 'page': 'otp'})

    return render(request, 'error.html', {'message': 'Invalid request method'})

    
def verify_otp(request):
    if request.method == 'POST':
        otp_entered = ''.join([
            request.POST.get('d1', ''),
            request.POST.get('d2', ''),
            request.POST.get('d3', ''),
            request.POST.get('d4', ''),
            request.POST.get('d5', ''),
            request.POST.get('d6', ''),
        ])

        otp_session = request.session.get('otp')
        email = request.session.get('email')
        password = request.session.get('password')
        action = request.session.get('action')

        if otp_entered == otp_session:
            if action == 'signup':
                if User.objects.filter(username=email).exists():
                    return render(request, 'otp.html', {
                        'email': email,
                        'error': 'Account already exists. Try logging in.',
                        'page': 'otp'
                    })
                user = User.objects.create_user(username=email, email=email, password=password)
                login(request, user)
                return redirect('dashboard')

            elif action == 'login':
                user = authenticate(request, username=email, password=password)
                if user:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'otp.html', {
                        'email': email,
                        'error': 'Login failed. Incorrect credentials.',
                        'page': 'otp'
                    })
        else:
            return render(request, 'otp.html', {
                'email': email,
                'error': 'Invalid OTP. Please try again.',
                'page': 'otp'
            })

    return render(request, 'error.html', {'message': 'Invalid request method'})
