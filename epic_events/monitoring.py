"""Configure application monitoring."""

import os

import sentry_sdk
from dotenv import load_dotenv


def init_sentry() -> None:
    """Initialize Sentry if DSN is configured."""

    load_dotenv()

    sentry_dsn = os.getenv("SENTRY_DSN")

    if not sentry_dsn:
        return

    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0")),
        enable_logs=True,
    )


def log_user_created(
    created_user_id: int,
    created_user_role: str,
    current_user_id: int,
) -> None:
    """Log user creation."""

    sentry_sdk.capture_message(
        (
            "Collaborateur créé | "
            f"id_user={created_user_id} | "
            f"role={created_user_role} | "
            f"created_by={current_user_id}"
        ),
        level="info",
    )


def log_user_updated(
    updated_user_id: int,
    current_user_id: int,
) -> None:
    """Log user update."""

    sentry_sdk.capture_message(
        (
            "Collaborateur modifié | "
            f"id_user={updated_user_id} | "
            f"updated_by={current_user_id}"
        ),
        level="info",
    )


def log_contract_signed(
    contract_id: int,
    current_user_id: int,
) -> None:
    """Log contract signature."""

    sentry_sdk.capture_message(
        ("Contrat signé | " f"id_contract={contract_id} | " f"signed_by={current_user_id}"),
        level="info",
    )
