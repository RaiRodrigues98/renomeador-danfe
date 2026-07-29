"""
Controle das estatísticas do processamento.
"""

from dataclasses import dataclass
from time import perf_counter


@dataclass(slots=True)
class Estatisticas:

    total_arquivos: int = 0
    processados: int = 0
    sucessos: int = 0
    erros: int = 0
    nao_encontrados: int = 0

    inicio: float = 0.0
    fim: float = 0.0

    def iniciar(self):
        self.inicio = perf_counter()

    def finalizar(self):
        self.fim = perf_counter()

    @property
    def tempo_total(self) -> float:

        if self.inicio == 0:
            return 0.0

        if self.fim == 0:
            return round(perf_counter() - self.inicio, 2)

        return round(self.fim - self.inicio, 2)

    @property
    def percentual_sucesso(self) -> float:

        if self.total_arquivos == 0:
            return 0.0

        return round(
            (self.sucessos / self.total_arquivos) * 100,
            1
        )

    def resumo(self) -> dict:

        return {
            "total": self.total_arquivos,
            "processados": self.processados,
            "sucessos": self.sucessos,
            "erros": self.erros,
            "nao_encontrados": self.nao_encontrados,
            "percentual_sucesso": self.percentual_sucesso,
            "tempo": self.tempo_total,
        }