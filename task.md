## Today Task

```
    class Tag(models.Model):
        name = models.CharField(max_length=120)
        
        
    class Author(models.Model):
        name = models.CharField(max_length=300)
        surname = models.CharField(max_length=400)
        age = models.PositiveIntegerField()
    
    
    class Profile(models.Model):
        author = models.OneToOneField(Author, on_delete=models.CASCADE)
        description = models.TextField()
        
        
        
    class Product(models.Model):
        author = models.ForeignKey(Author, on_delete=models.CASCADE)
        name = models.CharField(max_length=200)
        price = models.FloatField()
        discount = models.FloatField(blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        tags = models.ManyToManyField(Tag, blank=True)
```

1. Author querysetin'ə "fullname" ələvə etmək --> fullname = name + " " + surname
2. Profile querysetin'ə "age_check" əlavə etmək --> authorun age i 18dən kiçikdisə younger 18 31 yas arasidisa middle 31den coxdusa old olacaq valuelari
3. Product querysetin'ə "total_price" əlavə etmək --> discount burda faizdi pricedan faizi qeder cixib hesablamaq lazimdi
4. Author querysetin'ə "product_count" əlavə etmək --> product_count = hemin authora bagli olan mehsullarin sayi eger yoxdusa default olaraq 0
5. Author querysetin'ə "product_total_price" əlavə etmək --> product_total_price = hemin authora bagli olan mehsullarin total_price cemi eger yoxdusa default olaraq 0
    1. product_total_price gosterisde querysetde bele olmalidi, Numune: "129 AZN"
6. Product querysetin'ə "tag_count" əlavə etmək --> tag_count = hemin producta bagli olan taglarin sayi
7. 