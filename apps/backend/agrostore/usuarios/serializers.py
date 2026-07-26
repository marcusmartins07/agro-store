from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    idade = serializers.ReadOnlyField()

    class Meta:
        model = Usuario
        fields = [
            "id",
            "nome",
            "cpf",
            "email",
            "data_nascimento",
            "genero",
            "is_produtor",
            "idade",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()

        return user
    

class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            cpf=data["cpf"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("CPF ou senha inválidos")

        data["user"] = user
        return data

