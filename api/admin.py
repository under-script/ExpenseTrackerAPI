from django.contrib import admin

from api.models import Expense, Category


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 10

    class Meta:
        abstract = True


class ExpenseAdmin(BaseAdmin):
    list_display = [f.name for f in Expense._meta.fields]


class CategoryAdmin(BaseAdmin):
    list_display = [f.name for f in Category._meta.fields]


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
