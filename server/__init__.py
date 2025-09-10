from os import environ as env
from subprocess import run

from granian.constants import Interfaces
from granian.server import Server

from server.app import app
from server.config import Config


def main() -> None:
    """
    Summary
    -------
    programmatically run the server with Granian
    """
    config = Config()
    granian = Server(
        f'{app.__module__}:{app.__name__}',
        address='0.0.0.0',
        port=config.server_port,
        interface=Interfaces.ASGI,
        workers=config.worker_count,
        log_access=True,
        log_access_format='[%(time)s] %(status)d "%(method)s %(path)s %(protocol)s" %(addr)s in %(dt_ms).2f ms',
        url_path_prefix=config.server_root_path,
        factory=True,
        reload=False,
    )

    granian.serve()


def stub() -> None:
    env['STUB_TRANSLATOR'] = 'True'
    env['STUB_LANGUAGE_DETECTOR'] = 'True'
    main()


def cpu() -> None:
    docker_build = ['docker', 'build', '-t', 'nllb-api', '.']
    docker_run = [
        'docker',
        'run',
        '--init',
        '--rm',
        '-e',
        'TRANSLATOR_THREADS=4',
        '-e',
        'AUTH_TOKEN=Test',
        '-p',
        '7860:7860',
        'nllb-api',
    ]

    run(docker_build, check=True)
    run(docker_run, check=True)


def gpu() -> None:
    docker_build = ['docker', 'build', '--build-arg', 'USE_CUDA=1', '-f', 'Dockerfile.build', '-t', 'nllb-api', '.']
    docker_run = [
        'docker',
        'run',
        '--init',
        '--rm',
        '--gpus',
        'all',
        '-e',
        'TRANSLATOR_THREADS=4',
        '-e',
        'AUTH_TOKEN=Test',
        '-p',
        '7860:7860',
        'nllb-api',
    ]

    run(docker_build, check=True)
    run(docker_run, check=True)


def huggingface() -> None:
    docker_build = ['docker', 'build', '-t', 'nllb-api', '.']
    docker_run = ['docker', 'run', '--init', '--rm', '-p', '7860:7860', 'nllb-api']

    run(docker_build, check=True)
    run(docker_run, check=True)


if __name__ == '__main__':
    main()
