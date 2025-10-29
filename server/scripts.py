from os import environ as env
from random import randint
from shutil import which
from socket import AF_INET, SOCK_STREAM, socket
from subprocess import run

from server import main


def get_oci() -> str:
    """
    Summary
    -------
    get the available OCI runtime on the host machine

    Returns
    -------
    runtime (str)
        an available OCI runtime
    """
    return next(runtime for runtime in ("docker", "podman", "nerdctl") if which(runtime))


def run_args() -> tuple[str, ...]:
    """
    Summary
    -------
    get common arguments for running an OCI container

    Returns
    -------
    args (tuple[str, ...])
        common arguments for running an OCI container
    """
    return ("run", "--init", "--rm", "--gpus", "all")


def get_unused_port() -> int:
    """
    Summary
    -------
    get an unused port on the host machine

    Returns
    -------
    port (int)
        an unused port
    """
    port = 7860

    with socket(AF_INET, SOCK_STREAM) as client:
        while True:
            try:
                client.bind(("0.0.0.0", port))

            except OSError:
                port = randint(7860, 7999)  # noqa: S311

            else:
                return port


def stub() -> None:
    """
    Summary
    -------
    run the server without downloading any models
    """
    env["STUB_TRANSLATOR"] = "True"
    env["STUB_LANGUAGE_DETECTOR"] = "True"
    main()


def cpu() -> None:
    """
    Summary
    -------
    build and run the server with CPU inference
    """
    oci = get_oci()
    docker_build = [oci, "build", "-f", "Dockerfile.build", "-t", "nllb-api", "."]

    port = get_unused_port()
    docker_run = [
        oci,
        *run_args(),
        "-e",
        f"SERVER_PORT={port}",
        "-e",
        "TRANSLATOR_THREADS=4",
        "-e",
        "AUTH_TOKEN=Test",
        "-p",
        f"{port}:{port}",
        "nllb-api",
    ]

    run(docker_build, check=True)
    run(docker_run, check=True)


def gpu() -> None:
    """
    Summary
    -------
    build and run the server with GPU inference
    """
    oci = get_oci()
    docker_build = [oci, "build", "--build-arg", "USE_CUDA=1", "-f", "Dockerfile.build", "-t", "nllb-api", "."]

    port = get_unused_port()
    docker_run = [
        oci,
        *run_args(),
        "-e",
        f"SERVER_PORT={port}",
        "-e",
        "TRANSLATOR_THREADS=4",
        "-e",
        "AUTH_TOKEN=Test",
        "-p",
        f"{port}:{port}",
        "nllb-api",
    ]

    run(docker_build, check=True)
    run(docker_run, check=True)


def huggingface() -> None:
    """
    Summary
    -------
    run the production image from the GitHub Container Registry
    """
    oci = get_oci()
    docker_build = [oci, "build", "-t", "nllb-api", "."]
    docker_run = [oci, *run_args(), "-p", f"7860:{get_unused_port()}", "nllb-api"]

    run(docker_build, check=True)
    run(docker_run, check=True)
