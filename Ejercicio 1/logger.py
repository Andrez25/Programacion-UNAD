import os
from datetime import datetime

RUTA_LOG = os.path.join(os.path.dirname(__file__), "eventos_sistema.log")


def _escribir_log(nivel, mensaje):
    marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"
    try:
        with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
    except OSError:
        pass


def registrar_info(mensaje):
    _escribir_log("INFO", mensaje)
    print(f"  INFO  | {mensaje}")


def registrar_error(mensaje, excepcion=None):
    detalle = f"{mensaje}"
    if excepcion:
        detalle += f" — {type(excepcion).__name__}: {excepcion}"
    _escribir_log("ERROR", detalle)
    print(f"  ERROR | {detalle}")


def registrar_advertencia(mensaje):
    _escribir_log("ADVERTENCIA", mensaje)
    print(f"  AVISO | {mensaje}")


def registrar_evento(mensaje):
    _escribir_log("EVENTO", mensaje)
    print(f"  EVENTO| {mensaje}")
