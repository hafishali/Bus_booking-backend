from rest_framework import serializers
from Manager.models import users,Category,Busoperator,Buses,Review,Reservation,Payment

class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=users
        fields=["id","name","phone","username","date_of_birth","profile_picture","address","password"]

    def create(self, validated_data):
        return users.objects.create_user(**validated_data)
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Busoperator
        fields=["id","username","email","password","phone","name","description","address","website","logo"]

class BusSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    operator_name = serializers.CharField(source='Operator.name', read_only=True)

    class Meta:
        model = Buses
        fields = ["id", "name", "description", "price", "image", "is_active", "category_name", "boarding_point", "boarding_time", "dropping_point", "dropping_time", "duration", "capacity", "Operator","operator_name"]



class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields=["user","bus","rating","comment"]
        
        

class ReservationSerializer(serializers.ModelSerializer):
    bus=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    reservation_status=serializers.CharField(read_only=True)
    class Meta:
        model=Reservation
        fields="__all__"
        
    
    
    
class ReservationViewSerializer(serializers.ModelSerializer):
    bus=BusSerializer()
    user=serializers.CharField(read_only=True)
    reservation_status=serializers.CharField(read_only=True)
    class Meta:
        model=Reservation
        fields="__all__"
        

class PaymentviewSerializer(serializers.ModelSerializer):
    amount=serializers.CharField(read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    reservation_data = ReservationSerializer(source='reservation', read_only=True)
    class Meta:
        model=Payment
        fields=["id","amount","payment_time","payment_status","user","user_name","reservation"]

class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    bus = BusSerializer(source='reservation.bus', read_only=True)  # Nested serializer for bus details
    reservation_data = ReservationSerializer(source='reservation', read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "amount", "payment_time", "payment_status", "user", "bus","reservation_data"]
        
        
class profileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = users
        fields=["id","name","phone","username","date_of_birth","profile_picture","address"]