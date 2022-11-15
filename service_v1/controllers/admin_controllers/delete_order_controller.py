from service_v1.models import (
    user_model,
    user_auth_model,
    order_model,
    product_model
)

# import utility modules
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker

# import validation modules
from service_v1.validations.token_validations import token_validations


def delete_order_controller (header_request, body_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request.get("Token")

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # admin validation by token
                if admin_checker (access_token = access_token) :
                    http_status_code, message_response, data_response = delete_order (body_request)

                else :
                    http_status_code : int = 403
                    message_response : str =  "Maaf, kamu bukan admin."
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


def delete_order (body_request) : 

    if (
        (body_request.get('email') == (None or "")) 
        and (body_request.get('product_url') == (None or ""))
    ) :

        message_response : str  = "payload tidak sesuai"
        http_status_code : int  = 400
        data_response    : dict = {}

        return http_status_code, message_response, data_response


    user_id : user_model = user_model.objects.get(
        email = body_request.get('email')
    ) 

    product_id : product_model = product_model.objects.get(
        product_url = body_request.get('product_url')
    )

    if order_model.objects.filter(
        user = user_id, product = product_id
    ).exists() :

        order_data : order_model = order_model.objects.get(
            user = user_id, product = product_id)

        order_data.delete()

        message_response : str  = "berhasil menghapus pesanan"
        http_status_code : int  = 201
        data_response    : dict = {}

    else :
        message_response : str  = "pesanan tidak tersedia"
        http_status_code : int  = 404
        data_response    : dict = {}


    return http_status_code, message_response, data_response


def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)
    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin