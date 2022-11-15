from json import loads

from django.core import serializers

from service_v1.models import ( 
    user_model,
    user_auth_model,
    product_model,
    category_model
)

# import utility modules
from service_v1.utils.price_convert import rupiah_format
from service_v1.utils.token_checker import token_checker
from service_v1.utils.generate_token import generate_token
from service_v1.utils.expired_token_checker import expired_checker


# import validation modules
from service_v1.validations.token_validations import token_validations
from service_v1.validations.add_product_validations import add_product_validations


def add_product_controller (header_request, body_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request["Token"]

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # """ admin validation by token """

                if admin_checker (access_token = access_token) :
                    
                    http_status_code, message_response, data_response = add_product (
                        body_request = body_request
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




def add_product (body_request : dict) : 

    if add_product_validations().payload_validation(
        request = body_request) :

        get_catergory = category_model.objects.filter(

            product_category = body_request.get("product_category")
        ).values()

        if len(list(get_catergory)) :

            create_product = product_model.objects.create(

                category = category_model.objects.get(
                    product_category = body_request.get("product_category")
                ),

                product_name  = body_request.get("product_name"),
                product_price = int(body_request.get("product_price")),
                product_image = body_request.get("product_image"),
                product_url = "".join(
                    [
                        "-" if id_url == " " else id_url for id_url in body_request.get(
                            "product_name"
                        )
                    ]
                ) + f"-{generate_token(length = 16)}"
            )

            message_response : str = "Produk berhasil terdaftar"
            http_status_code : int = 201
            data_response = loads(
                serializers.serialize('json', [create_product])
            )[0]["fields"]


            # change response category
            data_response['category'] = category_model.objects.get(
                id = data_response.get('category')
            ).product_category
            

            # change response product price
            data_response['product_price'] = rupiah_format(
                int(body_request.get("product_price")),
                True
            )

        else :
            http_status_code : int = 403
            message_response : str =  "kategori tidak tersedia."
            data_response    : dict = {}

    else :
        http_status_code : int = 403
        message_response : str =  "Isi form dengan benar"
        data_response    : dict = {}

    return http_status_code, message_response, data_response




def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)

    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin