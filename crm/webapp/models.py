from django.db import models
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.full_name} {self.email} {self.created_at}")
    


# Model for product
class Product(models.Model):
        client = models.ForeignKey("Client", on_delete=models.CASCADE, related_name='product')
        product_name = models.CharField(max_length=100)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        date = models.DateTimeField(auto_now_add=True)
        

        def __str__(self):
            return f"product for {self.client.full_name} price {self.price}"   
        


# Signal to send email when a new product is purchased 
@receiver(post_save, sender=Product)
def send_thank_you_email(sender, instance, created, **kwargs):
     if created: # Ensures the email is sent only when a new purchase is added
            subject = "Thank You for Your Purchase!"
            message = f"Dear {instance.client.full_name},\n\nThank you for purchasing {instance.product_name} for ${instance.price}. We appreciate your business!\n\nBest regards,\nCrispy Cluck’s Fried Chicken"
            recipient_email = instance.client.email


            send_mail(
            subject,
            message,
            'your_email@gmail.com',  # Sender's email
            [recipient_email],  # Corrected recipient_list argument
            fail_silently=False,
        )
            
