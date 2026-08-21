from pathlib import Path

from huggingface_hub import snapshot_download, try_to_load_from_cache

from server.utils.has_internet_access import has_internet_access


def huggingface_download(repository: str) -> str:
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
    if isinstance(cached_file := try_to_load_from_cache(repository, "tokenizer.json"), str):
        return str(Path(cached_file).parent)

    return snapshot_download(
        repository,
        local_files_only=not has_internet_access(repository),
    )
