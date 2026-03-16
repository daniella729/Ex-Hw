import logging
import os
from abc import ABC, abstractmethod
from enum import Enum

from dotenv import load_dotenv


class RunMode(Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


MODE_ENV_VAR = "SCHOOL_MODE"
_PARENT_DIR = ".."
DEFAULT_DOTENV_PATH = os.path.join(os.path.dirname(__file__), _PARENT_DIR, ".env")
TEST_DOTENV_PATH = os.path.join(os.path.dirname(__file__), _PARENT_DIR, ".env.test")
DEFAULT_LOGGER = logging.getLogger(__name__)


class SecretNotFoundException(Exception):
    """Raised when a requested secret is not found in the environment."""


class BaseSecretsAccessor(ABC):

    @classmethod
    def get_app_mode(cls) -> str:
        mode = os.getenv(MODE_ENV_VAR, RunMode.DEV.value)
        return mode

    @abstractmethod
    def get_secret(self, secret_name: str) -> str: ...


class DotEnvSecretsAccessor(BaseSecretsAccessor):
    def __init__(
        self,
        logger: logging.Logger = DEFAULT_LOGGER,
    ) -> None:
        self._dotenv_path = self._get_dotenv_path()
        self._logger = logger
        self._logger.info("Loading secrets from %s", self._dotenv_path)
        load_dotenv(dotenv_path=self._dotenv_path)

    def get_secret(self, secret_name: str) -> str:
        secret_value = os.getenv(secret_name)
        if not secret_value:
            raise SecretNotFoundException(f"Secret {secret_name} not found")
        return secret_value

    def _get_dotenv_path(self) -> str:
        mode = self.get_app_mode()
        if mode == RunMode.TEST.value:
            return TEST_DOTENV_PATH
        return DEFAULT_DOTENV_PATH


def get_secrets_accessor() -> BaseSecretsAccessor:
    return DotEnvSecretsAccessor(logger=DEFAULT_LOGGER)
