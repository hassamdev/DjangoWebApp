from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,Group,Permission
from django.db import models
# from django.utils import timezone

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class employees(AbstractBaseUser, PermissionsMixin):
    emp_id = models.BigAutoField(auto_created=True,primary_key=True,verbose_name="_emp_id")
    email = models.EmailField(unique=True,verbose_name="_email")
    f_name = models.CharField(max_length=30,verbose_name="_f_name")
    l_name = models.CharField(max_length=30,verbose_name="_l_name")
    cell_no = models.CharField(max_length=13,verbose_name="_cell_no")
    designation = models.CharField(max_length=15,verbose_name="_designation")
    gender = models.CharField(max_length=15,verbose_name='_gender')
    password = models.CharField(max_length=254,verbose_name="_password")
    birth_date = models.DateField(default='2000-7-22')
    nfc_num = models.BigIntegerField(verbose_name="_nfc_num",default=-1)
    image = models.ImageField(null=True,upload_to='images/')

    is_active = models.BooleanField(default=True,verbose_name="is_active")
    is_staff = models.BooleanField(default=False,verbose_name="is_staff")
    
    groups = models.ManyToManyField(Group, verbose_name='Groups', blank=True, related_name='customuser_groups')

    # Set a unique related_name for the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='User permissions',
        blank=True,
        related_name='customuser_user_permissions'
    )


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    
    def is_valid(self):
        # print(self.email,self.f_name)
        if len(self.email)>253:
            return (False,"email is too large!")
        elif len(self.f_name)>30 or len(self.l_name)>30:
            return (False,"First or Last name is too large!")
        elif len(self.cell_no)>13:
            try:
                int(self.cell_no)
            except Exception as err:
                return (False,"wrong Cell no!")
            return (False,"Cell no should be =<13 numbers") 
        elif len(self.password) <8 or len(self.password)>254:
            return (False,"password should be =<8 and >=254")
        
        try:
            employees.objects.get(email = self.email)
            return  (False,"Email Already Exist!")
        except Exception as err:
            pass

        
        return (True,'correct')
        
        


class daily_hours(models.Model):
    emp_id = models.ForeignKey(employees,on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    hours = models.TimeField()

    def __str__(self) -> str:
        return self.emp_id,self.date,self.hours


class daily_status(models.Model):
    status_id = models.IntegerField(auto_created=True,primary_key=True,verbose_name="status_id")
    emp_id = models.ForeignKey(employees,on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=9)

    def __str__(self) -> str:
        return self.status_id