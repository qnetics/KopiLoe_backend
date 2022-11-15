from service_v1.models import (
    cart_model,
    user_model, 
    product_model,
    user_auth_model
)

# import utility modules
from service_v1.utils.price_convert import rupiah_format
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker

# import validation modules
from service_v1.validations.token_validations import token_validations


def show_cart_controller (header_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request.get("Token")

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # """ admin validation by token """

                if not admin_checker (access_token = access_token) :

                    http_status_code, message_response, data_response = show_cart (access_token)

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



def show_cart (access_token) : 

    response_data : dict = {}

    total_price   : int = 0

    # User Cart Contain
    user_cart_contain : list = []

    # User Cart Model
    user_cart_models  : list = list(cart_model.objects.filter(

        user = user_auth_model.objects.get(
            access_token = access_token).user
    ).values())[::-1]

    response_data['total_cart'] = len(user_cart_models)

    # Filtering User Cart Model
    for user_cart_model in user_cart_models :

        get_specific_product = product_model.objects.get(
            id = user_cart_model.get('product_id')
        )

        user_cart_model["product_name"]  = get_specific_product.product_name

        user_cart_model["product_price"] = rupiah_format(
            get_specific_product.product_price, True)

        user_cart_model["total_price"] = rupiah_format(
            get_specific_product.product_price *
            user_cart_model.get('order_quantity'), True)

        total_price += (
            get_specific_product.product_price *
            user_cart_model.get('order_quantity')
        )

        user_cart_model["product_url"]   : str = get_specific_product.product_url
        user_cart_model["product_image"] : str = get_specific_product.product_image


        del user_cart_model["id"]
        del user_cart_model["user_id"]
        del user_cart_model["product_id"]

        user_cart_contain.append(user_cart_model)

    response_data['total_price']  : str  = rupiah_format(total_price, True)
    response_data['detail_cart '] : list = user_cart_contain

    # View Return
    message_response : str  = "berhasil menampilkan data keranjang"
    http_status_code : int  = 200
    data_response    : dict = response_data

    return http_status_code, message_response, data_response



def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)

    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin