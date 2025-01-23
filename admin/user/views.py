from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from admin.user.models import CustomUser

# Create your views here.

@login_required(login_url='login')
def index(request):
    if request.method == 'GET':
        # Retrieve all users
        data = CustomUser.objects.all()
        return render(request, 'adminTemplates/user/index.html', {'data': data})


@login_required(login_url='login')
def details(request, id):
    if request.method == 'GET':
        try:
            # Retrieve user by primary key (id)
            usr = CustomUser.objects.get(pk=id)
            return render(request, 'adminTemplates/user/details.html', {'usr': usr})
        except CustomUser.DoesNotExist:
            # Display error message if user is not found
            messages.error(request, 'No such records found!')
            return redirect('user-index')
