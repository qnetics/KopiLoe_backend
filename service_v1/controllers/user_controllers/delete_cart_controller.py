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


def delete_cart_controller (header_request, body_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request.get("Token")

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # """ admin validation by token """

                if not admin_checker (access_token = access_token) :

                    http_status_code, message_response, data_response = delete_cart (access_token, body_request)

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



def delete_cart (access_token, body_request) : 

    # payload validation
    url_product : bool= not body_request.get("product_url") != (None and "")
    if url_product :

        http_status_code : int = 400
        message_response : str =  "Brosist.... Isi yang bener dong formulir -nya."
        data_response    : dict = {}

        return http_status_code, message_response, data_response


    if not len(product_model.objects.filter(
        product_url = body_request.get("product_url")).values()
    ) :

        message_response : str = "url produk tidak tersedia"
        http_status_code : int = 201
        data_response = {}

        return http_status_code, message_response, data_response


    if cart_model.objects.filter(
        user = user_auth_model.objects.get(
            access_token = access_token).user,

        product = product_model.objects.get(
            product_url = body_request.get("product_url")
        )
    ).exists() :

        cart_user = cart_model.objects.get(
            user = user_auth_model.objects.get(
                access_token = access_token).user,
                
            product = product_model.objects.get(product_url = body_request.get("product_url"))
        )

        cart_user.delete()

    else :
        message_response : str = "produk tidak tersedia di keranjang"
        http_status_code : int = 404
        data_response = {}

        return http_status_code, message_response, data_response



    message_response : str = "barang telah dihapus"
    http_status_code : int = 201
    data_response = {}

    return http_status_code, message_response, data_response



def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)

    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin