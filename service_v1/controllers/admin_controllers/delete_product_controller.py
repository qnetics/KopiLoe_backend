from service_v1.models import (
    
    user_model,
    user_auth_model,
    product_model
)


# import utility modules
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker


# import validation modules
from service_v1.validations.token_validations import token_validations


def delete_product_controller (header_request, product_url) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request["Token"]

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # """ admin validation by token """

                if admin_checker (access_token = access_token) :
                    
                    http_status_code, message_response, data_response = delete_product (
                        product_url  = product_url
                    )

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




def delete_product (product_url) : 

    # get data product by url
    get_data_product = product_model.objects.filter(product_url = product_url).values()

    # product url validation
    if not len(list(get_data_product)) :

        http_status_code : int = 404
        message_response : str =  "url tidak tersedia."
        data_response    : dict = {}

        return http_status_code, message_response, data_response

    else :
        
        data_product = product_model.objects.get(
        product_url = product_url)

        product_name = data_product.product_name

        data_product.delete()

    http_status_code : int  = 200
    message_response : str  = f"berhasil menghapus produk '{product_name}' "
    data_response    : dict = {}


    return http_status_code, message_response, data_response




def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)

    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin

