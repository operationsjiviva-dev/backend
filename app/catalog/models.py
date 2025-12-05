from django.db import models
from common.models import TimeStampedModel
import json


class FashionLine(TimeStampedModel):
    """High-level grouping like Couture, Diffuse, etc."""
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Gender(TimeStampedModel):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Collection(TimeStampedModel):
    """Curated grouping under a fashion line (Wedding, New In, Festive, etc.)."""
    fashion_line = models.ForeignKey(FashionLine, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=255)
    gender = models.ForeignKey(Gender, default=1, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("fashion_line", "name")

    def __str__(self):
        return f"{self.fashion_line.name} → {self.name}"


class Category(TimeStampedModel):
    """Product categories (hierarchical)."""
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="subcategories")
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    gender = models.ForeignKey(Gender, default=1, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("parent", "name")

    def __str__(self):
        return self.name


class Occasion(TimeStampedModel):
    """Occasions like Wedding, Mehendi, Cocktail, After Party."""
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    gender = models.ForeignKey(Gender, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    """Free-form product tags like 'Bestseller', 'New Arrival'."""
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ---------- Core Product Models ----------
class Product(TimeStampedModel):
    """Base product (design/idea) with shared details."""
    # sku_code = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=512)
    description = models.TextField(blank=True, null=True)
    fabric = models.CharField(max_length=255, default='', blank=True, null=True)
    color = models.CharField(max_length=255, default='', blank=True, null=True)
    primary_image = models.CharField(max_length=1000, default='')

    # relationships
    categories = models.ManyToManyField(Category, related_name="products", blank=True)
    collections = models.ManyToManyField(Collection, related_name="products", blank=True)
    occasions = models.ManyToManyField(Occasion, related_name="products", blank=True)
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)


    def __str__(self):
        return self.display_name


#TODO: add histories to product variant model to track updates
class ProductVariant(TimeStampedModel):
    """Variants of a product (size, SKU, stock, price)."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=50, blank=True, null=True)  # e.g. S, M, L, XL
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    # stock = models.PositiveIntegerField(default=0)

    # variant behavior
    is_primary = models.BooleanField(default=False)  # default shown on product page
    sort_order = models.PositiveIntegerField(default=0)  # for dropdown ordering

    class Meta:
        unique_together = ("product", "size")
        # ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.display_name} ({self.size or ''})"


class ProductImage(TimeStampedModel):
    """Images for a product, ordered for display."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=1000)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.display_name} image ({self.sort_order})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if self.sort_order == 0:
                self.product.primary_image = self.image_url
                self.product.save()
        except Exception as e:
            pass
        
    

class GenericBulkUploadResponse(TimeStampedModel):
    response_file_link = models.CharField(max_length=180, default='')
    status_choices = (
        ('INVALID_REQUEST_FILE', 'INVALID_REQUEST_FILE'),
        ('SERVER_ERROR', 'SERVER_ERROR'),
        ('SUCCESS', 'SUCCESS'),
        ('PROCESSING', 'PROCESSING'),
    )
    status = models.CharField(max_length=124, default='PROCESSING')
    error_trace = models.TextField(default='')
    process_start_time = models.DateTimeField(null=True)
    process_end_time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)


class GenericBulkUploadRequest(TimeStampedModel):
    response = models.OneToOneField(GenericBulkUploadResponse, null=True, on_delete=models.CASCADE)
    upload_type = models.CharField(max_length=72, default='')
    status_choices = (
        ('INVALID_REQUEST_FILE', 'INVALID_REQUEST_FILE'),
        ('SERVER_ERROR', 'SERVER_ERROR'),
        ('SUCCESS', 'SUCCESS'),
        ('PENDING', 'PENDING'),
        ('PROCESSING', 'PROCESSING'),
    )
    status = models.CharField(max_length=124, default='PENDING')
    params_passed = models.TextField(default='{}')
    request_file_link = models.CharField(max_length=180, default='')
    # redis_job_id = models.CharField(max_length=96, default='')
    admin_user = models.CharField(max_length=64, default='')

    @property
    def params_dict(self):
        return json.loads(self.params_passed)