from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<5 or len(phone)<10 or len(content)<10:
            messages.error(request, 'Please fill the form with valid details only.')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your contact details has been submitted successfully.')

    return render(request, 'home/contact.html')

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


def handleSignUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 10 or len(username) < 4 or not username.isalnum():
            messages.error(request, "Username doesn't match the required criteria. Username must contain only alphabets and numbers and should have 4-10 characters. Please try again.")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Password confirmation doesn't match to the selected password. Please try again.")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_namme = fname
        myuser.last_namme = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully registered.")
        return redirect('home')
    else:
        return HttpResponse("404 - Pge not found")

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, f'You have been successfully logged in with your iCoder username {loginusername}')
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
            return redirect('home')

def handleLogout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')