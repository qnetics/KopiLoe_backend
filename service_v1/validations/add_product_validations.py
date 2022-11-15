class add_product_validations :

    def __init__(self) -> None: pass


    def payload_validation (self, request : dict) -> bool :

        product_name_validation = request.get("product_name") != (None and "")
        product_price_validation = request.get("product_price") != (None and "")
        product_category_validation = request.get("product_category") != (None and "")
        product_image_validation = request.get("product_image") != (None and "")

        return (

            product_name_validation &
            product_price_validation &
            product_category_validation &
            product_image_validation
        )