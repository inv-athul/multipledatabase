from rest_framework.response import Response

from .models import Company
from rest_framework import serializers


class CompanyRegisterSerializer(serializers.ModelSerializer):
    '''serializer for user Users model'''

    class Meta:
        model = Company
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    company_user_name = serializers.CharField()
    company_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        errors = []
        check_user = Company.objects.filter(company_email=attrs["company_user_name"]).exists()
        if not check_user:
            errors.append({
                "message": "Invalid username or password"
            })
        if errors:
            raise serializers.ValidationError(
                {
                    'error': {
                        'status': 'invalid-data',
                        'message': 'Invalid data',
                        'details': errors
                    }
                }
            )

        return attrs


