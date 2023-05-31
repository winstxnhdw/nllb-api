
from pydantic import create_model_from_typeddict

from server.types import CPUSpecifications as Specifications

CPUSpecifications = create_model_from_typeddict(Specifications)  # type: ignore
