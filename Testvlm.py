import aerosandbox as asb
import aerosandbox.numpy as np

# 1. Define the V-22 Style Wing (Sized for a drone)
wing = asb.Wing(
    name="V-22 Drone Wing",
    xsecs=[
        # Left Tip (Swept forward)
        asb.WingXSec(xyz_le=[-0.05, -0.5, 0], chord=0.12, airfoil=asb.Airfoil("naca23012")),
        # Root (Center)
        asb.WingXSec(xyz_le=[0, 0, 0], chord=0.20, airfoil=asb.Airfoil("naca23012")),
        # Right Tip (Swept forward)
        asb.WingXSec(xyz_le=[-0.05, 0.5, 0], chord=0.12, airfoil=asb.Airfoil("naca23012")),
    ]
)

# 2. Setup the Airplane and Flight Conditions
airplane = asb.Airplane(wings=[wing])
op_point = asb.OperatingPoint(velocity=15, alpha=3) # 15 m/s at 3 deg AoA

# 3. Run the Vortex Lattice Method (VLM)
vlm = asb.VortexLatticeMethod(airplane, op_point)
results = vlm.run()

# 4. Print the Engineering Data
print("\n--- Simulation Results ---")
print(f"Lift Coefficient (CL): {results['CL']:.4f}")
print(f"Drag Coefficient (CD): {results['CD']:.4f}")
print(f"Efficiency (L/D):      {results['CL']/results['CD']:.2f}")

# 5. Open the 3D Visualization
vlm.draw(backend="plotly")
