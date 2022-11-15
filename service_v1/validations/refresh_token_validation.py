class refresh_token_validations :

    def __init__(self) -> None : pass


    def refresh_validation (self, request : dict) -> bool :

        try :

            refresh_token = request.get("refresh_token") != (None and "")

            return refresh_token

        except KeyError : return False