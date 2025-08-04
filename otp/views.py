from django.shortcuts import render
import random
import smtplib
from email.mime.text import MIMEText
from django.conf import settings

# Create your views here.
def otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        otp = random.randint(100000, 999999)

                # Prepare email
        subject = 'SlideGen OTP Code'
        body = f'Your OTP code for logging in Slidegen is: {otp}'
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = email

        # Send email using SMTP
        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, [email], msg.as_string())
            server.quit()
        except Exception as e:
            return render(request, 'error.html', {'message': f'Error sending email: {str(e)}'})

        # Store the OTP for verification (e.g., in session)
        request.session['otp'] = str(otp)
        request.session['email'] = email

        return render(request, 'otp.html', {'email': email, 'otp': otp, 'page': 'otp'})
    else:
        return render(request, 'error.html', {'page' : 'error'})
    
def verify_otp(request):
    if request.method == 'POST':
        # Get the 6 individual digits and join them
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

        if otp_entered == otp_session:
            return render(request, 'success.html', {'email': email})
        else:
            return render(request, 'otp.html', {
                'email': email,
                'error': 'Invalid OTP. Please try again.',
                'page': 'otp'
            })

    return render(request, 'error.html', {'message': 'Invalid request method'})
