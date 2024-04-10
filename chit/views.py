from django.shortcuts import render
from chit.models import MPin, otp_Registration, User_Management
from django.contrib.auth.models import User
from chit.serializers import User_Serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.authtoken.models import Token
import math, random
from django.utils import six
import base64
from Crypto.Cipher import AES
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse


def get_common_cipher():
    return AES.new(settings.COMMON_ENCRYPTION_KEY,
                   AES.MODE_CBC,
                   settings.COMMON_16_BYTE_IV_FOR_AES)


def index(request):
    return render(request,"home_page.html")


def encrypt_with_common_cipher(cleartext):
    common_cipher = get_common_cipher() 
    cleartext_length = len(cleartext)
    nearest_multiple_of_16 = 16 * math.ceil(cleartext_length/16)
    padded_cleartext = cleartext.rjust(nearest_multiple_of_16)
    raw_ciphertext = common_cipher.encrypt(padded_cleartext.encode("utf8"))
    return base64.b64encode(raw_ciphertext).decode('utf-8')

def decrypt_with_common_cipher(ciphertext):
    common_cipher = get_common_cipher()
    raw_ciphertext = base64.urlsafe_b64decode(ciphertext)
    decrypted_message_with_padding = common_cipher.decrypt(raw_ciphertext)
    return decrypted_message_with_padding.decode('utf-8').strip()

def encrypt(request,input):
    enc = encrypt_with_common_cipher(input)
    user_data={'Encrypted Format':enc}
    return JsonResponse(user_data)

def decrypt(request,input):
    enc = decrypt_with_common_cipher("Gv0aw7HGP4vorJ5zrdgDpgccMO3mRMapjumd/tfvw6fRrmZW7HantwKng3fqJMou+yyIbldMg+u9Ucw3wVkwwQ==")
    user_data={'Encrypted Format':enc}
    return JsonResponse(user_data)

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) 
        )
account_activation_token = TokenGenerator()

def generateOTP() :
	digits = "0123456789"
	OTP = ""
	for i in range(4) :
		OTP += digits[math.floor(random.random() * 10)]
	return OTP


def Registrationotp_phone(request,otp,user_id):
    get_user = User_Management.objects.get(id=user_id)
    if get_user:
          create_OTP = otp_Registration.objects.create(
            user=get_user,
            phone_number_opt = otp

          )   
    return  True



@api_view(['POST'])
def register(request):
    user__name = request.data['user_name']
    email = request.data['Email']
    phone = request.data['mobile_number']
    name_count = User.objects.filter(username = user__name).count()
    if name_count > 0 :
        user_data={"Msg":"Name Already Exists",'status':'false'}
        return Response(user_data)
    Email_count = User.objects.filter(email = email).count()
    if Email_count > 0 :
        user_data={"Msg":"Email Already Exists",'status':'false'}
        return Response(user_data)
    phone_count = User_Management.objects.filter(mobile_number = phone).count()
    if phone_count > 0 :
        user_data={"Msg":"Mobile Number Already Exists",'status':'false'}
        return Response(user_data)
    User_Management.objects.create(user_name=user__name,Email=email,mobile_number=phone)
    user_data = {"Msg": "OTP Send Successful",'status': 'true'}
    return Response(user_data)

@api_view(['POST'])
def send_otp(request):
    phone_number=request.data['number']
    user_details = User_Management.objects.get(mobile_number = phone_number)
    otp = generateOTP()
    Registrationotp_phone(request,otp,user_details.id)
    user_data = {"Msg": "OTP Send Successful", 'status': 'true'}
    return Response(user_data)


@api_view(['POST'])
def otp_verfication(request):
    phone_number=request.data['number']
    OTP_user = request.data['OTP']
    user_details = User_Management.objects.get(mobile_number = phone_number)
    user_otp = otp_Registration.objects.get(user = user_details.id)
    if int(user_otp.phone_number_opt) == int(OTP_user):
        user = User.objects.create(username=user_details.user_name,email=user_details.Email)
        token = Token.objects.create(user=user)
        user_data = {"Msg":"OTP Verified","status":"true",'token':token.key}
        return Response(user_data)
    else:
        user_data = {"Msg":"Invalid OTP","status":"false"}
        return Response(user_data)
    
@api_view(['POST'])
def create_mpin(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    pin = request.data['MPIN']
    user_details = User_Management.objects.get(user_name = token.user)
    create_pin = MPin.objects.create(user = user_details,status = 1,pin=pin)
    user_data = {"Msg":"MPIN Create Sccessful","status":"true",'token':token.key}
    return Response(user_data)

@api_view(['POST'])
def mpin_verfication(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_mpin = request.data['MPIN']
    user_details = User_Management.objects.get(user_name = token.user)
    mpin_user = MPin.objects.get(user = user_details.id)
    if int(mpin_user.pin) == int(user_mpin):
        user_data = {"Msg":"Login Successful","status":"true",'token':token.key}
        return Response(user_data)
    else:
        user_data = {"Msg":"Invalid MPIN","status":"false"}
        return Response(user_data)


@api_view(['POST'])
def forget_mpin(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    new_pin = request.data['new_pin']
    confirm_pin = request.data['confirm_pin']
    user_details = User_Management.objects.get(user_name = token.user)
    mpin_user = MPin.objects.get(user = user_details.id)
    if int(new_pin) == int(mpin_user.pin):
        user_data={"Msg":"You Cannot set Old Pin as New Pin",'status':'false'}
        return Response(user_data)
    else:
        if int(new_pin) == int(confirm_pin):
            mpin_user.pin = new_pin
            mpin_user.save()
            user_data={"Msg":"Pin Updated",'status':'true','token':token.key}
            return Response(user_data)
        else:
            user_data={"Msg":"Pin Mismatch",'status':'false'}
            return Response(user_data)
        



@api_view(['POST'])
def user_login(request):
    Token_header = request.headers['Token']
    token = Token.objects.get(key = Token_header)
    user_details = User_Management.objects.get(user_name = token.user)
    phone = request.data['mobile_number']
    if phone != user_details.mobile_number :
        user_data={"Msg":"Invalid Mobile Number",'status':'false'}
        return Response(user_data)
    user_data = {"Msg": "OTP Send Successful", 'status': 'true', 'token': token.key}
    return Response(user_data)

