from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .forms import LoginForm, RegistrationForm, UpdateUserForm, DeletionForm, AddAPIForm, UpdateAPIForm,MapAPIForm
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import User,API
from .serializers import UserSerializer,APISerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password,make_password
import json  


def render_home(request): 
    return render(request,'home.html')


def render_dashboard(request):
    return render(request,'dashboard.html')


def render_forms(request,form_type):

    user_table_columns = ['id','username','mobile','role']
    api_table_columns = ['id','name','description','endpoint','method','mapped_users','user_id']
    
    match form_type:
        case 'adduser': 
            form = RegistrationForm()
            info = {"button_name":"CREATE USER","columns":user_table_columns,"data_list":fetch_data('User'),"url_path":"/user/add/","request_method":"post"}
        case 'updateuser': 
            form = UpdateUserForm()
            info = {"button_name":"UPDATE USER","columns":user_table_columns,"data_list":fetch_data('User'),"url_path":"/user/update/","request_method":"post"}
        case 'deleteuser': 
            form = DeletionForm()
            info = {"button_name":"DELETE USER","columns":user_table_columns,"data_list":fetch_data('User'),"url_path":"/user/delete/","request_method":"delete"}
        case 'addapi':
            form = AddAPIForm()
            info = {"button_name":"CREATE API","columns":api_table_columns,"data_list":fetch_data('API'),"url_path":"/api/add/","request_method":"post"}
        case 'updateapi':
            form = UpdateAPIForm()
            info = {"button_name":"UPDATE API","columns":api_table_columns,"data_list":fetch_data('API'),"url_path":"/api/update/","request_method":"post"}
        case 'deleteapi':
            form = DeletionForm()
            info = {"button_name":"DELETE API","columns":api_table_columns,"data_list":fetch_data('API'),"url_path":"/api/delete/","request_method":"delete"}
        case 'mapapi':
            form = MapAPIForm()
            info = {"button_name":"MAP API","columns":api_table_columns,"data_list":fetch_data('API'),"url_path":"/map/api/","request_method":"post"}
        case 'unmapuser':
            form = MapAPIForm()
            info = {"button_name":"UNMAP USER","columns":api_table_columns,"data_list":fetch_data('API'),"url_path":"/unmap/user/","request_method":"post"}
        case _:
            form = None

    return render(request,'forms.html',{"form":form,"info":info})


def generate_jwt_token(payload):

    refresh = RefreshToken.for_user(payload)
    
    tokens = {
        "refresh":str(refresh),
        "access": str(refresh.access_token)
    }

    return tokens


def fetch_data(model_name):

    if model_name == 'User':
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
    else:
        apis = API.objects.all()
        serializer = APISerializer(apis,many=True)

    return serializer.data


@csrf_exempt 
def login(request):

    try:

        if request.method == 'POST':
    
            request_data = json.loads(request.body)
            username = request_data['username']
            password = request_data['password']
            
            user = User.objects.filter(username=username).first()

            if user:

                password_matched = check_password(password,user.password)

                if password_matched:

                    tokens = generate_jwt_token(User)
                    user.tokens = tokens
                    user.save()                             
                    return JsonResponse({"type":"success","tokens":tokens})

                else:
                    error = "invalid password"
                    return JsonResponse({"type":"failure","error":error})

            else:
                error = "username doesn't exist"
                return JsonResponse({"type":"failure","error":error})

        else:
            form = LoginForm()
            return render(request,'login.html',{"form":form})
        
    except Exception as e:
        return JsonResponse({str(e)})


@csrf_exempt
def add_user(request):

    try:
        token = request.headers.get('Authorization')[7:]

        # checking if user corresponding to this token exists in the db
        a = User.objects.get(username="ganesh")
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})

        if user.role == 'admin':

            if request.method == 'POST':

                request_data = json.loads(request.body)
                request_data['password'] = make_password(request_data['password'])
                
                serializer = UserSerializer(data=request_data)

                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({"type":"success","message":"user created successfully","user":serializer.data})
                else:
                    return JsonResponse({"type":"failure","error":json.dumps(serializer.errors.get('username'))})

            else:
                return JsonResponse({"type":"success","redirectUrl":"/forms/adduser/"})
        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})


    except Exception as e:
        return JsonResponse({e})


@csrf_exempt
def update_user(request):

    try:
        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})

        if user.role == 'admin':

            if request.method == 'POST':

                request_data = dict()
                form_input = json.loads(request.body)

                # checking for non-empty values 
                for key, val in form_input.items():
                    if len(val) > 0:
                        if key == 'password':
                            request_data[key] = make_password(val)
                        else:
                            request_data[key] = val

                user_to_be_updated = User.objects.filter(id=form_input['user_id']).first()

                if user_to_be_updated:

                    serializer = UserSerializer(user_to_be_updated,data=request_data,partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({"type":"success","message":"user updated successfully","user":serializer.data})
                
                else:
                    return JsonResponse({"type":"failure","error":"User with this id doesn't exist"})
            
            else:
                return JsonResponse({"type":"success","redirectUrl":"/forms/updateuser/"})

        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})

    except Exception as e:
        return JsonResponse({str(e)})


@csrf_exempt
def delete_user(request):

    try:
        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()
        
        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})

        if user.role == 'admin':

            if request.method == 'DELETE':
                
                request_data = json.loads(request.body)
                user_to_be_deleted = User.objects.filter(id=request_data['id']).first()

                if user_to_be_deleted:

                    deleted_user = {
                        "id":user_to_be_deleted.id,
                        "username":user_to_be_deleted.username
                    }

                    user_to_be_deleted.delete()

                    return JsonResponse({"type":"success","message":"user deleted successfully","user":deleted_user})
                else:
                    return JsonResponse({"type":"failure","error":"User with this id doesn't exist"})

            else:
                return JsonResponse({"type":"success","redirectUrl":"/forms/deleteuser/"})
        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})

    except Exception as e:
        return JsonResponse({str(e)})


@csrf_exempt
def add_API(request):

    try:
        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})
        
        if user.role == 'admin' or user.role == 'user':

            if request.method == 'POST':
                
                request_data = json.loads(request.body)
                
                request_data['user_id'] = user.id

                request_data['mapped_users'] = [user.id]

                serializer = APISerializer(data=request_data)

                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({"type":"success","message":"api created successfully","api":serializer.data})
                else:
                    return JsonResponse({"type":"failure","error":serializer.errors})

            else:
                return JsonResponse({"type":"success","redirectUrl":"/forms/addapi/"})
        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})
            
    except Exception as e:
        return Response(str(e))


@csrf_exempt
def update_API(request):

    try:

        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})

        if user.role == 'admin' or user.role == 'user':

            if request.method == 'POST':

                form_input = json.loads(request.body)
                api_to_be_updated = API.objects.filter(id=form_input['api_id']).first()
                
                if api_to_be_updated:
                    
                    # checking if the user is eligible to update this particular API

                    if user.id not in api_to_be_updated.mapped_users:
                        return JsonResponse({"type":"failure","error":"You cannot update this API"})

                    request_data = dict()

                    # checking for non-empty values 
                    for key, val in form_input.items():
                        if len(val) > 0:
                            request_data[key] = val

                    serializer = APISerializer(api_to_be_updated,data=request_data,partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({"type":"success","message":"api updated successfully","api":serializer.data})                
                else:
                    return JsonResponse({"type":"failure","error":"API with this id doesn't exist"})
                
            else:
                return JsonResponse({"type":"success","redirectUrl":"/forms/updateapi/"})
        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})
    
    except Exception as e:
        return JsonResponse({str(e)})


@csrf_exempt
def delete_API(request):

    try:
        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})

        if user.role == 'admin':

            if request.method == 'DELETE':
                
                request_data = json.loads(request.body)
                api_to_be_deleted = API.objects.filter(id=request_data['id']).first()

                if api_to_be_deleted:

                    if len(api_to_be_deleted.mapped_users) > 0:
                        return JsonResponse({"type":"failure","error":"API cannot be deleted"})

                    deleted_api = {
                        "id":api_to_be_deleted.id,
                        "name":api_to_be_deleted.name,
                        "endpoint":api_to_be_deleted.endpoint,
                        "method":api_to_be_deleted.method
                    }

                    api_to_be_deleted.delete()
                    return JsonResponse({"type":"success","message":"API deleted successfully","api":deleted_api})

                else:
                    return JsonResponse({"type":"failure","error":"API with this id doesn't exist"})
            else:
                return JsonResponse({"type":"success","redirectUrl":"/forms/deleteapi/"})
        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})

    except Exception as e:
        return JsonResponse({str(e)})

@csrf_exempt
def view_all_API(request):

    if request.method == 'GET':
        data = API.objects.all()
        serializer = APISerializer(data,many=True)
        return JsonResponse({"type":"success","apis":serializer.data,"detail":serializer.data})


# below function will display apis created by user
@csrf_exempt
def view_API_of_user(request):

    try:
        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})

        if request.method == 'GET':

            if user.role == 'admin' or user.role == 'user':
                api_data = API.objects.filter(user_id_id=user.id)
                if api_data.exists():
                    serializer = APISerializer(api_data,many=True)
                    return JsonResponse({"type":"success","detail":serializer.data})
                else:
                    return JsonResponse({"type":"failure","error":"You have not created any API's yet"})
            else:
                return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})

    except Exception as e:  
        return JsonResponse({str(e)})



@csrf_exempt
def view_mapped_API(request):
    
    try:
        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})
        
        if user.role == 'admin':
            # return all apis to admin
            return JsonResponse({"type":"success","detail":fetch_data('API')})
        elif user.role == 'user':
            apis = API.objects.filter(mapped_users__contains=[user.id])
            if apis.exists():
                serializer = APISerializer(apis,many=True)
                return JsonResponse({"type":"success","detail":serializer.data})
            else:
                return JsonResponse({"type":"failure","error":"no apis are mapped against this user"})
        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})

    except Exception as e:
        return JsonResponse({str(e)})


@csrf_exempt
def map_API_to_users(request):

    try:
        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})

        if user.role == 'admin':
            
            if request.method == 'POST':
                
                request_data = json.loads(request.body)
                api = API.objects.filter(id=request_data['api_id']).first()

                if api is None:
                    return JsonResponse({"type":"failure","error":"API with this id doesn't exist"})

                if user.id in api.mapped_users:
                    return JsonResponse({"type":"failure","error":"user is already mapped to this api"})
            
                api.mapped_users.append(request_data['user_id'])
                api.save()
                serializer = APISerializer(api)
                return JsonResponse({"type":"success","message":"user mapped successfully","api":serializer.data})
            else:
                return JsonResponse({"type":"success","redirectUrl":"/forms/mapapi/"})
        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})
    except Exception as e:
        return JsonResponse({str(e)})
    

@csrf_exempt
def unmap_user(request):

    try:
        token = request.headers.get('Authorization')[7:]
        user = User.objects.filter(tokens__contains={"access":token}).first()

        if user is None:
            return JsonResponse({"type":"failure","error":"token is invalid"})

        if user.role == 'admin':

            if request.method == 'POST':

                request_data = json.loads(request.body)
                api = API.objects.filter(id=request_data['api_id']).first()

                if api:
                   
                    user_id = int(request_data['user_id'])

                    if user_id not in api.mapped_users:
                        return JsonResponse({"type":"failure","error":"cannot unmap this user as it is not present in the mapped users"})

                    api.mapped_users.remove(user_id)
                    api.save()
                    return JsonResponse({"type":"success","message":"user unmapped successfully"})
                    
                    
                else:
                    return JsonResponse({"type":"failure","error":"API with this id doesn't exist"})
            else:
                return JsonResponse({"type":"success","redirectUrl":"/forms/unmapuser/"})

        else:
            return JsonResponse({"type":"failure","error":"401 UNAUTHORIZED"})
    except Exception as e:
        return JsonResponse({str(e)})