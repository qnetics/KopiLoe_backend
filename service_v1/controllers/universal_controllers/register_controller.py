from json import loads
from datetime import date

from django.core import serializers

from service_v1.models import user_model 
from service_v1.utils.hashing_password import hashing
from service_v1.validations.register_validations import register_validations


def register_controller (body_request) :

    # payload validation
    if not (register_validations()
        .payload_validation(request = body_request)) :

        http_status_code : int = 400
        message_response : str =  "Brosist.... Isi yang bener dong formulir -nya."
        data_response    : dict = {}


    # email validation
    elif user_model.objects.filter(email = body_request["email"]).exists() :

        http_status_code : int = 400
        message_response : str =  "Yahhh.. Email yang kamu daftarkan telah digunakan, gunakan email lain untuk mendaftar."
        data_response    : dict = {}


    else :

        create_user = user_model.objects.create(

            username   = body_request["username"],
            password   = hashing(body_request["password"]),
            email      = body_request["email"],
            is_admin   = False,
            verified   = False,
            last_login = date.today()

        )
            
        message_response : str = "Selamat, anda berhasil terdaftar"
        http_status_code : int = 201
        data_response = loads(
            serializers.serialize('json', [create_user]))[0]["fields"]  


    return http_status_code, message_response, data_response