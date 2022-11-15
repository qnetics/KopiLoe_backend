from service_v1.models import (
    user_model,
    user_auth_model,
    user_location_model
)

# import utility modules
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker

# import validation modules
from service_v1.validations.token_validations import token_validations


def show_location_controller (header_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request.get("Token")

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # """ admin validation by token """

                if not admin_checker (access_token = access_token) :

                    http_status_code, message_response, data_response = show_location (access_token)

                else :
                    http_status_code : int = 403
                    message_response : str =  "Maaf, kamu bukan user."
                    data_response    : dict = {}

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


def show_location (access_token) : 
    
    if user_location_model.objects.filter(
        user = user_model.objects.get(id = user_auth_model.objects.get(
            access_token = access_token
        ).user_id)
    ).exists() :

        user_location_data : user_location_model = user_location_model.objects.get(
            user = user_model.objects.get(id = user_auth_model.objects.get(
                access_token = access_token
        ).user_id))

        location = user_location_data.location 

    else :
        location : str = ""


    message_response : str = "berhasil menampilkan lokasi"
    http_status_code : int = 200
    data_response    : dict = {
        "user_location" : location
    }

    return http_status_code, message_response, data_response


def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)

    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin