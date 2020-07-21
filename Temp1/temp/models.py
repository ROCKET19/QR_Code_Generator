from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import types
import qrtools



class Demo(models.Model):
    # iid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, default=User.objects.last().username)
    address = models.CharField(max_length=256, default="na")
    phn_num = models.CharField(max_length=15, default="")
    pin_code = models.CharField(max_length=8, default="")
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        maker = self.name + '\n' + self.phn_num
        qrcode_img = qrcode.make(maker)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Demo.objects.create()

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()


class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='London')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)
    objects = models.Manager()
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    london = UserProfileManager()
    object = models.Manager()

    def save(self, *args, **kwargs):
        maker = self.user
        qrcode_img = qrcode.make(maker)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.user}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])
    post_save.connect(create_profile, sender=User)


