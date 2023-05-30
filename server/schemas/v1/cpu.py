from pydantic import BaseModel, Field


class CPUSpecifications(BaseModel):
    """
    Summary
    -------

    Attributes
    ----------
    VendorId (str) : the CPU vendor ID
    num_virtual_cores (int) : the number of virtual cores
    num_physical_cores (int) : the number of physical cores
    num_threads_per_core (int) : the number of threads per core
    num_cpus (int) : the number of CPUs
    cache_line_size (int) : the cache line size
    cache_L1_size (int) : the L1 cache size
    cache_L2_size (int) : the L2 cache size
    cache_L3_size (int) : the L3 cache size
    OS_x64 (bool) : whether the OS is 64-bit
    OS_AVX (bool) : whether the OS supports AVX instructions
    OS_AVX512 (bool) : whether the OS supports AVX-512 instructions
    MMX (bool) : whether the CPU supports MMX instructions
    x64 (bool) : whether the CPU is 64-bit
    ABM (bool) : whether the CPU supports ABM instructions
    RDRAND (bool) : whether the CPU supports RDRAND instructions
    BMI1 (bool) : whether the CPU supports BMI1 instructions
    BMI2 (bool) : whether the CPU supports BMI2 instructions
    ADX (bool) : whether the CPU supports ADX instructions
    PREFETCHWT1 (bool) : whether the CPU supports PREFETCHWT1 instructions
    MPX (bool) : whether the CPU supports MPX instructions
    SSE (bool) : whether the CPU supports SSE instructions
    SSE2 (bool) : whether the CPU supports SSE2 instructions
    SSE3 (bool) : whether the CPU supports SSE3 instructions
    SSSE3 (bool) : whether the CPU supports SSSE3 instructions
    SSE41 (bool) : whether the CPU supports SSE4.1 instructions
    SSE42 (bool) : whether the CPU supports SSE4.2 instructions
    SSE4a (bool) : whether the CPU supports SSE4.a instructions
    AES (bool) : whether the CPU supports AES instructions
    SHA (bool) : whether the CPU supports SHA instructions
    AVX (bool) : whether the CPU supports AVX instructions
    XOP (bool) : whether the CPU supports XOP instructions
    FMA3 (bool) : whether the CPU supports FMA3
    FMA4 (bool) : whether the CPU supports FMA4
    AVX2 (bool) : whether the CPU supports AVX2
    AVX512f (bool) : whether the CPU supports AVX-512F
    AVX512cd (bool) : whether the CPU supports AVX-512CD
    AVX512pf (bool) : whether the CPU supports AVX-512PF
    AVX512er (bool) : whether the CPU supports AVX-512ER
    AVX512vl (bool) : whether the CPU supports AVX-512VL
    AVX512bw (bool) : whether the CPU supports AVX-512BW
    AVX512dq (bool) : whether the CPU supports AVX-512DQ
    AVX512ifma (bool) : whether the CPU supports AVX-512IFMA
    AVX512vbmi (bool) : whether the CPU supports AVX-512VBMI
    AVX512vbmi2 (bool) : whether the CPU supports AVX-512VBMI2
    """
    VendorId: str
    num_virtual_cores: int
    num_physical_cores: int
    num_threads_per_core: int
    num_cpus: int
    cache_line_size: int
    cache_L1_size: int
    cache_L2_size: int
    cache_L3_size: int
    OS_x64: bool
    OS_AVX: bool
    OS_AVX512: bool
    MMX: bool
    x64: bool
    ABM: bool
    RDRAND: bool
    BMI1: bool
    BMI2: bool
    ADX: bool
    PREFETCHWT1: bool
    MPX: bool
    SSE: bool
    SSE2: bool
    SSE3: bool
    SSSE3: bool
    SSE4_1: bool = Field(alias='SSE4.1')
    SSE4_2: bool = Field(alias='SSE4.2')
    SSE4_a: bool = Field(alias='SSE4.a')
    AES: bool
    SHA: bool
    AVX: bool
    XOP: bool
    FMA3: bool
    FMA4: bool
    AVX2: bool
    AVX512f: bool
    AVX512pf: bool
    AVX512er: bool
    AVX512cd: bool
    AVX512vl: bool
    AVX512bw: bool
    AVX512dq: bool
    AVX512ifma: bool
    AVX512vbmi: bool
    AVX512vbmi2: bool
    AVX512vnni: bool
