from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions,status
from Manager.serializers import SuperAdminSerializer,OperatorSerializer,UserSerializer,BusSerializer,ReservationSerializer,profileSerializer
from Manager.models import Category,Busoperator,Buses,Reservation,users,Payment,SuperAdmin


class AdminCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=SuperAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="SuperAdmin")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



class busoperator(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = OperatorSerializer
        
    def list(self,request,*args,**kwargs):
        qs=Busoperator.objects.all()
        serializer=OperatorSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Busoperator.objects.get(id=id)
        serializer=OperatorSerializer(qs)
        return Response(data=serializer.data)
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            bus_operator = Busoperator.objects.get(pk=pk)
            bus_operator.delete()
            return Response({"message": "Bus operator deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Busoperator.DoesNotExist:
            return Response({"error": "Bus operator not found"}, status=status.HTTP_404_NOT_FOUND)
        


class usersview(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = UserSerializer
        
    def list(self,request,*args,**kwargs):
        qs=users.objects.all()
        serializer=UserSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=users.objects.get(id=id)
        serializer=UserSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = users.objects.get(pk=kwargs["pk"])
            instance.delete()
            return Response({"message": "User deleted successfully"},status=status.HTTP_204_NO_CONTENT)
        except users.DoesNotExist:
            return Response({"error": "User not found"},status=status.HTTP_404_NOT_FOUND)
        
class busview(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = UserSerializer
        
    def list(self,request,*args,**kwargs):
        qs=Buses.objects.all()
        serializer=BusSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Buses.objects.get(id=id)
        serializer=BusSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            bus_instance = Buses.objects.get(id=pk)
        except Buses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        bus_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class ReservationView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Reservation.objects.all()
        serializer=ReservationSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Reservation.objects.get(id=id)
        serializer=ReservationSerializer(qs)
        return Response(data=serializer.data)
    
class ProfileEdit(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    
    def get(self,request,*args,**kwargs):
        user_id=request.user.id
        qs=SuperAdmin.objects.get(id=user_id)
        serializer=SuperAdminSerializer(qs)
        return Response(data=serializer.data)
    
    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        user_instance = SuperAdmin.objects.get(id=user_id)
        serializer = profileSerializer(user_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)