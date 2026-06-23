"""
Smart Order Fulfillment & Inventory Management API
--------------------------------------------------

This backend service manages products, inventory, orders, payments,
and shipment workflows for an eCommerce-like system.

Designed to expose rich API behavior, business rules, and system flows
for generating API docs, sequence diagrams, flowcharts, SRS, and FRS.
"""

import uuid
import time
from datetime import datetime
from typing import Dict, List, Optional


# -------------------------
# Configuration
# -------------------------

class Settings:
    LOW_STOCK_THRESHOLD = 5
    PAYMENT_RETRY_LIMIT = 2
    SUPPORTED_PAYMENT_METHODS = ["CARD", "UPI", "WALLET"]


# -------------------------
# Domain Models
# -------------------------

class Product:
    def __init__(self, product_id: uuid.UUID, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price


class InventoryItem:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity
        self.updated_at = datetime.utcnow()


class Order:
    def __init__(self, order_id: uuid.UUID, customer_id: uuid.UUID):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items: Dict[uuid.UUID, int] = {}
        self.status = "CREATED"
        self.created_at = datetime.utcnow()


class Payment:
    def __init__(self, payment_id: uuid.UUID, order_id: uuid.UUID, amount: float):
        self.payment_id = payment_id
        self.order_id = order_id
        self.amount = amount
        self.status = "PENDING"


class Shipment:
    def __init__(self, shipment_id: uuid.UUID, order_id: uuid.UUID):
        self.shipment_id = shipment_id
        self.order_id = order_id
        self.status = "NOT_DISPATCHED"


# -------------------------
# Infrastructure Services
# -------------------------

class InventoryService:
    def __init__(self):
        self.inventory: Dict[uuid.UUID, InventoryItem] = {}

    def reserve_stock(self, product_id: uuid.UUID, quantity: int) -> bool:
        item = self.inventory.get(product_id)
        if not item or item.quantity < quantity:
            return False
        item.quantity -= quantity
        item.updated_at = datetime.utcnow()
        return True

    def add_stock(self, product: Product, quantity: int):
        self.inventory[product.product_id] = InventoryItem(product, quantity)


class PaymentGateway:
    def charge(self, amount: float, method: str) -> bool:
        time.sleep(0.5)
        return method in Settings.SUPPORTED_PAYMENT_METHODS


class NotificationService:
    def notify(self, customer_id: uuid.UUID, message: str):
        print(f"Notify {customer_id}: {message}")


# -------------------------
# Business Logic Layer
# -------------------------

class OrderService:
    def __init__(
        self,
        inventory: InventoryService,
        payment_gateway: PaymentGateway,
        notifier: NotificationService
    ):
        self.inventory = inventory
        self.payment_gateway = payment_gateway
        self.notifier = notifier

    def place_order(
        self,
        customer_id: uuid.UUID,
        items: Dict[Product, int],
        payment_method: str
    ) -> Order:

        order = Order(uuid.uuid4(), customer_id)

        for product, qty in items.items():
            success = self.inventory.reserve_stock(product.product_id, qty)
            if not success:
                order.status = "FAILED_STOCK"
                self.notifier.notify(customer_id, "Insufficient stock")
                return order
            order.items[product.product_id] = qty

        total_amount = sum(p.price * q for p, q in items.items())
        payment_success = self._process_payment(total_amount, payment_method)

        if not payment_success:
            order.status = "PAYMENT_FAILED"
            self.notifier.notify(customer_id, "Payment failed")
            return order

        order.status = "CONFIRMED"
        self.notifier.notify(customer_id, "Order confirmed")
        return order

    def _process_payment(self, amount: float, method: str) -> bool:
        for attempt in range(Settings.PAYMENT_RETRY_LIMIT):
            if self.payment_gateway.charge(amount, method):
                return True
        return False


# -------------------------
# API Layer
# -------------------------

class Request:
    def __init__(self, payload: Dict):
        self.payload = payload


class Response:
    def __init__(self, status: int, body: Dict):
        self.status = status
        self.body = body


class OrderAPI:
    def __init__(self, service: OrderService):
        self.service = service

    def create_order(self, request: Request) -> Response:
        customer_id = request.payload.get("customer_id")
        items = request.payload.get("items")
        payment_method = request.payload.get("payment_method")

        if not customer_id or not items or not payment_method:
            return Response(400, {"error": "Invalid request"})

        order = self.service.place_order(
            customer_id=customer_id,
            items=items,
            payment_method=payment_method
        )

        return Response(
            200,
            {
                "order_id": str(order.order_id),
                "status": order.status,
                "items": order.items
            }
        )


# -------------------------
# Bootstrap & Runtime
# -------------------------

def bootstrap() -> OrderAPI:
    inventory = InventoryService()
    payment_gateway = PaymentGateway()
    notifier = NotificationService()

    product_a = Product(uuid.uuid4(), "Wireless Mouse", 25.0)
    product_b = Product(uuid.uuid4(), "Keyboard", 45.0)

    inventory.add_stock(product_a, 10)
    inventory.add_stock(product_b, 2)

    order_service = OrderService(inventory, payment_gateway, notifier)
    return OrderAPI(order_service)


if __name__ == "__main__":
    api = bootstrap()

    request = Request(
        payload={
            "customer_id": uuid.uuid4(),
            "items": {},
            "payment_method": "CARD"
        }
    )

    response = api.create_order(request)
    print(response.status, response.body)
