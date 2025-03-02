from django.db import models
from django.contrib.auth.models import AbstractUser
import decimal
from django.utils import timezone


# Model สำหรับสมาชิก
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# Model สำหรับเมนูอาหารและเครื่องดื่ม
class MenuManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class Menu(models.Model):
    CATEGORY_CHOICES = [
        ('coffee', 'เมนูกาแฟ'),
        ('tea', 'เมนูชา'),
        ('cocoa_milk', 'เมนูโกโก้ และ นม'),
        ('snack', 'เมนูขนม'),
        ('bakery', 'เบเกอรี่'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='menu_images/')
    review = models.BooleanField(default=False)
    
    objects = MenuManager()

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

# Model สำหรับให้สมาชิกรีวิวเมนู
class Review(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='reviews')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)  # คะแนนเต็ม 1-5 ดาว
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.member.username} on {self.menu.name}"


# Model สำหรับโปรโมชั่น
class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()  # เช่น ลด 10%
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)
    usage_limit = models.PositiveIntegerField(
        default=0, 
        help_text="จำนวนครั้งที่ใช้ได้ (0 หมายถึงไม่จำกัด)"
    )
    # ฟิลด์นี้กำหนดว่าโปรโมชั่นนี้ใช้กับเมนูไหนบ้าง หากเว้นว่าง หมายถึงใช้ได้ทั้งร้าน
    applicable_menus = models.ManyToManyField(
        Menu, 
        blank=True, 
        related_name='promotions', 
        help_text="ถ้าเว้นว่างหมายถึงโปรโมชั่นใช้ได้กับทุกเมนู"
    )

    def __str__(self):
        return self.title


# Model สำหรับกิจกรรมทางร้าน
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    participants = models.ManyToManyField(Member, blank=True, related_name='events')

    def __str__(self):
        return self.title


# Model สำหรับคูปอง
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2)  # ส่วนลดเป็นตัวเลขหรือเปอร์เซ็นต์
    valid_from = models.DateField()
    valid_until = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='orders')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    
    # เก็บวันที่สั่งซื้อ
    order_date = models.DateTimeField(auto_now_add=True)

    # เก็บราคารวม
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        try:
            price = decimal.Decimal(self.menu.price)
        except Exception:
            price = decimal.Decimal("0.00")
        self.total_price = price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        local_time = timezone.localtime(self.order_date)
        return f"Order #{self.id} by {self.member.username} on {local_time.strftime('%d %b %Y, %I:%M %p')}"
