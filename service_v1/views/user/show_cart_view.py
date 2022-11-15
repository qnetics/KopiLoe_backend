from json import loads, decoder

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 

from service_v1.controllers.user_controllers.show_cart_controller import show_cart_controller



@csrf_exempt
def show_cart_view (request) :

    if request.method == "GET" :

        try :
            loads_body_request = loads(

                request.body.decode("utf-8")
            )

        except decoder.JSONDecodeError :
            loads_body_request = request.POST.dict()


        http_status_code, message_response, data_response = show_cart_controller(
            header_request = request.headers)

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


