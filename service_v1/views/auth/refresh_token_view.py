from json import loads

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

from service_v1.controllers.universal_controllers.refresh_token_controller import refresh_token_controller

@csrf_exempt
def refresh_token_view (request) :


    if request.method == "POST" :
        loads_body_request = loads(
            
            request.body.decode("utf-8")
        )

        http_status_code, message_response, data_response = refresh_token_controller(
            body_request = loads_body_request
        )

        if http_status_code == 201 :

            del data_response["token_exp"]

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