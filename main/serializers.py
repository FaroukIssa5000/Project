from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import serializers
from .models import *

class CraftmanSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Craftman
        fields = ('craft',)

class EngneerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engneer
        fields = ('certifcate',)

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = ('companyName',)      

class UserSerializer(serializers.ModelSerializer):
    

    class Meta:
         model = User
         fields=['id','email','mobile','password','first_name','last_name','userType','specialization']

  


class VerificationSerializer(serializers.Serializer):
    mobile=serializers.CharField(max_length=10)
    verificationCode=serializers.CharField(max_length=6)
        


class MobileChangeSerializer(serializers.Serializer):
    mobile_new = serializers.CharField(max_length=10)



    


class ProfileSerializer(serializers.ModelSerializer):
    image_url=serializers.SerializerMethodField()
    profileType=serializers.CharField(required=False)
    specialization=serializers.ReadOnlyField(source='user.specialization')
    fname = serializers.ReadOnlyField(source='user.first_name')
    lname = serializers.ReadOnlyField(source='user.last_name')
    class Meta:
        model = Profile
        fields = ('fname','lname','specialization' ,'biography', 'experienceYears','image_url','image','address','profileType','mobileWork')
    def get_image_url(self,obj):
        if obj.image:
            return obj.image.url 


class ContractorProfilesPublicSerializer(serializers.ModelSerializer):
    fname = serializers.ReadOnlyField(source='user.first_name')
    lname = serializers.ReadOnlyField(source='user.last_name')
    image_url = serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields=('image_url','fname','lname','rating')

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

   
    

class EngneerProfilesPublicSerializer(serializers.ModelSerializer):
    fname = serializers.ReadOnlyField(source='user.first_name')
    lname = serializers.ReadOnlyField(source='user.last_name')
    specialization=serializers.ReadOnlyField(source='user.specialization')

    image_url = serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields=('image_url','fname','lname','rating','specialization')

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None



class CraftmanProfilesPublicSerializer(serializers.ModelSerializer):
    fname = serializers.ReadOnlyField(source='user.first_name')
    lname = serializers.ReadOnlyField(source='user.last_name')
    specialization=serializers.ReadOnlyField(source='user.specialization')

    image_url = serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields=('image_url','fname','lname','rating','specialization')

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


class PortifolioSerializer(serializers.ModelSerializer):

    class Meta:
        model=Portfolio
        fields=('location','timeForFinish','description','image1','image2','image3')

class IdentificationUserSerializer(serializers.ModelSerializer):
    profileImage = serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('first_name','last_name','specialization','profileImage')

    def get_profileImage(self, obj):
        if obj.profile.image:
            return obj.profile.image.url
        return None

class PortifolioPublicSerializer(serializers.ModelSerializer):
    
    image1_url = serializers.SerializerMethodField()
    image2_url = serializers.SerializerMethodField()
    image3_url = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = ('location', 'timeForFinish', 'description', 'image1_url', 'image2_url', 'image3_url')

   
    def get_image1_url(self, obj):
        if obj.image1:
            return obj.image1.url
        return None

    def get_image2_url(self, obj):
        if obj.image2:
            return obj.image2.url
        return None

    def get_image3_url(self, obj):
        if obj.image3:
            return obj.image3.url
        return None
    
class PersonalPortifolioSerializer(serializers.Serializer):
    identificationUser =IdentificationUserSerializer(source='user')
    portfolios=PortifolioPublicSerializer(many=True)

class CatogaryEngneerSerilizer(serializers.ModelSerializer):
    class Meta:
        model= CatogaryEngneerForProject
        fields=('number_eng','catogary_eng')        


class CatogaryCraftmanSerilizer(serializers.ModelSerializer):
    class Meta:
        model= CatogaryCraftmanForProject
        fields=('catogary_craft','number_craft')

  

class ProjectSerializer(serializers.ModelSerializer):
    catogary_engneer= CatogaryEngneerSerilizer(many=True)
    catogary_craftman=CatogaryCraftmanSerilizer(many=True)
    class Meta:
        model=Project
        fields=('projectName','location','mobileCall','dateOfFinish','description','catogary_engneer','catogary_craftman')



       




# class ProjectRegisterSerialilizer(serializers.Serializer):
#     catogary_engneer= CatogaryEngneerSerilizer(many=True)
#     catogary_craftman=CatogaryCraftmanSerilizer(many=True)
#     project_data=ProjectSerializer(source='project')
#########################################################################################################33
#####################################################################################################333



# curl -X POST http://localhost:8000/project/ \
#      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIxOTEzMzQ0LCJpYXQiOjE3MjE5MTMwNDQsImp0aSI6IjllMGM1OWY5YWE0YzQzMWVhMjNiZGFjMmNkMTg2ZWU0IiwidXNlcl9pZCI6NH0.PfxCevxzASGd9jTICTvg6-Utuz4XdZYrSaSuD1Ho2i0" \
#      -H "Content-Type: application/json" \
#      -d '{
#          "projectName": "New Project",
#          "location": "Location",
#          "mobileCall": "1234567890",
#          "dateOfFinish": "2024-12-31",
#          "description": "Project Description",
        
#      }'


# class ProjectSerializer(serializers.ModelSerializer):
#     eng=CatengSerilizer(many=True)
#     craft=CatcraftSerilizer(many=True)
    
#     class Meta:
#         model= Project
#         fields=('projectname','location','dateofstart','dateoffinish','eng','craft','phone')        

