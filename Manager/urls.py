from django.urls import path
from Manager import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register("busoperators",views.busoperator,basename="busoperators_list")
router.register("users",views.usersview,basename="users_list")
router.register("buses",views.busview,basename="bus_list")
router.register("reservation",views.ReservationView,basename="reservation_list")
router.register("PaymentView",views.PaymentView,basename="PaymentView")






urlpatterns = [
    path("register/",views.AdminCreationView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    path("profile/",views.ProfileEdit.as_view(),name="profile"),

   
]+router.urls