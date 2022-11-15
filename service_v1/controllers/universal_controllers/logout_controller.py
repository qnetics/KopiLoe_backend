from service_v1.models import user_auth_model

from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker
from service_v1.validations.token_validations import token_validations

def logout_controller (header_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request["Token"]

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                http_status_code, message_response, data_response = logout_process(
                    access_token = access_token) 

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



def logout_process (access_token : str) -> dict :

    auth_data = user_auth_model.objects.get(access_token = access_token)
    auth_data.delete()

    http_status_code : int = 200
    message_response : str =  "Kamu Berhasil Logout"
    data_response    : dict = {} 


    return http_status_code, message_response, data_response
