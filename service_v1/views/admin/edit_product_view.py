from json import loads, decoder

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from service_v1.controllers.admin_controllers.edit_product_controller import edit_product_controller

@csrf_exempt
def edit_product_view (request, product_url) :

    if request.method == "PUT" :

        try :
            loads_body_request = loads(

                request.body.decode("utf-8") 
            )

        except decoder.JSONDecodeError :
            loads_body_request = request.POST.dict()


        http_status_code, message_response, data_response = edit_product_controller(
            header_request = request.headers,
            body_request = loads_body_request,
            upload_file  = request.FILES,
            product_url  = product_url
        )

        # if http_status_code == 201 :

        #     del data_response["id"]
        #     del data_response["password"]
        #     del data_response["is_admin"]
        #     del data_response["verified"]
        #     del data_response["last_login"]

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
