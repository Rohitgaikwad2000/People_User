from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import json
from .keys import public_key, private_key
from .serializers import PeopleSerializer
from .models import People


@api_view(["POST"])
def encrypt_message(request):
    """Encrypt the incoming JSON data."""
    data = request.data
    try:
        # Convert the entire data to a JSON string
        message = json.dumps(data)
        recipient_key = RSA.import_key(public_key)
        cipher_rsa = PKCS1_OAEP.new(recipient_key)
        encrypted_message = cipher_rsa.encrypt(message.encode())
        encrypted_message_b64 = base64.b64encode(encrypted_message).decode("utf-8")
        return Response({"encrypted_message": encrypted_message_b64})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def decrypt_message(request):
    """Decrypt the incoming base64 encoded encrypted message."""
    encrypted_message_b64 = request.data.get("encrypted_data")
    if not encrypted_message_b64:
        return Response(
            {"error": "No encrypted message provided"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        encrypted_message = base64.b64decode(encrypted_message_b64)
        private_key_rsa = RSA.import_key(private_key)
        cipher_rsa = PKCS1_OAEP.new(private_key_rsa)
        decrypted_message = cipher_rsa.decrypt(encrypted_message)
        return Response({"decrypted_message": decrypted_message.decode("utf-8")})
    except (ValueError, TypeError) as e:
        return Response(
            {"error": "Decryption failed: " + str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def add_person(request):
    """Add a new person after validating and encrypting their details."""
    serializer = PeopleSerializer(data=request.data)
    if serializer.is_valid():
        person = serializer.save()
        response_data = {
            "name": person.name,
            "contact_no": person.contact_no,
            "gender": person.gender,
            "email_id": person.email_id,
            "date_of_birth": str(person.date_of_birth),
            "nationality": person.nationality,
        }

        # Encrypt the response data
        try:
            recipient_key = RSA.import_key(public_key)
            cipher_rsa = PKCS1_OAEP.new(recipient_key)
            encrypted_response_data_b64 = {
                key: base64.b64encode(cipher_rsa.encrypt(str(value).encode())).decode(
                    "utf-8"
                )
                for key, value in response_data.items()
            }
            return Response(encrypted_response_data_b64, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def decrypt_all_people(request, contact_no=None):
    """Decrypt all people's data that are stored as encrypted."""

    if contact_no is not None:
        try:
            obj = People.objects.get(contact_no=contact_no)
            ser = PeopleSerializer(obj)
            return Response(ser.data, status=status.HTTP_200_OK)
        except People.DoesNotExist:
            return Response(
                {"error": "Person not found."}, status=status.HTTP_404_NOT_FOUND
            )
    else:
        objs = People.objects.all()
        ser = PeopleSerializer(objs, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
