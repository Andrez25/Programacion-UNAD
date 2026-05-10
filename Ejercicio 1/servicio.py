from abc import abstractmethod
from entidad_base import EntidadBase
from excepciones import (
    ErrorServicioNoDisponible,
    ErrorParametroInvalido,
    ErrorCalculoCosto,
    ErrorDuracionInvalida,
)
from logger import registrar_info, registrar_advertencia

IVA = 0.19


class Servicio(EntidadBase):
    def __init__(self, nombre, precio_hora, disponible=True):
        super().__init__(nombre)
        self._precio_hora = None
        self._disponible = disponible
        self.precio_hora = precio_hora

    @property
    def precio_hora(self):
        return self._precio_hora

    @precio_hora.setter
    def precio_hora(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError) as excepcion:
            raise ErrorParametroInvalido("precio_hora", valor) from excepcion
        if valor <= 0:
            raise ErrorParametroInvalido("precio_hora", valor)
        self._precio_hora = valor

    @property
    def disponible(self):
        return self._disponible

    def activar(self):
        self._disponible = True
        registrar_info(f"Servicio activado: {self._nombre}")

    def desactivar(self):
        self._disponible = False
        registrar_advertencia(f"Servicio desactivado: {self._nombre}")

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ErrorServicioNoDisponible(self._nombre)

    def _validar_duracion(self, duracion):
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as excepcion:
            raise ErrorDuracionInvalida(duracion) from excepcion
        if duracion <= 0:
            raise ErrorDuracionInvalida(duracion)
        return duracion

    def calcular_costo(self, duracion_horas, con_iva=False, descuento=0.0):
        try:
            duracion_horas = self._validar_duracion(duracion_horas)

            if not isinstance(descuento, (int, float)) or not (0 <= descuento < 1):
                raise ErrorCalculoCosto(
                    f"El descuento debe ser un valor entre 0 y 1, se recibió: {descuento!r}"
                )

            costo_base = self._precio_hora * duracion_horas
            costo_con_descuento = costo_base * (1 - descuento)
            costo_adicional = self._calcular_costo_adicional(duracion_horas)
            costo_total = costo_con_descuento + costo_adicional

            if con_iva:
                costo_total = costo_total * (1 + IVA)

            return round(costo_total, 2)

        except (ErrorDuracionInvalida, ErrorCalculoCosto):
            raise
        except Exception as excepcion:
            raise ErrorCalculoCosto(
                f"Error al calcular costo del servicio '{self._nombre}'"
            ) from excepcion

    @abstractmethod
    def _calcular_costo_adicional(self, duracion_horas):
        pass

    @abstractmethod
    def validar_parametros_reserva(self, **kwargs):
        pass

    def validar(self):
        return self._precio_hora is not None and self._precio_hora > 0

    @abstractmethod
    def describir(self):
        pass


class ReservaSala(Servicio):
    CAPACIDAD_MINIMA = 2
    CAPACIDAD_MAXIMA = 50

    def __init__(self, nombre, precio_hora, capacidad, disponible=True):
        super().__init__(nombre, precio_hora, disponible)
        self._capacidad = None
        self.capacidad = capacidad
        registrar_info(
            f"Servicio creado: Sala '{nombre}', capacidad {capacidad} personas."
        )

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError) as excepcion:
            raise ErrorParametroInvalido("capacidad", valor) from excepcion
        if not (self.CAPACIDAD_MINIMA <= valor <= self.CAPACIDAD_MAXIMA):
            raise ErrorParametroInvalido("capacidad", valor)
        self._capacidad = valor

    def _calcular_costo_adicional(self, duracion_horas):
        if self._capacidad > 20:
            return self._precio_hora * duracion_horas * 0.10
        return 0.0

    def validar_parametros_reserva(self, **kwargs):
        asistentes = kwargs.get("asistentes", 1)
        try:
            asistentes = int(asistentes)
        except (TypeError, ValueError) as excepcion:
            raise ErrorParametroInvalido("asistentes", asistentes) from excepcion
        if asistentes < 1:
            raise ErrorParametroInvalido("asistentes", asistentes)
        if asistentes > self._capacidad:
            raise ErrorReservaSalaExcedida(asistentes, self._capacidad)
        return True

    def describir(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Sala] {self._nombre} | Capacidad: {self._capacidad} personas "
            f"| Precio/hora: ${self._precio_hora:,.0f} | {estado}"
        )


class AlquilerEquipo(Servicio):
    EQUIPOS_VALIDOS = {"laptop", "proyector", "camara", "drone", "servidor"}

    def __init__(self, nombre, precio_hora, tipo_equipo, cantidad=1, disponible=True):
        super().__init__(nombre, precio_hora, disponible)
        self._tipo_equipo = None
        self._cantidad = None
        self.tipo_equipo = tipo_equipo
        self.cantidad = cantidad
        registrar_info(
            f"Servicio creado: Equipo '{nombre}' ({tipo_equipo} x{cantidad})."
        )

    @property
    def tipo_equipo(self):
        return self._tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor):
        if (
            not isinstance(valor, str)
            or valor.strip().lower() not in self.EQUIPOS_VALIDOS
        ):
            raise ErrorParametroInvalido("tipo_equipo", valor)
        self._tipo_equipo = valor.strip().lower()

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError) as excepcion:
            raise ErrorParametroInvalido("cantidad", valor) from excepcion
        if valor < 1:
            raise ErrorParametroInvalido("cantidad", valor)
        self._cantidad = valor

    def _calcular_costo_adicional(self, duracion_horas):
        if self._cantidad > 1:
            return self._precio_hora * (self._cantidad - 1) * duracion_horas * 0.80
        return 0.0

    def validar_parametros_reserva(self, **kwargs):
        cantidad_solicitada = kwargs.get("cantidad_solicitada", 1)
        try:
            cantidad_solicitada = int(cantidad_solicitada)
        except (TypeError, ValueError) as excepcion:
            raise ErrorParametroInvalido(
                "cantidad_solicitada", cantidad_solicitada
            ) from excepcion
        if cantidad_solicitada < 1 or cantidad_solicitada > self._cantidad:
            raise ErrorParametroInvalido("cantidad_solicitada", cantidad_solicitada)
        return True

    def describir(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Equipo] {self._nombre} | Tipo: {self._tipo_equipo} "
            f"| Cantidad: {self._cantidad} | Precio/hora: ${self._precio_hora:,.0f} | {estado}"
        )


class AsesoriaEspecializada(Servicio):
    AREAS_VALIDAS = {"software", "redes", "seguridad", "datos", "gestion"}

    def __init__(self, nombre, precio_hora, area, nivel_experto=False, disponible=True):
        super().__init__(nombre, precio_hora, disponible)
        self._area = None
        self._nivel_experto = nivel_experto
        self.area = area
        registrar_info(
            f"Servicio creado: Asesoría '{nombre}' | Área: {area} "
            f"| Experto: {'Sí' if nivel_experto else 'No'}."
        )

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, valor):
        if (
            not isinstance(valor, str)
            or valor.strip().lower() not in self.AREAS_VALIDAS
        ):
            raise ErrorParametroInvalido("area", valor)
        self._area = valor.strip().lower()

    @property
    def nivel_experto(self):
        return self._nivel_experto

    def _calcular_costo_adicional(self, duracion_horas):
        if self._nivel_experto:
            return self._precio_hora * duracion_horas * 0.50
        return 0.0

    def validar_parametros_reserva(self, **kwargs):
        tema = kwargs.get("tema", "")
        if not tema or not isinstance(tema, str) or len(tema.strip()) < 5:
            raise ErrorParametroInvalido("tema", tema)
        return True

    def describir(self):
        estado = "Disponible" if self._disponible else "No disponible"
        nivel = "Experto" if self._nivel_experto else "Estándar"
        return (
            f"[Asesoría] {self._nombre} | Área: {self._area} "
            f"| Nivel: {nivel} | Precio/hora: ${self._precio_hora:,.0f} | {estado}"
        )


class ErrorReservaSalaExcedida(Exception):
    def __init__(self, asistentes, capacidad):
        super().__init__(
            f"No hay capacidad: se solicitaron {asistentes} asistentes pero la sala tiene capacidad para {capacidad}."
        )
        self.asistentes = asistentes
        self.capacidad = capacidad
