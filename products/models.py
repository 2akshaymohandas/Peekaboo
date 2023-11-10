from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from image_cropping import ImageRatioFieldcls





# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique = True)
    slug = AutoSlugField(populate_from='category_name',unique=True,null=True,default=None)


    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def get_url(self):
        return reverse('products_by_category', args = [self.slug])
    
    def __str__(self):
        return self.category_name




class Brand(models.Model):
    brand_name = models.CharField(max_length=200,unique=True)
    slug = AutoSlugField(populate_from='brand_name',unique=True,null=True,default=None)


    def __str__(self):
        return self.brand_name



# Product Table
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = AutoSlugField(populate_from='product_name',unique=True,null=True,default=None)
    discription  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
  # stock        = models.IntegerField(default=0) 
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    image        = models.ImageField(upload_to='products/')
    cropping = ImageRatioField('image', '430x360')
    is_available  =models.BooleanField(default=True)
    Category      =models.ForeignKey(Category,on_delete=models.CASCADE)
    Brand         =models.ForeignKey(Brand,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    

class Product_offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

class Category_offer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()




# Product Table
class Size(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, default=None)

    name=models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name





# Color Table
# class Color(models.Model):
#     name=models.CharField(max_length=100)
#     price = models.IntegerField(default=0)
    
#     def __str__(self) -> str:
#         return self.name




class ProductVariant(models.Model):

    product_name=models.ForeignKey(Product, on_delete=models.CASCADE,related_name="product_variant")
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    # color = models.CharField(max_length=50, default='black')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    

    def __str__(self) -> str:
        return self.product_name.product_name+':'+self.size.name




class ProductImage(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.image.url
    
class CategoryOffer(models.Model):
    offer_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    offer_percent = models.IntegerField(default=0)
    
    def __str__(self):
        return self.offer_category