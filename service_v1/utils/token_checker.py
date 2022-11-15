from service_v1.models import user_auth_model


def token_checker (access_token : str) -> bool :

    if access_token == "" : return False

    access_token_check = user_auth_model.objects.filter(

        access_token = access_token
    )

    # access token not exist
    if len(list(access_token_check.values())) :

        return True

    else : return False