from __future__ import annotations

from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import Ticket, TicketMessage


class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ["id", "sender", "body", "created_by", "created_at"]
        read_only_fields = ["id", "sender", "created_by", "created_at"]


class TicketSerializer(serializers.ModelSerializer):
    messages = TicketMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "subject",
            "status",
            "created_at",
            "updated_at",
            "messages",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at", "messages"]


class TicketCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Ticket
        fields = ["id", "customer_name", "customer_email", "subject", "message"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        message_body = validated_data.pop("message", "").strip()
        ticket = Ticket.objects.create(**validated_data)
        if message_body:
            TicketMessage.objects.create(
                ticket=ticket,
                sender=TicketMessage.Sender.CUSTOMER,
                body=message_body,
            )
        return ticket


class TicketMessageCreateSerializer(serializers.Serializer):
    body = serializers.CharField()
    customer_email = serializers.EmailField(required=False)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.prefetch_related("messages")

    def get_permissions(self):
        if self.action in {"create", "add_message"}:
            return [AllowAny()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.action == "create":
            return TicketCreateSerializer
        return TicketSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = serializer.save()
        return Response(TicketSerializer(ticket, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"], url_path="messages")
    def add_message(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketMessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if request.user and request.user.is_staff:
            sender = TicketMessage.Sender.ADMIN
            created_by = request.user
        else:
            supplied_email = (serializer.validated_data.get("customer_email") or "").strip().lower()
            if not supplied_email or supplied_email != ticket.customer_email.strip().lower():
                return Response(
                    {"detail": "customer_email is required and must match the ticket."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            sender = TicketMessage.Sender.CUSTOMER
            created_by = None

        message = TicketMessage.objects.create(
            ticket=ticket,
            sender=sender,
            body=serializer.validated_data["body"],
            created_by=created_by,
        )

        return Response(TicketMessageSerializer(message).data, status=status.HTTP_201_CREATED)
