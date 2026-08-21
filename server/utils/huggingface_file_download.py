from huggingface_hub import hf_hub_download, try_to_load_from_cache

from server.utils.has_internet_access import has_internet_access


def huggingface_file_download(repository: str, file: str) -> str:
    """
    Summary
    -------
    download a file from the huggingface hub

    Parameters
    ----------
    repository (str) : the name of the Hugging Face repository
    file (str) : the name of the file to download

    Returns
    -------
    file_path (str) : local path to the downloaded file
    """
    if isinstance(cached_file := try_to_load_from_cache(repository, file), str):
        return cached_file

    return hf_hub_download(
        repository,
        file,
        local_files_only=not has_internet_access(repository),
    )
