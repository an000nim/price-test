from decimal import Decimal
from unittest import IsolatedAsyncioTestCase

from starter import recommend_price


class RecommendPriceTests(IsolatedAsyncioTestCase):
    async def test_calculates_price_from_eligible_competitors(self):
        async def fetch_offers():
            return {
                "status": "success",
                "offers": [
                    {"seller": "MyShOp", "price": Decimal("70.00"), "delivery_days": 1},
                    {"seller": "SLOW", "price": Decimal("80.00"), "delivery_days": 7},
                    {"seller": "UNKNOWN", "price": Decimal("90.00"), "delivery_days": None},
                    {"seller": "FAST", "price": Decimal("100.01"), "delivery_days": 6},
                    {"seller": "OTHER", "price": Decimal("110.00"), "delivery_days": 2},
                ],
            }

        result = await recommend_price(fetch_offers, Decimal("105.00"), Decimal("95.00"))

        self.assertIsInstance(result["price"], Decimal)
        self.assertEqual(result["price"], Decimal("98.50"))
        self.assertEqual(result["decision"], "APPLY")

    async def test_applies_minimum_at_exactly_thirty_percent(self):
        async def fetch_offers():
            return {
                "status": "success",
                "offers": [
                    {"seller": "PARTS", "price": Decimal("120.00"), "delivery_days": 2},
                ],
            }

        result = await recommend_price(fetch_offers, Decimal("100.00"), Decimal("130.00"))

        self.assertEqual(result["price"], Decimal("130.00"))
        self.assertEqual(result["decision"], "APPLY")
