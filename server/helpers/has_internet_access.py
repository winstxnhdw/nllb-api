from http.client import HTTPConnection


def has_internet_access(repository: str) -> bool:
    """
    Summary
    -------
    check if the server has internet access

    Parameters
    ----------
    repository (str) : the name of the Hugging Face repository

    Returns
    -------
    has_internet_access (bool) : whether there is relevant internet connection
    """
    connection = HTTPConnection('huggingface.co', timeout=1)

    try:
        connection.request('HEAD', f'/{repository}')
        return True

    except (TimeoutError, OSError):
        return False

    finally:
        connection.close()
