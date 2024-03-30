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

    class Meta:
        model = Buses
        fields = ["id", "name", "description", "price", "image", "is_active", "category_name", "boarding_point", "boarding_time", "dropping_point", "dropping_time", "duration", "capacity", "Operator"]



class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields=["user","bus","rating","comment"]

class ReservationSerializer(serializers.ModelSerializer):
    bus = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    reservation_status = serializers.CharField(read_only=True)
    seat_number = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Reservation
        fields = ['seat_number', 'journey_date', 'user', 'bus', 'reservation_status']
       
    def validate_seat_number(self, value):
        journey_date = self.initial_data.get('journey_date')
        if not journey_date:
            raise serializers.ValidationError("Journey date is required.")
        
        # Convert the list of seat numbers to integers
        seat_numbers = value if value else []
        
        # Check if any of the seat numbers are already reserved for the given journey date
        for seat in seat_numbers:
            if Reservation.objects.filter(seat_number=str(seat), journey_date=journey_date).exists():
                raise serializers.ValidationError(f"Seat number {seat} is already reserved for {journey_date}.")
        
        # Check if any seat number is duplicated
        if len(seat_numbers) != len(set(seat_numbers)):
            raise serializers.ValidationError("Duplicate seat numbers are not allowed.")

        return seat_numbers
    
    
class ReservationViewSerializer(serializers.ModelSerializer):
    bus=BusSerializer()
    user=serializers.CharField(read_only=True)
    reservation_status=serializers.CharField(read_only=True)
    class Meta:
        model=Reservation
        fields="__all__"
        

class PaymentSerializer(serializers.ModelSerializer):
    amount=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    reservation=serializers.CharField(read_only=True)
    class Meta:
        model=Payment
        fields="__all__"
        
        
class profileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = users
        fields=["id","name","phone","username","date_of_birth","profile_picture","address"]