from enum import Enum


class Route(str, Enum):
    SLM = "slm"
    RAG = "rag"
    DATA = "data"


SMALL_TALK_PHRASES = {
    "hello",
    "hi",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "how are you",
    "thanks",
    "thank you",
    "bye",
    "goodbye",
}


DATA_QUERY_HINTS = {
    "average",
    "mean",
    "median",
    "sum",
    "total",
    "count",
    "how many",
    "highest",
    "lowest",
    "maximum",
    "minimum",
    "percentage",
    "percent",
}


HOUSEHOLD_KEYWORDS = {
    "household",
    "income",
    "savings",
    "expense",
    "expenses",
    "tax",
    "taxes",
    "financial",
    "country",
    "city",
    "family",
    "earners",
    "health score",
    "financial health",
    "cluster",
    "shap",
    "anova",
}

KNOWLEDGE_QUERY_HINTS = {
    "shap",
    "anova",
    "statistical test",
    "pearson",
    "mann-whitney",
    "ols",
    "regression",
    "cluster",
    "feature importance",
    "explainability",
    "finding",
    "findings",
    "revealed",
    "showed",
}


def normalize_query(query: str) -> str:
    return " ".join(
        query.lower().strip().split()
    )


def route_query(query: str) -> Route:
    normalized = normalize_query(query)

    if normalized in SMALL_TALK_PHRASES:
        return Route.SLM

    is_knowledge_query = any(
        hint in normalized
        for hint in KNOWLEDGE_QUERY_HINTS
    )

    is_household_query = any(
        keyword in normalized
        for keyword in HOUSEHOLD_KEYWORDS
    )

    is_data_query = any(
        hint in normalized
        for hint in DATA_QUERY_HINTS
    )

    # Analytical findings / explanations should use RAG.
    if is_knowledge_query:
        return Route.RAG

    # Numeric/aggregation questions over the dataset use Pandas.
    if is_household_query and is_data_query:
        return Route.DATA

    # Other household-domain questions use RAG.
    if is_household_query:
        return Route.RAG

    return Route.SLM