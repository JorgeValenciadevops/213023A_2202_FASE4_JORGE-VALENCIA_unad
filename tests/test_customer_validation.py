import unittest

from customers import validar_datos_cliente


class CustomerValidationTests(unittest.TestCase):
    def test_nombre_con_numeros_debe_lanzar_error(self):
        with self.assertRaisesRegex(ValueError, "solo puede contener letras"):
            validar_datos_cliente("Juan123", "juan@example.com", "3001234567")

    def test_nombre_con_caracteres_especiales_debe_lanzar_error(self):
        with self.assertRaisesRegex(ValueError, "solo puede contener letras"):
            validar_datos_cliente("Juan@", "juan@example.com", "3001234567")

    def test_email_invalido_debe_lanzar_error(self):
        with self.assertRaisesRegex(ValueError, "Email"):
            validar_datos_cliente("Juan", "correo-invalido", "3001234567")

    def test_telefono_invalido_debe_lanzar_error(self):
        with self.assertRaisesRegex(ValueError, "Teléfono"):
            validar_datos_cliente("Juan", "juan@example.com", "abc")


if __name__ == "__main__":
    unittest.main()
