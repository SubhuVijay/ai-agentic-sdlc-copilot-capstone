import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from holdshelf.catalog import Catalog, Hold
from holdshelf.overdue import select_overdue, validate_days
from holdshelf.server import ShelfApp


class HoldShelfTests(unittest.TestCase):
    def setUp(self):
        self.app = ShelfApp(Catalog([
            Hold("H-1042", "The Thursday Murder Club", "Maya Chen", "2026-11-02", "ready", "555-0142"),
            Hold("H-1048", "Braiding Sweetgrass", "Luis Ortega", "2026-11-16", "ready", None),
        ]))

    def test_health(self):
        status, body = self.app.handle("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"status": "ok"})

    def test_lists_holds_and_keeps_a_missing_phone_as_null(self):
        status, body = self.app.handle("GET", "/api/holds")
        self.assertEqual(status, 200)
        by_id = {hold["id"]: hold for hold in body["holds"]}
        self.assertEqual(by_id["H-1042"]["title"], "The Thursday Murder Club")
        self.assertEqual(by_id["H-1042"]["status"], "ready")
        self.assertIsNone(by_id["H-1048"]["phone"])

    def test_pickup_marks_the_hold_and_rejects_a_second_pickup(self):
        status, body = self.app.handle("POST", "/api/holds/H-1042/pickup")
        self.assertEqual(status, 200)
        self.assertEqual(body["hold"]["status"], "picked-up")
        status, body = self.app.handle("POST", "/api/holds/H-1042/pickup")
        self.assertEqual(status, 409)
        self.assertIn("already picked up", body["error"])

    def test_unknown_hold_returns_404(self):
        status, body = self.app.handle("POST", "/api/holds/H-0000/pickup")
        self.assertEqual(status, 404)
        self.assertIn("H-0000", body["error"])

    def test_page_loads_the_hold_api(self):
        status, page = self.app.handle("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("Hold shelf", page)
        self.assertIn("/api/holds", page)
        self.assertIn("/api/health", page)

    def test_page_contract_includes_overdue_controls_and_failure_states(self):
        status, page = self.app.handle("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("Overdue Holds", page)
        self.assertIn('id="overdue-days"', page)
        self.assertIn('value="7"', page)
        self.assertIn("/api/holds/overdue?days=", page)
        self.assertIn("waitingDays", page)
        self.assertIn("Not Found", page)
        self.assertIn("No ready hold is past the pickup window.", page)
        self.assertIn("Retry", page)
        self.assertIn("clearOverdueRows", page)
        self.assertIn("positive integer", page)
        self.assertIn("/api/holds", page)
        self.assertIn("pickup", page)

    def test_unknown_path_returns_404(self):
        status, body = self.app.handle("GET", "/api/other")
        self.assertEqual(status, 404)
        self.assertIn("error", body)

    def test_overdue_service_uses_strict_window_and_maps_missing_phone(self):
        holds = [
            {"id": "old", "title": "Old", "patron": "A", "readySince": "2026-11-02",
             "status": "ready", "phone": "555-0100"},
            {"id": "boundary", "title": "Boundary", "patron": "B",
             "readySince": "2026-11-11", "status": "ready", "phone": None},
            {"id": "picked", "title": "Picked", "patron": "C",
             "readySince": "2026-10-01", "status": "picked-up", "phone": "555-0101"},
            {"id": "missing", "title": "Missing", "patron": "D",
             "readySince": None, "status": "ready", "phone": None},
            {"id": "bad", "title": "Bad", "patron": "E",
             "readySince": "not-a-date", "status": "ready", "phone": None},
        ]
        result = select_overdue(holds, days=7, today=date(2026, 11, 18))
        self.assertEqual([hold["id"] for hold in result], ["old"])
        self.assertEqual(result[0]["waitingDays"], 16)
        self.assertEqual(result[0]["phone"], "555-0100")

        short_result = select_overdue(holds, days=6, today=date(2026, 11, 18))
        self.assertEqual(
            {hold["id"] for hold in short_result}, {"old", "boundary"}
        )
        self.assertEqual(
            next(hold for hold in short_result if hold["id"] == "boundary")["phone"],
            "Not Found",
        )

    def test_overdue_api_contract_and_validation(self):
        app = ShelfApp(self.app.catalog, today=date(2026, 11, 18))
        status, body = app.handle("GET", "/api/holds/overdue")
        self.assertEqual(status, 200)
        self.assertEqual(body["holds"][0]["id"], "H-1042")
        self.assertEqual(body["holds"][0]["waitingDays"], 16)

        status, body = app.handle("GET", "/api/holds/overdue?days=0")
        self.assertEqual(status, 400)
        self.assertEqual(body, {"error": "days must be a positive integer"})
        status, body = app.handle("GET", "/api/holds/overdue?days=")
        self.assertEqual(status, 400)
        status, body = app.handle("GET", "/api/holds/overdue?days=2&days=3")
        self.assertEqual(status, 400)
        self.assertEqual(validate_days(None), 7)
        with self.assertRaises(ValueError):
            validate_days("1.5")


class OverdueAcceptanceTests(unittest.TestCase):
    """Black-box acceptance coverage through the public ShelfApp interface."""

    def setUp(self):
        self.app = ShelfApp(Catalog([
            Hold("H-1042", "The Thursday Murder Club", "Maya Chen",
                 "2026-11-02", "ready", "555-0142"),
            Hold("H-1048", "Braiding Sweetgrass", "Luis Ortega",
                 "2026-11-16", "ready", None),
            Hold("H-0991", "Project Hail Mary", "Imani Brooks",
                 "2026-10-28", "picked-up", "555-0190"),
            Hold("H-NODATE", "A Book Without a Date", "Rae Singh",
                 None, "ready", "555-0166"),
            Hold("H-BADDATE", "A Book With a Bad Date", "Noah Kim",
                 "not-a-date", "ready", "555-0188"),
        ]), today=date(2026, 11, 18))

    def test_api_and_page_expose_the_same_overdue_contract(self):
        status, api_body = self.app.handle("GET", "/api/holds/overdue?days=7")
        self.assertEqual(status, 200)
        self.assertEqual([hold["id"] for hold in api_body["holds"]], ["H-1042"])
        self.assertEqual(api_body["holds"][0]["waitingDays"], 16)

        status, page = self.app.handle("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("/api/holds/overdue?days=", page)
        self.assertIn("hold.id", page)
        self.assertIn("hold.waitingDays", page)
        self.assertIn("hold.phone", page)
        self.assertIn("Not Found", page)

    def test_anchored_default_window_includes_only_the_approved_hold(self):
        status, body = self.app.handle("GET", "/api/holds/overdue")
        self.assertEqual(status, 200)
        self.assertEqual([hold["id"] for hold in body["holds"]], ["H-1042"])
        self.assertNotIn("H-1048", {hold["id"] for hold in body["holds"]})
        self.assertNotIn("H-0991", {hold["id"] for hold in body["holds"]})

    def test_short_window_includes_recent_ready_hold_and_serializes_missing_phone(self):
        status, body = self.app.handle("GET", "/api/holds/overdue?days=1")
        self.assertEqual(status, 200)
        by_id = {hold["id"]: hold for hold in body["holds"]}
        self.assertEqual(set(by_id), {"H-1042", "H-1048"})
        self.assertEqual(by_id["H-1048"]["waitingDays"], 2)
        self.assertEqual(by_id["H-1048"]["phone"], "Not Found")

    def test_invalid_windows_return_a_clear_bad_request(self):
        for value in ("0", "-1", "1.5", "tomorrow", "7x", ""):
            with self.subTest(value=value):
                status, body = self.app.handle(
                    "GET", "/api/holds/overdue?days=" + value
                )
                self.assertEqual(status, 400)
                self.assertEqual(
                    body, {"error": "days must be a positive integer"}
                )

        status, body = self.app.handle(
            "GET", "/api/holds/overdue?days=2&days=3"
        )
        self.assertEqual(status, 400)
        self.assertEqual(body, {"error": "days must be a positive integer"})

    def test_missing_and_malformed_dates_are_excluded(self):
        status, body = self.app.handle("GET", "/api/holds/overdue?days=1")
        self.assertEqual(status, 200)
        result_ids = {hold["id"] for hold in body["holds"]}
        self.assertNotIn("H-NODATE", result_ids)
        self.assertNotIn("H-BADDATE", result_ids)

    def test_empty_success_and_empty_catalog(self):
        status, body = self.app.handle("GET", "/api/holds/overdue?days=100")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"holds": []})

        empty_app = ShelfApp(Catalog([]), today=date(2026, 11, 18))
        status, body = empty_app.handle("GET", "/api/holds/overdue")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"holds": []})

    def test_pickup_changes_subsequent_overdue_results(self):
        status, body = self.app.handle("GET", "/api/holds/overdue")
        self.assertEqual(status, 200)
        self.assertIn("H-1042", {hold["id"] for hold in body["holds"]})

        status, body = self.app.handle("POST", "/api/holds/H-1042/pickup")
        self.assertEqual(status, 200)
        self.assertEqual(body["hold"]["status"], "picked-up")

        status, body = self.app.handle("GET", "/api/holds/overdue")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"holds": []})

    def test_existing_health_list_and_pickup_routes_remain_compatible(self):
        status, body = self.app.handle("GET", "/api/health")
        self.assertEqual((status, body), (200, {"status": "ok"}))

        status, body = self.app.handle("GET", "/api/holds")
        self.assertEqual(status, 200)
        by_id = {hold["id"]: hold for hold in body["holds"]}
        self.assertIsNone(by_id["H-1048"]["phone"])
        self.assertEqual(by_id["H-0991"]["status"], "picked-up")

        status, body = self.app.handle("POST", "/api/holds/H-1048/pickup")
        self.assertEqual(status, 200)
        self.assertEqual(body["hold"]["status"], "picked-up")
        status, body = self.app.handle("POST", "/api/holds/H-1048/pickup")
        self.assertEqual(status, 409)


if __name__ == "__main__":
    unittest.main()
