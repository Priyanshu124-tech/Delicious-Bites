# Delicious Bites

Django-based restaurant ordering app with menu management, user accounts, cart, and order billing.

Restaurant Project is a Django application for managing a restaurant's menu and orders.
Admins can create and edit menu items, assign categories, and upload photos.
Customers can browse the menu, add items to a cart, and update quantities.
A simple checkout flow produces an order bill for each purchase.
Includes a management command to populate sample menu data for testing.
Built with Django templates and SQLite for quick local development.
Easy to extend with payment gateways, delivery zones, or a REST API.

## Quick start

```powershell
# Create virtualenv and activate (Windows PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install Django (or use requirements.txt if present)
pip install django

# Apply migrations and create superuser
python manage.py migrate
python manage.py createsuperuser

# (Optional) populate sample data
python manage.py populate_menu

# Run the dev server
python manage.py runserver
```

---

This README was added to the repository and pushed to GitHub. Feel free to edit or ask me to expand it.