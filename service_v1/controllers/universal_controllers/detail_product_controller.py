from service_v1.models import category_model, product_model

from service_v1.utils.price_convert import rupiah_format

def detail_product_controller (product_url) :

    # get data product by url
    get_data_product = product_model.objects.filter(
        product_url = product_url).values()

    # product url validation
    if not len(list(get_data_product)) :

        http_status_code : int = 404
        message_response : str =  "url tidak tersedia."
        data_response    : dict = {}

        return http_status_code, message_response, data_response

    else :

        http_status_code : int  = 200
        message_response : str  = f"berhasil mengambil detail produk"
        data_response    : dict = list(product_model.objects.filter(
            product_url = product_url
        ).values())[0]

        # change response category
        data_response['category'] = category_model.objects.get(

            id = data_response.get('category_id')
        ).product_category
            
        # change response product price
        data_response['product_price'] = rupiah_format(
            int(data_response.get("product_price")),
            True
        )

        del data_response['id']
        del data_response['category_id']

    return http_status_code, message_response, data_response