from django.urls import path
from main import views
urlpatterns = [
      path('user/' ,views.UserView.as_view(),name='signupUser'),
      path('user/<int:pk>/' ,views.UserView.as_view(),name='user'),
      path('verify/', views.VerifyView.as_view(), name='verify'),
      path('mobileChange/', views.MobileChangeView.as_view(), name='mobileChange'),
      path('profile/', views.ProfileView.as_view(), name='registerProfile'),
      path('contractors/', views.ContractorProfilesView.as_view(), name='contractorProfiles'),
      path('contractors/<int:pk>/', views.ContractorProfilesView.as_view(), name='contractorProfilesDetails'),
      path('engneers/', views.EngneerProfilesView.as_view(), name='engneerProfiles'),
      path('engneers/<int:pk>/', views.EngneerProfilesView.as_view(), name='engneerProfilesDetails'),
      path('craftmans/', views.CraftmanProfilesView.as_view(), name='craftmanProfiles'),
      path('craftmans/<int:pk>/', views.CraftmanProfilesView.as_view(), name='craftmanProfilesDetails'),
      path('portifolio/', views.PortifolioView.as_view(), name='PortifolioView'),
      path('portifolios/<int:pk>/', views.PortifolioPublicView.as_view(), name='PortifolioPublicView'),
      path('project/', views.ProjectView, name='registerProject'),

    

]
