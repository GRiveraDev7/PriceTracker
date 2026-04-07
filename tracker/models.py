from django.db import models

class Store(models.Model):
    DAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    base_url = models.URLField(blank=True)
    
    promo_change_day = models.PositiveSmallIntegerField(
        choices=DAY_CHOICES,
        null=True,
        blank=True,
        help_text="Day of the week when specials usually change."
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100, blank=True)
    weight_grams = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    barcode = models.CharField(
        max_length=100,
        blank=True,
        help_text="EAN/UPC/GTIN if known."
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "brand", "weight_grams"],
                name="unique_product_name_brand_weight"
            )
        ]

    def __str__(self):
        parts = [self.brand, self.name, self.weight_grams]
        return " ".join(part for part in parts if part).strip()


class StoreProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="store_products"
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="store_products"
    )

    external_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="Store-specific product ID if available."
    )
    product_url = models.URLField()
    current_title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Current title as shown on the store website."
    )

    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    is_available = models.BooleanField(default=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    last_price_change = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["store__name", "product__name"]
        constraints = [
            models.UniqueConstraint(
                fields=["store", "product"],
                name="unique_store_product_pair"
            )
        ]

    def __str__(self):
        return f"{self.product} @ {self.store}"


class PriceRecord(models.Model):
    store_product = models.ForeignKey(
        StoreProduct,
        on_delete=models.CASCADE,
        related_name="price_records"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_at = models.DateTimeField()
    is_on_special = models.BooleanField(default=False)
    special_text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-checked_at"]

    def __str__(self):
        return f"{self.store_product} - {self.price} on {self.checked_at}"