import unittest

from reservations import validar_rango_fechas


class ReservationDateValidationTests(unittest.TestCase):
    def test_fecha_fin_mayor_a_inicio(self):
        self.assertTrue(validar_rango_fechas("2026-07-05 10:00", "2026-07-05 11:00"))

    def test_fecha_fin_igual_a_inicio_debe_lanzar_error(self):
        with self.assertRaisesRegex(ValueError, "mayor"):
            validar_rango_fechas("2026-07-05 10:00", "2026-07-05 10:00")

    def test_fecha_fin_menor_a_inicio_debe_lanzar_error(self):
        with self.assertRaisesRegex(ValueError, "mayor"):
            validar_rango_fechas("2026-07-05 11:00", "2026-07-05 10:00")


if __name__ == "__main__":
    unittest.main()
