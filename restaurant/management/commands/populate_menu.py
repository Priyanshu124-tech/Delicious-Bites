from django.core.management.base import BaseCommand
from restaurant.models import MenuItem

class Command(BaseCommand):
    help = 'Populate the database with sample menu items'

    def handle(self, *args, **options):
        # Clear existing items
        MenuItem.objects.all().delete()
        
        # Italian dishes
        MenuItem.objects.create(
            name="Truffle Margherita Pizza",
            description="Hand-stretched dough topped with San Marzano tomatoes, fresh mozzarella di bufala, aromatic truffle oil, and fresh basil leaves",
            price=28.00,
            category="Italian"
        )
        
        MenuItem.objects.create(
            name="Lobster Ravioli",
            description="Handmade pasta parcels filled with fresh Maine lobster, served in a delicate saffron cream sauce with cherry tomatoes",
            price=42.00,
            category="Italian"
        )
        
        MenuItem.objects.create(
            name="Osso Buco Milanese",
            description="Slow-braised veal shanks in white wine and vegetables, served with saffron risotto and gremolata",
            price=48.00,
            category="Italian"
        )

        # Indian dishes
        MenuItem.objects.create(
            name="Butter Chicken",
            description="Tender chicken pieces in a rich, creamy tomato-based curry with aromatic spices, served with basmati rice",
            price=24.00,
            category="Indian"
        )
        
        MenuItem.objects.create(
            name="Lamb Biryani",
            description="Fragrant basmati rice layered with spiced lamb, caramelized onions, mint, and saffron, cooked in a sealed pot",
            price=26.00,
            category="Indian"
        )
        
        MenuItem.objects.create(
            name="Paneer Makhani",
            description="Fresh cottage cheese cubes in a velvety tomato and cashew curry, finished with cream and aromatic spices",
            price=22.00,
            category="Indian"
        )

        # Chinese dishes
        MenuItem.objects.create(
            name="Peking Duck",
            description="Crispy roasted duck served with pancakes, spring onions, cucumber, and hoisin sauce",
            price=38.00,
            category="Chinese"
        )
        
        MenuItem.objects.create(
            name="Kung Pao Chicken",
            description="Wok-fried chicken with peanuts, vegetables, and chilies in a savory and slightly sweet sauce",
            price=20.00,
            category="Chinese"
        )
        
        MenuItem.objects.create(
            name="Szechuan Mapo Tofu",
            description="Silky tofu in a spicy, aromatic sauce with ground pork and Szechuan peppercorns",
            price=18.00,
            category="Chinese"
        )

        # Mexican dishes
        MenuItem.objects.create(
            name="Mole Poblano",
            description="Traditional Mexican dish with chicken in a rich, complex sauce made from chocolate and various spices",
            price=26.00,
            category="Mexican"
        )
        
        MenuItem.objects.create(
            name="Carne Asada Tacos",
            description="Grilled marinated beef served in corn tortillas with onions, cilantro, and salsa verde",
            price=16.00,
            category="Mexican"
        )
        
        MenuItem.objects.create(
            name="Chiles en Nogada",
            description="Poblano peppers stuffed with picadillo, topped with walnut cream sauce and pomegranate seeds",
            price=24.00,
            category="Mexican"
        )

        # Other dishes
        MenuItem.objects.create(
            name="Wagyu Beef Tenderloin",
            description="Premium A5 Wagyu beef tenderloin, grilled to perfection and served with seasonal vegetables and red wine reduction",
            price=85.00,
            category="Other"
        )
        
        MenuItem.objects.create(
            name="Pan-Seared Salmon",
            description="Fresh Atlantic salmon with lemon herb crust, served with asparagus and hollandaise sauce",
            price=32.00,
            category="Other"
        )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated menu with sample items')
        )
