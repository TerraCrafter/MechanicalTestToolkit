from Toolkit.Ingestion.Creep_Ingestion import IngestCreepFile
from Toolkit.Analysis.Creep import AnalyzeCreep
from Toolkit.Plotting.Creep_Plotter import CreepPlotter

def RunCreepTest(path, geometry, style="lab", make_plots=True):

    # Step 1: Ingest raw data
    raw = IngestCreepFile(path, geometry)

    # Step 2: Analyze creep behavior
    result = AnalyzeCreep(
        time=raw["time"],
        strain=raw["strain"],
        stress=raw["stress"],
        temperature=raw["temperature"],
        geom=geometry
    )

    # Step 3: Plotting
    figs = {}
    if make_plots:
        plotter = CreepPlotter(style=style)
        fig_curve, ax_curve = plotter.plot_creep_curve(result)
        fig_rate, ax_rate = plotter.plot_creep_rate(result)

        figs["creep_curve"] = fig_curve
        figs["creep_rate"] = fig_rate

    # Step 4: Return everything
    return {
        "raw": raw,
        "analysis": result,
        "figures": figs
    }
