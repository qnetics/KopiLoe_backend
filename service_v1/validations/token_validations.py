class token_validations :

    def __init__(self) -> None: pass


    def token_header_validation (self, request : dict) -> bool :

        try :

            token_validation    = request.get("Token") != (None and "")

            return token_validation
            
        except KeyError : return False