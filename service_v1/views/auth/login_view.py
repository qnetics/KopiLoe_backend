from json import loads

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

from service_v1.controllers.universal_controllers.login_controller import login_controller

@csrf_exempt
def login_view (request) :

    if request.method == "POST" :
        loads_body_request = loads(
            
            request.body.decode("utf-8")
        )

        http_status_code, message_response, data_response = login_controller(
            body_request = loads_body_request
        )

        if http_status_code == 200 :

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
