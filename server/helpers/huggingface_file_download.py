from huggingface_hub import hf_hub_download

from server.helpers.has_internet_access import has_internet_access


def huggingface_file_download(repository: str, file: str) -> str:
    """
    Summary
    -------
    download the huggingface model

    Parameters
    ----------
    repository (str) : the name of the Hugging Face repository

    Returns
    -------
    repository_path (str) : local path to the downloaded repository
    """
    return hf_hub_download(
        repository,
        file,
        local_files_only=not has_internet_access(repository),
    )
