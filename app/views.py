from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate , login , logout
import re , json
from .models import blogs
from django.utils import timezone
from app.function import validate_email , validate_pass,  firstAndLastName, LastName, validate_dob, validate_gender, validate_add, validate_phoneNo
from app.models import User
from django.contrib.auth.decorators import login_required







def signupview(request):
    if request.method == 'POST':
        
        if not request.body.strip():
            return JsonResponse({"Error": "Enter The User Informations"}, status= 400)
        
        data = json.loads(request.body)
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phoneNo = data.get('phone_No')
        DOB = data.get('DOB')
        gender = data.get('gender')
        address = data.get('address')
        password = data.get('password')
        conf_password = data.get('Confirm_password')
        
       
        
        
        
    
        if  password and email and first_name and conf_password and phoneNo and DOB and gender and address and conf_password:
                if  User.objects.filter(email=email).exists():
                    return JsonResponse({"Error" : "User already registered, Please try singing in!"} , status = 409)
                
        
                if password != conf_password:
                   return JsonResponse({"Error": "Password and confirm_password both must be same"}, status = 400)
                
                if not validate_phoneNo(phoneNo):
                    return JsonResponse({"Error" : "Enter valid phone no"}, status= 400) 
                
                if not validate_dob(DOB):
                    return JsonResponse({"Error" : "Enter valid DOB no"}, status= 400) 
                    
                if not validate_gender(gender):
                     return JsonResponse({"Error" : "Enter 0 for male, 1 for female, and 2 for other"}, status= 400)    
                
                if not validate_add(address):
                     return JsonResponse({"Error" : "Enter address"}, status= 400) 
                  
                
                if not validate_pass(password):
                    return JsonResponse({"Error" : "Password is mandtory and Password must contain atleast a Uppercase, a lowercase , a special charcter and a number and minimum length must be 6"}, status= 400) 
                if not validate_email(email):
                    return JsonResponse({"Error": "Email is manadtory and Enter a valid Email"}, status = 400)
                if not firstAndLastName(first_name):
                    return JsonResponse({"Error": "First name is mandatory and First name must contain only alphabetical"}, status = 400)
                if not LastName(last_name):
                    return JsonResponse({"Error":"Last name must contain only alphabetical"}, status = 400)
                else:

                    user= User.objects.create(
                        email = email,
                        first_name = first_name,
                        last_name = last_name,
                        phone_No= phoneNo,
                        date_of_birth = DOB,
                        gender = gender,
                        address = address,
                        password = password,
                        
                    )
                    
                    user.set_password(password)
                    user.save()
                    return JsonResponse({"message" :"User Registerd Successfully"
                                            }, status = 201)    
                    
        else:
                return JsonResponse({"Error": "Enter all required field"}, status=400)
    else :
       
        return JsonResponse({"error" :"method not allowed"}, status = 405)
    
    
    
    
        
def loginview(request):
    if request.method == 'POST':
        if  not request.body.strip():
                return JsonResponse({"Error": "Enter The email and password"}, status= 400)
            
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
         
        if not email or not password:
                return JsonResponse({"Error": "email and password both mandatory"}, status=400)
        
        user = authenticate(request=request, email= email, password=password)
       
        if user is not None:
            login(request, user)
            
            return JsonResponse({"message": "User logged in successfully" }, status = 200)
          
        else:
            return JsonResponse({"message": "User or Password is incorrect"}, status = 401)    
        
    else:
        return JsonResponse({"Error": "Method not allowed"}, status = 405)    
        
# @login_required     
def userdetails(request): 
    user = request.user
    if request.method =='GET':
     
     if request.user.is_authenticated:   
        if user is None:
            return JsonResponse({"Error": "user is not login"}, status = 400)
        else:
            data= {
            "firstName":user.first_name,
            "lastname": user.last_name,
            "email" : user.email,
            "phoneNO" : user.phone_No,
            "DOB" : user.date_of_birth,
            "Address": user.address,
            "gender" : user.gender,
            }
        
            return JsonResponse(data, status = 200)
     else:
         return JsonResponse({"Error": "user not login"}, status = 400)
    else:
        return JsonResponse({"Error": "Method not allowed"}, status = 405)


def logoutview(request):
    if request.method == 'DELETE':
        if request.user.is_authenticated:

            logout(request)
            return JsonResponse({"message" :"you are successfully logout"}, status = 200)
        else:
            return JsonResponse({"Error" :"User is not login"}, status = 400)
    else:
        return JsonResponse({"Error" :"Method not allowed"}, status = 405)
    
    

def createblog(request):
     if request.method == 'POST':
          if not request.body.strip():
            return JsonResponse({"Error": "Enter the task"}, status= 400)
        
          data = json.loads(request.body)
          
          title = data.get('title')
          description = data.get('description')
          if request.user.is_authenticated:
            if title and description  :
                blog= blogs.objects.create(
                            title= title,
                            description  = description ,
                            user_id = request.user.id,
                        )
                blog.save()
                return JsonResponse({"message": "Task added successfully"}, status =201)
            else :
                return JsonResponse({"Error": "Enter title and description"}, status = 400)
          else:
             return JsonResponse({"Error": "user is not loged in"}, status = 400)
             
            
     else:
          return JsonResponse({"error" :"method not allowed"}, status = 405)
      
      
      
def readblog(request):
    if request.method == 'GET':
     if request.user.is_authenticated:
         x =blogs.objects.filter(active =True, user_id = request.user.id).values("title", "description", "create", "id")
 
         return JsonResponse({"Details": list(x)}, status = 200)
     else:
         return JsonResponse({"Error": "You are not Login"}, status =400)
    else :
       return JsonResponse({"error" :"method not allowed"}, status = 405)

 
def updateblog(request):
      if request.method == 'PUT':
          if not request.body.strip():
            return JsonResponse({"Error": "Enter The User Informations"}, status= 400)
        
          data = json.loads(request.body)
          
          updateid = data.get('id')
          updateTitle= data.get('updateTitle')
          updatedis = data.get('updatedis')
          
        
          
          if request.user.is_authenticated :
                if updateid is not None and updateTitle is not None and updatedis is None:
                 blogs.objects.filter(id=updateid).update(title=updateTitle, update = timezone.now())
            
                 return JsonResponse({"Message": "Titile Updated successfully"}, status = 200)

             
             
                if updateid is not None and updatedis is not None and updateTitle is None:
                      blogs.objects.filter(id =updateid).update(description = updatedis, update = timezone.now())
                    
                      return JsonResponse({"Message": "description Updated successfully"}, status = 200)
                  
                if updateid is not None and updateTitle is not None and updatedis is not None:
                    blogs.objects.filter(id = updateid).update(title = updateTitle, description= updatedis, update = timezone.now())
                    
                    return JsonResponse({"Message": "title and ddescription Updated successfully"}, status = 200)
                if updateid is not None and updateTitle is None and updatedis is None:
                
                    return JsonResponse({"Message":"Enter title or description for update"}, status= 400)
                    
                else :
                     return JsonResponse({"Error": "task was not found"}, status = 400)
                    
            
          else:
                return JsonResponse({"Error": "You are not Login"}, status = 400)

      else:
          return JsonResponse({"error" :"method not allowed"}, status = 405)
       
       
def deleteblog(request):
      if request.method == 'DELETE':
           
          delid = request.GET.get('id')
          
          print(delid)
          
          if request.user.is_authenticated :
              
             if not delid :
                return JsonResponse({"Message": "id required"}, status = 400)
              
             if blogs.objects.filter(id = delid , active = True):
             
              blogs.objects.filter(id = delid).update(active= False, delete = timezone.now(), trash = True)
              return JsonResponse({"Message": "blog deleted successfully"})   
          
             else:  
              return JsonResponse({"Error": "invalid delid"} , status = 400)
          else:  
              return JsonResponse({"Error": "You are not Login"} , status = 400)
          
      else:
          return JsonResponse({"error" :"method not allowed"}, status = 405)
      

def trash(request):
    if request.method == 'GET':
     if request.user.is_authenticated:
         x =blogs.objects.filter(active =False, trash = True, user_id = request.user.id).values("title", "description", "create", "id")  
         return JsonResponse({"Details": list(x)})
     else:
         return JsonResponse({"Error": "You are not Login"}, status =400)
    else :
       return JsonResponse({"error" :"method not allowed"}, status = 405)
      
      

def deletetrash(request):
      if request.method == 'DELETE':
           
          delid = request.GET.get('id')
          
          print(delid)
          
          if request.user.is_authenticated :
              
             if not delid :
                return JsonResponse({"Message": "id required"}, status = 400)
              
             if blogs.objects.filter(id = delid , active = False):
             
              blogs.objects.filter(id = delid).update(active= False, delete = timezone.now(), trash = False)
              return JsonResponse({"Message": "blog deleted successfully"})   
          
             else:  
              return JsonResponse({"Error": "invalid delid"} , status = 400)
          else:  
              return JsonResponse({"Error": "You are not Login"} , status = 400)
          
      else:
          return JsonResponse({"error" :"method not allowed"}, status = 405)


def restore(request):
      if request.method == 'PUT':
        
          
          restoreid = request.GET.get("id")
          print(restoreid)
          
        
          
          if request.user.is_authenticated :
                if restoreid is not None :
                 blogs.objects.filter(active =False, trash = True, user_id = request.user.id, id= restoreid).update(trash = False, active = True)
                
                 return JsonResponse({"Message": "restored succeffully"}, status = 200)

                else :
                     return JsonResponse({"Error": "id not found"}, status = 400)
                    
            
          else:
                return JsonResponse({"Error": "You are not Login"}, status = 400)

      else:
          return JsonResponse({"error" :"method not allowed"}, status = 405)

          

