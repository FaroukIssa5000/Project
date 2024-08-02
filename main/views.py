# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view,permission_classes

from django.contrib.auth.hashers import make_password
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from .serializers import *
import random
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication


crafts_catogary = {
    "builder":"حرفي بناء",
    "peton":"حرفي نجارة البيتون",
    "carpenter":"حرفي نجارةالخشب",
    "blacksmither":"حرفي الحدادة",
    "paver":"حرفي أرضيات",
    "painter":"حرفي دهان",
    "cladding":"حرفي تلييس",
    "electricaler":"حرفي كهربائي",
    "sewager":"حرفي الصرف الصحي",
    "aluminum":"حرفي نجارة الألمنيوم",
}
certicicates_catogary={
    "civil":"الهندسة المدنية",
    "architecture":"الهندسة المعمارية",
    "electrical":"الهندسة الكهربائية",
    "drainage":"هندسة الصرف الصحي",
    "decoration":"هندسةالديكور",
    "airconditioning":"هندسة التكييف"
}  

def generate_random_digits(length=6):
  digits = '0123456789'
  return ''.join(random.choice(digits) for i in range(length))



class UserView(APIView):
   
   def get(self,request,pk=None,format=None):
     if pk==None: 
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)
     else:
         user=User.objects.get(id=pk)
         serializer=UserSerializer(user)
         return Response(serializer.data)
   
   def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])
            user=serializer.save()
            verification_code = generate_random_digits(length=6)
            verification_code_obj = VerificationCode.objects.create(user=user, code=verification_code)
            verification_code_obj.save()
            if serializer.validated_data['userType'] == 'contractor':
                contractor_obj=Contractor.objects.create(user=user,companyName=serializer.validated_data['specialization'])
                contractor_obj.save()
            elif serializer.validated_data['userType'] == 'craftman':
                chosen_category_value = serializer.validated_data['specialization']  # Assuming 'specialization' is the field name
                category_label=None

                for choice,craft in crafts_catogary.items():
                    if choice == chosen_category_value:  # Check for matching value
                       category_label = craft
                       break
                craftman_obj=Craftman.objects.create(user=user,craft=category_label)
                craftman_obj.save()
            elif serializer.validated_data['userType'] == 'engneer':
                chosen_category_value = serializer.validated_data['specialization']  
                for choice,certificate in certicicates_catogary.items():
                    if choice == chosen_category_value:  # Check for matching value
                       category_label = certificate
                       break
                engneer_obj=Engneer.objects.create(user=user,certifcate=category_label)
                engneer_obj.save()
            else:
                user.delete()
                raise ValidationError("userType not in (contarctor,engneer,craftman) or ")         
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   



       
class VerifyView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = VerificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = request.user  
                mobile_number = serializer.validated_data["mobile"]
                verification_code = serializer.validated_data["verificationCode"]

                if user.mobile != mobile_number:
                    return Response({"details": "Mobile number mismatch. Please verify the mobile number associated with your account."}, status=status.HTTP_400_BAD_REQUEST)

                verification_code_obj = VerificationCode.objects.get(user=user, code=verification_code)
                verification_code_obj.save()
               #  verification_code_obj.delete()  # Delete used verification code

                user.isVerified = True
                user.save()

                return Response({"details": "Account verified successfully"}, status=status.HTTP_200_OK)
            except (User.DoesNotExist, VerificationCode.DoesNotExist):
                return Response({"details": "Invalid verification code or user not found"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"details": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class MobileChangeView(APIView):
     permission_classes = [IsAuthenticated]
     
     def patch(self,request,format=None):
         serializer=MobileChangeSerializer(data=request.data)
         user=request.user
         if serializer.is_valid():
             verification_code=VerificationCode.objects.filter(user=user)
             verification_code.delete()
             user.mobile=serializer.validated_data['mobile_new']
             verification_code = generate_random_digits(length=6)
             verification_code_obj = VerificationCode.objects.create(user=user, code=verification_code)
             verification_code_obj.save()
             user.save()
             return Response({"details":"mobile number changed"},status=status.HTTP_200_OK)
         else: return Response({serializer.errors},status=status.HTTP_400_BAD_REQUEST)

             
class ProfileView(APIView):
     permission_classes = [IsAuthenticated]
     authentication_classes = [JWTAuthentication]
     def post(self,request,format=None):
               serializer=ProfileSerializer(data=request.data)
               if serializer.is_valid():
                     user=request.user
                     user_type=user.userType

                     serializer.validated_data['profileType']=user_type
                     serializer.save(user=user)
                     return Response(serializer.data,status=status.HTTP_201_CREATED)
               else:
                   return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


  
                       
class ContractorProfilesView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,pk=None,formate=None):

        if pk==None:
             queryset = Profile.objects.filter(profileType__exact='contractor') # Filter for contractor profiles
             serializer = ContractorProfilesPublicSerializer(queryset, many=True)
             return Response(serializer.data)
        else:
            profile=Profile.objects.get(user_id=pk)
            serializer=ProfileSerializer(profile,many=False)
            return Response(serializer.data)
            
        


class EngneerProfilesView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,pk=None,formate=None):

        if pk==None:
             data=request.data
             certificate=data["certificate"]
             queryset = Profile.objects.filter(profileType__exact='engneer',user__specialization=certificate) # Filter for contractor profiles
             serializer = EngneerProfilesPublicSerializer(queryset, many=True)
             return Response(serializer.data)
        else:
            profile=Profile.objects.get(user_id=pk)
            serializer=ProfileSerializer(profile,many=False)
            return Response(serializer.data)
            
           
class CraftmanProfilesView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,pk=None,formate=None):

        if pk==None:
             data=request.data
             craft=data["craft"]
             queryset = Profile.objects.filter(profileType__exact='craftman',user__specialization=craft) # Filter for contractor profiles
             serializer = EngneerProfilesPublicSerializer(queryset, many=True)
             return Response(serializer.data)
        else:
            profile=Profile.objects.get(user_id=pk)
            serializer=ProfileSerializer(profile,many=False)
            return Response(serializer.data)
                    
class PortifolioView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    
    def post(self,request,formate=None):
        user=request.user
        serializer=PortifolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"details":"Portifolio created sucessfully"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

class PortifolioPublicView(APIView):
    permission_classes=[AllowAny]
    def get(self,request,pk=None,formate=None):
        user=User.objects.get(id=pk)
        portifolios=Portfolio.objects.filter(user_id=pk)
        personal_data = IdentificationUserSerializer(user).data
        portfolio_data = PortifolioPublicSerializer(portifolios, many=True).data

        response_data = {
            'personal': personal_data,
            'portfolios': portfolio_data
        }

        return Response(response_data)
    

# class ProjectView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         print(request.headers)
#         user = request.user
#         try:
#             contractor = Contractor.objects.get(user=user)
#         except Contractor.DoesNotExist:
#             return Response({"error": "Contractor not found for the authenticated user."}, status=status.HTTP_404_NOT_FOUND)
#         request_data = request.data.copy()
#         request_data['contractor'] = contractor.id
#         serializer=ProjectSerializer(data=request_data)
#         if serializer.is_valid():
#             serializer.save()            
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

    # def get(self, request, pk=None, format=None):
    #     if pk is None:
    #         projects = Project.objects.all()
    #         serializer = ProjectSerializer(projects, many=True)
    #         return Response(serializer.data)
    #     else:
    #         projects_of_contractor = Project.objects.filter(contractor__user_id=pk)
    #         serializer = ProjectSerializer(projects_of_contractor, many=True)
    #         return Response(serializer.data)




#########################################################################################
#########################################################################################


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def ProjectView(request):
    data = request.data
    serializer = ProjectSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(first_name='fadi')

    # Pop the nested data
    catogary_engneer = data.pop('catogary_engneer')
    catogary_craftman = data.pop('catogary_craftman')

    try:
        contractor = Contractor.objects.get(user=user)
    except Contractor.DoesNotExist:
        return Response({"error": "Contractor not found"}, status=status.HTTP_404_NOT_FOUND)

    if user.userType == 'contractor':
        # Create the project
        project = Project.objects.create(
            contractor=contractor,
            projectName=data["projectName"],
            location=data["location"],
            dateOfFinish=data["dateOfFinish"],
            mobileCall=data["mobileCall"],
            description=data["description"]
        )

        # Create related CatogaryEngneerForProject instances
        for ele in catogary_engneer:
            CatogaryEngneerForProject.objects.create(
                projectid_eng=project,
                catogary_eng=ele["catogary_eng"],
                number_eng=ele["number_eng"]
            )

        # Create related CatogaryCraftmanForProject instances
        for ele in catogary_craftman:
            CatogaryCraftmanForProject.objects.create(
                projectid_craft=project,
                catogary_craft=ele["catogary_craft"],
                number_craft=ele["number_craft"]
            )

        # Return the serialized project data
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "User is not a contractor"}, status=status.HTTP_403_FORBIDDEN)

    
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def getProfile(request,pk):
#      user=get_object_or_404(User,id=pk)
#      profile=get_object_or_404(Profile,userid=user)
    #  content = {
    #     "name": user.first_name + " " + user.last_name,
    #     "image_profile": profile.imageurlprofile.url,
    #     "biography": profile.biography,
    #     "exp_year": profile.experienceyears
    # }
#      if user.type_user =="Contractor":
#           contractor = get_object_or_404(Contractor, user=user)
#           content["specialist"] = user.type_user
#           content["company_name"] = contractor.companyname
#      elif user.type_user=="Engneer":
#           engneer = get_object_or_404(Engneer, user=user)
#           content["specialist"] = engneer.certifcate
#      elif user.type_user=="Craftman":
#           craftman = get_object_or_404(Craftman, user=user)
#           content["specialist"] = craftman.craft
#      else:
#           return Response({"details":"User unexist"},status=status.HTTP_404_NOT_FOUND)     
#      return Response({"content":content},status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([AllowAny])
# def getPortifolio(request,pk):
#      user=get_object_or_404(User,id=pk)
#      profile=get_object_or_404(Profile,userid=user)
#      portifolios=Portfolio.objects.all().filter(user=user)

#      content={
#           "name": user.first_name + " " + user.last_name,
#           "image_profile": profile.imageurlprofile.url,

#      }
    
#      if user.type_user =="Contractor":
#           contractor = get_object_or_404(Contractor, user=user)
#           content["specialist"] = user.type_user

#      elif user.type_user=="Engneer":
#           engneer = get_object_or_404(Engneer, user=user)
#           content["specialist"] = engneer.certifcate

#      elif user.type_user=="Craftman":
#           craftman = get_object_or_404(Craftman, user=user)
#           content["specialist"] = craftman.craft     
    
#      for portifolio in portifolios:
#           content[portifolio.id]={
#                          "image1":portifolio.image1.url,
#                          "image2":portifolio.image2.url,
#                          "image3":portifolio.image3.url,
#                          "location":portifolio.location,
#                          "durationofcompletion":portifolio.durationofcompletion,
#                          "description":portifolio.description

#                     }
          
          
#      if content:
#           return Response({"content":content},status=status.HTTP_200_OK)
#      else:
#           return Response({"details":"There is not portfolios"},status=status.HTTP_404_NOT_FOUND)
  
