from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import SignupForm
from .models import UserDetails
from django.views.decorators.csrf import csrf_exempt
from .serializer import UserSerializer
import json

# Create your views here.
@csrf_exempt
def signup_view(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = UserDetails(username=username,email=email,password=password)
            user.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request,'signupform.html',{'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return JsonResponse({"success": False, 'message': 'Email and password are required'}, status = 400)
        
        user = UserDetails.objects.get(email = email)
        
        if user.password == password:
            return HttpResponse('Success ----!', status = 200)
        else:
            return render(request, 'loginform.html', {'error':'Invalid Credentials'})
        
    return render(request, 'loginform.html')


#Get all user details view: Retrieves and displays details of all users.
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = UserDetails.objects.all()
        serializer = UserSerializer(users, many=True) #true since we are having many users
        return JsonResponse(serializer.data, safe=False) #safe = False will allow Json to handle more complex data structures like dictionary
    

#Get a single user using by email view: Retrieves and displays details of a specific user based on their name    
@csrf_exempt
def user_detail(request,username):
    try:
        user = UserDetails.objects.get(username=username)

    except UserDetails.DoesNotExist:
        return JsonResponse({'error':'user not found'}, status=404)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)


# Update User details
@csrf_exempt
def update_user(request,username):
    try:
        user = UserDetails.objects.get(username=username)

    except UserDetails.DoesNotExist:
        return JsonResponse({'error':'user not found'}, status=404)
    
    if request.method == 'PUT':
        data = json.loads(request.body) 
        serializer = UserSerializer(user,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors,status=400)
        


#To delete a user using its email.
@csrf_exempt
def delete_user(request,email):
    try:
        user = UserDetails.objects.get(email=email)

    except UserDetails.DoesNotExist:
        return JsonResponse({'error':'user not found'}, status=404)
  
    if request.method == 'DELETE':
        user.delete()
        return HttpResponse('successfully deleted', status=204)
    else:
        return HttpResponse(status=405)



