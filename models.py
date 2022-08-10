from django.db import models
from django.core import exceptions

TYPE_CHOICES = [
    ('OFFER', 'offer'),
    ('CATEGORY', 'category')
]


class ShopUnit(models.Model):
    id = models.UUIDField(primary_key=True, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    price = models.PositiveBigIntegerField(null=True, default=None)
    date = models.DateTimeField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=8)

    # Service data

    # The number of the products in the category subtree. Equals to 1, if it's a product
    tree_products_count = models.PositiveBigIntegerField(default=0)

    # The sum of the product prices in the category subtree. Equals to price, if it's a product
    tree_total_price = models.PositiveBigIntegerField(default=0)

    def get_price(self):
        if self.price is None:
            return 0
        return self.price

    @classmethod
    def get_unit(cls, pk):
        try:
            return ShopUnit.objects.get(pk=pk)
        except exceptions.ObjectDoesNotExist:
            return None

    def update(self, child=None):
        if child:
            self.date = child.date
        self.update_price()
        self.save()

        if self.parent:
            self.parent.update(child=self)

    def update_price(self):
        """
        Recount category/product price
        """

        self.update_tree_products_count()
        self.update_tree_total_price()

        if self.type == 'CATEGORY':
            if self.tree_products_count == 0:
                self.price = None
            else:
                self.price = self.tree_total_price // self.tree_products_count

    def update_tree_products_count(self):
        """
        Recounts the number of the products in subtree by summing values in children
        """

        if self.type == 'OFFER':
            self.tree_products_count = 1
            return
        self.tree_products_count = 0
        for child in self.shopunit_set.all():
            self.tree_products_count += child.tree_products_count

    def update_tree_total_price(self):
        """
        Recount the sum of the products in subtree by summing values in children
        """
        if self.type == 'OFFER':
            self.tree_total_price = self.get_price()
            return
        self.tree_total_price = 0
        for child in self.shopunit_set.all():
            self.tree_total_price += child.tree_total_price
