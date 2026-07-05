# Programacion-UNAD
# Sistema Integral de Gestión — Software

Sistema orientado a objetos desarrollado en Python para gestionar clientes, servicios y reservas de la empresa Software FJ. No utiliza bases de datos; toda la información se maneja mediante objetos, listas y un archivo de logs.

---

## Requisitos

- Python 3.8 o superior
- No requiere librerías externas

---

## Estructura del proyecto

```
Ejercicio 1/
├── main.py            # Punto de entrada — ejecuta la simulación completa
├── entidad_base.py    # Clase abstracta base del sistema
├── cliente.py         # Clase Cliente con validaciones y encapsulación
├── servicio.py        # Clase abstracta Servicio y tres servicios especializados
├── reserva.py         # Clase Reserva con confirmación, cancelación y estados
├── excepciones.py     # Excepciones personalizadas del sistema
├── logger.py          # Registro de eventos y errores en archivo de log
└── eventos_sistema.log  # Generado automáticamente al ejecutar
```

---

## Cómo ejecutar

```bash
cd Ejercicio 1
python main.py
```

No se requiere ninguna configuración previa. El archivo `eventos_sistema.log` se crea automáticamente en la misma carpeta.

---

## Principios de POO aplicados

| Principio | Implementación |
|---|---|
| Abstracción | `EntidadBase` y `Servicio` son clases abstractas con métodos obligatorios |
| Herencia | `Cliente` hereda de `EntidadBase`; los tres servicios heredan de `Servicio` |
| Polimorfismo | Cada servicio implementa su propio cálculo de costo, descripción y validación |
| Encapsulación | Todos los atributos son privados (`_atributo`) con acceso controlado por `@property` |

---

## Servicios disponibles

- **ReservaSala** — Reserva de salas con control de capacidad y recargo por grupos grandes
- **AlquilerEquipo** — Alquiler de equipos tecnológicos con soporte para múltiples unidades
- **AsesoriaEspecializada** — Asesorías por área (software, redes, seguridad, datos, gestión) con tarifa adicional por nivel experto

---

## Manejo de excepciones

El sistema implementa manejo robusto de errores en todo momento:

- `try/except` — captura y reporta errores sin detener el programa
- `try/except/finally` — garantiza el registro del intento incluso si falla
- Encadenamiento de excepciones con `raise ... from excepcion`
- Excepciones personalizadas con códigos identificadores:

| Excepción | Código | Situación |
|---|---|---|
| `ErrorClienteInvalido` | CLI-001 | Datos de cliente incorrectos o duplicados |
| `ErrorServicioNoDisponible` | SRV-001 | Servicio desactivado |
| `ErrorParametroInvalido` | PAR-001 | Parámetro fuera de rango o tipo incorrecto |
| `ErrorReservaInvalida` | RES-001 | Reserva con datos incorrectos |
| `ErrorOperacionNoPermitida` | OPE-001 | Acción no válida según el estado actual |
| `ErrorCalculoCosto` | CAL-001 | Error en el cálculo del valor del servicio |
| `ErrorDuracionInvalida` | DUR-001 | Duración negativa, cero o mayor a 24 horas |

---

## Operaciones simuladas

El archivo `main.py` ejecuta 14 operaciones que demuestran el funcionamiento completo:

1. Registro de cliente válido
2. Registro de cliente con correo inválido (error esperado)
3. Registro de cliente con cédula duplicada (error esperado)
4. Registro de segundo cliente válido
5. Creación de los tres servicios
6. Creación de servicio con tipo de equipo inválido (error esperado)
7. Reserva de sala con IVA incluido
8. Reserva excediendo la capacidad de la sala (error esperado)
9. Reserva de asesoría con descuento del 15%
10. Intento de confirmar una reserva ya confirmada (error esperado)
11. Reserva sobre servicio desactivado (error esperado)
12. Reserva de equipo, confirmación y cancelación justificada
13. Reserva con duración inválida (error esperado)
14. Reserva de asesoría con tema demasiado corto (error esperado)

---

## Registro de eventos

Cada operación queda registrada en `eventos_sistema.log` con marca de tiempo, nivel y detalle del evento. El sistema nunca se detiene ante errores; los captura, los registra y continúa ejecutando.


Sergio Andrez Rueda Soto