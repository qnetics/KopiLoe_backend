from time import time
from service_v1.models import user_auth_model
from service_v1.utils.timestamp_generator import generate_timestamp 

def expired_checker (access_token : str) :

    if access_token == "" : return False

    access_token_check = user_auth_model.objects.filter(

        access_token = access_token
    )

    # access token not exist
    if not len(list(access_token_check.values())) : return False

    else : auth_data = list(access_token_check.values())[0]

    # access code expired
    if float(auth_data["token_exp"]) < time() :

        auth_data = user_auth_model.objects.get(access_token = access_token)

        auth_data.access_token = ""
        auth_data.token_exp    = str(generate_timestamp(delta = 5))

        auth_data.save()

        return True

    else : return False