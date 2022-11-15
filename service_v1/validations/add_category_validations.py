class add_category_validations :

    def __init__(self) -> None: pass


    def key_validation (self, request : dict) -> bool :

        try :

            token_validation = request.get("product_category") != (None and "")

            return token_validation
            
        except KeyError : return False