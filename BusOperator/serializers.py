
from rest_framework import serializers
from Manager.models import Busoperator,Category,Buses,Offer,Review,Reservation,Payment,users

class OperatorSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Busoperator
        fields=["id","username","email","password","phone","name","description","address","website","logo"]

    def create(self, validated_data):
        return Busoperator.objects.create_user(**validated_data)
    
class CategorySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    is_active=serializers.BooleanField(read_only=True)
    class Meta:
        model = Category
        fields =["id","name","is_active"]

class BusSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Buses
        fields = ["id", "name", "description", "price", "image", "is_active", "category", "boarding_point", "boarding_time", "dropping_point", "dropping_time", "duration", "capacity"]
        
        
class BusEditSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    

    class Meta:
        model = Buses
        fields = ["id", "name", "description", "price",  "is_active", "category", "boarding_point", "boarding_time", "dropping_point", "dropping_time", "duration", "capacity"]

    # Override the update method to handle image field not being required
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.method == 'PUT':
            # Mark image field as not required for updates
            validated_data['image'] = validated_data.get('image', instance.image)
            # Add more fields as needed
        return super().update(instance, validated_data)

    
            # Add more fields as needed

class OfferSerializer(serializers.ModelSerializer):
    bus=serializers.CharField(read_only=True)
    id=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    busoperators=serializers.CharField(read_only=True)
    class Meta:
        model = Offer
        fields="__all__"


class ReviewSerializer(serializers.ModelSerializer):
    bus_name = serializers.CharField(source='bus.name', read_only=True)
    bus_operators = serializers.CharField(source='bus.Operator', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'bus_name','bus_operators','user_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=users
        fields=["name","profile_picture","date_of_birth","address"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"

    def filter_by_operator_id(self, operator_id):
        reservations = Reservation.objects.filter(bus__Operator__id=operator_id)
        return reservations


class profileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Busoperator
        fields=["id","username","email","phone","name","description","address","website","logo"]


