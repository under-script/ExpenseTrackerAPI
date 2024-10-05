import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ExpenseTrackerAPI.settings')
django.setup()

from api.models import Category  # Replace with your actual app name

# List of categories to be added
categories = [
    'Groceries',
    'Leisure',
    'Electronics',
    'Utilities',
    'Clothing',
    'Health',
    'Others',
]

# Create categories
for category_name in categories:
    category, created = Category.objects.get_or_create(name=category_name)
    if created:
        print(f'Created category: {category_name}')
    else:
        print(f'Category already exists: {category_name}')
