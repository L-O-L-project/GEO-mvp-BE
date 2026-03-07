import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app


class GeoTestPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_geo_test_page_served(self):
        res = self.client.get("/geo-test")
        self.assertEqual(res.status_code, 200)
        self.assertIn("text/html", res.headers.get("content-type", ""))
        self.assertIn("GEO Audit Test Console", res.text)
        self.assertIn("Verified Details", res.text)
        self.assertIn("Valid JSON-LD pages", res.text)

    def test_geo_audit_requires_url(self):
        res = self.client.post("/api/geo-audit", json={})
        self.assertEqual(res.status_code, 400)
        body = res.json()
        self.assertEqual(body.get("detail", {}).get("errorCode"), "URL_REQUIRED")

    def test_geo_audit_runs_and_returns_result(self):
        fake_result = {
            "url": "https://example.com",
            "geo_score": 88,
            "checks": {"title": True},
            "structured_data": ["Organization"],
            "recommendations": [],
            "evidence": {
                "origin": "https://example.com",
                "target": "https://example.com",
                "json_ld_summary": {"total_pages": 1, "valid_pages": 1, "missing_pages": 0, "invalid_pages": 0},
                "json_ld_pages": [
                    {
                        "url": "https://example.com",
                        "path": "/",
                        "depth": 0,
                        "status_code": 200,
                        "present": True,
                        "applied_well": True,
                        "block_count": 1,
                        "valid_block_count": 1,
                        "invalid_block_count": 0,
                        "types": ["Organization"],
                        "target_types": ["Organization"],
                        "issues": [],
                        "blocks": [],
                    }
                ],
                "crawled_pages": [{"url": "https://example.com", "path": "/", "depth": 0, "status_code": 200}],
            },
            "verified_sections": [
                {
                    "id": "meta",
                    "label": "Meta Tags",
                    "summary": "1/1 checks passed",
                    "passCount": 1,
                    "totalCount": 1,
                    "items": [
                        {"key": "title", "label": "Page title", "passed": True, "status": "PASS", "value": "Present"}
                    ],
                },
                {
                    "id": "json_ld_pages",
                    "label": "Page JSON-LD Coverage",
                    "summary": "1/1 page(s) have valid JSON-LD",
                    "passCount": 1,
                    "totalCount": 1,
                    "items": [
                        {"key": "json_ld:/", "label": "/", "passed": True, "status": "PASS", "value": ["Organization"]}
                    ],
                }
            ],
        }
        with patch("app.routers.geo.run_geo_audit", AsyncMock(return_value=fake_result)) as mocked:
            res = self.client.post("/api/geo-audit", json={"url": "https://example.com"})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json(), fake_result)
            mocked.assert_awaited_once_with("https://example.com")
