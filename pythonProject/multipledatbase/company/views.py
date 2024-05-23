from django.contrib.auth import authenticate
from django.shortcuts import render
import jwt
# Create your views here.
import MySQLdb
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from django.core.management import call_command
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import CompanyRegisterSerializer, LoginSerializer
from multipledatbase.settings import JWT_SECRET_KEY


def create_database(db_name, db_user, db_password, db_host='localhost', db_port='3306'):
    # Connect to the default database
    conn = MySQLdb.connect(
        db=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        passwd=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=int(settings.DATABASES['default']['PORT']),
    )
    conn.autocommit(True)
    cursor = conn.cursor()

    # Create the new database
    cursor.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

    # Close the default database connection
    cursor.close()
    conn.close()

    # Set up the new database settings
    new_db_settings = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': db_host,
        'PORT': db_port,
    }

    # Add the new database settings to Django
    settings.DATABASES[db_name] = new_db_settings

    # Ensure the connection for the new database is ready
    connections.ensure_defaults(db_name)
    connections.prepare_test_settings(db_name)
    connection = connections[db_name]

    # Run migrations on the new database
    call_command('migrate', database=db_name)


def create_new_db_view(request):
    db_name = "new_database"
    db_user = "your_db_user"
    db_password = "your_db_password"
    create_database(db_name, db_user, db_password)
    return HttpResponse(f"Database {db_name} created successfully.")


class CompanyManagement(APIView):

    def create(self, request):
        try:
            company_data = request.data
            serializer = CompanyRegisterSerializer(data=company_data)
            if serializer.is_valid():
                serializer.save()

                return Response({
                    "message": "company registration is success"
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e)


class CompanyLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)

            if serializer.is_valid():
                company_user_name = serializer.validated_data['company_user_name']
                company_password = serializer.validated_data['company_password']

                login_data = {
                    "user_name": company_user_name,
                    "password": company_password

                }

                access_token = jwt.encode(login_data, JWT_SECRET_KEY, algorithm="HS256")

                return Response({"access_token": access_token}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e)


@api_view(["POST"])
def add_details(request):




    pass
