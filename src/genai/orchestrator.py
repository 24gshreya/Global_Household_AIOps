from dataclasses import dataclass, field
from time import perf_counter

from src.genai.data_tool import HouseholdDataTool
from src.genai.llm import HouseholdLLM, LLMResponse
from src.genai.router import Route, route_query
from src.genai.slm import SmallLanguageModel
from src.observability.telemetry import get_tracer
from src.rag.retriever import HouseholdRetriever


tracer = get_tracer(__name__)


@dataclass
class OrchestrationResponse:
    text: str
    route: str
    model: str
    sources: list[str] = field(
        default_factory=list
    )


class Orchestrator:
    """Route user requests to SLM, RAG, or data analytics."""

    def __init__(self):
        # Lazy-load the local SLM only when a small-talk
        # request actually needs it.
        self.slm: SmallLanguageModel | None = None

        self.llm = HouseholdLLM()

        self.retriever = HouseholdRetriever(
            knowledge_dir="knowledge"
        )

        self.data_tool = HouseholdDataTool()

    def get_slm(self) -> SmallLanguageModel:
        """Create the local SLM client only when required."""

        if self.slm is None:
            self.slm = SmallLanguageModel()

        return self.slm

    def handle(
        self,
        query: str,
    ) -> OrchestrationResponse:
        """Route and process a user query."""

        start = perf_counter()

        with tracer.start_as_current_span(
            "orchestrator.handle"
        ) as span:

            route = route_query(query)

            span.set_attribute(
                "ai.route",
                route.value,
            )

            sources: list[str] = []

            # ---------------------------------
            # SLM route
            # ---------------------------------
            if route == Route.SLM:

                with tracer.start_as_current_span(
                    "slm.generate"
                ) as slm_span:

                    result = (
                        self.get_slm()
                        .generate(query)
                    )

                    slm_span.set_attribute(
                        "genai.model",
                        result.model,
                    )

            # ---------------------------------
            # DATA route
            # ---------------------------------
            elif route == Route.DATA:

                with tracer.start_as_current_span(
                    "data_tool.query"
                ):

                    answer = (
                        self.data_tool
                        .answer_query(query)
                    )

                result = LLMResponse(
                    text=answer,
                    model="pandas-analytics-v1",
                )

                sources = [
                    (
                        "data/raw/"
                        "Global_Household_"
                        "Financial_Dynamics.csv"
                    )
                ]

            # ---------------------------------
            # RAG route
            # ---------------------------------
            else:

                with tracer.start_as_current_span(
                    "rag.retrieve"
                ) as rag_span:

                    retrieved = (
                        self.retriever.retrieve(
                            query=query,
                            top_k=4,
                        )
                    )

                    rag_span.set_attribute(
                        "rag.top_k",
                        4,
                    )

                    rag_span.set_attribute(
                        "rag.result_count",
                        len(retrieved),
                    )

                context = "\n\n".join(
                    (
                        f"Source: "
                        f"{item['source']}\n"
                        f"{item['text']}"
                    )
                    for item in retrieved
                )

                sources = list(
                    dict.fromkeys(
                        item["source"]
                        for item in retrieved
                    )
                )

                with tracer.start_as_current_span(
                    "llm.generate"
                ) as llm_span:

                    result = self.llm.generate(
                        query=query,
                        context=context,
                    )

                    llm_span.set_attribute(
                        "genai.model",
                        result.model,
                    )

                    if (
                        result.input_tokens
                        is not None
                    ):
                        llm_span.set_attribute(
                            "genai.input_tokens",
                            result.input_tokens,
                        )

                    if (
                        result.output_tokens
                        is not None
                    ):
                        llm_span.set_attribute(
                            "genai.output_tokens",
                            result.output_tokens,
                        )

                    if (
                        result.prompt_version
                        is not None
                    ):
                        llm_span.set_attribute(
                            "genai.prompt_version",
                            result.prompt_version,
                        )

            # ---------------------------------
            # Common telemetry
            # ---------------------------------
            latency_ms = (
                perf_counter() - start
            ) * 1000

            span.set_attribute(
                "ai.model",
                result.model,
            )

            span.set_attribute(
                "ai.source_count",
                len(sources),
            )

            span.set_attribute(
                "ai.latency_ms",
                latency_ms,
            )

            return OrchestrationResponse(
                text=result.text,
                route=route.value,
                model=result.model,
                sources=sources,
            )