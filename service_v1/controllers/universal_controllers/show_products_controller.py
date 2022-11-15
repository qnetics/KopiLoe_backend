from service_v1.models import (
    user_model, user_auth_model,
    category_model, product_model
)


# import utility modules
from service_v1.utils.price_convert import rupiah_format


def show_products_controller (product_limit, search_product, contain_by_category) :


    http_status_code, message_response, data_response = show_product_user (
        product_limit, search_product, contain_by_category)

    return http_status_code, message_response, data_response
    


def show_product_user (product_limit, search_product, contain_by_category) :

    default_limit : int  = 50
    result_data   : list = []


    # Limit Validation
    if (product_limit is not None) and (product_limit.isnumeric()) :
        default_limit : int = int(product_limit)

    if ((product_limit is None) or (not product_limit.isnumeric())
        or (int(product_limit) > default_limit)) :

        default_limit : int  = 50


    # Search Validation
    if search_product is not None :
        raw_product_data : list =  product_model.objects.filter(
            product_name__contains = search_product
        ).values()[:default_limit]

    else :
        raw_product_data : list = product_model.objects.filter().values()[:default_limit]


    # Contain Validation
    if ((contain_by_category is not None) and (contain_by_category.isnumeric())
        and (int(contain_by_category) == 1)
        and (len(category_model.objects.all().values()) > 0)):

        categories : list = category_model.objects.all().values()

        for category in categories :

            product_category : str = category.get('product_category')
            contain_product : list = [] 

            for index_result_data in raw_product_data :
                
                # change response category
                category = category_model.objects.get(

                    id = index_result_data.get('category_id')
                ).product_category

                if product_category == category :

                    index_result_data['product_price'] = rupiah_format(
                        int(index_result_data.get("product_price")),
                        True
                    )

                    del index_result_data["id"]
                    contain_product.append(index_result_data)

            result_data.append({
                "category" : product_category,
                "products" : contain_product
            })



    else :

        for index_result_data in raw_product_data :

            # change response category
            index_result_data['category'] = category_model.objects.get(

                id = index_result_data.get('category_id')
            ).product_category

            # change response product price
            index_result_data['product_price'] = rupiah_format(
                int(index_result_data.get("product_price")),
                True
            )

            del index_result_data["id"]
            del index_result_data['category_id']

            result_data.append(index_result_data)



    http_status_code : int  = 200
    message_response : str  = f"berhasil mengambil produk"
    data_response    : list = result_data


    return http_status_code, message_response, data_response


def admin_checker (access_token : str) -> bool : 

    get_auth_data = user_auth_model.objects.get(access_token = access_token)

    get_user_data = user_model.objects.get(id = get_auth_data.user_id)

    return get_user_data.is_admin