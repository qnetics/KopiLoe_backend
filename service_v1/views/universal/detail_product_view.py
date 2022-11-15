from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from service_v1.controllers.universal_controllers.detail_product_controller import detail_product_controller

@csrf_exempt
def detail_product_view (request, product_url) :

    if request.method == "GET" :

        http_status_code, message_response, data_response = detail_product_controller(
            product_url  = product_url
        )

        response = {

            "http_status_code" : http_status_code,
            "message_response" : message_response,
            "data_response"    : data_response
        }

    else :

        http_status_code : int = 400
        
        response = {

            "http_status_code" : http_status_code,
            "message_response" : f"{request.method} method not found!",
            "data_response"    : {}
        }

    return JsonResponse(data = response, status = http_status_code, safe=True)
