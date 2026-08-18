import numpy as np
import pandas as pd

def NormalizeColumns(df):
    colmap = {
        "Time": "time",
        "ElapsedTime": "time",
        "t": "time",
        "Strain": "strain",
        "Extension": "extension",
        "Disp": "extension",
        "Stress": "stress",
        "Load": "load",
        "Temp": "temperature",
        "Temperature": "temperature",
    }

    new_cols = {}
    for c in df.columns:
        key = c.strip()
        if key in colmap:
            new_cols[c] = colmap[key]
        else:
            new_cols[c] = key.lower()

    return df.rename(columns=new_cols)

def CleanTime(time):
    time = np.asarray(time, dtype=float)

    # Remove duplicates
    _, idx = np.unique(time, return_index=True)
    time = time[np.sort(idx)]

    # Convert seconds → hours if needed
    if time.max() > 10000:  # heuristic
        time = time / 3600.0

    return time

def ComputeStrain(df, geom):
    if "strain" in df.columns:
        return df["strain"].to_numpy()

    if "extension" in df.columns:
        return df["extension"].to_numpy() / geom.length_0

    raise ValueError("No strain or extension column found.")

def IngestCreepFile(path, geom):
    df = pd.read_csv(path)
    df = NormalizeColumns(df)

    time = CleanTime(df["time"])
    strain = ComputeStrain(df, geom)

    # Stress: constant for creep
    if "stress" in df.columns:
        stress = float(df["stress"].iloc[0])
    elif "load" in df.columns:
        stress = float(df["load"].iloc[0] / geom.area_0)
    else:
        raise ValueError("No stress or load column found.")

    # Temperature
    if "temperature" in df.columns:
        temperature = float(df["temperature"].mean())
    else:
        temperature = np.nan

    metadata = {
        "raw_file": path,
        "specimen_id": df.get("specimen_id", None),
        "operator": df.get("operator", None),
        "machine": df.get("machine", None),
    }

    return {
        "time": time,
        "strain": strain,
        "stress": stress,
        "temperature": temperature,
        "metadata": metadata,
    }
