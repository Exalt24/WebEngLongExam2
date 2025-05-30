from django.db import models
from django.conf import settings
import uuid

class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("user", "name")
        ordering = ("name",)

class Entry(models.Model):
    INCOME = 'IN'
    EXPENSE = 'EX'
    TYPE_CHOICES = [(INCOME, 'Income'), (EXPENSE, 'Expense')]

    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    title    = models.CharField(max_length=50)
    amount   = models.DecimalField(max_digits=10, decimal_places=2)
    date     = models.DateField()
    type     = models.CharField(max_length=2, choices=TYPE_CHOICES)
    notes    = models.TextField(blank=True, max_length=80)

    class Meta:
        unique_together = (
            ('user', 'title', 'date', 'category'),
        )

class Budget(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(
        'Category',
        null=True, blank=True,
        on_delete=models.CASCADE,
        help_text="Leave blank for a total budget"
    )
    month    = models.DateField(help_text="First day of the month this budget applies to")
    amount   = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'category', 'month')
        ordering = ('-month',)

    def __str__(self):
        if self.category:
            return f"{self.user} – {self.month:%b %Y} – {self.category.name}: ₱{self.amount}"
        return f"{self.user} – {self.month:%b %Y} – Total: ₱{self.amount}"

class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return f"Password reset token for {self.user.email}"
    
class ContactMessage(models.Model):
    """Model for storing contact form messages."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class EmailVerificationToken(models.Model):
    user       = models.OneToOneField(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE)
    token      = models.UUIDField(default=uuid.uuid4,
                                 unique=True,
                                 editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used       = models.BooleanField(default=False)

    def __str__(self):
        return f"Verify {self.user.email} → {self.token}"