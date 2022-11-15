# import model data module
from service_v1.models import user_model, user_auth_model

# import utility modules
from service_v1.utils.hashing_password import hashing
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker

# import validation modules
from service_v1.validations.token_validations import token_validations
from service_v1.validations.register_validations import register_validations

 
def edit_profile_controller (header_request, body_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request["Token"]

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                user_auth_data = user_auth_model.objects.get(

                    access_token = access_token
                ) 
                
                http_status_code, message_response, data_response = edit_profile(

                    user_id = user_auth_data.user_id,
                    body_request = body_request
                )

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



def edit_profile (user_id : int, body_request : dict) -> dict :

    # get data user by id
    edit_user = user_model.objects.get(id = user_id)

    # password validation
    if body_request.get("password") != (None and "") :
        edit_user.password = hashing(
            password = body_request.get("password"))

    # email validation
    if body_request.get("email") != (None and "") :
        if user_model.objects.filter(email = body_request["email"]).exists() :

            http_status_code : int = 400
            message_response : str =  "Yahhh.. Email yang kamu mau ganti telah digunakan, gunakan email lain untuk mendaftar."
            data_response    : dict = {}

            return http_status_code, message_response, data_response

        elif not register_validations().email_validation(
            email_address = body_request.get("email")) :

            http_status_code : int = 400
            message_response : str =  "bro.. Email lo gk sesuai."
            data_response    : dict = {}

            return http_status_code, message_response, data_response

        else : edit_user.email = body_request.get("email")

    # username validation
    if body_request.get("username") != (None and "") :
        edit_user.username = body_request.get("username")

    edit_user.save()

    # get new data
    new_user_data : dict = list(user_model.objects.filter(
            
        id = user_id
    ).values())[0]

    # data for user consume
    http_status_code : int = 201
    message_response : str =  "Berhasil Mengedit Data"
    data_response    : dict = new_user_data

    return http_status_code, message_response, data_response