import re
from entidad_base import EntidadBase
from excepciones import ErrorClienteInvalido
from logger import registrar_info, registrar_error


class Cliente(EntidadBase):
    _clientes_registrados = []

    def __init__(self, nombre, cedula, correo, telefono):
        try:
            super().__init__(nombre)
            self._cedula = None
            self._correo = None
            self._telefono = None
            self._activo = True
            self._reservas = []

            self.cedula = cedula
            self.correo = correo
            self.telefono = telefono

            self.validar()
            Cliente._clientes_registrados.append(self)
            registrar_info(f"Cliente registrado: {self._nombre} (CC: {self._cedula})")

        except ErrorClienteInvalido:
            raise
        except Exception as excepcion:
            raise ErrorClienteInvalido(
                f"Error inesperado al crear cliente '{nombre}'"
            ) from excepcion

    @property
    def cedula(self):
        return self._cedula

    @cedula.setter
    def cedula(self, valor):
        if not valor or not str(valor).strip().isdigit():
            raise ErrorClienteInvalido(
                "La cédula debe contener solo dígitos.", campo="cedula"
            )
        if len(str(valor).strip()) < 6 or len(str(valor).strip()) > 10:
            raise ErrorClienteInvalido(
                "La cédula debe tener entre 6 y 10 dígitos.", campo="cedula"
            )
        for cliente in Cliente._clientes_registrados:
            if cliente._cedula == str(valor).strip():
                raise ErrorClienteInvalido(
                    f"Ya existe un cliente con cédula {valor}.", campo="cedula"
                )
        self._cedula = str(valor).strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor or not isinstance(valor, str):
            raise ErrorClienteInvalido(
                "El correo no puede estar vacío.", campo="correo"
            )
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron, valor.strip()):
            raise ErrorClienteInvalido(f"Correo inválido: '{valor}'.", campo="correo")
        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not str(valor).strip().isdigit():
            raise ErrorClienteInvalido(
                "El teléfono debe contener solo dígitos.", campo="telefono"
            )
        if len(str(valor).strip()) < 7:
            raise ErrorClienteInvalido(
                "El teléfono debe tener al menos 7 dígitos.", campo="telefono"
            )
        self._telefono = str(valor).strip()

    @property
    def activo(self):
        return self._activo

    @property
    def reservas(self):
        return list(self._reservas)

    def agregar_reserva(self, reserva):
        self._reservas.append(reserva)

    def desactivar(self):
        self._activo = False
        registrar_info(f"Cliente desactivado: {self._nombre}")

    def validar(self):
        if not self._nombre or not self._nombre.strip():
            raise ErrorClienteInvalido(
                "El nombre del cliente no puede estar vacío.", campo="nombre"
            )
        if len(self._nombre.strip()) < 3:
            raise ErrorClienteInvalido(
                "El nombre debe tener al menos 3 caracteres.", campo="nombre"
            )
        return True

    def describir(self):
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente #{self._id} | {self._nombre} | CC: {self._cedula} "
            f"| Correo: {self._correo} | Tel: {self._telefono} | Estado: {estado}"
        )

    @classmethod
    def buscar_por_cedula(cls, cedula):
        for cliente in cls._clientes_registrados:
            if cliente._cedula == str(cedula).strip():
                return cliente
        return None

    @classmethod
    def total_clientes(cls):
        return len(cls._clientes_registrados)
