import numpy as np
from dataclasses import dataclass
from scipy.signal import savgol_filter

@dataclass
class CreepResult:
    time: np.ndarray
    strain: np.ndarray
    strain_rate: np.ndarray
    min_creep_rate: float
    min_rate_time: float
    rupture_time: float
    rupture_strain: float
    regions: dict
    metadata: dict

def ComputeStrainRate(time, strain):
    time = np.asarray(time)
    strain = np.asarray(strain)

    dt = np.diff(time)
    de = np.diff(strain)

    rate = de / dt
    # Pad to same length as length / time
    rate = np.concatenate(([rate[0]], rate))
    return rate

def Smooth(y, window = 51, poly = 3):
    if len(y) < window:
        return y
    return savgol_filter(y, window_length = window, polyorder = poly)

def AnalyzeCreep(time, strain, stress, temperature, geom=None):
    time = np.asarray(time)
    strain = np.asarray(strain)

    # Basic validation
    if len(time) != len(strain):
        raise ValueError("Time and strain length mismatch")

    # Strain rate
    rate = ComputeStrainRate(time, strain)
    rate_smooth = Smooth(rate)

    # Minimum creep rate (secondary creepy)
    idx_min = int(np.argmin(rate_smooth))
    min_creep_rate = float(rate[idx_min])
    min_rate_time = float(time[idx_min])

    # Rupture
    rupture_time = float(time[-1])
    rupture_strain = float(strain[-1])

    # Simple region indices
    i_primary_end = max(1, idx_min // 2)
    i_secondary_end = min(len(time) - 2, idx_min + (len(time) - idx_min) // 3)

    regions = {
        "primary": (0, i_primary_end),
        "secondary": (i_primary_end, i_secondary_end),
        "tertiary": (i_secondary_end, len(time) - 1),
    }

    metadata = {
        "stress": stress,
        "temperature": temperature,
        "used_geom": geom,
        "smoothing": "Savitsky-Golay",
    }

    return CreepResult(
        time = time,
        strain = strain,
        strain_rate = rate_smooth,
        min_creep_rate = min_creep_rate,
        min_rate_time = min_rate_time,
        rupture_time = rupture_time,
        rupture_strain = rupture_strain,
        regions = regions,
        metadata = metadata,
    )