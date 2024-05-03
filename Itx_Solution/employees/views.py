from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from employees.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime,timedelta
import json
from django.db import connection
from django.db.models import Q
# from django.views.decorators.http import require_POST,require_GET
from functools import wraps
from django.http import HttpResponseForbidden



def restrict_direct_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Add your access control logic here
        # For example, check for custom headers, authentication, or IP whitelisting
        
        # Example: Check for a custom header
        custom_header_value = request.headers
        print(custom_header_value)
        try:
            if custom_header_value["header-check"] != 'function-request':
                return HttpResponseForbidden("Access denied")
        except KeyError:
            return HttpResponseForbidden("Access denied")
        
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def app_auth(func):
    @wraps(func)
    def wrap(request,*args,**kwargs):
        # print(request.headers)
        try:
            if request.headers["auth-app"] != 'itx_solution':
                return HttpResponseForbidden("Access denied")
        except KeyError:
            return HttpResponseForbidden("Access denied")
        # print("function called")
        return func(request, *args, **kwargs)
    return wrap


# flags for messages

flag_dict = {
    "Something went wrong":3,
    "Already Checked In":4,
    "Please Checked In first":5,
    "Already Checked Out":6,
    "Successfully Checked In":7,
    "Successfully Checked Out":8,
    "Anonymous":9,
    "Door open":10
}


def upload_data(_user,status):
    x=datetime.now()
    day =x.strftime("%A") 
    date =x.strftime("%Y-%m-%d") 
    time = x.strftime("%X")
    temp_status = None
    try:
        if status=="1":
            try:
                daily_status.objects.get(emp_id=_user,date=date,status="Check In")
                return flag_dict["Already Checked In"]        
            except Exception as err:
                temp_status = "Check In"
                pass
        elif status=="2":
            try:
                daily_status.objects.get(emp_id=_user,date=date,status="Check In")
            except Exception as err:
                return flag_dict["Please Checked In first"]
            try:
                daily_status.objects.get(emp_id=_user,date=date,status="Check Out")
                return flag_dict["Already Checked Out"]
            except Exception as err:
                temp_status = "Check Out"
        # adding status in database
        daily_status.objects.create(emp_id=_user,day = day,date= date,time = time,status=temp_status)
        if status=="2":
            s = daily_status.objects.filter(emp_id=_user,date=date)
            for a in s.all():
                print(type(a.time))
                if a.status=="Check In":
                    time_str1=a.time
                elif a.status=="Check Out":
                    time_str2 = a.time
            # Calculate the time difference
            time_difference = timedelta(hours=time_str2.hour,minutes=time_str2.minute,seconds=time_str2.second) - timedelta(hours=time_str1.hour,minutes=time_str1.minute,seconds=time_str1.second)
            # print(type(time_difference))
            daily_hours.objects.create(emp_id = _user,date=date,hours=str(time_difference))
        if status =="1":
            return flag_dict["Successfully Checked In"]
        elif status =="2":
            return flag_dict["Successfully Checked Out"]
    except:
        return flag_dict["Something went wrong"]


#this endpoint is used for arduino chip module,
@app_auth
def rfid_auth(request):
    open_door = '0'
    check_in = '1'
    check_out = '2'
    body = request.headers
    flag = None
    print(body)
    
    # user = authenticate(nfc_num=int(body["nfcnum"]))
    try:
        user= employees.objects.get(nfc_num=int(body["nfcnum"]))
    except employees.DoesNotExist:
        user = None
    
    # print(user)
    
    if user: # authenticate the user to open the door.
        if body["flag"]==open_door:
            print('door open')
            return JsonResponse({"flag":flag_dict["Door open"]})
        elif body["flag"]==check_in: # uploads the check in status
            # print("upload called")
            data = upload_data(user,check_in)
            # print(data)
            return JsonResponse({"flag":data})
        elif body["flag"]==check_out:# uploads the check out status
            # print("upload called")
            data = upload_data(user,check_out)
            # print(data)
            return JsonResponse({"flag":data})
    else:
        return JsonResponse({"flag":flag_dict["Anonymous"]})
    



@app_auth
def auth_app_user(request):
    body = json.loads(request.body)
    flag = None
    user = authenticate(email=body["email"],password =body["password"])
    if user:
        flag= True
    else:
        flag = False
    return JsonResponse({'flag':flag})



@app_auth
def add_user_by_app(request):
    body = json.loads(request.body)
    print(body)
    temp_emp = employees(f_name=body["f_name"].upper(),l_name=body["l_name"].upper(),email=body["email"],cell_no=body["cell_no"],gender=body["gender"],
                             birth_date=body["birth_date"],designation="admin")
    temp_emp.set_password(body["password"])
    temp_emp.save()

    return JsonResponse({'flag':True})







def _logout(request):
    logout(request)
    return redirect("/")


def login_page(request):
    
    if request.user.is_authenticated:
        return redirect("/after_login")

    if request.method=="POST":
        email = request.POST["email"]
        password = request.POST["password"]
        print(email,password)
        user = authenticate(email=email,password =password)
        if user:
            login(request,user)
            return redirect("/after_login")
        else:
            pass
            # return JsonResponse({'Message': 'Invalid Credentials'})
    return render(request,"login_page.html")


# @restrict_direct_access
# def login_credentials(request):




def signUp_page(request):
    if request.method =="POST":
        f_name = request.POST.get("f_name")
        l_name= request.POST.get("l_name")
        email= request.POST.get("email")
        cell_no= request.POST.get("cell_no")
        gender= request.POST.get("gender")
        birth_date= request.POST.get("birth_date")
        password= request.POST.get("password")
        cnf_password= request.POST.get("cnf_password")
        if password != cnf_password:
            messages.add_message(request,messages.ERROR,'Please enter the same password!')
            return redirect("/signUp")
        temp_emp = employees(f_name=f_name.upper(),l_name=l_name.upper(),email=email,cell_no=cell_no,gender=gender,
                             birth_date=birth_date,designation="employ")
        temp_emp.set_password(password)
        check,msg =temp_emp.is_valid()
        if not check:
            messages.add_message(request,messages.ERROR,msg)
            return redirect("/signUp")
        else:
            temp_emp.save()
            messages.add_message(request,messages.SUCCESS,"Account Created")
            return redirect("/")
    return render(request,'signup_page.html')


#for users, not admin
@login_required()
def after_login_page(request):
    print(request.user)
    data  = employees.objects.get(email = request.user)
    # print(data.image.read,"image type")
    # Assuming data.image is a binary image data field in your model
    image_data = data.image
    if not image_data:
        print("only hassam")
    
    print(image_data,"image_data")

    temp_dict = {
        "user_dp":image_data,
        "full_name":f"{data.f_name} {data.l_name}",
        "user_email":f"{data.email}",
        "user_cell_no":f"{data.cell_no}",
        "user_birth_date":f"{data.birth_date}"
    }
    return render(request,"after_login_page.html",context=temp_dict)

# users hours data , not admin
@login_required()
def hours_page(request):

    x=datetime.now()
    date =x.strftime("%Y-%m-%d") 
    emp = employees.objects.get(email =request.user)
    check_in_time = "-"
    check_out_time = "-"
    total_hr = "-"
    try:
        sta =daily_status.objects.filter(emp_id =emp,date=date)    
        hr_obj = daily_hours.objects.get(emp_id = emp,date =date)
        total_hr = hr_obj.hours
    except:
        pass

    for obj  in sta.all():
        if obj.status=="Check In":
            check_in_time = obj.time
        elif obj.status=="Check Out":
            check_out_time = obj.time
    
    data_dic = {
        "today_data":{"date":date,"Check_In":check_in_time,"Check_Out":check_out_time,"hour":str(total_hr)}
    }

    return render(request,"hours_page.html",context=data_dic)


@login_required()
@restrict_direct_access
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('img'):
        uploaded_img = request.FILES['img']
        print(type(uploaded_img),"hassam ")
        data  = employees.objects.get(email = request.user)
        data.image = uploaded_img
        data.save()
        messages.add_message(request,messages.SUCCESS,'Image uploaded successfully')
        # Process the uploaded image, save it, or perform any necessary operations
        return JsonResponse({'message': 'Image uploaded successfully'})




@login_required()
@restrict_direct_access
def upload_status(request):
    # print(request.user)
    if request.method=="POST":
        x=datetime.now()
        day =x.strftime("%A") 
        date =x.strftime("%Y-%m-%d") 
        time = x.strftime("%X")
        body_dict =json.loads(request.body)

        # getting employee instance
        emp = employees.objects.get(email=request.user)
        if body_dict["status"]=="Check In":
            try:
                daily_status.objects.get(emp_id=emp,date=date,status="Check In")
                return JsonResponse({"Message":"Already Checked In."})        
            except Exception as err:
                pass
        elif body_dict["status"]=="Check Out":
            try:
                daily_status.objects.get(emp_id=emp,date=date,status="Check In")
            except Exception as err:
                return JsonResponse({"Message":"Please Checked In first."})
            try:
                daily_status.objects.get(emp_id=emp,date=date,status="Check Out")
                return JsonResponse({"Message":"Already Checked Out."})
            except Exception as err:
                pass
        # adding status in database
        daily_status.objects.create(emp_id=emp,day = day,date= date,time = time,status=body_dict["status"])
        if body_dict["status"]=="Check Out":
            s = daily_status.objects.filter(emp_id=emp,date=date)
            for a in s.all():
                print(type(a.time))
                if a.status=="Check In":
                    time_str1=a.time
                elif a.status=="Check Out":
                    time_str2 = a.time
            # Calculate the time difference
            time_difference = timedelta(hours=time_str2.hour,minutes=time_str2.minute,seconds=time_str2.second) - timedelta(hours=time_str1.hour,minutes=time_str1.minute,seconds=time_str1.second)
            # print(type(time_difference))
            daily_hours.objects.create(emp_id = emp,date=date,hours=str(time_difference))
        return JsonResponse({"Message":"status successfully uploaded:"})        



def time_format(time):
    h,m,s = time.split(":")
    if int(h) in range(0,12):
        return h+":"+m+"am"
    else:
        h1 = int(h)%12
        return str(h1)+":"+m+"pm"




def sort_the_data(from_date,to_date,emp):
    temp_dict =dict()
    total_time  =timedelta(hours=0,minutes=0,seconds=0)
    hr = daily_hours.objects.raw(f"select id,date,hours from employees_daily_hours where date <='{to_date}' and date>='{from_date}' and emp_id_id ={emp.emp_id}")
    sta =daily_status.objects.raw(f"select status_id,date,time,status from employees_daily_status where date <='{to_date}' and date>='{from_date}' and emp_id_id ={emp.emp_id}")
    for a in hr:
        total_time += timedelta(hours=a.hours.hour,minutes=a.hours.minute,seconds=a.hours.second)
        temp_dict[str(a.date)]={"hours":a.hours}
    for s_data in sta:
        if s_data.status=="Check In":
            try:
                temp_dict[str(s_data.date)]['Check_In']=time_format((str(s_data.time)))
            except KeyError:
                print("Check In time not found!")
                pass
        elif s_data.status=="Check Out":
            temp_dict[str(s_data.date)]["Check_Out"]=time_format((str(s_data.time)))

    data_dict ={"data":temp_dict,"total_time":str(total_time)}
    return data_dict




@login_required()
@restrict_direct_access
def week_data(request):
    custom_header_value = request.headers
    # 'header-check':"function-request"
    print(custom_header_value["header-check"])
    emp = employees.objects.get(email=request.user)
    x=datetime.now()
    yesterday_date =  (x-timedelta(days=1)).strftime("%Y-%m-%d")
    week_date = (x-timedelta(days=7)).strftime("%Y-%m-%d")
    return JsonResponse(sort_the_data(from_date=week_date,to_date=yesterday_date,emp=emp))


@login_required()
@restrict_direct_access
def month_data(request):
    emp = employees.objects.get(email=request.user)
    x=datetime.now()
    yesterday_date =  (x-timedelta(days=1)).strftime("%Y-%m-%d")
    month_date = (x-timedelta(days=30)).strftime("%Y-%m-%d")
    return JsonResponse(sort_the_data(from_date=month_date,to_date=yesterday_date,emp=emp))


@login_required()
@restrict_direct_access
def year_data(request):
    emp = employees.objects.get(email=request.user)
    x=datetime.now()
    yesterday_date =  (x-timedelta(days=1)).strftime("%Y-%m-%d")
    year_date = (x-timedelta(days=365)).strftime("%Y-%m-%d")
    return JsonResponse(sort_the_data(from_date=year_date,to_date=yesterday_date,emp=emp))



@login_required()
@restrict_direct_access
def filter_data(request):
    body_dict =json.loads(request.body)
    start_date = body_dict["start_date"]
    end_date = body_dict["end_date"]
    emp = employees.objects.get(email=request.user)
    return JsonResponse(sort_the_data(from_date=start_date,to_date=end_date,emp=emp))

