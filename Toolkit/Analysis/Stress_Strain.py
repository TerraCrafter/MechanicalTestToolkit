import numpy as np
from dataclasses import dataclass
from scipy.signal import savgol_filter

@dataclass
class Geometry:
    area_0: float # m^2
    length_0: float # m

@dataclass
class StressStrainResult:
    strain: np.ndarray
    stress: np.ndarray
    true_strain: np.ndarray
    true_stress: np.ndarray
    E: float
    yield_strength: float
    uts: float(stress_smooth.max())
    elongation_pct: float
    metadata: dict

def ValidateInputs(load, disp, strain_ext):
    load = np.asarray(load)
    disp = np.asarray(disp)

    if strain_ext is not None:
        strain_ext = np.asarray(strain_ext)
        if len(strain_ext) != len(load):
            raise ValueError("Extensometer strain length mismatch.")

    if len(load) != len(disp):
        raise ValueError("Load and displacement length mismatch.")

    return load, disp, strain_ext

def ComputeStrain(disp, geom, strain_ext):
    if strain_ext is not None:
        return strain_ext
    return disp / geom.length_0

def ComputeStress(load, geom):
     return load / geom.area_0

def SmoothCurve(y, window = 51, poly = 3):
    if len(y) < window:
        return y
    return savgol_filter(y, window_length = window, polyorder = poly)

def EstimateModulus(strain, stress):
    # Automatically detect linear region using small-strain window
    mask = strain <= 0.0025
    eps = strain[mask]
    sig = stress[mask]

    # Smooth stress for better regression
    sig_smooth = SmoothCurve(sig)

    # Linear regression
    eps_mean = eps.mean()
    sig_mean = sig_smooth.mean()
    num = np.sum((eps - eps_mean) * (sig_smooth - sig_mean))
    den = np.sum((eps  - eps_mean)**2)

    return num / den

def FindOffsetYield(strain, stress, E, offset = 0.002):
    sigma_offset = E * (strain - offset)
    diff = stress - sigma_offset

    for i in range(len(diff) - 1):
        if diff[i] * diff[i + 1] < 0:
            # Interpolate intersection
            s1, s2 = stress[i], stress[i + 1]
            d1, d2 = diff[i], diff[i + 1]
            frac = abs(d1) / (abs(d1) + abs(d2))
            return s1 + frac * (s2 - s1)

    return np.nan

def AnalyzeStressStrain(load,disp,geom: Geometry, strain_ext=None):
    load, disp, strain_ext = ValidateInputs(load, disp, strain_ext)

    strain = ComputeStrain(disp, geom, strain_ext)
    stress = ComputeStress(load, geom)

    # Smooth stress for better feature detection
    stress_smooth = SmoothCurve(stress)

    # True values
    true_strain = np.log(1 + strain)
    true_stress = stress * (1 + strain)

    # Material properties
    E = EstimateModulus(strain, stress_smooth)
    ys = FindOffsetYield(strain, stress_smooth, E)
    elongation_pct = float(strain[-1] * 100.0)

    metadata = {
    "area_0": geom.area_0,
    "length_0": geom.length_0,
    "used_extensometer": strain_ext is not None,
    "smoothing": "Savitzky-Golay",
    "offset_method": "0.2%"
    }

    return StressStrainResult(
        strain = strain,
         stress = stress_smooth,
        true_strain = true_strain,
        true_stress = true_stress,
         E = E,
         yield_strength = ys,
         elongation_pct = elongation_pct,
         metadata = metadata,
    )