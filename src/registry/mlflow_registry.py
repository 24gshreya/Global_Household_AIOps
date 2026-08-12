from mlflow import MlflowClient


CHAMPION_ALIAS = "champion"


def promote_to_champion(
    model_name: str,
    model_version: str,
) -> None:
    """
    Assign the champion alias to an approved
    registered model version.
    """

    client = MlflowClient()

    client.set_registered_model_alias(
        name=model_name,
        alias=CHAMPION_ALIAS,
        version=model_version,
    )


def get_champion_version(
    model_name: str,
):
    """
    Return the model version currently assigned
    to the champion alias.
    """

    client = MlflowClient()

    return client.get_model_version_by_alias(
        name=model_name,
        alias=CHAMPION_ALIAS,
    )
