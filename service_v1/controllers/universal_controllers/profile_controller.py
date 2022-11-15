
from service_v1.models import user_model, user_auth_model

from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker
from service_v1.validations.token_validations import token_validations

def profile_controller (header_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request["Token"]

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                user_datas = get_profile_data(access_token)

                http_status_code : int = 200
                message_response : str =  "Berhasil mendapatkan data"
                data_response    : dict = user_datas

            else :

                http_status_code : int = 403
                message_response : str =  "Token salah atau tidak tersedia."
                data_response    : dict = {}

        else :

            http_status_code : int = 400
            message_response : str =  "Token telah kadaluarsa."
            data_response    : dict = {}


    else :

        http_status_code : int = 403
        message_response : str =  "Header 'Token' tidak tersedia"
        data_response    : dict = {} 

    return http_status_code, message_response, data_response



def get_profile_data(access_token : str) -> dict :

    auth_data = user_auth_model.objects.get(

        access_token = access_token
    )

    user_datas = list(user_model.objects.filter(

        id = auth_data.user_id
    ).values())[0]

    del user_datas["id"]
    del user_datas["password"]
    del user_datas["verified"]

    return user_datas