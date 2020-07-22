from django.shortcuts import render, reverse
from .models import Logins, Unlocks
import json
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from djangoProject.mpesa.LipaNaMpesa import lipa_na_mpesa
from MpesaApp.models import LNMOnline2
from django.db.models.signals import post_save

code_signal = {}

def lnm_signal(sender, instance, **kwargs):

    phone_number = instance.PhoneNumber
    amount = instance.Amount
    if instance.paid == False:

        code_signal["phone"] = phone_number
        code_signal["amount"] = amount 
        code_signal["instance_id"]= instance.id
        print(code_signal, "CODE SIGNAL")
    else:
        pass

post_save.connect(lnm_signal, sender=LNMOnline2)


@csrf_exempt
def realtime_validate(request):
    k = json.loads(request.body.decode('utf-8'))
    phone = k["body"]["phone"]
    req_id = k["body"]["req_id"]
    

    print(phone, "from valid pay")
    
    
    data = {}


    if "phone" in  code_signal:
        
        fon = code_signal['phone']
        amount = code_signal['amount']
        instance_id = code_signal["instance_id"]
        print(phone, fon, "this fon numbers")

        if str(phone) == str(fon):

            result1 = LNMOnline2.objects.filter( id = instance_id, paid = False).exists()
            print(result1)


            if result1 == True: 

                result = LNMOnline2.objects.get(id = instance_id, paid = False)
                
                result.paid =True
                result.save()

            if int(amount) <= 50:
                data["message"]= True
                unlock = Unlocks.objects.get(req_id = req_id)

                unlock.status = True
                unlock.save()

            if int(amount) > 50:
                data["message"]= True
                login = Logins.objects.get(req_id = req_id)
                login.status = True
                login.save()

    else:
        print("key phone not in code signal or phone not same")
        data["message"]= False
    
        print(data["message"], "this is data.message")
    code_signal.clear()

    return JsonResponse(data)

@csrf_exempt
def validate_mpesa_code(request):
    code = json.loads(request.body.decode('utf-8'))
    print(code)
    mpesa_code = code["body"]["mpesa_code"]
    req_id = code["body"]["req_id"]
    amount = code["body"]["amount"]
    
    data = {}  
    
    print(mpesa_code)

    if mpesa_code:
        result1 = LNMOnline2.objects.filter( MpesaReceiptNumber__iexact=mpesa_code, paid = False).exists()
        print(result1)


        if result1 == True: 

            result = LNMOnline2.objects.get(MpesaReceiptNumber = mpesa_code, paid = False)
            
            result.paid =True
            result.save()

            if int(amount) == 50:
                data["message"] = "Transaction Successful"
                print("transaction successful")
                unlock = Unlocks.objects.get(req_id = req_id)

                unlock.status = True
                unlock.save()

            if int(amount) > 50:
                data["message"] = "Transaction Successful"
                print("transaction successful")
                login = Logins.objects.get(req_id = req_id)
                login.status = True
                login.save()
                
            
            
            return JsonResponse(data)

        else:

            data["message"] = "Mpesa Code Does not exist"
                
            return JsonResponse(data)

    else:

        data["message"] = "Enter Mpesa Code"
                
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class UnlocksView(generic.CreateView):
    model = Unlocks
    fields = ["full_Names","category", "email", "Url"]
    template_name = "UnlocksApp/unlock.html"



@csrf_exempt
def unlocks_post(request):
    print(request.body)
    k = json.loads(request.body.decode('utf-8'))
    full_Names = k["body"]["full_names"]
    category = k["body"]["category"]
    email = k["body"]["email"]
    url = k["body"]["url"]

    unlock = Unlocks.objects.create(
        # user = request.user,
        full_Names = full_Names,
        category = category,
        email =   email,
        Url =   url  ,
    )
    

    data ={
        "order_id":unlock.req_id,
    }

    return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class LoginsView(generic.CreateView):
    model = Logins
    fields = ["full_Names","category", "email"]
    template_name = "UnlocksApp/logins.html"



@csrf_exempt
def logins_post(request):
    print(request.body)
    k = json.loads(request.body.decode('utf-8'))
    full_Names = k["body"]["full_names"]
    category = k["body"]["category"]
    email = k["body"]["email"]


    login = Logins.objects.create(
        # user = request.user,
        full_Names = full_Names,
        category = category,
        email =   email, 
    )
    

    data ={
        "order_id":login.req_id,
    }

    return JsonResponse(data)



def unlockloginView(request):

    context = {
        "result": "hey you"
    }
    
    return render(request, 'UnlocksApp/unlocklogins.html' ,context)

@csrf_exempt
def Unlock_Mpesa_pay(request):

    data = {}  
    print(request.body, "this is body")
    print(request.body, "this is post")
    data4 = json.loads(request.body.decode('utf-8'))
    phone_number = data4["body"]["phone_number"]
    amount = data4["body"]["amount"]

    callbackurl = request.build_absolute_uri(reverse('MpesaApp:lnm_unlock_callbackurl'))
    print(callbackurl, " this is callbackuri")

    
    print(phone_number)

    
    if phone_number:
        
        try: 
            obj=lipa_na_mpesa(phone_number = phone_number, amount = amount, callbackurl = callbackurl, AccountReference = "123456" )
            obj1 = json.loads(obj)
           
            
               
            data["message"] = obj1
        
            
                
            return JsonResponse(data)
           
                
        except:
            # messages.warning(request, " Type in the correct Phone Number ")
            data[" err_message"] =  " Type in the correct Phone Number "
            return JsonResponse(data)

    else :

        # messages.warning(request, " The form is not valid ")
        data[" err_message"] =  " Type in the correct Phone Number "
        return JsonResponse(data)

