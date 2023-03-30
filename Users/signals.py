from django.db.models.signals import post_save
from .models import MyUser,Profile
from django.dispatch import receiver


@receiver(post_save,sender=MyUser)
def create_rofile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        # Transactions.objects.create(user=instance)
# @receiver(post_save,sender=MyUser)
# def save_rofile(sender,instance,created,**kwargs):
#     instance.profile.save()