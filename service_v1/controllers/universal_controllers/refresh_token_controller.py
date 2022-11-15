from service_v1.models import user_auth_model
from service_v1.validations.refresh_token_validation import refresh_token_validations
from service_v1.utils.generate_token import generate_access_refresh_token
from service_v1.utils.timestamp_generator import generate_timestamp


def refresh_token_controller (body_request) :

    # payload validation
    if (refresh_token_validations()
        .refresh_validation(request = body_request)) :

        auth_data : user_auth_model =  user_auth_model.objects.filter(

            refresh_token = body_request["refresh_token"]
        )

        # username and password validation
        if len(list(auth_data.values())) :

            id_auth_data : int = list(auth_data.values())[0]["id"]

            auth_data_model = user_auth_model.objects.get(id = id_auth_data)

            access_token, refresh_token = generate_access_refresh_token(

                length = 256,
                user_auth_model = user_auth_model
            )

            auth_data_model.access_token  = access_token
            auth_data_model.refresh_token = refresh_token
            auth_data_model.token_exp = str(generate_timestamp(delta = 6))

            auth_data_model.save()


            http_status_code : int  = 200
            message_response : str  = "Token berhasil di refresh"
            data_response    : dict = user_auth_model.objects.filter(

                id = id_auth_data
            ).values()[0]

            del data_response["id"]
            del data_response["user_id"]


        else :
                
            http_status_code : int  = 400
            message_response : str  = "Oppss... refresh_token kamu salah."
            data_response    : dict = {}

        return http_status_code, message_response, data_response
