from dataclasses import dataclass
from time import perf_counter


@dataclass
class RequestMetrics:
    route: str
    model: str
    latency_ms: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost: float | None = None


class Timer:

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        self.elapsed_ms = (
            perf_counter() - self.start
        ) * 1000