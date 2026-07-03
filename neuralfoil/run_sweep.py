import sys
import os
import numpy as np
import neuralfoil as nf
import aerosandbox as asb

def main():
    task_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0

    thickness = 6 + (task_id * 2)
    airfoil_name = f"naca24{thickness:02d}"
    print(f"--> Processing airfoil geometry: {airfoil_name}")

    airfoil = asb.Airfoil(airfoil_name)
    alpha_range = np.linspace(-6, 16, 45)
    reynolds = 5e5

    aero = nf.get_aero_from_airfoil(
        airfoil=airfoil,
        alpha=alpha_range,
        Re=reynolds
    )

    output_dir = "./results_data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{airfoil_name}_data.npz")
    np.savez(output_path, alpha=alpha_range, cl=aero["CL"], cd=aero["CD"], cm=aero["CM"])
    print(f"--> Saved to: {output_path}")

if __name__ == "__main__":
    main()
