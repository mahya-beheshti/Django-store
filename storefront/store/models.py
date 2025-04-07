from django.db import models

# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Product(models.Model):
    # sku = models.CharField(max_length=25 , primary_key=True) --> no id filed anymore
    title = models.CharField(max_length=225)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey("Collection", on_delete=models.PROTECT)
    promotions = models.ManyToManyField(
        "Promotion", related_name="Products"
    )  # in promotion
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True)

    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_CHOICES = [(MEMBERSHIP_BRONZE, "Bronza"), ("S", "Silver"), ("G", "Gold")]
    # can be B or S or G
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )
    # atomatically add adress

    # class Meta:
    #     db_table = 'store_customers'
    #     indexes = [models.Index(fields=['last_name' , 'first_name'])]

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    class Meta:
        ordering = ['first_name' , 'last_name']

class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)

    PAYMENT_CHOICES = [("P", "Pending"), ("C", "Complete"), ("F", "Failed")]
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_CHOICES, default="P"
    )
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipi = models.CharField(max_length=255 , null=True)
    # customer = models.OneToOneField(
    #     Customer, on_delete=models.CASCADE, primary_key=True
    # ) 1..1
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey("Product", on_delete=models.PROTECT)


class CartItem(models.Model):
    quantity = models.PositiveSmallIntegerField()
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
