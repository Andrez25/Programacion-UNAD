from datetime import datetime
from excepciones import (
    ErrorReservaInvalida,
    ErrorOperacionNoPermitida,
    ErrorDuracionInvalida,
    ErrorServicioNoDisponible,
)
from logger import registrar_info, registrar_error, registrar_evento

ESTADOS = {"pendiente", "confirmada", "cancelada", "completada"}


class Reserva:
    _reservas_registradas = []

    def __init__(self, cliente, servicio, duracion_horas, **parametros_adicionales):
        self._id = len(Reserva._reservas_registradas) + 1
        self._cliente = None
        self._servicio = None
        self._duracion_horas = None
        self._estado = "pendiente"
        self._fecha_creacion = datetime.now()
        self._fecha_confirmacion = None
        self._costo_total = None
        self._parametros_adicionales = parametros_adicionales

        try:
            self._asignar_cliente(cliente)
            self._asignar_servicio(servicio)
            self._asignar_duracion(duracion_horas)

            servicio.verificar_disponibilidad()
            servicio.validar_parametros_reserva(**parametros_adicionales)

            Reserva._reservas_registradas.append(self)
            cliente.agregar_reserva(self)
            registrar_info(
                f"Reserva #{self._id} creada — Cliente: {cliente.nombre} "
                f"| Servicio: {servicio.nombre} | Duración: {duracion_horas}h"
            )

        except (ErrorReservaInvalida, ErrorServicioNoDisponible, ErrorDuracionInvalida):
            raise
        except Exception as excepcion:
            raise ErrorReservaInvalida(
                f"No se pudo crear la reserva: {excepcion}"
            ) from excepcion

    def _asignar_cliente(self, cliente):
        from cliente import Cliente

        if not isinstance(cliente, Cliente):
            raise ErrorReservaInvalida("El cliente proporcionado no es válido.")
        if not cliente.activo:
            raise ErrorReservaInvalida(
                f"El cliente '{cliente.nombre}' está inactivo y no puede hacer reservas."
            )
        self._cliente = cliente

    def _asignar_servicio(self, servicio):
        from servicio import Servicio

        if not isinstance(servicio, Servicio):
            raise ErrorReservaInvalida("El servicio proporcionado no es válido.")
        self._servicio = servicio

    def _asignar_duracion(self, duracion):
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as excepcion:
            raise ErrorDuracionInvalida(duracion) from excepcion
        if duracion <= 0 or duracion > 24:
            raise ErrorDuracionInvalida(duracion)
        self._duracion_horas = duracion

    @property
    def id(self):
        return self._id

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def costo_total(self):
        return self._costo_total

    def calcular_costo(self, con_iva=False, descuento=0.0):
        try:
            costo = self._servicio.calcular_costo(
                self._duracion_horas, con_iva=con_iva, descuento=descuento
            )
            self._costo_total = costo
            return costo
        except Exception as excepcion:
            registrar_error(f"Error calculando costo de reserva #{self._id}", excepcion)
            raise

    def confirmar(self, con_iva=False, descuento=0.0):
        try:
            if self._estado != "pendiente":
                raise ErrorOperacionNoPermitida(
                    "confirmar",
                    f"La reserva está en estado '{self._estado}', no 'pendiente'.",
                )

            self._costo_total = self.calcular_costo(
                con_iva=con_iva, descuento=descuento
            )
            self._estado = "confirmada"
            self._fecha_confirmacion = datetime.now()

            registrar_evento(
                f"Reserva #{self._id} CONFIRMADA — "
                f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} "
                f"| Costo: ${self._costo_total:,.2f}"
            )
            return self._costo_total

        except (ErrorOperacionNoPermitida, ErrorReservaInvalida):
            raise
        except Exception as excepcion:
            registrar_error(f"Error al confirmar reserva #{self._id}", excepcion)
            raise ErrorReservaInvalida(
                f"No se pudo confirmar la reserva #{self._id}"
            ) from excepcion
        finally:
            registrar_info(
                f"Intento de confirmación procesado para reserva #{self._id}"
            )

    def cancelar(self, motivo="Sin motivo especificado"):
        try:
            if self._estado == "cancelada":
                raise ErrorOperacionNoPermitida(
                    "cancelar", "La reserva ya está cancelada."
                )
            if self._estado == "completada":
                raise ErrorOperacionNoPermitida(
                    "cancelar", "No se puede cancelar una reserva completada."
                )

            estado_anterior = self._estado
            self._estado = "cancelada"
            registrar_evento(
                f"Reserva #{self._id} CANCELADA — Motivo: {motivo} "
                f"| Estado anterior: {estado_anterior}"
            )

        except ErrorOperacionNoPermitida:
            raise
        except Exception as excepcion:
            raise ErrorReservaInvalida(
                f"Error al cancelar reserva #{self._id}"
            ) from excepcion
        finally:
            registrar_info(f"Intento de cancelación procesado para reserva #{self._id}")

    def completar(self):
        try:
            if self._estado != "confirmada":
                raise ErrorOperacionNoPermitida(
                    "completar",
                    f"Solo se pueden completar reservas confirmadas. Estado actual: '{self._estado}'.",
                )
            self._estado = "completada"
            registrar_evento(
                f"Reserva #{self._id} COMPLETADA — Servicio: {self._servicio.nombre}"
            )

        except ErrorOperacionNoPermitida:
            raise
        finally:
            registrar_info(f"Intento de completar procesado para reserva #{self._id}")

    def describir(self):
        costo_str = (
            f"${self._costo_total:,.2f}"
            if self._costo_total is not None
            else "No calculado"
        )
        return (
            f"Reserva #{self._id} | Estado: {self._estado.upper()} "
            f"| Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} "
            f"| Duración: {self._duracion_horas}h | Costo: {costo_str}"
        )

    def __str__(self):
        return self.describir()

    @classmethod
    def total_reservas(cls):
        return len(cls._reservas_registradas)

    @classmethod
    def reservas_por_estado(cls, estado):
        return [r for r in cls._reservas_registradas if r._estado == estado]
