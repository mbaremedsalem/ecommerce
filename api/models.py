from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import UserManager 
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

Role=(
    ('Manager', 'Manager'),
    ('Vendor', 'Vendor'),
)  

class UserBerid(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=16,unique=True)
    email = models.EmailField(max_length=50,blank=True)
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    restricted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role= models.CharField(max_length=30, choices=Role, default='Manager')
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []

    def __str__(self): 
        return self.name 
    
def image_uoload_profile(instance,filname):
    imagename,extention =  filname.split(".")
    return "user/%s.%s"%(instance.id,extention)    

class Vendor(UserBerid):
    image=models.ImageField(upload_to=image_uoload_profile ,null=True)
   

class Manager(UserBerid):
    image=models.ImageField(upload_to=image_uoload_profile ,null=True)   


class Wallet(models.Model):
    balance= models.FloatField(max_length=255, default=0)
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    def __str__(self): 
        return f"Wallet balance: {self.balance}"
    
@receiver(post_save,sender=Vendor)   
def create_user_wallet(sender,instance,created,**kawargs):
    if created:
        Wallet.objects.create(vendor=instance)

def image_uoload_profile(instance,filname):
    imagename,extention =  filname.split(".")
    return "category/%s.%s"%(instance.id,extention)  

class Categorie(models.Model):
    nom=models.CharField(max_length=100)
    image = models.ImageField(upload_to=image_uoload_profile ,null=True)

    def __str__(self):
        return self.nom
    
class MarquePrive(models.Model):
    nom=models.CharField(max_length=100)

    def __str__(self):
        return self.nom
def image_uoload(instance,filname):
    imagename,extention =  filname.split(".")
    return "product/%s.%s"%(instance.id,extention)
    
class Produit(models.Model):
    available = models.BooleanField(default=True)
    nom = models.CharField(max_length=200)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.IntegerField(default=1)
    description = models.CharField(max_length=200)
    manager = models.ForeignKey(UserBerid, on_delete=models.CASCADE)
    marqueprives = models.ForeignKey(MarquePrive, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=image_uoload, null=True)

    def __str__(self):
        return self.nom


class Transaction(models.Model):
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.FloatField()
    numTransaction = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return f"Transaction {self.sender_wallet.vendor.phone}"


class Favoris(models.Model):
    vendor = models.ForeignKey(Vendor, related_name="client", on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, related_name="produit", on_delete=models.CASCADE)
    def __str__(self):
        return self.produit.nom