from django.db import models

class Todo(models.Model):
    item = models.CharField(max_length = 100)

class resource_model (models.Model) :
    incomes = models.IntegerField()

class user_model (models.Model) :
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email    = models.CharField(max_length=64)
    is_admin = models.BooleanField()
    verified = models.BooleanField()
    last_login = models.DateField()

    def __str__ (self) :
        return "username=%s, is_admin=%s" % (self.username, self.is_admin)

class user_location_model (models.Model) :
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    location = models.CharField(max_length=500)

    def __str__ (self) :
        return "location=%s" % (self.location)

class user_auth_model (models.Model) :
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    access_token  = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
    token_exp = models.CharField(max_length=256)

    def __str__ (self) :
        return "user_id=%s" % (self.user)

class otp_verified_model (models.Model) :
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)

    def __str__ (self) :
        return "token=%s" % (self.token)

class category_model (models.Model) :
    product_category = models.CharField(max_length=64)

    def __str__ (self) :
        return "category=%s" % (self.product_category)
	
class product_model (models.Model) :
    category = models.ForeignKey(category_model, on_delete=models.CASCADE)
    product_name  = models.CharField(max_length=128)
    product_price = models.IntegerField()
    product_image = models.CharField(max_length=128)
    product_url   = models.CharField(max_length=150)

    def __str__ (self) :
        return "product_name=%s" % (self.product_name)

class cart_model (models.Model) :
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    product = models.ForeignKey(product_model, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()

    def __str__ (self) :
        return "quantity=%s" % (self.order_quantity)

class order_model (models.Model) :
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    product = models.ForeignKey(product_model, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    order_date = models.CharField(max_length=32)

    # pending | success
    status = models.CharField(max_length=32)

    def __str__ (self) :
        return "status=%s" % (self.status)