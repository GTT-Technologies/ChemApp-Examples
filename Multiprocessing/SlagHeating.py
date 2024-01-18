from pathlib import Path
import numpy as np
from collections import OrderedDict

from multiprocessing import Pool, freeze_support
import functools
import time
import os

from chemapp.friendly import (
    StreamCalculation as casc,
    ThermochemicalSystem as cats,
    Units as cau,
    TemperatureUnit,
    PressureUnit,
    VolumeUnit,
    AmountUnit,
    EnergyUnit,
)
from chemapp.core import (
    ChemAppError,
)


def calculate(T: float):
    """Calculate equilibrium at a given temperature"""
    # > Load data file
    cst_file = Path("SlagHeating.cst")
    # load the database file
    cats.load(cst_file)

    # Units setup
    cau.set(
        T=TemperatureUnit.C,
        P=PressureUnit.atm,
        V=VolumeUnit.dm3,
        A=AmountUnit.gram,
        E=EnergyUnit.J,
    )

    # Calculation
    # print(f"Process {os.getpid():>6d}: calculating at T =", T)

    # Fixed conditions
    casc.set_eq_P(1.0)

    # Stream setup
    casc.create_st(name="#1", T=25, P=1)

    # Set incoming amounts
    casc.set_IA_pc("#1", "Al2O3_gamma(s)", "Al2O3_gamma(s)", 15.0)
    casc.set_IA_pc("#1", "CaO_Lime(s)", "CaO_Lime(s)", 33.0)
    casc.set_IA_pc("#1", "MgO_periclase(s)", "MgO_periclase(s)", 15.0)
    casc.set_IA_pc("#1", "SiO2_Quartz(l)(s)", "SiO2_Quartz(l)(s)", 37.0)
    casc.set_IA_pc("#1", "FeO_Wustite(s)", "FeO_Wustite(s)", 0.001)
    casc.set_IA_pc("#1", "Fe2O3_hematite(s)", "Fe2O3_hematite(s)", 0.001)
    casc.set_IA_pc("#1", "Cr2O3_solid(s)", "Cr2O3_solid(s)", 0.001)
    casc.set_IA_pc("#1", "MnO_solid(s)", "MnO_solid(s)", 0.001)
    # casc.set_IA_pc("#1", "TiO2_Rutile(s)", "TiO2_Rutile(s)", 0.001)
    # casc.set_IA_pc("#1", "K2O_solid(s)", "K2O_solid(s)", 0.001)
    # casc.set_IA_pc("#1", "Na2O_Solid-A(s)", "Na2O_Solid-A(s)", 0.001)
    # casc.set_IA_pc("#1", "V2O5_solid(s)", "V2O5_solid(s)", 0.001)
    # casc.set_IA_pc("#1", "NiO_solid(s)", "NiO_solid(s)", 0.001)
    # casc.set_IA_pc("#1", "Cu2O_solid(s)", "Cu2O_solid(s)", 0.001)
    # casc.set_IA_pc("#1", "Ni3S2_Solid_I(s)", "Ni3S2_Solid_I(s)", 0.001)
    # casc.set_IA_pc("#1", "Cu2S_Chalcocite(s)", "Cu2S_Chalcocite(s)", 0.001)
    # casc.set_IA_pc("#1", "FeS_solid(s)", "FeS_solid(s)", 0.001)
    # casc.set_IA_pc("#1", "S_alpha_orthorhombic_(s)", "S_alpha_orthorhombic_(s)", 0.001)

    try:
        # calculate
        casc.calculate_eq()
        # return result
        return casc.get_result_object()
    except ChemAppError as c_err:
        print(f"[<T> = { T }] ChemApp Error {c_err.errno}:")
        print(c_err)

    return None


if __name__ == "__main__":
    freeze_support()
    results = OrderedDict()
    # > Variable conditions
    T_range = np.linspace(1400.0, 1500.0, 256)

    # Multiprocessing setup
    N_PROC_MAX = int(os.getenv("CAX_NPROC_MAX", 1))

    # generate the number of processes to use
    lof_proc = [2**k for k in range(0, N_PROC_MAX + 1)]

    times = []
    i = 0
    # for i in range(5):
    #     print(f"Run {i}")
    for chunksize in [1, 8, 16, 32]:
        print("Starting calculations...")
        # for n_proc in reversed([1, 2, 4, 8, 16, 32, 48]):
        tthread = time.thread_time_ns()
        for n_proc in reversed([16]):
            tthread2 = time.thread_time_ns()
            # start the timer

            print(f"Run {i}: Using {n_proc} processes, {chunksize} items per process.")

            # run the calculation, distributed on the number of processes
            with Pool(n_proc) as p:
                results = p.map(calculate, T_range, chunksize=10)
            # print_with_timediff(tthread, "End of the Python script.")
            print(times)
            times.append((n_proc, chunksize, (time.thread_time_ns() - tthread2) / 1e9))
        times.append((n_proc, chunksize, (time.thread_time_ns() - tthread) / 1e9))

    print(times)
    print("Finished.")
