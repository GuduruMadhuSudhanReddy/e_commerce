from django.shortcuts import render,redirect,reverse,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.conf import settings
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout 

# Create your views here.
def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.error(request,'password is not matching')
            return render(request, 'signup.html')

        try:
            if User.objects.get(username=email):
                messages.info(request, 'Email is already registered.')
                return render(request, 'signup.html')
                
        except Exception as identifier:
            pass

        user = User.objects.create_user(email, email, password)
        user.is_active=False
        user.save() 

         # Send welcome email
        email_subject ="Activate your Account"
        message=render_to_string('activate.html', {
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
     
        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()
        messages.success(request,"activate your account by clicking the  below link in your gmail")
        return redirect('/auth/login')
    return render(request, "signup.html")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('/auth/login')
        return render(request, 'activatefail.html')



def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser = authenticate(username=username, password=userpassword)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('/')
        
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/auth/login')
    
    return render(request, 'login.html')



def handlelogout(request):
     logout(request)
     messages.info(request, "logout success")
     return redirect('/auth/login')