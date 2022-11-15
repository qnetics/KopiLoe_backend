from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

from service_v1.controllers.universal_controllers.profile_controller import profile_controller

@csrf_exempt
def profile_view (request) :


    if request.method == "GET" :

        http_status_code, message_response, data_response = profile_controller (

            header_request = request.headers
        )

        # if http_status_code == 201 :

        #     del data_response["token_exp"]

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