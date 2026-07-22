from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from inventory.models import Product
from .models import Customer, Sale, SaleItem


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "customer_id",
            "name",
            "phone",
            "email",
            "address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "customer_id", "created_at", "updated_at"]


class POSProductSerializer(serializers.ModelSerializer):
    """Lightweight product representation for the POS medicine grid."""

    class Meta:
        model = Product
        fields = [
            "id",
            "product_code",
            "name",
            "generic_name",
            "category",
            "selling_price",
            "stock",
        ]


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_code = serializers.CharField(source="product.product_code", read_only=True)

    class Meta:
        model = SaleItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_code",
            "quantity",
            "unit_price",
            "discount",
            "subtotal",
        ]
        read_only_fields = ["id", "unit_price", "subtotal"]


class SaleSerializer(serializers.ModelSerializer):
    """Read-only representation of a sale, used for detail/list responses."""

    items = SaleItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "sale_number",
            "status",
            "payment_method",
            "note",
            "customer",
            "created_by_name",
            "subtotal",
            "discount",
            "tax_percent",
            "tax_amount",
            "total",
            "items",
            "created_at",
            "updated_at",
            "completed_at",
        ]
        read_only_fields = fields


class SaleItemInputSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    discount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, default=Decimal("0")
    )


class SaleCreateSerializer(serializers.ModelSerializer):
    """Write serializer used by the POS screen to create/hold/complete a sale."""

    items = SaleItemInputSerializer(many=True, write_only=True)

    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), required=False, allow_null=True, write_only=True
    )
    customer_name = serializers.CharField(required=False, allow_blank=True, write_only=True)
    customer_phone = serializers.CharField(required=False, allow_blank=True, write_only=True)

    class Meta:
        model = Sale
        fields = [
            "status",
            "payment_method",
            "note",
            "discount",
            "tax_percent",
            "items",
            "customer",
            "customer_name",
            "customer_phone",
        ]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        return value

    def validate(self, attrs):
        status_value = attrs.get("status", Sale.Status.HOLD)
        if status_value not in (Sale.Status.HOLD, Sale.Status.COMPLETED):
            raise serializers.ValidationError(
                {"status": "Only HOLD or COMPLETED is allowed when creating a sale."}
            )
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        organization = request.user.organization

        items_data = validated_data.pop("items")
        customer = validated_data.pop("customer", None)
        customer_name = validated_data.pop("customer_name", "").strip()
        customer_phone = validated_data.pop("customer_phone", "").strip()
        status_value = validated_data.get("status", Sale.Status.HOLD)

        if customer is None and customer_name:
            customer, _ = Customer.objects.get_or_create(
                organization=organization,
                name=customer_name,
                phone=customer_phone,
            )

        with transaction.atomic():
            sale = Sale.objects.create(
                organization=organization,
                customer=customer,
                created_by=request.user,
                **validated_data,
            )

            for item in items_data:
                product = item["product"]
                if product.organization_id != organization.id:
                    raise serializers.ValidationError(
                        f"Product '{product.name}' does not belong to your organization."
                    )

                quantity = item["quantity"]

                if status_value == Sale.Status.COMPLETED and product.stock < quantity:
                    raise serializers.ValidationError(
                        f"Insufficient stock for '{product.name}'. Available: {product.stock}."
                    )

                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=quantity,
                    unit_price=product.selling_price,
                    discount=item.get("discount", Decimal("0")),
                )

                if status_value == Sale.Status.COMPLETED:
                    product.stock -= quantity
                    product.save()

            sale.recalculate_totals(save=False)
            if status_value == Sale.Status.COMPLETED:
                from django.utils import timezone

                sale.completed_at = timezone.now()
            sale.save()

        return sale


class SaleCompleteSerializer(serializers.Serializer):
    """Used to transition a HOLD sale to COMPLETED, deducting stock at that point."""

    payment_method = serializers.ChoiceField(choices=Sale.PaymentMethod.choices, required=False)

    def save(self, **kwargs):
        sale = self.context["sale"]

        if sale.status != Sale.Status.HOLD:
            raise serializers.ValidationError("Only a held sale can be completed.")

        payment_method = self.validated_data.get("payment_method")

        with transaction.atomic():
            for item in sale.items.select_related("product"):
                product = item.product
                if product.stock < item.quantity:
                    raise serializers.ValidationError(
                        f"Insufficient stock for '{product.name}'. Available: {product.stock}."
                    )

            for item in sale.items.select_related("product"):
                product = item.product
                product.stock -= item.quantity
                product.save()

            if payment_method:
                sale.payment_method = payment_method

            from django.utils import timezone

            sale.status = Sale.Status.COMPLETED
            sale.completed_at = timezone.now()
            sale.save()

        return sale
