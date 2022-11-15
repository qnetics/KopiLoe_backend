from json import loads 

from django.core import serializers

from service_v1.models import user_model, user_auth_model, category_model

# import utility modules
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker

# import validation modules
from service_v1.validations.token_validations import token_validations
from service_v1.validations.add_category_validations import add_category_validations


def add_category_controller (header_request, body_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request.get("Token")

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # """ admin validation by token """

                if admin_checker (access_token = access_token) :

                    http_status_code, message_response, data_response = add_category (body_request)

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



def add_category (body_request) : 

    # payload validation
    if not (add_category_validations()
        .key_validation(request = body_request)) :

        http_status_code : int = 400
        message_response : str =  "Brosist.... Isi yang bener dong formulir -nya."
        data_response    : dict = {}


    # email validation
    elif category_model.objects.filter(

        product_category = body_request.get("product_category")
    ).exists() :

        http_status_code : int = 400
        message_response : str =  "Mimin.. Kategori yang ini sudah kamu daftarkan waktu itu."
        data_response    : dict = {}

    else :

        create_category = category_model.objects.create(

            product_category = body_request.get("product_category")
        )

        message_response : str = "horee... kategori produk telah dibuat"
        http_status_code : int = 201
        data_response = loads(
            serializers.serialize('json', [create_category])
        )[0]["fields"]


    return http_status_code, message_response, data_response



def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)

    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin