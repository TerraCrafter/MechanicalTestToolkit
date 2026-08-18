import tkinter as tk
from tkinter import filedialog, messagebox
from Toolkit.Analysis.Stress_Strain import Geometry
from Toolkit.Analysis.Creep_Runner import RunCreepTest

def RunCreepGUI():
    root = tk.Tk()
    root.title("Creep Test Runner")
    root.geometry("400x250")

    # Labels
    tk.Label(root, text="Cross-sectional Area (m^2):").pack()
    area_entry = tk.Entry(root)
    area_entry.pack()

    tk.Label(root, text="Gauge Length (m):").pack()
    length_entry = tk.Entry(root)
    length_entry.pack()

    # File selection
    def SelectFile():
        file_path = filedialog.askopenfilename(
            title="Select Creep CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        file_label.config(text=file_path)

    tk.Button(root, text="Select CSV File", command=SelectFile).pack()
    file_label = tk.Label(root, text="No file selected")
    file_label.pack()

    # Run creep test
    def RunTest():
        try:
            area = float(area_entry.get())
            length = float(length_entry.get())
            path = file_label.cget("text")

            if path == "No file selected":
                messagebox.showerror("Error", "Please select a CSV file.")
                return

            geom = Geometry(area_0 = area, length_0 = length)
            output = RunCreepTest(path, geom)

            # Show plots
            figs = output["figures"]
            figs["creep_curve"].show()
            figs["creep_rate"].show()

            messagebox.showinfo("Success", "Creep test completed.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Run Creep Test", command=RunTest).pack()

    root.mainloop()

if __name__ == "__main__":
    RunCreepGUI()