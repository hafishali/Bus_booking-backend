from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions,status
from rest_framework import viewsets

from Manager.models import Category,Busoperator,Buses,Reservation,users,Payment


from Userapp.serializers import UserSerializer,CategorySerializer,OperatorSerializer,BusSerializer,ReviewSerializer,PaymentSerializer,ReservationViewSerializer,profileSerializer,ReservationSerializer,PaymentviewSerializer


# Create your views here.



class UserCreationView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="users")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class CategoryView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = CategorySerializer
        
    def list(self,request,*args,**kwargs):
        qs=Category.objects.filter(is_active=True)
        serializer=CategorySerializer(qs,many=True)
        return Response(data=serializer.data)
    

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
    

class BusView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = BusSerializer
        
    def list(self,request,*args,**kwargs):  
        qs=Buses.objects.filter(is_active=True)
        serializer=BusSerializer(qs,many=True)
        return Response(data=serializer.data)
    

    @action(methods=["post"],detail=True)
    def reserve_bus(self,request,*args,**kwargs):
        serializer=ReservationSerializer(data=request.data)
        bus_id=kwargs.get("pk")
        user_id=request.user.id
        user_obj=users.objects.get(id=user_id)
        Bus_obj=Buses.objects.get(id=bus_id)
        
        if serializer.is_valid():
            serializer.save(bus=Bus_obj, user=user_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    
    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        bus_object=Buses.objects.get(id=id) 
        user=request.user.users
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user,bus=bus_object)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    

class UserBuses(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    
    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        user_obj = users.objects.get(id=user_id)
        reservations = Reservation.objects.filter(user=user_obj)
        serializer = ReservationViewSerializer(reservations, many=True)
        return Response(serializer.data)
    
    @action(methods=["post"], detail=True)
    def payment(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        reservation_id = kwargs.get("pk")
        reservation_obj = Reservation.objects.get(id=reservation_id)
        bus_price = reservation_obj.bus.price
        user_id = request.user.id
        user_obj = users.objects.get(id=user_id)
        
        if serializer.is_valid():
            serializer.save(reservation=reservation_obj, user=user_obj, amount=bus_price)
            
            # Update reservation status
            reservation_obj.reservation_status = "Completed"
            reservation_obj.save()  # Save the changes
            
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ProfileEdit(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    
    def get(self,request,*args,**kwargs):
        user_id=request.user.id
        qs=users.objects.get(id=user_id)
        serializer=UserSerializer(qs)
        return Response(data=serializer.data)
    
    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        user_instance = users.objects.get(id=user_id)
        serializer = profileSerializer(user_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
from rest_framework import filters
from datetime import datetime

from django.db.models import Q


class BusesViewSet(viewsets.ModelViewSet):
    queryset = Buses.objects.all()
    serializer_class = BusSerializer
    
    @action(methods=['post'], detail=False)
    def search(self, request):
        from_location = request.data.get('from_location', None)
        to_location = request.data.get('to_location', None)
        category = request.data.get('category', None)

        if from_location and to_location and category:
            queryset = Buses.objects.filter(
                Q(boarding_point=from_location) | Q(dropping_point=to_location),
                category__name=category
            )
        elif from_location and to_location:
            queryset = Buses.objects.filter(
                Q(boarding_point=from_location) | Q(dropping_point=to_location)
            )
        elif category:
            queryset = Buses.objects.filter(
                category__name=category
            )
        else:
            return Response({'error': 'At least one parameter (from_location, to_location, or category) is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if queryset.exists():
            serializer = BusSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
        
class PaymentView(ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        user_id = request.user.id  # Get the logged-in user's ID
        qs = Payment.objects.filter(id=user_id)  
        serializer = PaymentSerializer(qs, many=True)
        return Response(data=serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        qs = Payment.objects.get(id=id, user=request.user.id)  
        serializer = PaymentSerializer(qs)
        return Response(data=serializer.data)