from dataclasses import dataclass, field

from src.genai.llm import HouseholdLLM, LLMResponse
from src.genai.router import Route, route_query
from src.genai.slm import SmallLanguageModel
from src.rag.retriever import HouseholdRetriever
from src.genai.data_tool import HouseholdDataTool

@dataclass
class OrchestrationResponse:
    text: str
    route: str
    model: str
    sources: list[str] = field(
        default_factory=list
    )


class Orchestrator:

    def __init__(self):
        self.slm = SmallLanguageModel()
        self.llm = HouseholdLLM()
        self.retriever = HouseholdRetriever(knowledge_dir="knowledge")
        self.data_tool = HouseholdDataTool()

    def handle(
        self,
        query: str,
    ) -> OrchestrationResponse:
        
        route = route_query(query)
        sources = []

        if route == Route.SLM:
            result = self.slm.generate(query)
        elif route == Route.DATA:
            answer = self.data_tool.answer_query(query)

            result = LLMResponse(
                text=answer,
                model="pandas-analytics-v1",
            )

            sources = [
                "data/raw/"
                "Global_Household_Financial_Dynamics.csv"
            ]

        else:
            retrieved = self.retriever.retrieve(
                query=query,
                top_k=4,
            )

            context = "\n\n".join(
                (
                    f"Source: {item['source']}\n"
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

            result = self.llm.generate(
                query=query,
                context=context,
            )

        return OrchestrationResponse(
            text=result.text,
            route=route.value,
            model=result.model,
            sources=sources
        )