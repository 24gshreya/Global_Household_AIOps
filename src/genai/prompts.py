from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REGISTRY_PATH = PROJECT_ROOT / "prompts" / "registry.yaml"


def load_prompt(
    prompt_name: str,
    version: str | None = None,
) -> tuple[str, str]:
    """
    Load a versioned prompt.

    Returns:
        prompt_text,
        resolved_version
    """

    with open(
        REGISTRY_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        registry = yaml.safe_load(file)

    prompt_config = registry["prompts"][prompt_name]

    resolved_version = (
        version
        or prompt_config["production"]
    )

    relative_path = prompt_config["versions"][
        resolved_version
    ]

    prompt_path = PROJECT_ROOT / relative_path

    prompt_text = prompt_path.read_text(
        encoding="utf-8"
    )

    return (
        prompt_text,
        resolved_version,
    )