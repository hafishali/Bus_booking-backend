from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions
from Manager.models import Busoperator,Category,Buses,Offer,Review,Payment,Reservation
from BusOperator.serializers import BusSerializer,CategorySerializer,OperatorSerializer,OfferSerializer,ReviewSerializer,PaymentSerializer,ReservationSerializer,profileSerializer,BusEditSerializer
from django.utils import timezone


# Create your views here.
class OperatorCreationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OperatorSerializer(data=request.data)
        if serializer.is_valid():
            bus_operator = serializer.save(user_type="Busoperator")
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        




        
class CategoryView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    
    def create(self,request,*args,**kwargs):
        serializer=CategorySerializer(data=request.data)
        operator_id=request.user.id
        print(operator_id)
        operator_object=Busoperator.objects.get(id=operator_id)
        if operator_object:
            if serializer.is_valid():
                serializer.save(Busoperators=operator_object)
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)
        else:
            return Response(request,"Bus OPerator not found")
        
    def list(self,request,*args,**kwargs):
        operator_id=request.user.id
        operator_object=Busoperator.objects.get(id=operator_id)
        qs=Category.objects.filter(Busoperators=operator_object)
        serializer=CategorySerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Category.objects.get(id=id)
        serializer=CategorySerializer(qs)
        return Response(data=serializer.data)
    
    
    def destroy(self,request,*args,**kwargs):
        id = kwargs.get("pk")
        category = Category.objects.get(id=id)
        category.is_active = False
        category.save()
        return Response(data={"message": "category is now inactive"})
    
    
    @action(methods=["post"],detail=True)
    def add_bus(self,request,*args,**kwargs):
        serializer=BusSerializer(data=request.data)
        cat_id=kwargs.get("pk")
        category_obj=Category.objects.get(id=cat_id)
        operator=request.user.id
        operator_object=Busoperator.objects.get(id=operator) 
        if serializer.is_valid():
            serializer.save(category=category_obj,Operator=operator_object,is_active=True)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class BusView(ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BusSerializer

    def list(self, request, *args, **kwargs):
        qs = Buses.objects.filter(Operator=request.user.busoperator)
        serializer = BusSerializer(qs, many=True)
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        obj = get_object_or_404(Buses, id=id)
        serializer = BusSerializer(instance=obj, data=request.data, partial=True)  # Use partial=True to allow partial updates
        if obj.Operator == request.user.busoperator:
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        instance = get_object_or_404(Buses, id=id)
        if instance.Operator == request.user.busoperator:
            instance.delete()
            return Response(data={"msg": "Deleted"})
        else:
            return Response(data={"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        qs = get_object_or_404(Buses, id=id)
        if qs.Operator == request.user.busoperator:
            serializer = BusSerializer(qs)
            return Response(data=serializer.data)
        else:
            return Response(data={"message": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
    @action(methods=["post"],detail=True)
    def offer_add(self,request,*args,**kwargs):
        serializer=OfferSerializer(data=request.data)
        bus_id=kwargs.get("pk")
        bus_obj=Buses.objects.get(id=bus_id)
        busoperator=request.user.id
        busoperator_object=Busoperator.objects.get(id=busoperator) 
        if serializer.is_valid():
            serializer.save(bus=bus_obj,busoperators=busoperator_object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        


    # @action(methods=["get"],detail=True)  
    # def review_list(self,request,*args,**kwargs):
    #     bus_id=kwargs.get("pk")
    #     bus_obj=Buses.objects.get(id=bus_id)
    #     qs=Review.objects.filter(bus=bus_obj)
    #     serializer=ReviewSerializer(qs,many=True)
    #     return Response(data=serializer.data)
    




class OfferView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OfferSerializer


    def list(self,request,*args,**kwargs):
        qs=Offer.objects.filter(busoperators=request.user.busoperator,due_date__gte=timezone.now())
        serializer=OfferSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,args,*kwargs):
        id=kwargs.get("pk")
        instance=Offer.objects.get(id=id)
        if instance.busoperators==request.user.busoperator:
            instance.delete()
            return Response(data={"msg":"offer deleted"})
        else:
            return Response(data={"message":"permission denied"})
        


class PaymentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Payment.objects.all()
        serializer=PaymentSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Payment.objects.get(id=id)
        serializer=PaymentSerializer(qs)
        return Response(data=serializer.data)
    


class ReservationView(ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        # Filter reservations based on the operator of the authenticated user's bus
        qs = Reservation.objects.filter(bus__Operator=request.user.busoperator)
        serializer = ReservationSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            qs = Reservation.objects.get(id=id)
            serializer = ReservationSerializer(qs)
            return Response(data=serializer.data)
        except Reservation.DoesNotExist:
            return Response(data={"message": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
class ReviewListView(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all reviews
        qs = Review.objects.select_related('bus', 'user').all()
        
        # Serialize the queryset
        serializer = ReviewSerializer(qs, many=True)
        
        # Return the serialized data
        return Response(serializer.data)
        
class ProfileEdit(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        qs = Busoperator.objects.get(id=user_id)
        serializer = profileSerializer(qs)  # Using the serializer class here
        return Response(data=serializer.data)

    def put(self, request, *args, **kwargs):
        user_id = request.user.id
        user_instance = Busoperator.objects.get(id=user_id)
        serializer = profileSerializer(user_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        




