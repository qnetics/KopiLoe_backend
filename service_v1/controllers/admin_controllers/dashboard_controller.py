from service_v1.models import (
    user_model,
    user_auth_model,
    order_model,
    product_model,
    resource_model
)

# import utility modules
from service_v1.utils.price_convert import rupiah_format
from service_v1.utils.token_checker import token_checker
from service_v1.utils.expired_token_checker import expired_checker

# import validation modules
from service_v1.validations.token_validations import token_validations

def dashboard_controller (header_request) :

    # Header Validation
    if token_validations().token_header_validation(
        request = header_request) :

        access_token = header_request.get("Token")

        if not expired_checker(access_token = access_token) :

            if token_checker(access_token = access_token) :

                # admin validation by token
                if admin_checker (access_token = access_token) :
                    http_status_code, message_response, data_response = show_dashboard()

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


def show_dashboard () : 

    # Response view
    response_view : dict = {}

    # Get Customers data
    response_view["customers"] : str = str(
        len(user_model.objects.filter(is_admin = 0).values())
    )

    # Get Products data
    response_view["products"] : str = str(
        len(product_model.objects.values())
    )

    # Get Orders data
    response_view["orders"] : str = str(
        len(order_model.objects.filter(status = "pending").values())
    )

    # Get Incomes
    if not resource_model.objects.filter(id = 1).exists() :
            resource_model.objects.create(incomes = 0)

    incomes : str = rupiah_format(
        resource_model.objects.get(id = 1).incomes, True)

    # Rp. xx.xxx,xx -> xx.xxx
    response_view["incomes"] : str = incomes[4:len(incomes)-3]

    # Get Active Orders
    if len(order_model.objects.filter(status = "pending").values()) < 1 :
        response_view["active_orders"] : list = []

    else :
        order_filter  : list = []
        order_datas   : list = list(
            order_model.objects.filter(status = "pending").values()
        )[::-1]

        for order_data in order_datas :

            # Get username
            get_username : str = user_model.objects.get(
                id = order_data.get('user_id')).username

            # Get product name
            get_product_name : str = product_model.objects.get(
                id = order_data.get('product_id')).product_name

            # Get order quantity
            order_quantity : int = order_data.get('order_quantity')

            order_filter.append(
                {
                    "username" : get_username,
                    "product_name" : get_product_name,
                    "quantity" : order_quantity
                }
            )

        response_view["active_orders"] : list = order_filter

    message_response : str  = "berhasil menampilkan dashboard"
    http_status_code : int  = 200
    data_response    : dict = response_view

    return http_status_code, message_response, data_response


def admin_checker (access_token : str) -> bool :

    get_auth_data = user_auth_model.objects.get(access_token = access_token)
    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin