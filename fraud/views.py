from datetime import datetime
import random
import string
from .serializer import *
from .models import *
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT
from rest_framework.authtoken.serializers import AuthTokenSerializer
from paymob.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests

def check_in_BL(serializer,type1):
    #description
    """
        check if object with this *data* in Black list
        args:-
            serializer --> Transaction serializer if check use in send transaction (no type field)
                                                    OR
                        Blacklist Transaction  if check in add to Black List (come with type field of black list)
                        
            type1 -->   this is type field add if we search when (do Action) if this row with this type (return *found=True*) 
                        and active object if deactive in leter using (return *object*)
        returns:-
            found: if data is exist
            status: if data found and data active
            message: note
            object: if object found -> return object
    """
    if serializer.is_valid(): 
        #attributes
        name=serializer.validated_data['name']
        email=serializer.validated_data['email']
        phone=serializer.validated_data['phone']  
        card_num=serializer.validated_data['card_num']
        merchant=serializer.validated_data['merchant']
        ip=serializer.validated_data['ip']
        if("type" in serializer.validated_data):
            type=serializer.validated_data['type']
        elif(type1!=""):
            type=type1
        else:
            type=""
        #blacklist data
        blacklist=Blacklist.objects.all()
        #checkers
        status=False
        found=False
        object=None
        message=""
        if (type!=""):
            #check in add to black list and do action
            if (blacklist.filter(type='ip',ip=ip,merchant=merchant).exists()==True and type=='ip'):
                object=blacklist.get(type='ip',ip=ip,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True
                message="IP in BL of merchant : "+merchant+"-" 
                return status,message,found,object  
            if (blacklist.filter(type='name',name=name,merchant=merchant).exists()==True and type=='name'):
                object=blacklist.get(type='name',name=name,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True
                message="client in BL of merchant : "+merchant+"-"
                return status,message,found,object   
            if (blacklist.filter(type='email',email=email,merchant=merchant).exists()==True and type=='email'):
                object=blacklist.get(type='email',email=email,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True 
                message="email in BL of merchant : "+merchant+"-"
                return status,message,found,object 
            if (blacklist.filter(type='phone',phone=phone,merchant=merchant).exists()==True and type=='phone'):
                object=blacklist.get(type='phone',phone=phone,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True
                message="phone in BL of merchant : "+merchant+"-"
                return status,message,found,object 
            if (blacklist.filter(type='card_num',card_num=card_num,merchant=merchant).exists()==True and type=='card_num'):
                object=blacklist.get(type='card_num',card_num=card_num,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True
                message="card-num in BL of merchant : "+merchant+"-"
                return status,message,found,object 
        else:
            if(blacklist.filter(type='ip',ip=ip,merchant=merchant,active=True).exists()==True):
                status=True
                message="IP in BL of merchant : "+merchant+"-"
                return status,message,found,object 
            if(blacklist.filter(type='name',name=name,merchant=merchant,active=True).exists()==True):
                status=True
                message="client in BL of merchant : "+merchant+" -"
                return status,message,found,object 
            if(blacklist.filter(type='email',email=email,merchant=merchant,active=True).exists()==True):
                status=True
                message="email in BL of merchant : "+merchant+" -"
                return status,message,found,object 
            if(blacklist.filter(type='phone',phone=phone,merchant=merchant,active=True).exists()==True):
                status=True
                message="phone in BL of merchant : "+merchant+" -"
                return status,message,found,object 
            if(blacklist.filter(type='card_num',card_num=card_num,merchant=merchant,active=True).exists()==True):
                status=True
                message="card-num in BL of merchant : "+merchant+" -"
                return status,message,found,object 
        return status,message,found,object       
def check_in_GBL(serializer,type1):
    #like as check_in_BL but in Global Black list
    if serializer.is_valid(): 
        #attributes
        name=serializer.validated_data['name']
        email=serializer.validated_data['email']
        phone=serializer.validated_data['phone']  
        card_num=serializer.validated_data['card_num']
        ip=serializer.validated_data['ip']
        if("type" in serializer.validated_data):
            type=serializer.validated_data['type']
        elif(type1!=""):
            #if send from doAction method to check if found
            type=type1
        else:
            type=""
        #blacklist data
        blacklist=GlobalBlacklist.objects.all()
        #checkers
        status=False
        found=False
        object=None
        message=""
        if(type!=""):
            if (blacklist.filter(type='ip',ip=ip).exists()==True and type=='ip'):
                object=blacklist.get(type='ip',ip=ip)
                found=True
                if (object.active==True):
                    status=True
                message="IP in Global Black-List"
                return status,message,found,object
            if (blacklist.filter(type='name',name=name).exists()==True and type=='name'):
                object=blacklist.get(type='name',name=name)
                found=True
                if (object.active==True):
                    status=True
                message="client in Global Black-List"
                return status,message,found,object  
            if (blacklist.filter(type='email',email=email).exists()==True and type=='email'):
                object=blacklist.get(type='email',email=email)
                found=True
                if (object.active==True):
                    status=True 
                message="email in Global Black-List"
                return status,message,found,object
            if (blacklist.filter(type='phone',phone=phone).exists()==True and type=='phone'):
                object=blacklist.get(type='phone',phone=phone)
                found=True
                if (object.active==True):
                    status=True
                message="phone in Global Black-List"
                return status,message,found,object
            if (blacklist.filter(type='card_num',card_num=card_num).exists()==True and type=='card_num'):
                object=blacklist.get(type='card_num',card_num=card_num)
                found=True
                if (object.active==True):
                    status=True
                message="card-num in Global Black-List"
                return status,message,found,object
        else:
            if (blacklist.filter(type='ip',ip=ip,active=True).exists()==True):
                status=True
                message="IP in Global Black-List"
                return status,message,found,object
            if (blacklist.filter(type='name',name=name,active=True).exists()==True):
                status=True
                message="client in Global Black-List"
                return status,message,found,object 
            if (blacklist.filter(type='email',email=email,active=True).exists()==True):
                status=True
                message="email in Global Black-List"
                return status,message,found,object
            if (blacklist.filter(type='phone',phone=phone,active=True).exists()==True):
                status=True
                message="phone in Global Black-List"
                return status,message,found,object
            if (blacklist.filter(type='card_num',card_num=card_num,active=True).exists()==True):
                status=True
                message="card-num in Global Black-List"
                return status,message,found,object
        return status,message,found,object
def check_in_WL(serializer):
    #like as check_in_BL but without arg(type1) because (check_in_WL) dont use in (do_action)
    if serializer.is_valid(): 
        #attributes
        name=serializer.validated_data['name']
        email=serializer.validated_data['email']
        phone=serializer.validated_data['phone']  
        card_num=serializer.validated_data['card_num']
        merchant=serializer.validated_data['merchant']
        ip=serializer.validated_data['ip']
        if("type" in serializer.validated_data):
            type=serializer.validated_data['type']
        else:
            type=""
        #white List data
        whitelist=Whitelist.objects.all()
        #checkers
        status=False
        found=False
        object=None
        message=""
        if (type!=""):
            if (whitelist.filter(type='ip',ip=ip,merchant=merchant).exists()==True and type=='ip'):
                object=whitelist.get(type='ip',ip=ip,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True
                message="IP in WL of merchant : "+merchant+" -"
                return status,message,found,object
            if (whitelist.filter(type='name',name=name,merchant=merchant).exists()==True and type=='name'):
                object=whitelist.get(type='name',name=name,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True
                message="client in WL of merchant : "+merchant+" -"
                return status,message,found,object
            if (whitelist.filter(type='email',email=email,merchant=merchant).exists()==True and type=='email'):
                object=whitelist.get(type='email',email=email,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True 
                message="email in WL of merchant : "+merchant+" -"
                return status,message,found,object
            if (whitelist.filter(type='phone',phone=phone,merchant=merchant).exists()==True and type=='phone'):
                object=whitelist.get(type='phone',phone=phone,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True
                message="phone in WL of merchant : "+merchant+" -"
                return status,message,found,object
            if (whitelist.filter(type='card_num',card_num=card_num,merchant=merchant).exists()==True and type=='card_num'):
                object=whitelist.get(type='card_num',card_num=card_num,merchant=merchant)
                found=True
                if (object.active==True):
                    status=True
                message="card-num in BL of merchant : "+merchant+" -"
                return status,message,found,object
        else:
            if(whitelist.filter(type='ip',ip=ip,merchant=merchant,active=True).exists()==True):
                status=True
                message="IP in WL of merchant : "+merchant+" -"
                return status,message,found,object
            if(whitelist.filter(type='name',name=name,merchant=merchant,active=True).exists()==True):
                status=True
                message="client in WL of merchant : "+merchant+" -"
                return status,message,found,object
            if(whitelist.filter(type='email',email=email,merchant=merchant,active=True).exists()==True):
                status=True
                message="email in WL of merchant : "+merchant+" -"
                return status,message,found,object
            if(whitelist.filter(type='phone',phone=phone,merchant=merchant,active=True).exists()==True):
                status=True
                message="phone in WL of merchant : "+merchant+" -"
                return status,message,found,object
            if(whitelist.filter(type='card_num',card_num=card_num,merchant=merchant,active=True).exists()==True):
                status=True
                message="card-num in WL of merchant : "+merchant+" -"
                return status,message,found,object
        return status,message,found,object       
def check_in_GWL(serializer):
    
    if serializer.is_valid(): 
        #attributes
        name=serializer.validated_data['name']
        email=serializer.validated_data['email']
        phone=serializer.validated_data['phone']  
        card_num=serializer.validated_data['card_num']
        ip=serializer.validated_data['ip']
        if ("type" in serializer.validated_data):
            type=serializer.validated_data['type']
        else:
            type=""
        #Global white List data
        whitelist=GlobalWhitelist.objects.all()
        #checkers
        status=False
        found=False
        object=None
        message=""
        if(type!=""):
            if (whitelist.filter(type='ip',ip=ip).exists()==True and type=='name'):
                object=whitelist.get(type='ip',ip=ip)
                found=True
                if (object.active==True):
                    status=True
                message="IP in Global white-List"
                return status,message,found,object  
            if (whitelist.filter(type='name',name=name).exists()==True and type=='name'):
                object=whitelist.get(type='name',name=name)
                found=True
                if (object.active==True):
                    status=True
                message="client in Global white-List"
                return status,message,found,object  
            if (whitelist.filter(type='email',email=email).exists()==True and type=='email'):
                object=whitelist.get(type='email',email=email)
                found=True
                if (object.active==True):
                    status=True 
                message="email in Global white-List"
                return status,message,found,object
            if (whitelist.filter(type='phone',phone=phone).exists()==True and type=='phone'):
                object=whitelist.get(type='phone',phone=phone)
                found=True
                if (object.active==True):
                    status=True
                message="phone in Global white-List"
                return status,message,found,object
            if (whitelist.filter(type='card_num',card_num=card_num).exists()==True and type=='card_num'):
                object=whitelist.get(type='card_num',card_num=card_num)
                found=True
                if (object.active==True):
                    status=True
                message="card-num in Global white-List"
                return status,message,found,object
        else:
            if(whitelist.filter(type='ip',ip=ip,active=True).exists()==True):
                status=True
                message="IP in Global white-List"
                return status,message,found,object
            if(whitelist.filter(type='name',name=name,active=True).exists()==True):
                status=True
                message="client in Global white-List"
                return status,message,found,object
            if(whitelist.filter(type='email',email=email,active=True).exists()==True):
                status=True
                message="email in Global white-List"
                return status,message,found,object
            if(whitelist.filter(type='phone',phone=phone,active=True).exists()==True):
                status=True
                message="phone in Global white-List"
                return status,message,found,object
            if(whitelist.filter(type='card_num',card_num=card_num,active=True).exists()==True):
                status=True
                message="card-num in Global white-List"
                return status,message,found,object
        return status,message,found,object

def activeObject(object):
    #active object if object in blacklist but not active
    if object.active==False:
        object.active=True
        object.save()
        message="re-active object - "
        return message

def doAction(serializer,actions):
    serializer.is_valid(raise_exception=True)
    ip=serializer.validated_data['ip']
    name=serializer.validated_data['name']
    email=serializer.validated_data['email']
    phone=serializer.validated_data['phone']
    card_num=serializer.validated_data['card_num']
    merchant=serializer.validated_data['merchant']
    message=""
    status=True
    for action in actions:
        if action.name=='accept transaction' and action.active:
            #make transaction status==True
            message=message+"Transiction accepted - "
            status=True
            continue
        if action.name=='block transaction' and action.active:
            #make transaction status==False
            message=message+"Transiction not accepted - "
            status=False
            continue
        if action.name=='global block email' and action.active:
            result=check_in_GBL(serializer,"email") #status,message,found,object
            if (result[2]==True):
                #if object found --> reactive 
                message=message+str(result[1])+activeObject(result[3])
            else:
                GlobalBlacklist.objects.create(type='email',ip=ip,email=email,name=name,phone=phone,card_num=card_num)
                message=message+"email added to GB - "
            continue
        if action.name=='global block phone' and action.active:
            result=check_in_GBL(serializer,"phone") 
            if (result[2]==True):
                message=message+str(result[1])+activeObject(result[3])
            else:
                GlobalBlacklist.objects.create(type='phone',ip=ip,email=email,name=name,phone=phone,card_num=card_num)
                message=message+"phone added to GB - "
            continue
        if action.name=='global block card number' and action.active:
            result=check_in_GBL(serializer,"card_num")
            if (result[2]==True):
                message=message+str(result[1])+activeObject(result[3])
            else:
                GlobalBlacklist.objects.create(type='card_num',ip=ip,email=email,name=name,phone=phone,card_num=card_num)
                message=message+"card-num added to GB - "
            continue
        if action.name=='global block client' and action.active:
            result=check_in_GBL(serializer,"name") 
            if (result[2]==True):
                message=message+str(result[1])+activeObject(result[3])
            else:
                GlobalBlacklist.objects.create(type='name',ip=ip,email=email,name=name,phone=phone,card_num=card_num)
                message=message+"name added to GB - "
            continue
        if action.name=='global block ip' and action.active:
            result=check_in_GBL(serializer,"ip")
            if (result[2]==True):
                message=message+str(result[1])+activeObject(result[3])
            else:
                GlobalBlacklist.objects.create(type='ip',ip=ip,email=email,name=name,phone=phone,card_num=card_num)
                message=message+"IP added to GB - "
            continue
        if action.name=='block client' and action.active:
            result=check_in_BL(serializer,"name")
            if (result[2]==True):
                message=message+str(result[1])+activeObject(result[3])
            else:
                Blacklist.objects.create(type='name',ip=ip,email=email,name=name,phone=phone,card_num=card_num,merchant=merchant)
                message=message+"client added to BL - "
            continue
        if action.name=='block card number' and action.active:
            result=check_in_BL(serializer,"card_num")
            if (result[2]==True):
                message=message+str(result[1])+activeObject(result[3])
            else:
                Blacklist.objects.create(type='card_num',ip=ip,email=email,name=name,phone=phone,card_num=card_num,merchant=merchant)
                message=message+"card-num added to BL - "
            continue
        if action.name=='block email' and action.active:
            result=check_in_BL(serializer,"email") 
            if (result[2]==True):
                message=message+str(result[1])+activeObject(result[3])
            else:
                Blacklist.objects.create(type='email',ip=ip,email=email,name=name,phone=phone,card_num=card_num,merchant=merchant)
                message=message+"email added to BL - "
            continue
        if action.name=='block phone' and action.active:
            result=check_in_BL(serializer,"phone")
            if (result[2]==True):
                message=message+str(result[1])+activeObject(result[3])
            else:
                Blacklist.objects.create(type='phone',ip=ip,email=email,name=name,phone=phone,card_num=card_num,merchant=merchant)
                message=message+"phone added to BL - "
            continue
        if action.name=='block ip' and action.active:
            result=check_in_BL(serializer,"ip")
            if (result[2]==True):
                message=str(result[1])+activeObject(result[3])
            else:
                Blacklist.objects.create(type='ip',ip=ip,email=email,name=name,phone=phone,card_num=card_num,merchant=merchant)
                message=message+"IP added to BL - "
            continue
    
    return status,message

def compare_checker( count,value,compare_type ):
    if((compare_type=='more than' and count>value) or
        (compare_type=='less than' and count<value) or
        (compare_type=='equal' and count==value) or
        (compare_type=='more than or equal' and count>=value) or
        (compare_type=='less than or equal' and count<=value)):
        print("compare_checker: True")
        return True
    print("compare_checker: False")
    return False

def check_in_WL_response(serializer):
    serializer.is_valid(raise_exception=True)
    result=check_in_WL(serializer)
    status=result[0]
    message=str(result[1])
    if status==True:
        serializer.validated_data['transaction_status']=True
        serializer.validated_data['message']=message
        serializer.save()
        return Response({'status':"succes",'message':message},HTTP_200_OK)
    else:
        return False
def check_in_GWL_response(serializer):
    serializer.is_valid(raise_exception=True)
    result=check_in_GWL(serializer) #status,
    status=result[0]
    message=result[1]
    if status==True:
        serializer.validated_data['transaction_status']=True
        serializer.validated_data['message']=message
        serializer.save()
        return Response({'status':"succes",'message':message},HTTP_200_OK)
    else:
        return False
def check_in_GBL_response(serializer): 
    serializer.is_valid(raise_exception=True)
    #attributes
    result=check_in_GBL(serializer,"")
    status=result[0]
    message=result[1]
    if status==True:
        serializer.validated_data['transaction_status']=False
        serializer.validated_data['message']=message
        serializer.save()
        return Response({'status':"fail",'message':message},HTTP_400_BAD_REQUEST)
    else:
        return False
def check_in_BL_response(serializer):
    serializer.is_valid(raise_exception=True)
    result=check_in_BL(serializer,"")
    status=result[0]
    message=result[1]
    if status==True:
        serializer.validated_data['transaction_status']=False
        serializer.validated_data['message']=message
        serializer.save()
        return Response({'status':"fail",'message':message},HTTP_400_BAD_REQUEST)
    return False
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def is_VPN(ip):
    if ip=="":
        ip='8.8.8.8'
    backend_url="https://vpnapi.io/api/"+str(ip)+'?key=84dabe28108a4e989102c4dea54cae0b'
    response=requests.get(backend_url)
    response_data=response.json()
    if('security' in response_data):
        if(response_data['security']['vpn']==True):
            return True
    return False
def check_conditions(conditions,serializer):
    #description
    """
        args:
            conditions: list of conditions of a rule
            serializer: serializer of the transaction
        description:
            method take 2 arguments, conditions and serializer
            and create variable (count_condition) to count the number of conditions
            then it loop on the conditions and check if the condition is true or false
            using method (compare_checker) and if the condition is true it decrease (count_condition)
            - if one of conditions is false it break loop and return 
        return:
            count_condition: if count_condition=0 it means all conditions are true
                             else it means one of conditions is false
    """
    serializer.is_valid(raise_exception=True)
    count_conditions=len(conditions)
    print ("count_conditions",count_conditions)
    for condition in conditions :
        print("condition type",condition.type)
        if condition.type=='VPN':
            ip=serializer.validated_data['ip']
            if(is_VPN(ip)==True):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='amount':
            amount=serializer.validated_data['amount']
            print("amount",amount,"value",condition.value,"compare_type",condition.compare_type)
            if (compare_checker(amount,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        
        if condition.type=='num refuse transaction with card number today':
            card_num=serializer.validated_data['card_num']
            #count false with card today
            count=Transaction.objects.filter(card_num=card_num,transaction_status=False,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                print("compare_checker")
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num refuse transaction with email today':
            email=serializer.validated_data['email']
            #count false with email today
            count=Transaction.objects.filter(email=email,transaction_status=False,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num refuse transaction with phone today':
            phone=serializer.validated_data['phone']
            #count false with phone today
            count=Transaction.objects.filter(phone=phone,transaction_status=False,created_at__date=datetime.now().date()).count()
            print("count",count)
            if (compare_checker(count,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num refuse transaction with name today':
            name=serializer.validated_data['name']
            #count false with name today
            count=Transaction.objects.filter(name=name,transaction_status=False,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num refuse transaction with ip today':
            ip=serializer.validated_data['ip']
            #count false with card today
            count=Transaction.objects.filter(ip=ip,transaction_status=False,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                print("compare_checker")
                count_conditions-=1
                continue
            else:
                break
        
        if condition.type=='num transaction with card number today':
            card_num=serializer.validated_data['card_num']
            #count false with card today
            count=Transaction.objects.filter(card_num=card_num,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                print("compare_checker")
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num transaction with email today':
            email=serializer.validated_data['email']
            #count transactions with email today
            count=Transaction.objects.filter(email=email,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num transaction with phone today':
            phone=serializer.validated_data['phone']
            #count T with phone today
            count=Transaction.objects.filter(phone=phone,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num transaction with name today':
            name=serializer.validated_data['name']
            #count T with name today
            count=Transaction.objects.filter(name=name,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num transaction with ip today':
            ip=serializer.validated_data['ip']
            #count T with card today
            count=Transaction.objects.filter(ip=ip,created_at__date=datetime.now().date()).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                count_conditions-=1
                continue
            else:
                break
        
        if condition.type=='num refuse transaction with card number month':
            card_num=serializer.validated_data['card_num']
            #count false with card month
            count=Transaction.objects.filter(card_num=card_num,transaction_status=False,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                print("compare_checker")
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num refuse transaction with email month':
            email=serializer.validated_data['email']
            #count false with email month
            count=Transaction.objects.filter(email=email,transaction_status=False,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num refuse transaction with phone month':
            phone=serializer.validated_data['phone']
            #count false with phone month
            count=Transaction.objects.filter(phone=phone,transaction_status=False,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num refuse transaction with name month':
            name=serializer.validated_data['name']
            #count false with name month
            count=Transaction.objects.filter(name=name,transaction_status=False,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num refuse transaction with ip month':
            ip=serializer.validated_data['ip']
            #count false with card month
            count=Transaction.objects.filter(ip=ip,transaction_status=False,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                print("compare_checker")
                count_conditions-=1
                continue
            else:
                break
        
        if condition.type=='num transaction with card number month':
            card_num=serializer.validated_data['card_num']
            #count transactions with card_num on current month
            count=Transaction.objects.filter(card_num=card_num,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                print("compare_checker")
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num transaction with email month':
            email=serializer.validated_data['email']
            #count transactions with email on current month
            count=Transaction.objects.filter(email=email,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num transaction with phone month':
            phone=serializer.validated_data['phone']
            #count transactions with phone on current month
            count=Transaction.objects.filter(phone=phone,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num transaction with name month':
            name=serializer.validated_data['name']
            #count transactions with name on current month
            count=Transaction.objects.filter(name=name,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)):
                count_conditions-=1
                continue
            else:
                break
        if condition.type=='num transaction with ip month':
            ip=serializer.validated_data['ip']
            #count transactions with email on current month
            count=Transaction.objects.filter(ip=ip,created_at__month=datetime.now().month).count()
            if (compare_checker(count,condition.value,condition.compare_type)): 
                count_conditions-=1
                continue
            else:
                break
        
    return int(count_conditions)
   
   
   
    # {
#     "name":"moahmed",
#     "card_num":"66",
#     "phone":"012",
#     "email":"a@asd.com",
#     "ip":"",
#     "merchant":"khaled",
#     "amount":"1500"
# }
def add_review(data):
    serializer = ReviewSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
class Send_transaction(APIView):
    permission_classes=[AllowAny]
    #description
    """
        description:
            send transaction make in 3 steps
            1. check if the transaction is in white_list or black_list or global_white_list or global_black_list
                - if check in white_list or global_white_list 
                    accept transaction and save it in database
                - if check in black_list or global_black_list
                    refuse transaction and save it in database
                
            2. if (1) done and transaction not (accept or refuse) --> get active rules
            3. loop on rules 
            4. check conditions of rule if all is true then apply actions of rule and break loop
            5. if all rules is false then save transaction and return success (no rule applied)
            
    """
    def post(self, request):
        serializer = TransctionSerializer(data=request.data)
        
        if serializer.is_valid():
            print ("send_transaction")
            response=check_in_WL_response(serializer)
            if response!=False: #found in WL
                return response
            response=check_in_BL_response(serializer)
            if response!=False: #found in BL
                return response
            response=check_in_GWL_response(serializer)
            if response!=False: #found in GWL
                return response
            response=check_in_GBL_response(serializer)
            if response!=False: #found in GBL
                return response
            
            rules=Rule.objects.filter(active=True).order_by('priority')
            if rules.count()>0:
                print("rule",rules)
                rule_name=""
                result=['True','No rule applied']
                for rule in rules :
                    
                    conditions=rule.condition.all()
                    conditions=conditions.filter(active=True)
                    count_conditions=check_conditions(conditions,serializer)
                    print("count_conditions222 :",count_conditions)
                    if count_conditions==0:
                        actions=rule.action.all()
                        actions=actions.filter(active=True)
                        result=doAction(serializer,actions)
                        rule_name=rule.name
                        break
                status=result[0]
                message=result[1]
                
                serializer.validated_data['rule']=rule_name
                serializer.validated_data['transaction_status']=status
                if (rule_name!=""):
                    if "add to review" in rule_name.action.all().values_list('name',flat=True):
                        add_review(serializer.validated_data)   
                        message=message+" add to review"
                    
                serializer.validated_data['message']=message
                serializer.save()
                if status==False:
                    return Response({'status':"fail",'message':message},HTTP_400_BAD_REQUEST)
                else:
                    return Response({'status':"success",'message':message},HTTP_200_OK)
            
            else:
                serializer.validated_data['transaction_status']=True
                message=serializer.validated_data['message']="Transiction accepted *no rules found"
                print("message",message)
                serializer.save()
                return Response({'status':"success","message":message},HTTP_200_OK)
        else:
            return Response({'status':"fail",'message':"serializer.errors"+str(serializer.errors)},HTTP_400_BAD_REQUEST)

class List_transaction(generics.ListAPIView):
    #list all transactions
    queryset=Transaction.objects.all()
    serializer_class=TransctionSerializer
    
class List_review_transaction(generics.ListAPIView):
    #list all transactions that need review
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
class Add_to_blacklist(generics.ListCreateAPIView):
    queryset=Blacklist.objects.all()
    serializer_class=BlacklistSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result=check_in_BL(serializer,"")
            status=result[0]
            message=result[1]
            found=result[2]
            object=result[3]
            print("status",status)
            print("message",message)
            print("found",found)
            if(found==True and status==False): #found in BL but not active
                return Response({"message":"object found in BL and "+ activeObject(object)+" -","status":"success"},HTTP_200_OK)
            elif(found==True and status==True): #found in BL and active
                return Response({"message":message,"status":"success"},HTTP_200_OK)
            else:
                serializer.save()
                return Response({'message':"data added to blacklist","status":"success"},HTTP_200_OK)
        else:
            return Response({'message':"serializer.errors"+str(serializer.errors),"status":"fail"},HTTP_400_BAD_REQUEST) 
class Add_to_whitelist(generics.ListCreateAPIView):
    queryset=Whitelist.objects.all()
    serializer_class=WhitelistSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result=check_in_WL(serializer=serializer)
            status=result[0]
            message=result[1]
            found=result[2]
            object=result[3]
            if(found==True and status==False):
                object.active=True
                object.save()
                return Response({"message":"record found in WL and " + activeObject(object)+" - ","status":"success"},HTTP_200_OK)
            elif(found==True and status==True):
                return Response({"message":message,"status":"success"},HTTP_200_OK)
            else:
                serializer.save()
                return Response({'message':"data added to White List","status":"success"},HTTP_200_OK)
        else:
            return Response({'message':"serializer.errors"+str(serializer.errors),"status":"fail"},HTTP_400_BAD_REQUEST)
class Add_to_global_blacklist(generics.ListCreateAPIView):
    queryset=GlobalBlacklist.objects.all()
    serializer_class=GlobalBlacklistSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            result=check_in_GBL(serializer,"")
            status=result[0]
            message=result[1]
            found=result[2]
            object=result[3]
            if(found==True and status==False):
                object.active=True
                object.save()
                return Response({"message":"record found in GBL and "+activeObject(object)+ " - ","status":"success"},HTTP_200_OK)
            elif(found==True and status==True):
                return Response({"message":message,"status":"success"},HTTP_200_OK)
            else:
                serializer.save()
                return Response({'message':"data added to Global Blacklist","status":"success"},HTTP_200_OK)
        else:
            return Response({'message':"serializer.errors"+str(serializer.errors),"status":"fail"},HTTP_400_BAD_REQUEST)
class Add_to_global_whitelist(generics.ListCreateAPIView):
    queryset=GlobalWhitelist.objects.all()
    serializer_class=GlobalWhitelistSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid):
            result=check_in_GWL(serializer=serializer)
            status=result[0]
            message=result[1]
            found=result[2]
            object=result[3]
            if(found==True and status==False):
                object.active=True
                object.save()
                return Response({"message":"record found in GWL and "+ activeObject(object)+" - ","status":"success"},HTTP_200_OK)
            elif(found==True and status==True):
                return Response({"message":message,"status":"success"},HTTP_200_OK)
            else:
                serializer.save()
                return Response({'message':"data added to Global White List","status":"success"},HTTP_200_OK)
        else:
            return Response({'message':"serializer.errors"+str(serializer.errors),"status":"fail"},HTTP_400_BAD_REQUEST)


def generate_password():
    return ''.join(random.choice(string.ascii_uppercase+ string.digits +string.ascii_lowercase) for _ in range(8))
    
    
class Change_password(APIView):
    serializer_class=ChangePasswordSerializer
    def post(self,request):
        if (request.user.is_authenticated):
            serializer=self.serializer_class(data=request.data)
            if serializer.is_valid():
                if not request.user.check_password(serializer.data.get("old_password")):
                    return Response({"message":"old password is incorrect","status":"fail"},HTTP_400_BAD_REQUEST)
                request.user.set_password(serializer.data.get("password"))
                request.user.save()
                return Response({"message":"password changed successfully","status":"success"},HTTP_200_OK)
            else:
                return Response({"message":"error: "+str(serializer.errors),"status":"fail"},HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"user not logged in","status":"fail"},HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email=request.data.get("email")
    if (User.objects.filter(email=email).exists()):
        user=User.objects.get(email=email)
        password=generate_password()
        subject = 'Your Paymob New Password is '+str(password)
        htmlMessage=render_to_string('reset_password_email.html',{'password': password,'image_src':"https://cms.almalnews.com/wp-content/uploads/2020/08/PAY-MOB-1024x628.png"})
        text=strip_tags(htmlMessage)
        to = str(email)
        mail=EmailMultiAlternatives(subject,text,EMAIL_HOST_USER, [to])
        mail.attach_alternative(htmlMessage, "text/html")
        try:
            mail.send()
        except Exception as e:
            return Response({'status':'fail','message':'Email not sent try again later '+ str(e) },status=400)
        user.set_password(password)
        user.save()
        return Response({'status':'success','message':'Reset Password Done and Email has been sent'},status=200)
    else:
        return Response({'status':'fail','message':'Email not found'},status=400)
               
@api_view(['POST'])
@permission_classes([AllowAny])
def login_API(request):
    serializer=AuthTokenSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.validated_data['user']
        token=Token.objects.get_or_create(user=user)
        
        return Response({'status':'success',
            'userInfo':{
            'id':user.id,
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            },
            'token':token[0].key
            },status=200)
    else:
        return Response({'status':'fail','message':'Invalid username or password'},status=400)

@api_view(['POST'])    
@permission_classes([AllowAny])
def sign_up_API(request):
    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid():
        password=generate_password()
        username=serializer.validated_data['username']
        email=serializer.validated_data['email']
        first_name=serializer.validated_data['first_name']
        last_name=serializer.validated_data['last_name']
        user = User.objects.create(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
        )
        
        #send email to the user
        subject = 'Welcome in PayMob Froud System'
        htmlMessage=render_to_string('signup_email.html',{'password': password,'image_src':"https://cms.almalnews.com/wp-content/uploads/2020/08/PAY-MOB-1024x628.png"})
        text=strip_tags(htmlMessage)
        to = str(email)
        mail=EmailMultiAlternatives(subject,text,EMAIL_HOST_USER, [to])
        mail.attach_alternative(htmlMessage, "text/html")
        try:
            mail.send()
        except Exception as e:
            user.delete()
            return Response({'status':'fail','message':'Email not sent '+ str(e) },status=400)
        user.set_password(password)
        user.save()
        return Response({'status':'success','message':'User created successfully Password Send To Email'},status=200)
    else:
        return Response({'status':'fail','message':serializer.errors},status=400)