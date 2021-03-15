from django.contrib import admin
from .models import User, Grampanchayat, Observar, District, Taluka, Panchayat, Payment, Agency, Confirmation, Audit
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','is_gp', 'is_observar', 'is_s2', 'is_staff', 'last_login', 'is_superuser', 'username','first_name','last_name', 'email', 'is_active', 'date_joined','password')

@admin.register(Grampanchayat)
class GrampanchayatAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'district', 'taluka', 'panchayat', 'designation', 'phone_number', 'date')
    
@admin.register(Observar)
class ObservarAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'first_name', 'last_name', 'username')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id','district', 'date',)

@admin.register(Taluka)
class TalukaAdmin(admin.ModelAdmin):
    list_display = ('id','district', 'date','taluka')

@admin.register(Panchayat)
class PanchayatAdmin(admin.ModelAdmin):
    list_display = ('id','panchayat', 'date','taluka')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'utrno', 'remark', 'status', 'phaseno') 

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'choose_goverment', 'choose_local', 'already_certified')

@admin.register(Confirmation)
class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'phaseno', 'yes_no')

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('id','status', 'date', 'document', 'phaseno')

