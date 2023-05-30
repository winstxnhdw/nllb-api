from cpufeature.extension import CPUFeature

from server.api.v1 import v1


@v1.get('/cpu', response_model=dict[str, str])
async def cpu():
    """
    Summary
    -------
    the `/cpu` route returns the CPU specifications of the machine
    """
    return CPUFeature
