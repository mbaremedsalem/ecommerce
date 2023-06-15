from django.contrib import admin
from .models import UserBerid,Manager,Vendor,Wallet,Transaction,Categorie,MarquePrive,Produit,Favoris

# Register your models here.

class UserAdminConfig(admin.ModelAdmin):
    model = UserBerid
    search_fields = ('email', 'name', 'phone',)
    list_filter = ('email', 'name', 'phone', 'is_active', 'is_staff')
    ordering = ('name',)  # Update the ordering field here
    list_display = ('phone', 'email', 'name', 'is_superuser',
                    'is_active', 'is_staff', 'is_blocked', 'password',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone','image','role',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_blocked')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'phone', 'is_active', 'is_staff', 'is_blocked')
            }
         ),
    )

admin.site.register(UserBerid, UserAdminConfig)
admin.site.register(Vendor, UserAdminConfig)
admin.site.register(Manager, UserAdminConfig)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Categorie)
admin.site.register(MarquePrive)
admin.site.register(Produit)
admin.site.register(Favoris)

