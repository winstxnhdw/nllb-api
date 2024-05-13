from typing import Required, TypedDict

from server.types import ComputeTypes, Devices


class TranslatorOptions(TypedDict):
    """
    Summary
    -------
    the parameters to initialise the LLM

    Attributes
    ----------
    model_path (str) : the path to the model
    device (Devices) : the device to use
    compute_type (ComputeTypes) : the compute type
    inter_threads (int) : the number of inter-threads
    """
    model_path: Required[str]
    device: Devices
    compute_type: ComputeTypes
    inter_threads: int
