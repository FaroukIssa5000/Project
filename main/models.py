from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
import random
def generate_random_digits(length=6):
  digits = '0123456789'
  return ''.join(random.choice(digits) for i in range(length))
class City(models.TextChoices):
    Homs='حمص',
    Hama='حماه',
    Latakia='اللاذقية',
    Tartous='طرطوس',
    Aleppo='حلب',
    Edlib='إدلب',
    Alhasaka='الحسكة',
    Dairalzor='دير الزور',
    Damascus='دمشق',
    Alsowaidaa='السويداء',
    Daraa='درعا',
    Alraka='الرقة',

class UserType(models.TextChoices):
    CONTRACTOR='contractor',
    ENGNEER='engneer',
    CRAFTMAN='craftman',

class CatogaryOfEngneer(models.TextChoices):
    civil='الهندسة المدنية'
    architecture='الهندسة المعمارية'
    electrical ='الهندسة الكهربائية'
    drainage='هندسة الصرف الصحي'
    decoration='هندسة الديكور'
    airconditioning='هندسةالتكييف والتبريد' 
class CatogaryOfCraftman(models.TextChoices):
    builder='بناء'
    peton='نجار بيتون'
    carpenter='نجار أخشاب'
    blacksmither='حداد'
    paver='مبلط'
    painter='دهان'
    cladding='مليس'
    electricaler='كهربائي'
    sewager='حرفي الصرف الصحي'
    aluminum='نجار ألمنيوم'



class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')
        if not mobile:
            raise ValueError('mobile is not provided')
        user = self.model(
            email = email,
            first_name = first_name,
            last_name = last_name,
            mobile = mobile,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, first_name, last_name, mobile, password, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField( unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=10,unique=True,db_index=True)
    isVerified = models.BooleanField(default=False)
    userType=models.CharField(max_length=50)
    specialization=models.CharField(max_length=200)
    is_staff = models.BooleanField(default=True) 
    is_active = models.BooleanField(default=True) 
    is_superuser = models.BooleanField(default=False) 
    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['first_name','last_name','email']
    def __str__(self):
            return self.first_name +" "+ self.last_name
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

        

class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=generate_random_digits)  # Randomly generated verification code
    def __str__(self):
        return f"Verification code for user: {self.user.first_name +" "+ self.user.last_name}"
   

class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyName=models.CharField(max_length=200)
    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name
class Craftman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    craft = models.CharField(max_length=100)
    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name

class Engneer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certifcate = models.CharField(max_length=100)
    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name

   
class Portfolio(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    location = models.CharField(max_length=500,blank=False)
    timeForFinish = models.IntegerField(blank=False) 
    description = models.TextField()
    image1=models.ImageField( upload_to='media/portfolio_images/') 
    image2=models.ImageField( upload_to='media/portfolio_images/') 
    image3=models.ImageField( upload_to='media/portfolio_images/') 
    rating=models.IntegerField(default=0)
    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    mobileWork=models.CharField(max_length=10)
    image = models.ImageField( upload_to='media/profile_images/',null=True,blank=True)  
    biography = models.TextField()
    experienceYears = models.IntegerField()
    profileType=models.CharField(max_length=50)
    address=models.CharField(max_length=50,choices=City.choices)
    rating=models.IntegerField(default=0)
    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name

class Project(models.Model):
    contractor = models.ForeignKey(Contractor,on_delete=models.CASCADE)  
    projectName = models.CharField( max_length=100)  
    location = models.CharField(max_length=500)
    mobileCall=models.CharField(max_length=10)
    description=models.TextField()
    dateOfFinish = models.DateField()  
    
class CatogaryEngneerForProject(models.Model):
    catogary_eng = models.CharField(max_length=100)
    number_eng = models.IntegerField(blank=False)
    projectid_eng = models.ForeignKey(Project ,blank=False,on_delete=models.CASCADE)  


class CatogaryCraftmanForProject(models.Model):
    catogary_craft = models.CharField(max_length=100)
    number_craft = models.IntegerField(blank=False)
    projectid_craft = models.ForeignKey(Project,blank=False,on_delete=models.CASCADE)