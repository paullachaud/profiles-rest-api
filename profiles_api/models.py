from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

from django.utils.translation import gettext_lazy as _

class UserProfileManager(BaseUserManager):
    """Manager for user profile"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)
        
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email
# Create your models here.

class Goal(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    deadline = models.DateTimeField()
    name = models.CharField(max_length=126)
    description = models.TextField(max_length=255)
    # TODO: state { start current end }
    # TODO: measures { list<habits>}




class Habit(models.Model):
    user = models.ForeignKey(UserProfile, related_name='habits', on_delete= CASCADE)
    class Frequency(models.TextChoices):
        HOURLY= 'Hourly'
        DAILY = 'Daily'
        WEEKLY = 'Weekly'
        MONTHLY = 'Monthly'

    created = models.DateTimeField(auto_now_add= True)
    frequency = models.CharField(
        max_length = 10,
        choices= Frequency.choices,
        default= Frequency.DAILY,
    )
    name = models.CharField(max_length=30)
    # TODO: Category
    # TODO: Quantity/Units/Duration
    # TODO: streak
    # TODO: Reminder
    # TODO: When {time of day (morning, evening, afternoon, anytime), actual time}
    # TODO: Excpected time

    def __str__(self):
        return self.name

class HabitInstance(models.Model):

    class Day(models.TextChoices):
        MONDAY = 'Mon', _('Monday')
        TUESDAY = 'Tue', _('Tuesday')
        WEDNESDAY = 'Wed', _('Wednesday')
        THURSDAY = 'Thur', _('Thursday')
        FRIDAY = 'Fri', _('Friday')
        SATURDAY = 'Sat', _('Saturday')
        SUNDAY = 'Sun', _('Sunday')

    class Status(models.IntegerChoices):
        INCOMPLETE = 0
        COMPLETE = 1
        SKIPPED = 2

    habit = models.ForeignKey(Habit, related_name='habit_instance', on_delete=models.CASCADE)
    status = models.IntegerField(
        choices= Status.choices,
        default= Status.INCOMPLETE
    )
    day = models.CharField(
        max_length= 4,
        choices = Day.choices,
        default= Day.MONDAY
    )
    # TODO: Time complete
    note = CharField(max_length = 255)

class Todo(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField()

    def __str__(self):
        return self.title