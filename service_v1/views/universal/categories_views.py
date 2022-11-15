from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from service_v1.controllers.universal_controllers.categories_controller import categories_controller

@csrf_exempt
def categories_view (request) :

    if request.method == "GET" :

        http_status_code, message_response, data_response = categories_controller()

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
