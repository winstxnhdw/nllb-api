from os import environ as env
from random import randint
from socket import AF_INET, SOCK_STREAM, socket
from subprocess import run

from server import main


def get_oci() -> str:
    return 'docker'


def get_unused_port() -> int:
    port = 7860

    with socket(AF_INET, SOCK_STREAM) as client:
        while True:
            try:
                client.bind(('0.0.0.0', port))

            except OSError:
                port = randint(7860, 7999)  # noqa: S311

            else:
                return port


def stub() -> None:
    env['STUB_TRANSLATOR'] = 'True'
    env['STUB_LANGUAGE_DETECTOR'] = 'True'
    main()


def cpu() -> None:
    oci = get_oci()
    docker_build = [oci, 'build', '-f', 'Dockerfile.build', '-t', 'nllb-api', '.']

    port = get_unused_port()
    docker_run = [
        oci,
        'run',
        '--init',
        '--rm',
        '-e',
        f'SERVER_PORT={port}',
        '-e',
        'TRANSLATOR_THREADS=4',
        '-e',
        'AUTH_TOKEN=Test',
        '-p',
        f'{port}:{port}',
        'nllb-api',
    ]

    run(docker_build, check=True)
    run(docker_run, check=True)


def gpu() -> None:
    oci = get_oci()
    docker_build = [oci, 'build', '--build-arg', 'USE_CUDA=1', '-f', 'Dockerfile.build', '-t', 'nllb-api', '.']

    port = get_unused_port()
    docker_run = [
        oci,
        'run',
        '--init',
        '--rm',
        '--gpus',
        'all',
        '-e',
        f'SERVER_PORT={port}',
        '-e',
        'TRANSLATOR_THREADS=4',
        '-e',
        'AUTH_TOKEN=Test',
        '-p',
        f'{port}:{port}',
        'nllb-api',
    ]

    run(docker_build, check=True)
    run(docker_run, check=True)


def huggingface() -> None:
    oci = get_oci()
    docker_build = [oci, 'build', '-t', 'nllb-api', '.']
    docker_run = [oci, 'run', '--init', '--rm', '-p', f'7860:{get_unused_port()}', 'nllb-api']

    run(docker_build, check=True)
    run(docker_run, check=True)
