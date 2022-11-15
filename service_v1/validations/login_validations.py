class login_validations :

    def __init__(self) -> None: pass


    def payload_validation (self, request : dict) -> bool :

        try :

            email_validation    = request.get("email") != (None and "")
            password_validation = request.get("password") != (None and "") 

            return (

                email_validation and
                password_validation
            )

        except KeyError : return False