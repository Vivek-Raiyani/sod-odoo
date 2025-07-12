from django.db import models
from accounts.models import User
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
class Item(models.Model):
    CATEGORY_CHOICES = [
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('worn', 'Worn'),
        ('well_worn', 'Well Worn'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='items/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    tags = models.ManyToManyField(Tag, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    swap_points= models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SwapRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='swap_requests')
    requested_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='swap_requests')
    
    # For direct swaps: the item being offered in exchange
    offered_item = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='offered_in_swaps',
        help_text="Item being offered in exchange (for direct swaps)"
    )
    
    # For point-based swaps
    via_points = models.BooleanField(default=False)
    points_used = models.IntegerField(
        default=0,
        help_text="Points to be deducted for this swap"
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        if self.via_points:
            return f"{self.user.username} wants {self.requested_item.title} for {self.points_used} points"
        else:
            return f"{self.user.username} wants {self.requested_item.title} for {self.offered_item.title if self.offered_item else 'Unknown Item'}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Either via_points should be True OR offered_item should be provided
        if self.via_points and self.offered_item:
            raise ValidationError("Cannot use both points and item for the same swap")
        
        if not self.via_points and not self.offered_item:
            raise ValidationError("Must either use points or provide an item to swap")
        
        # Ensure user owns the offered item
        if self.offered_item and self.offered_item.owner != self.user:
            raise ValidationError("You can only offer items that you own")
        
        # Ensure user doesn't request their own item
        if self.requested_item.owner == self.user:
            raise ValidationError("You cannot request your own item")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)