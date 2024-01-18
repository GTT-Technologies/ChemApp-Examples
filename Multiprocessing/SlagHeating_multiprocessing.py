from pathlib import Path
import numpy as np
from collections import OrderedDict

from multiprocessing import Pool
import time

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
def calculate(T: float):
    """Calculate equilibrium at a given temperature"""
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
    casc.set_IA_pc("#1", "TiO2_Rutile(s)", "TiO2_Rutile(s)", 0.001)
    casc.set_IA_pc("#1", "K2O_solid(s)", "K2O_solid(s)", 0.001)
    casc.set_IA_pc("#1", "Na2O_Solid-A(s)", "Na2O_Solid-A(s)", 0.001)
    casc.set_IA_pc("#1", "V2O5_solid(s)", "V2O5_solid(s)", 0.001)

    try:
        # calculate
        casc.calculate_eq()
        # return result
        return casc.get_result_object()
    except ChemAppError as c_err:
        print(f"[<T> = { T }] ChemApp Error {c_err.errno}:")
        print(c_err)

    # This is a 'fallthrough' return, which is only reached if the calculation
    # fails. Likely, this is not what you want.
    return None


# this is the name-main idiom, which makes sure that the code is only executed
# when the script is run directly, not when it is imported, and which allows
# multiprocessing to work
if __name__ == "__main__":
    results = OrderedDict()

    # we just aim for some amount of calculations to be done
    # using linspace allows to set the number of calculations
    number_of_calculations = 80
    T_range = np.linspace(1400.0, 1500.0, number_of_calculations)

    # Set the number of processes to use
    number_of_processes = 8

    # Set the chunksize (number of calculations per process)
    chunksize = 1

    # start the timer
    tstart = time.perf_counter()

    print(f"Using {number_of_processes} processes")

    # run the calculation, distributed on the number of processes
    with Pool(processes=number_of_processes) as p:
        results = p.map(calculate, T_range, chunksize=chunksize)

    # print the timing result
    print(f"{time.perf_counter() - tstart:.2f}s runtime")

    # continue with your work with the results
    # ...

    print("End of script.")
