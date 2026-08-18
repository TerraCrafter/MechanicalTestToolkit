import matplotlib.pyplot as plt

class CreepPlotter:
    def __init__(self, style = "lab"):
        self.style = style
        self.apply_style()

    def apply_style(self):
        if self.style == "lab":
            plt.style.use("seaborn-v0_8")

        elif self.style == "publication":
            plt.style.use("ggplot")

        elif self.style == "dark":
            plt.style.use("dark_background")

    def plot_creep_curve(self, result):
        fig, ax = plt.subplots(figsize=(9, 6))

        # Base curve
        ax.plot(result.time, result.strain,
                label = "Creep Strain",
                linewidth = 2)

        # Region shading
        p0, p1 = result.regions["primary"]
        s0, s1 = result.regions["secondary"]
        t0, t1 = result.regions["tertiary"]

        ax.axvspan(result.time[p0], result.time[p1],
                   alpha = 0.2, color = "blue", label = "Primary")
        ax.axvspan(result.time[s0], result.time[s1],
                   alpha = 0.2, color = "green", label = "Secondary")
        ax.axvspan(result.time[t0], result.time[t1],
                   alpha = 0.2, color = "red", label = "Tertiary")

        # Minimum creep rate marker
        ax.scatter(result.min_rate_time,
                   result.strain[result.time == result.min_rate_time],
                   color = "black", s = 60, label = "Min Creep Rate")

        # Rupture marker
        ax.scatter(result.rupture_time,
                   result.rupture_strain,
                   color = "purple", s = 60, label = "Rupture")

        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("Creep Stress (mm / mm)")
        ax.set_title("Creep Curve")
        ax.legend()
        ax.grid(True)

        return fig, ax

    def plot_creep_rate(self, result):
        fig, ax = plt.subplots(figsize=(9, 6))

        ax.plot(result.time, result.strain_rate,
                label = "Creep Strain Rate",
                linewidth = 2)

        # Minimum creep rate marker
        ax.scatter(result.min_rate_time,
                   result.min_creep_rate,
                   color = "black", s = 60, label = "Min Creep Rate")

        ax.set_xlabel("Time (hours)")
        ax.set_ylabel("Strain Rate (1 / hr)")
        ax.set_title("Creep Strain Rate Curve")
        ax.legend()
        ax.grid(True)

        return fig, ax