from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction , connection
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models.aggregates import Count, Max, Min, Sum
from store.models import Product, OrderItem, Order, Customer, Collection

# Create your views here.


def say_hello(request):
    # query_set = Product.objects.all()
    # product = Product.objects.filter(pk=0).first() #return non not exeption
    # query_set = Product.objects.filter(unit_price__gt = 20)
    # query_set = Product.objects.filter(unit_price__range = (20,30))
    # query_set = Product.objects.filter(collection__id__range = (1,3))
    # query_set = Product.objects.filter(title__icontains='c' )
    # query_set = Product.objects.filter(last_update__year=2023 )
    # query_set = Product.objects.filter(description__isnull = True )

    # AND:
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__gt=20)
    # or
    # query_set = Product.objects.filter(inventory__lt=10).filter( unit_price__gt=20)

    # OR:
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__gt=20))

    # not -> ~Q()

    # compare:
    # query_set = Product.objects.filter(inventory = F('unit_price'))

    # sort:
    # query_set = Product.objects.order_by('-title' , 'unit_price').reverse()
    # product = Product.objects.earliest('unit_price')

    # Pages od product:
    # query_set = Product.objects.all()[:5]

    # select valus
    # query_set = Product.objects.values('title','id' , 'collection__title') --> dictionaly
    # query_set = Product.objects.values_list('title','id' , 'collection__title')

    # query_set = Product.objects.only('id' , 'title')
    # work any way 1000 of query
    # query_set = Product.objects.defer('description')

    # query_set = Product.objects.all()
    # if want collection -->1000 extra query

    # query_set = Product.objects.select_related('collection').all() -->1..1

    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()

    # query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # Aggregates
    result = Product.objects.aggregate(count=Count("id"), min_price=Min("unit_price"))

    # Annotte
    # query_set = Customer.objects.annotate(is_new = Value(True))
    query_set = Customer.objects.annotate(
        full_name=Func(F("first_name"), Value(" "), F("last_name"), function="CONCAT")
    )

    return render(request, "hello.html", {"name": "mash", "result": list(query_set)})


# @transaction.atomic() -->all the function
def say_bye(request):
    # Create:

    # collection = Collection()
    # collection.title = "Video Games"
    # collection.featured_product = Product(pk=1)
    # collection.save()
    # collection_id = collection.id

    # UPDATE:

    # collection1 = Collection.get(pk=11) #get--> no data loss or use update method
    # collection1.title = "Games"
    # collection1.save()
    # collection_id = collection1.id
    collection_id = 1004

    # Delete:
    # collection = Collection(pk=1004)
    # collection.delete()

    # Collection.objects.filter(id__gt=1000).delete()

    # Transaction:
    # with transaction.atomic():
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()

    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = -1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # RAW Querys:

    query_set = Product.objects.raw('SELECT * FROM store_product')
    
    with connection.cursor() as cursor:
        cursor.execute('')
        cursor.callproc('')

    return render(request, "bye.html", {"name": "Mahya", "id": collection_id , 'results':list(query_set)})
