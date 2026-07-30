from dataclasses import asdict, dataclass


@dataclass(slots=True)
class ResultadoProcessamento:
    arquivo_original: str
    arquivo_final: str | None = None
    numero_nf: str | None = None
    status: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
