from service_v1.models import (
    user_model,
    user_auth_model,
    product_model,
    category_model
)


# import utility modules
from service_v1.utils.price_convert import rupiah_format
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker


# import validation modules
from service_v1.validations.token_validations import token_validations


def edit_product_controller (header_request, body_request,
    upload_file, product_url) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request["Token"]

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # """ admin validation by token """

                if admin_checker (access_token = access_token) :
                    
                    http_status_code, message_response, data_response = edit_product (
                        body_request = body_request,
                        upload_file  = upload_file,
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




def edit_product (body_request : dict, upload_file, product_url) : 

    # get data product by url
    get_data_product = product_model.objects.filter(product_url = product_url).values()

    # product url validation
    if not len(list(get_data_product)) :

        http_status_code : int = 404
        message_response : str =  "url tidak tersedia."
        data_response    : dict = {}

        return http_status_code, message_response, data_response

    else : data_product = product_model.objects.get(
        product_url = product_url)


    # product name validation
    if body_request.get("product_name") != (None and "") :
        url_product  : str = data_product.product_url
        url_token : str = product_url[
            (len(url_product) - 17):len(url_product)
        ]

        data_product.product_url : str =  "".join(
            [
                "-" if id_url == " " else id_url for id_url in body_request.get(
                    "product_name"
                )
            ]
        ) + url_token

        data_product.product_name =  body_request.get("product_name")


    # product price validation
    if body_request.get("product_price") != (None and "") :
        data_product.product_price =  body_request.get("product_price")


    # product image validation
    if upload_file.get("product_image") != (None and "") :
        data_product.product_image =  upload_file.get("product_image")

    # product category validation
    if body_request.get("category") != (None and "") :

        get_category_product  =  category_model.objects.filter(

            product_category = body_request.get("category")
        ).values()

        if len(list(get_category_product)) :
            data_product.category = body_request.get("category")
            

        else :
            http_status_code : int = 400
            message_response : str =  "kategori tidak tersedia."
            data_response    : dict = {}

            return http_status_code, message_response, data_response

    data_product.save()

    http_status_code : int  = 201
    message_response : str  = "berhasil mengedit produk"
    data_response    : dict = list(product_model.objects.filter(

            id = list(get_data_product)[0].get("id")
        ).values()
    )[0]


    # change response category
    data_response['category'] = category_model.objects.get(

        id = data_response.get('category_id')
    ).product_category
            
    # change response product price
    data_response['product_price'] = rupiah_format(
        int(data_response.get("product_price")),
        True
    )

    del data_response['id']
    del data_response['category_id']

    return http_status_code, message_response, data_response




def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)

    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin

