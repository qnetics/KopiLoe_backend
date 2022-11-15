from service_v1.models import (
    cart_model,
    user_model, 
    order_model,
    product_model,
    user_auth_model 
)


from datetime import datetime

# import utility modules
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker

# import validation modules
from service_v1.validations.token_validations import token_validations


def add_order_controller (header_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request.get("Token")

        if not expired_checker (access_token = access_token) :

            if token_checker (access_token = access_token) :

                # admin validation by token
                if not admin_checker (access_token = access_token) :
                    http_status_code, message_response, data_response = add_order(access_token)

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


def add_order (access_token) :  

    cart_model_identify : list = list(cart_model.objects.filter(
        user = user_auth_model.objects.get(
            access_token = access_token).user
    ).values())

    for add_order in cart_model_identify :
        get_user_by_id : user_model = user_model.objects.get(
            id = add_order.get('user_id'))

        get_product_by_id : product_model = product_model.objects.get(
            id = add_order.get('product_id'))

        if order_model.objects.filter(
            user = get_user_by_id,
            product = get_product_by_id
        ).exists() :

            user_order : order_model = order_model.objects.get(
                user = get_user_by_id,
                product = get_product_by_id
            )

            user_order.order_quantity += add_order.get('order_quantity')
            user_order.save()

        else :       
            order_model.objects.create(
                user = get_user_by_id,
                product = get_product_by_id,
                order_quantity = add_order.get('order_quantity'),
                order_date = datetime.now().strftime('%H:%M:%S %d-%m-%Y'),
                status  = "pending"
            )

    http_status_code : int = 201
    message_response : str =  "berhasil menambahkan barang ke keranjang"
    data_response    : list = cart_model_identify

    return http_status_code, message_response, data_response



def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)
    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin