from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from .constant import Account_type


class RegistrerSerializer(serializers.ModelSerializer):


    confirm_password=serializers.CharField(required=True)
    account_type=serializers.ChoiceField(choices=Account_type,default='Buyer',required=False)
    mobile_no=serializers.CharField(max_length=12)
    address=serializers.CharField(max_length=100,required=False)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password','confirm_password','mobile_no','address','account_type']
        read_only_fields = ['account_type']

    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        mobile_no=self.validated_data['mobile_no']
        password=self.validated_data['password']
        confirm_password=self.validated_data['confirm_password']
        address = self.validated_data.get('address', '')
       

        if password != confirm_password:
            raise serializers.ValidationError({
                'error':"Password And Confirm Pass Doesn't Matched"

            })
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {
                    'error':'Email Already Exists'
                }
            )
        account=User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
           
            )
        
        account.set_password(password)
        account.is_active=False
        account.account_type='Buyer'
        account.save()
        UserProfile.objects.create(user=account,mobile_no=mobile_no, address=address)
        return account



class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)        
    password=serializers.CharField(required=True)        


class UpdateProfileSerializer(serializers.ModelSerializer):
    mobile_no=serializers.CharField(max_length=12)
    address=serializers.CharField(max_length=100)
    account_type=serializers.ChoiceField(choices=Account_type,required=False,read_only=True)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','mobile_no','address','account_type']
        read_only_fields = ['username','account_type']


