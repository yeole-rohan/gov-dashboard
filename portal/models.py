from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, EmailValidator, validate_slug, URLValidator

# Create your models here.
''' Global decleration '''
PAYMENT_STATUS = [
    ('pending' , 'Pending'),
    ('matched' , 'Matched'),
    ('unmatched' , 'Unmatched')
]
DESIGNATION = [
    ('gram_sevak', 'Gram Sevak'),
    ('gram_vikas_adhikari', 'Gram Vikas Adhikari'),
]
''' Abstract User creation '''
class User(AbstractUser):
    is_gp = models.BooleanField(default=False)
    is_observar = models.BooleanField(default=False)
    is_s2 = models.BooleanField(default=False)
    is_ceo = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return str(self.id)

class Grampanchayat(models.Model):
    user = models.OneToOneField("User", primary_key=True, verbose_name="GP", on_delete=models.CASCADE)
    first_name = models.CharField( max_length=100)
    last_name = models.CharField( max_length=100)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    taluka = models.ForeignKey('Taluka', on_delete=models.CASCADE)
    panchayat = models.ForeignKey('Panchayat', on_delete=models.CASCADE)
    designation = models.CharField( choices=DESIGNATION, max_length=200, )
    phone_regex = RegexValidator(regex=r'^\d{10,10}$', message="Phone number must be entered in the format: '1234567890'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True)
    date = models.DateTimeField(auto_now=True)
    email =  models.EmailField(max_length=254, validators=[EmailValidator], unique=True)
    username = models.TextField()

    class Meta:
        verbose_name = "Grampanchayat"
        verbose_name_plural = "Grampanchayats"

    def __str__(self):
        return str(self.first_name + self.last_name)

class Observar(models.Model):
    user = models.OneToOneField("User", primary_key=True, verbose_name="observar", on_delete=models.CASCADE)
    first_name = models.CharField( max_length=100)
    last_name = models.CharField( max_length=100)
    date = models.DateTimeField(auto_now=True)
    username = models.TextField()
    
    class Meta:
        verbose_name = "Observar"
        verbose_name_plural = "Observars"

    def __str__(self):
        return str(self.first_name + self.last_name)

class CEO(models.Model):
    user = models.OneToOneField("User", primary_key=True, verbose_name="CEO", on_delete=models.CASCADE)
    first_name = models.CharField( max_length=100)
    last_name = models.CharField( max_length=100)
    date = models.DateTimeField(auto_now=True)
    username = models.TextField()
    
    class Meta:
        verbose_name = "CEO"
        verbose_name_plural = "CEO"

    def __str__(self):
        return str(self.first_name + self.last_name)

class S2(models.Model):
    user = models.OneToOneField("User", primary_key=True, verbose_name="account", on_delete=models.CASCADE)
    first_name = models.CharField( max_length=100)
    last_name = models.CharField( max_length=100)
    date = models.DateTimeField(auto_now=True)
    username = models.TextField(default="ac")

    class Meta:
        verbose_name = "S2"
        verbose_name_plural = "S2S"

    def __str__(self):
        return str(self.first_name + self.last_name)

''' Chained models '''
class District(models.Model):
    district = models.CharField(max_length=1000)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.district)

class Taluka(models.Model):
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    taluka = models.CharField(max_length=1000)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.taluka)

class Panchayat(models.Model):
    taluka = models.ForeignKey('Taluka', on_delete=models.CASCADE)
    panchayat = models.CharField(max_length=1000)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.panchayat)

''' Normal Models'''
class Confirmation(models.Model):
    date = models.DateTimeField(auto_now=True)
    phaseno = models.PositiveSmallIntegerField(default=1)
    yes_no = models.BooleanField(default=False)
    user = models.ManyToManyField("Grampanchayat", verbose_name="Grampanchayat Confirmation")

    class Meta:
        verbose_name = "Confirmation"
        verbose_name_plural = "Confirmations"

    def __str__(self):
        return str(self.id)

class Payment(models.Model):
    user = models.ManyToManyField("Grampanchayat", verbose_name="Grampanchayat Payment")
    date = models.DateTimeField( auto_now=True)
    utrno = models.PositiveIntegerField()
    phaseno = models.PositiveSmallIntegerField(default=1)
    remark = models.CharField(max_length=500)
    status = models.CharField(choices=PAYMENT_STATUS, max_length=1000,default="pending")

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return str(self.id)

class Audit(models.Model):
    user = models.ManyToManyField("Grampanchayat", verbose_name="Grampanchayat Audit")
    date = models.DateTimeField( auto_now=True)
    document = models.FileField(upload_to="document/", max_length=100)
    phaseno = models.PositiveSmallIntegerField()
    status = models.CharField(choices=PAYMENT_STATUS, max_length=1000,default="pending")

    class Meta:
        verbose_name = "Audit"
        verbose_name_plural = "Audits"

    def __str__(self):
        return str(self.id)

class Servilence(models.Model):
    user = models.ManyToManyField("Grampanchayat", verbose_name="Grampanchayat Servilence")
    date = models.DateTimeField( auto_now=True)
    document = models.ImageField( upload_to="document/", height_field=None, width_field=None, max_length=None)
    phoseno = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Servilence"
        verbose_name_plural = "Servilences"

    def __str__(self):
        return str(self.id)

class ServilencePayment(models.Model):
    user = models.ManyToManyField("Grampanchayat", verbose_name="Grampanchayat ServilencePayment")
    date = models.DateTimeField( auto_now=True)
    phoseno = models.PositiveSmallIntegerField()
    utrno = models.PositiveIntegerField()
    remark = models.CharField(max_length=500)
    status = models.CharField(choices=PAYMENT_STATUS, max_length=1000)
    class Meta:
        verbose_name = "ServilencePayment"
        verbose_name_plural = "ServilencePayments"

    def __str__(self):
        return str(self.id)

class Agency(models.Model):
    user = models.ForeignKey("User", verbose_name="user_agency", on_delete=models.CASCADE)
    choose_goverment = models.BooleanField(default=False)
    choose_local = models.BooleanField(default=False)
    already_certified = models.BooleanField(default=False)
    date = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.choose_goverment) + ' ' + str(self.choose_local)
