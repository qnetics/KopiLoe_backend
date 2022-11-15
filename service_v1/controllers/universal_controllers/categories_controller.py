from service_v1.models import category_model

def categories_controller () :

    categories = []

    for category in category_model.objects.all().values() :
        categories.append(
            category.get('product_category')
        )

    http_status_code : int = 200
    message_response : str =  "Berhasil mengeluarkan kategori."
    data_response    : dict = categories

    return http_status_code, message_response, data_response
