import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import (
    ErrorClienteInvalido,
    ErrorServicioNoDisponible,
    ErrorParametroInvalido,
    ErrorReservaInvalida,
    ErrorOperacionNoPermitida,
    ErrorCalculoCosto,
    ErrorDuracionInvalida,
)
from logger import (
    registrar_info,
    registrar_error,
    registrar_advertencia,
    registrar_evento,
)


def separador(titulo):
    print(f"\n{'=' * 60}")
    print(f"  OPERACION: {titulo}")
    print(f"{'=' * 60}")


def main():
    print("\n" + "=" * 60)
    print("     SOFTWARE  — SISTEMA DE GESTION INTEGRAL")
    print("=" * 60)

    clientes = {}
    servicios = {}
    reservas = []

    separador("1 — Registro de cliente valido")
    try:
        c1 = Cliente(
            "Carlos Mendoza", "1098234567", "cmendoza@correo.com", "3001234567"
        )
        clientes["c1"] = c1
        print(f"  OK: {c1.describir()}")
    except ErrorClienteInvalido as e:
        registrar_error("Fallo registro cliente valido", e)

    separador("2 — Registro de cliente con correo invalido")
    try:
        c2 = Cliente("Laura Torres", "1098876543", "correo_mal_formado", "3109876543")
        clientes["c2"] = c2
    except ErrorClienteInvalido as e:
        registrar_error("Registro rechazado (esperado)", e)
        print(f"  Sistema continua operando correctamente.")

    separador("3 — Registro de cliente con cedula duplicada")
    try:
        c_dup = Cliente("Carlos Copia", "1098234567", "copia@correo.com", "3201112233")
    except ErrorClienteInvalido as e:
        registrar_error("Cedula duplicada detectada (esperado)", e)
        print(f"  Sistema continua operando correctamente.")

    separador("4 — Registro de segundo cliente valido")
    try:
        c2 = Cliente("Ana Gutierrez", "987654321", "ana@empresa.co", "3157654321")
        clientes["c2"] = c2
        print(f"  OK: {c2.describir()}")
    except ErrorClienteInvalido as e:
        registrar_error("Fallo registro segundo cliente", e)

    separador("5 — Creacion de servicios validos")
    try:
        sala = ReservaSala("Sala Alfa", precio_hora=80000, capacidad=15)
        equipo = AlquilerEquipo(
            "Laptop ProX", precio_hora=25000, tipo_equipo="laptop", cantidad=3
        )
        asesoria = AsesoriaEspecializada(
            "Consultoria de Software",
            precio_hora=120000,
            area="software",
            nivel_experto=True,
        )
        servicios["sala"] = sala
        servicios["equipo"] = equipo
        servicios["asesoria"] = asesoria
        print(f"  OK: {sala.describir()}")
        print(f"  OK: {equipo.describir()}")
        print(f"  OK: {asesoria.describir()}")
    except ErrorParametroInvalido as e:
        registrar_error("Error creando servicios", e)

    separador("6 — Creacion de servicio con tipo de equipo invalido")
    try:
        equipo_malo = AlquilerEquipo(
            "Equipo Raro", precio_hora=15000, tipo_equipo="microondas"
        )
    except ErrorParametroInvalido as e:
        registrar_error("Tipo de equipo invalido detectado (esperado)", e)
        print(f"  Sistema continua operando correctamente.")

    separador("7 — Reserva exitosa de sala con IVA")
    try:
        r1 = Reserva(clientes["c1"], servicios["sala"], duracion_horas=3, asistentes=10)
        costo = r1.confirmar(con_iva=True)
        reservas.append(r1)
        print(f"  OK: {r1.describir()}")
        print(f"  Costo con IVA: ${costo:,.2f}")
    except (ErrorReservaInvalida, ErrorServicioNoDisponible) as e:
        registrar_error("Fallo reserva de sala", e)

    separador("8 — Reserva de sala excediendo capacidad")
    try:
        r_mala = Reserva(
            clientes["c1"], servicios["sala"], duracion_horas=2, asistentes=99
        )
    except Exception as e:
        registrar_error("Capacidad excedida detectada (esperado)", e)
        print(f"  Sistema continua operando correctamente.")

    separador("9 — Reserva de asesoria con descuento")
    try:
        r2 = Reserva(
            clientes["c2"],
            servicios["asesoria"],
            duracion_horas=2,
            tema="Arquitectura de microservicios en la nube",
        )
        costo = r2.confirmar(con_iva=False, descuento=0.15)
        reservas.append(r2)
        print(f"  OK: {r2.describir()}")
        print(f"  Costo con 15% de descuento: ${costo:,.2f}")
    except (ErrorReservaInvalida, ErrorOperacionNoPermitida) as e:
        registrar_error("Fallo reserva de asesoria", e)

    separador("10 — Intento de confirmar reserva ya confirmada")
    try:
        if reservas:
            reservas[0].confirmar()
    except ErrorOperacionNoPermitida as e:
        registrar_error("Doble confirmacion bloqueada (esperado)", e)
        print(f"  Sistema continua operando correctamente.")

    separador("11 — Reserva sobre servicio desactivado")
    try:
        servicios["equipo"].desactivar()
        r_inactiva = Reserva(
            clientes["c1"], servicios["equipo"], duracion_horas=4, cantidad_solicitada=2
        )
    except ErrorServicioNoDisponible as e:
        registrar_error("Servicio no disponible detectado (esperado)", e)
        print(f"  Sistema continua operando correctamente.")
        servicios["equipo"].activar()

    separador("12 — Reserva de equipo y cancelacion justificada")
    try:
        r3 = Reserva(
            clientes["c2"], servicios["equipo"], duracion_horas=5, cantidad_solicitada=2
        )
        costo = r3.confirmar(con_iva=True, descuento=0.10)
        reservas.append(r3)
        print(f"  OK: {r3.describir()}")
        print(f"  Costo con IVA y 10% descuento: ${costo:,.2f}")
        r3.cancelar(motivo="El cliente reagendo la sesion.")
        print(f"  Tras cancelacion: {r3.describir()}")
    except (ErrorReservaInvalida, ErrorOperacionNoPermitida) as e:
        registrar_error("Error en operacion de equipo", e)

    separador("13 — Duracion invalida en nueva reserva")
    try:
        r_dur = Reserva(
            clientes["c1"], servicios["sala"], duracion_horas=-2, asistentes=5
        )
    except ErrorDuracionInvalida as e:
        registrar_error("Duracion invalida detectada (esperado)", e)
        print(f"  Sistema continua operando correctamente.")

    separador("14 — Reserva sin tema en asesoria (parametro faltante)")
    try:
        r_sin_tema = Reserva(
            clientes["c1"], servicios["asesoria"], duracion_horas=1, tema="ok"
        )
    except ErrorParametroInvalido as e:
        registrar_error("Tema demasiado corto detectado (esperado)", e)
        print(f"  Sistema continua operando correctamente.")
    except ErrorReservaInvalida as e:
        registrar_error("Reserva invalida (esperado)", e)
        print(f"  Sistema continua operando correctamente.")

    print("\n" + "=" * 60)
    print("     RESUMEN FINAL DEL SISTEMA")
    print("=" * 60)
    print(f"  Clientes registrados : {Cliente.total_clientes()}")
    print(f"  Reservas totales     : {Reserva.total_reservas()}")
    print(f"  Reservas confirmadas : {len(Reserva.reservas_por_estado('confirmada'))}")
    print(f"  Reservas canceladas  : {len(Reserva.reservas_por_estado('cancelada'))}")
    print(f"  Reservas pendientes  : {len(Reserva.reservas_por_estado('pendiente'))}")
    print(f"\n  Detalle de reservas activas:")
    for r in Reserva._reservas_registradas:
        print(f"    {r.describir()}")

    print(f"\n  Log guardado en: eventos_sistema.log")
    print("=" * 60)
    registrar_evento("Simulacion completa finalizada exitosamente.")


if __name__ == "__main__":
    main()
