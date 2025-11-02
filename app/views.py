from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate , login , logout
import re , json
from .models import blogs
from django.utils import timezone
from app.function import validate_email , validate_pass,  firstAndLastName, LastName, validate_dob, validate_add, validate_phoneNo, validate_gender, validate_id, blogvalidate, validate_dis
from app.models import User
from django.forms.models import model_to_dict







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
        
       
        
        gendervalidate = validate_gender(gender)
        
        if  password and email and first_name and conf_password and phoneNo and DOB and gender and address:
                if  User.objects.filter(email=email).exists():
                    return JsonResponse({"msg" : "User already registered, Please try again!"} , status = 409)
                
        
                if password != conf_password:
                   return JsonResponse({"msg": "Password and confirm_password both must be same"}, status = 400)
                
                if not validate_phoneNo(phoneNo):
                    return JsonResponse({"msg" : "Enter valid phone no"}, status= 400) 
                
                if not validate_dob(DOB):
                    return JsonResponse({"msg" : "Enter valid DOB"}, status= 400) 
               
                if  gendervalidate is None:
                     return JsonResponse({"msg" : "gender must be MALE or FEMALE"}, status= 400)    
                
                if not validate_add(address):
                     return JsonResponse({"msg" : "Enter address"}, status= 400) 
                  
                
                if not validate_pass(password):
                    return JsonResponse({"msg" : "Password is mandtory and Password must contain atleast a Uppercase, a lowercase , a special charcter and a number and minimum length must be 6"}, status= 400) 
                if not validate_email(email):
                    return JsonResponse({"msg": "Email is manadtory and Enter a valid Email"}, status = 400)
                if not firstAndLastName(first_name):
                    return JsonResponse({"msg": "First name is mandatory and First name must contain only alphabetical"}, status = 400)
                if not LastName(last_name):
                    return JsonResponse({"msg":"Last name must contain only alphabetical"}, status = 400)
                else:
                    

                    user= User(
                        email = email,
                        first_name = first_name,
                        last_name = last_name,
                        phone_No= phoneNo,
                        date_of_birth = DOB,
                        gender = gendervalidate,
                        address = address,
                    )
                
                    user.set_password(password)
                    user.save()
                    

                    
                    return JsonResponse({"msg" :"User Registerd Successfully"
                                            }, status = 201)    
                    
        else:
                return JsonResponse({"msg": "Enter all required field"}, status=400)
    else :
       
        return JsonResponse({"msg" :"method not allowed"}, status = 405)
    
    
    
    
       
def loginview(request):
    if request.method == 'POST':
        if  not request.body.strip():
                return JsonResponse({"msg": "Enter The email and password"}, status= 400)
            
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        if request.user.is_authenticated:
             return JsonResponse({"msg": "User already logged in " }, status = 200)
        
        if not email or not password:
                return JsonResponse({"msg": "email and password both mandatory"}, status=400)
        
       
        
        user = authenticate(request=request, email= email, password=password)
       
        if user is not None:
            login(request, user)
            
            return JsonResponse({"msg": "User logged in successfully" }, status = 200)
          
        else:
            return JsonResponse({"msg": "User or Password is incorrect"}, status = 401)    
        
    else:
        return JsonResponse({"msg": "Method not allowed"}, status = 405)    
        
    
def userdetails(request): 
    user = request.user
    if request.method =='GET':
     
     if user.is_authenticated:   
        if user is None:
            return JsonResponse({"msg": "user is not login"}, status = 400)
        else:
            
           
            
            columns = [
                "first_name", 
                "last_name", 
                "email", 
                "phone_No", 
                "date_of_birth", 
                "address", 
                "gender"
             ]
            
            data = model_to_dict(user, fields=columns)
            
            
            return JsonResponse(data, status = 200)
     else:
         return JsonResponse({"msg": "user not login"}, status = 400)
    else:
        return JsonResponse({"msg": "Method not allowed"}, status = 405)


def logoutview(request):
    if request.method == 'DELETE':
        if request.user.is_authenticated:

            logout(request)
            return JsonResponse({"msg" :"you are successfully logout"}, status = 200)
        else:
            return JsonResponse({"msg" :"User is not login"}, status = 400)
    else:
        return JsonResponse({"msg" :"Method not allowed"}, status = 405)
    
    

def createblog(request):
     if request.method == 'POST':
          if not request.body.strip():
            return JsonResponse({"msg": "Enter the task"}, status= 400)
        
          data = json.loads(request.body)
          
          title = data.get('title')
          description = data.get('description')
          if request.user.is_authenticated:
            if blogvalidate(title) and blogvalidate(description)  :
                blog= blogs(
                            title= title,
                            description  = description ,
                            user_id = request.user.id,
                        )
                blog.save()
                return JsonResponse({"msg": "Task added successfully"}, status =201)
            else :
                return JsonResponse({"msg": "Enter title and description"}, status = 400)
          else:
             return JsonResponse({"msg": "user is not loged in"}, status = 400)
             
            
     else:
          return JsonResponse({"msg" :"method not allowed"}, status = 405)
      
      
      
def readblog(request):
    if request.method == 'GET':
     if request.user.is_authenticated:
         x =blogs.objects.filter(active =True, user_id = request.user.id).values("title", "description", "create", "id")
         return JsonResponse({"Details": list(x)}, status = 200)
     else:
         return JsonResponse({"msg": "You are not Login"}, status =400)
    else :
       return JsonResponse({"msg" :"method not allowed"}, status = 405)

 
def updateblog(request):
      if request.method == 'PUT':
          if not request.body.strip():
            return JsonResponse({"msg": "Enter The User Informations"}, status= 400)
        
          data = json.loads(request.body)
          
          updateid = data.get('id')
          updateTitle= data.get('updateTitle')
          updatedis = data.get('updatedis')
          
          if not blogvalidate(updateTitle):
              return JsonResponse({"msg": "Title must less then 200 characters"}, status = 400)
              
          if not validate_dis(updatedis):
              return JsonResponse({"msg":"Enter Discription"}, status = 400)
          
          if  validate_id(updateid): 
              return JsonResponse({"msg": "id required"}, status = 400)
          
          if not blogs.objects.filter(id = updateid).exists():
              return JsonResponse({"msg": "id not found"}, status = 400)

          current_user = request.user
          cid = current_user.id
          
          if current_user.is_authenticated:
                
                if updateid is not None and updateTitle is not None and updatedis is None:
                     x= blogs.objects.filter(id=updateid , user_id= cid, active = True).update(title=updateTitle, update = timezone.now())
                     if not x:
                         return JsonResponse({"msg": "user is not loged in"}, status = 401)
                     return JsonResponse({"msg": "Titile Updated successfully"}, status = 200)

             
             
                if updateid is not None and updatedis is not None and updateTitle is None:
                      x = blogs.objects.filter(id =updateid, user_id= cid).update(description = updatedis, update = timezone.now())
                      if not x:
                         return JsonResponse({"msg": "user is not loged in"}, status = 401)
                    
                      return JsonResponse({"msg": "description Updated successfully"}, status = 200)
                  
                if updateid is not None and updateTitle is not None and updatedis is not None:
                    x= blogs.objects.filter(id = updateid, user_id= cid).update(title = updateTitle, description= updatedis, update = timezone.now())
                    if not x:
                         return JsonResponse({"msg": "user is not loged in"}, status = 401)
                    
                    return JsonResponse({"msg": "title and ddescription Updated successfully"}, status = 200)
                if updateid is not None and updateTitle is None and updatedis is None:
                
                    return JsonResponse({"msg":"Enter title or description for update"}, status= 400)
                    
                else :
                     return JsonResponse({"msg": "task was not found"}, status = 400)
                    
            
          else:
                return JsonResponse({"msg": "You are not Login"}, status = 400)

      else:
          return JsonResponse({"msg" :"method not allowed"}, status = 405)
       
       
def deleteblog(request):
      if request.method == 'DELETE':
           
          delid = request.GET.get('id')
          
          current_user = request.user
          xid = current_user.id
          
          if current_user.is_authenticated:
             
             if not delid:
                return JsonResponse({"msg": "id required"}, status = 400)
              
             if blogs.objects.filter(id = delid , active = True, user_id= xid):
             
              blogs.objects.filter(id = delid).update(active= False, delete = timezone.now(), trash = True)
              return JsonResponse({"msg": "blog deleted successfully"})   
          
             else:  
              return JsonResponse({"msg": "invalid delid"} , status = 400)
          else:  
              return JsonResponse({"msg": "You are not Login"} , status = 400)
          
      else:
          return JsonResponse({"msg" :"method not allowed"}, status = 405)
      

def trash(request):
    if request.method == 'GET':
     if request.user.is_authenticated:
         x =blogs.objects.filter(active =False, trash = True, user_id = request.user.id).values("title", "description", "create", "id")  
         return JsonResponse({"Details": list(x)})
     else:
         return JsonResponse({"msg": "You are not Login"}, status =400)
    else :
       return JsonResponse({"msg" :"method not allowed"}, status = 405)
      
      

def deletetrash(request):
      if request.method == 'DELETE':
           
          delid = request.GET.get('id')
          
          print(delid)
          
          if request.user.is_authenticated :
              
             if not delid :
                return JsonResponse({"msg": "id required"}, status = 400)
              
             if blogs.objects.filter(id = delid , active = False):
             
              blogs.objects.filter(id = delid).update(active= False, delete = timezone.now(), trash = False)
              return JsonResponse({"msg": "blog deleted successfully"})   
          
             else:  
              return JsonResponse({"msg": "invalid delid"} , status = 400)
          else:  
              return JsonResponse({"msg": "You are not Login"} , status = 400)
          
      else:
          return JsonResponse({"msg" :"method not allowed"}, status = 405)


def restore(request):
      if request.method == 'PUT':
        
          
          restoreid = request.GET.get("id")
          print(restoreid)
          
        
          
          if request.user.is_authenticated :
                if restoreid is not None :
                 blogs.objects.filter(active =False, trash = True, user_id = request.user.id, id= restoreid).update(trash = False, active = True)
                
                 return JsonResponse({"msg": "restored succeffully"}, status = 200)

                else :
                     return JsonResponse({"Error": "id not found"}, status = 400)
                    
            
          else:
                return JsonResponse({"msg": "You are not Login"}, status = 400)

      else:
          return JsonResponse({"msg" :"method not allowed"}, status = 405)

          

