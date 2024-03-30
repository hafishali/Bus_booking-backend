from rest_framework import serializers
from Manager.models import SuperAdmin,Busoperator,users,Buses,Reservation

class SuperAdminSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=SuperAdmin
        fields=["id","name","username","email_address","phone_number","password"]

    def create(self, validated_data):
        return SuperAdmin.objects.create_user(**validated_data)
    
    
class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Busoperator
        fields=["id","username","email","password","phone","name","description","address","website","logo"]
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=users
        fields=["id","name","phone","username","date_of_birth","profile_picture","address"]
        
        
        
        
class BusSerializer(serializers.ModelSerializer):
    Operator=serializers.StringRelatedField()
    class Meta:
        model = Buses
        fields = ["id","name","description","price","image","is_active","category","boarding_point","boarding_time","dropping_point","dropping_time","duration","capacity","Operator"]
        

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields="_all_"
        

class profileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = SuperAdmin
        fields=["id","name","username","email_address","phone_number"]