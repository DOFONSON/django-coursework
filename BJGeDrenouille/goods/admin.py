from django.contrib import admin

from goods.models import Companies, Products

@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}