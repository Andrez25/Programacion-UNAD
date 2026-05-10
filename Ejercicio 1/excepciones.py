class ErrorSistema(Exception):
    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        if self.codigo:
            return f"[Error {self.codigo}] {self.mensaje}"
        return self.mensaje


class ErrorClienteInvalido(ErrorSistema):
    def __init__(self, mensaje, campo=None):
        super().__init__(mensaje, codigo="CLI-001")
        self.campo = campo


class ErrorServicioNoDisponible(ErrorSistema):
    def __init__(self, nombre_servicio):
        super().__init__(
            f"El servicio '{nombre_servicio}' no está disponible.", codigo="SRV-001"
        )
        self.nombre_servicio = nombre_servicio


class ErrorParametroInvalido(ErrorSistema):
    def __init__(self, parametro, valor):
        super().__init__(
            f"Parámetro inválido: '{parametro}' = {valor!r}", codigo="PAR-001"
        )
        self.parametro = parametro
        self.valor = valor


class ErrorReservaInvalida(ErrorSistema):
    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="RES-001")


class ErrorOperacionNoPermitida(ErrorSistema):
    def __init__(self, operacion, razon):
        super().__init__(
            f"Operación '{operacion}' no permitida: {razon}", codigo="OPE-001"
        )
        self.operacion = operacion


class ErrorCalculoCosto(ErrorSistema):
    def __init__(self, mensaje):
        super().__init__(mensaje, codigo="CAL-001")


class ErrorDuracionInvalida(ErrorSistema):
    def __init__(self, duracion):
        super().__init__(
            f"Duración inválida: {duracion!r}. Debe ser un número positivo.",
            codigo="DUR-001",
        )
        self.duracion = duracion
