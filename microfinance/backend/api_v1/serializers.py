import random
import math

from rest_framework import serializers

from authentication.jwt_helpers import create_token_from_dict


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=300, write_only=True)

    class Meta:
        fields = (
            'token',
        )


class RefreshEmailSerializer(TokenSerializer):
    newEmail = serializers.EmailField(write_only=True)
    
    class Meta:
        fields = (
            'token',
            'newEmail',
        )


class RefreshPasswordSerializer(TokenSerializer):
    oldPassword = serializers.CharField(max_length=100, write_only=True)
    newPassword = serializers.CharField(max_length=100, write_only=True)
    
    class Meta:
        fields = (
            'token',
            'oldPassword',
            'newPassword',
        )


class PawnTicketOperationsSerializer(TokenSerializer):
    loanId = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        fields = (
            'token',
            'pawnTicketId',
        )


class PawnPropertiesSerializer(TokenSerializer):
    loanId = serializers.CharField(max_length=100, write_only=True)
    propertyId = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        fields = (
            'token',
            'pawnTicketId',
            'propertyId',
        )


class ProlongationPawnTicketSerializer(TokenSerializer):
    loanId = serializers.CharField(max_length=100, write_only=True)
    totalSum = serializers.FloatField(write_only=True)
    mainDebtSum = serializers.FloatField(write_only=True)
    newPeriod = serializers.IntegerField(write_only=True)
    prd = serializers.SerializerMethodField(read_only=True)
    referenceId = serializers.SerializerMethodField(read_only=True)

    def get_prd(self, data):
        return create_token_from_dict({
            "mainDebtSum": data.get("mainDebtSum", 0),
            "newPeriod": data["newPeriod"],
            "loanId": data["loanId"],
        }, 0)

    def get_referenceId(self, data):
        return str(int(random.random() * math.pow(10, 15)))[:12]

    class Meta:
        fields = (
            'token',
            'loanId',
            'totalSum',
            'mainDebtSum',
            'newPeriod',
            'prd',
            'customer_reference_num',
        )


class LoanPayBackSerializer(TokenSerializer):
    loanId = serializers.CharField(max_length=100, write_only=True)
    mainDebtSum = serializers.FloatField(write_only=True)
    prd = serializers.SerializerMethodField(read_only=True)
    referenceId = serializers.SerializerMethodField(read_only=True)

    def get_prd(self, data):
        return create_token_from_dict({
            "mainDebtSum": data.get("mainDebtSum", 0),
            "loanId": data["loanId"],
        }, 0)

    def get_referenceId(self, data):
        return str(int(random.random() * math.pow(10, 15)))[:12]

    class Meta:
        fields = (
            'token',
            'loanId',
            'mainDebtSum',
            'prd',
            'customer_reference_num',
        )


class CheckStatusSerializer(TokenSerializer):
    token_processing = serializers.CharField(max_length=500, write_only=True)
    type_loan = serializers.CharField(max_length=50, write_only=True)
    reference_id = serializers.CharField(max_length=50, write_only=True)
    type_transaction = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        fields = (
            'token',
            'token_processing',
            'type_loan',
            'reference_id',
            'type_transaction',
        )
