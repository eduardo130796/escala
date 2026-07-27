class EscalaError(Exception):
    """Erro base do sistema."""


class SistemaBloqueadoError(EscalaError):
    pass


class DiaInvalidoError(EscalaError):
    pass


class DiaDuplicadoError(EscalaError):
    pass


class LimiteDiasError(EscalaError):
    pass


class MesInvalidoError(EscalaError):
    pass


class ServidorNaoEncontradoError(EscalaError):
    pass