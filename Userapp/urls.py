from django.urls import path
from Userapp import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("category",views.CategoryView,basename="category")
router.register("busoperators",views.busoperator,basename="busoperators_list")
router.register("bus",views.BusView,basename="bus")
router.register("UserBuses",views.UserBuses,basename="UserBuses")
# router.register("userProfileEdit",views.ProfileEdit,basename="userProfileEdit")







urlpatterns = [
    path("register/",views.UserCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    path("profile/",views.ProfileEdit.as_view(),name="profile"),
    path('buses/search/', views.BusesViewSet.as_view({'post': 'search'}), name='buses-search'),
] +router.urls