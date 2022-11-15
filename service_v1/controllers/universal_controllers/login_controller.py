from json import loads

from django.core import serializers 

from service_v1.models import user_model, user_auth_model

from service_v1.validations.login_validations import login_validations

from service_v1.utils.hashing_password import hashing
from service_v1.utils.timestamp_generator import generate_timestamp
from service_v1.utils.generate_token import generate_access_refresh_token
from service_v1.utils.expired_token_checker import expired_checker


###
### Login Controller
###
def login_controller (body_request) :

    # payload validation
    if (login_validations()
        .payload_validation(request = body_request)) :

        user_data : user_model =  user_model.objects.filter(

            email = body_request["email"],
            password = hashing(body_request["password"])
        )

        # username and password validation
        if len( list(user_data.values()) ) :

            http_status_code : int = 200
            message_response : str = "Yeyy.. Kamu berhasil login"
            data_response = token_filter(body_request, user_data)

        else :
                
            http_status_code : int  = 400
            message_response : str  = "Oppss... Password / Username yang kamu masukan salah."
            data_response    : dict = {}

    else :

        http_status_code : int = 400
        message_response : str =  "Brosist... Password dan Username gk boleh kosong."
        data_response    : dict = {}

 
    return http_status_code, message_response, data_response




###
### Token Filter
###
def token_filter (loads_body_request : dict, user_data : user_model) :

    filter = user_auth_model.objects.filter(

        user_id = list(user_data.values())[0]["id"]
    )

    # mengecek keberadaan pengguna
    if len(list(filter.values())) :

        data_response = user_auth_model.objects.filter(

            user_id = list(user_data.values())[0]["id"]
        ).values()[0]

        del data_response["id"]
        del data_response["user_id"]


        if expired_checker(access_token = data_response["access_token"]) :

            data_response = login_expired_checker(user_data = user_data)

            del data_response["id"]
            del data_response["user_id"]

        elif list(filter.values())[0]["access_token"] == "" :

            access_token, refresh_token = generate_access_refresh_token(

                length = 256,
                user_auth_model = user_auth_model
            )

            auth_data = user_auth_model.objects.get(

                user_id = list(user_data.values())[0]["id"]
            )

            auth_data.access_token  = access_token
            auth_data.refresh_token = refresh_token
            auth_data.token_exp = str(generate_timestamp(delta = 6))

            auth_data.save()

            data_response : dict = {
                "access_token"  : auth_data.access_token,
                "refresh_token" : auth_data.refresh_token,
                "token_exp"     : auth_data.token_exp
            }

        

    else :

        access_token, refresh_token = generate_access_refresh_token(

            length = 256,
            user_auth_model = user_auth_model
        )
                
        create_token : user_auth_model = user_auth_model.objects.create(

            user = user_model.objects.get(

                email = loads_body_request["email"],
                password = hashing(loads_body_request["password"])
            ),

            access_token  = access_token,
            refresh_token = refresh_token,
            token_exp = str(generate_timestamp(delta = 6))
        )

        data_response : dict = loads(

            serializers.serialize('json', [create_token])
        )[0]["fields"]

        del data_response["user"]


    return data_response



###
### Login Expired Checker
###
def login_expired_checker (user_data : user_model) -> dict :

    auth_data = user_auth_model.objects.get(
        user_id = list(user_data.values())[0]["id"])

    access_token, refresh_token = generate_access_refresh_token(

        length = 256,
        user_auth_model = user_auth_model
    )

    auth_data.access_token  = access_token
    auth_data.refresh_token = refresh_token
    auth_data.token_exp = str(generate_timestamp(delta = 6))

    auth_data.save()

    return user_auth_model.objects.filter(

        user_id = list(user_data.values())[0]["id"]
    ).values()[0]