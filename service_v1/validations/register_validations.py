import re

class register_validations :

    def __init__(self) -> None: pass


    def payload_validation (self, request : dict) -> bool :

        username_validation = request.get("username") != (None and "")
        password_validation = request.get("password") != (None and "")
        email_validation    = request.get("email")    != (None and "") 

        if email_validation : email_validation = self.email_validation(
            request.get("email")
        )

        return (

            username_validation &
            password_validation &
            email_validation
        )


    def email_validation (self, email_address : str) -> bool :

        regex_pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

        return bool(re.search(regex_pattern, email_address))

        