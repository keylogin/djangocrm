from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
# Create your views here.
from .models import Record


def home(request):
    records = Record.objects.all()
    # Check to see if loggin in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
         
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging in, Please Try Again....")
            return redirect('home')
    else:    
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome.")
            return redirect('home')
    else:
        form = SignUpForm()    
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You Must Be Logged In First...")
        return redirect('home')
    
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_rec = Record.objects.get(id=pk)
        delete_rec.delete()
        messages.success(request, "Records Delete Successfull")
        return redirect('home')
    else:
        messages.success(request, "To delete something, need to be logged in!")
        return redirect('login')
    

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
            return render(request, 'add_record.html', {'form':form})
        else:
            return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In First...")
        return redirect('home')
    
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated...")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You Must Be Logged In First...")
        return redirect('home')