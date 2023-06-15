from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers 
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException
from rest_framework import generics 
from .models import Wallet,Produit,Favoris,Transaction
from .serializer import TransactionSerializer,MyTokenObtainPairVendorSerializer,MyTokenObtainPairManagerSerializer,RegisterManagerSerializer,RegisterVendorSerializer,ProductSerializer,ProduitAllSerializer,FavorisSerializer
import random
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView





# Create your views here.

## logon manager
class InvalidInformationException(APIException):
    status_code = 400
    default_detail = 'Informations invalides'

class MytokenManager(TokenObtainPairView):
    serializer_class = MyTokenObtainPairManagerSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
            'message': 'Informations invalides',
            'status':status.HTTP_400_BAD_REQUEST, 
        })
            
        
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'login success',
            'status':status.HTTP_200_OK, 
            'id': user.id,
            'role':user.role,
            'email': user.email,
            'nom': user.name,
            'phone': user.phone,
            'access': str(refresh.access_token),
            'refresh_token': str(refresh),  
        })

#login vendor 
class InvalidInformationException(APIException):
    status_code = 400
    default_detail = 'Informations invalides'

class MytokenVendor(TokenObtainPairView):
    serializer_class = MyTokenObtainPairVendorSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
            'message': 'Informations invalides',
            'status':status.HTTP_400_BAD_REQUEST, 
        })
            
        
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'login success',
            'status':status.HTTP_200_OK, 
            'id': user.id,
            'role':user.role,
            'email': user.email,
            'nom': user.name,
            'phone': user.phone,
            'access': str(refresh.access_token),
            'refresh_token': str(refresh),  
        })
    
##transfer between les vendor 
class TransferBalanceAPIView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        sender_wallet = serializer.validated_data['sender_wallet']
        receiver_wallet = serializer.validated_data['receiver_wallet']
        amount = serializer.validated_data['amount']
        
        if not self.request.user.check_password(self.request.data.get('password')):
            raise serializers.ValidationError("Invalid password.")

        if amount > sender_wallet.balance:
            raise serializers.ValidationError("Insufficient balance.")
        
        sender_wallet.balance -= amount
        receiver_wallet.balance += amount

        # Generate a random numTransaction value
        numTransaction = str(random.randint(100000, 999999))

        # Save the updated wallets and create the transaction
        sender_wallet.save()
        receiver_wallet.save()
        serializer.save(numTransaction=numTransaction)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        receiver_wallet_id = request.data.get('receiver_wallet')
        receiver_wallet = Wallet.objects.get(id=receiver_wallet_id)
        receiver_name = receiver_wallet.vendor.name
        receiver_phone = receiver_wallet.vendor.phone

        response.data['receiver_name'] = receiver_name
        response.data['receiver_phone'] = receiver_phone
        response.data['numTransaction'] = response.data.get('numTransaction')

        response_data = {
            'message': 'Balance transfer successful',
            'receiver_name': receiver_name,
            'receiver_phone': receiver_phone,
            'numTransaction': "TR"+response.data.get('numTransaction'),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)    

## REGISTER MANAGER
class RegisterManagerAPI(TokenObtainPairView):
    serializer_class = RegisterManagerSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        role = request.data.get('role',False)
        if phone and password and role=='Manager':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = serializer.save()
                user.set_password(password)
                user.save()
                refresh = RefreshToken.for_user(user)

                return Response({
                    'phone': user.phone,
                    'name': user.name,
                    'role': user.role,
                    'image': request.data.get('image'),
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            except:
                return Response({'status':status.HTTP_400_BAD_REQUEST, 'Message':'Bad request'})

        return Response({'status':status.HTTP_400_BAD_REQUEST, 'Message':'Envoyez le numéro de telephone exist'})    

##REGISTER VENDOR

class RegisterVendorAPI(TokenObtainPairView):
    serializer_class = RegisterVendorSerializer

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        role = request.data.get('role',False)
        if phone and password and role=='Vendor':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = serializer.save()
                user.set_password(password)
                user.save()
                refresh = RefreshToken.for_user(user)

                return Response({
                    'phone': user.phone,
                    'name': user.name,
                    'role': user.role,
                    'image': request.data.get('image'),
                    'token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                })
            except:
                return Response({'status':status.HTTP_400_BAD_REQUEST, 'Message':'Bad request'})

        return Response({'status':status.HTTP_400_BAD_REQUEST, 'Message':'Envoyez le numéro de telephone exist'})    




class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(manager=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProductListView(generics.ListAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitAllSerializer

class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Produit.objects.all()
    serializer_class = ProduitAllSerializer
    lookup_field = 'id'    



class FavorisCreateView(generics.CreateAPIView):
    queryset = Favoris.objects.all()
    serializer_class = FavorisSerializer


class FavorisListView(generics.ListAPIView):
    queryset = Favoris.objects.all()
    serializer_class = FavorisSerializer

class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer    

