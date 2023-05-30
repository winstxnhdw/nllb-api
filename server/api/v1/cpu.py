from cpufeature.extension import CPUFeature

from server.api.v1 import v1
from server.schemas.v1 import CPUSpecifications


@v1.get('/cpu', response_model=CPUSpecifications)
async def cpu():
    """
    Summary
    -------
    the `/cpu` route returns the CPU specifications of the machine
    """
    return CPUFeature
