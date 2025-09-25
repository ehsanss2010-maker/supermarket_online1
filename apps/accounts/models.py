from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class User(AbstractUser, BaseModel):
    # فیلدهای اضافی برای کاربر
    phone = models.CharField(_('phone number'), max_length=15, blank=True, null=True, unique=True)
    national_id = models.CharField(_('national ID'), max_length=10, blank=True, null=True, unique=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to='users/avatars/', blank=True, null=True)

    # آدرس‌های کاربر
    default_shipping_address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    default_billing_address = models.ForeignKey(
        'Address',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    # تنظیمات کاربر
    email_verified = models.BooleanField(_('email verified'), default=False)
    phone_verified = models.BooleanField(_('phone verified'), default=False)
    newsletter_subscription = models.BooleanField(_('newsletter subscription'), default=True)

    # امتیاز وفاداری
    loyalty_points = models.PositiveIntegerField(_('loyalty points'), default=0)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def has_complete_profile(self):
        return all([self.first_name, self.last_name, self.email, self.phone])


class Address(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    title = models.CharField(_('address title'), max_length=100)  # مثلا: خانه، محل کار
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    phone = models.CharField(_('phone number'), max_length=15)

    # آدرس
    province = models.CharField(_('province'), max_length=100)
    city = models.CharField(_('city'), max_length=100)
    address_line = models.TextField(_('address line'))
    postal_code = models.CharField(_('postal code'), max_length=10)

    # موقعیت جغرافیایی (اختیاری)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # پیش‌فرض
    is_default_shipping = models.BooleanField(_('default shipping address'), default=False)
    is_default_billing = models.BooleanField(_('default billing address'), default=False)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
        ordering = ['-is_default_shipping', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.city}"

    def save(self, *args, **kwargs):
        # اگر این آدرس به عنوان پیش‌فرض تنظیم شد، سایر آدرس‌های کاربر را آپدیت کن
        if self.is_default_shipping:
            Address.objects.filter(user=self.user, is_default_shipping=True).update(is_default_shipping=False)
        if self.is_default_billing:
            Address.objects.filter(user=self.user, is_default_billing=True).update(is_default_billing=False)
        super().save(*args, **kwargs)


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # اطلاعات شخصی
    gender = models.CharField(_('gender'), max_length=1, choices=[
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other'))
    ], blank=True, null=True)

    # ترجیحات
    preferred_language = models.CharField(_('preferred language'), max_length=10, default='fa')
    preferred_currency = models.CharField(_('preferred currency'), max_length=3, default='IRT')

    # تنظیمات نوتیفیکیشن
    email_notifications = models.BooleanField(_('email notifications'), default=True)
    sms_notifications = models.BooleanField(_('SMS notifications'), default=True)
    push_notifications = models.BooleanField(_('push notifications'), default=True)

    # آمار کاربر
    total_orders = models.PositiveIntegerField(_('total orders'), default=0)
    total_spent = models.DecimalField(_('total spent'), max_digits=12, decimal_places=2, default=0)
    last_order_date = models.DateTimeField(_('last order date'), null=True, blank=True)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self):
        return f"Profile of {self.user.username}"