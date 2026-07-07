import unittest
from datetime import date

from ui import formatear_fecha_hora_seleccionada


class FormatoFechaHoraTests(unittest.TestCase):
    def test_convierte_hora_12h_a_formato_24h(self):
        self.assertEqual(
            formatear_fecha_hora_seleccionada(date(2026, 7, 5), "09", "30", "AM"),
            "2026-07-05 09:30"
        )

    def test_convierte_hora_de_tarde_correctamente(self):
        self.assertEqual(
            formatear_fecha_hora_seleccionada(date(2026, 7, 5), "12", "45", "PM"),
            "2026-07-05 12:45"
        )

    def test_convierte_medianoche_correctamente(self):
        self.assertEqual(
            formatear_fecha_hora_seleccionada(date(2026, 7, 5), "12", "00", "AM"),
            "2026-07-05 00:00"
        )


if __name__ == "__main__":
    unittest.main()
