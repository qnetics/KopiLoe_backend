from random import randint
from string import digits, ascii_lowercase, ascii_uppercase



###
### Generate Token (length default = 256)
###
def generate_token (length : int) -> str :

    token = ""
    character = ascii_uppercase + ascii_lowercase + digits

    for _ in range(length) : token += character[randint(0, len(character) - 1)]

    return token



###
### Generate Access Refresh Token
###
def generate_access_refresh_token (length : int, user_auth_model) :

    while True :

        access_token  = generate_token(length)
        refresh_token = generate_token(length)

        is_token_exist = list(user_auth_model.objects.filter(

            access_token  = access_token,
            refresh_token = refresh_token
        ).values())

        if is_token_exist : continue

        else : break

    return access_token, refresh_token
