from .models import Transaction,Vendor,Manager,Produit,Favoris
from rest_framework import serializers 
from django.contrib.auth import authenticate



class UserManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model= Manager
        fields= ('phone','name')

class UserVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vendor
        fields= ('phone','name')

## serializer Vendor 
class MyTokenObtainPairVendorSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and not user.is_blocked:
            user.number_attempt=0
            user.save()
            return user
        
        elif user and user.is_active and user.is_blocked:
            # return Response('message')
            # return Response(serializers.errors)
            
            raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        
        try:
            obj= Vendor.objects.get(phone=data['phone'])
            if obj.number_attempt<3:
                obj.number_attempt +=1
                obj.save()
                raise serializers.ValidationError({'message':'Informations invalides.'})
            else:
                obj.number_attempt +=1
                obj.is_blocked=True
                obj.save()
                raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        except:
            raise serializers.ValidationError({'message':'Informations invalides.'})   
             
## serializer Manager         
class MyTokenObtainPairManagerSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active and not user.is_blocked:
            user.number_attempt=0
            user.save()
            return user
        
        elif user and user.is_active and user.is_blocked:
            # return Response('message')
            # return Response(serializers.errors)
            
            raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        
        try:
            obj= Manager.objects.get(phone=data['phone'])
            if obj.number_attempt<3:
                obj.number_attempt +=1
                obj.save()
                raise serializers.ValidationError({'message':'Informations invalides.'})
            else:
                obj.number_attempt +=1
                obj.is_blocked=True
                obj.save()
                raise serializers.ValidationError({'message':'Compte blocké, veillez contacter lagence '})
        except:
            raise serializers.ValidationError({'message':'Informations invalides.'})    

##Transaction 
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'sender_wallet', 'receiver_wallet', 'amount','numTransaction']            
        
## register manager 
class RegisterManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ('id', 'phone', 'name', 'email', 'password','role','image')
        extra_kwargs = {
            'password': {'write_only': True}
        }

## register vendor
class RegisterVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id', 'phone', 'name', 'email', 'password','role','image')
        extra_kwargs = {
            'password': {'write_only': True}
        }



## post product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = ['nom', 'prix', 'description', 'categories', 'marqueprives', 'image']
        



class ProduitAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'



class FavorisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favoris
        fields = '__all__'   

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'                
