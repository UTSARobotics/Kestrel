import aerosandbox as asb
import aerosandbox.numpy as np

# ==========================================
# 2026 F1 ACTIVE AERO TOGGLE
# ==========================================
# Change this to "Straight Mode" to open the flaps and reduce drag
aero_mode = "Corner Mode" 

if aero_mode == "Corner Mode":
    front_flap_angle = -12.0 # Steep angle for max front grip
    rear_flap_angle = -15.0  # Steep angle for max rear grip
else: # "Straight Mode"
    front_flap_angle = -2.0  # Flap opens up to shed drag
    rear_flap_angle = -2.0   # DRS fully open

# ==========================================
# 1. 2026 FRONT WING (Simplified, Active)
# Span: ~1.9m (Narrower for 2026)
# ==========================================
front_mainplane = asb.Wing(
    name="2026 Front Wing Mainplane",
    symmetric=True,
    xsecs=[
        # Root (Center of car)
        asb.WingXSec(
            xyz_le=[0.0, 0.0, 0.05], 
            chord=0.35, 
            twist=-4.0, 
            airfoil=asb.Airfoil("naca6412")
        ),
        # Tip (Near the endplate)
        asb.WingXSec(
            xyz_le=[0.10, 0.95, 0.10], # 1.9m total span
            chord=0.25, 
            twist=-2.0, 
            airfoil=asb.Airfoil("naca4412")
        )
    ]
)

front_flap = asb.Wing(
    name="2026 Active Front Flap",
    symmetric=True,
    xsecs=[
        # Flap Root 
        asb.WingXSec(
            xyz_le=[0.33, 0.0, 0.12], 
            chord=0.18, 
            twist=front_flap_angle, # Dynamically controlled by Aero Mode
            airfoil=asb.Airfoil("naca4412")
        ),
        # Flap Tip
        asb.WingXSec(
            xyz_le=[0.33, 0.95, 0.15], 
            chord=0.15, 
            twist=front_flap_angle, 
            airfoil=asb.Airfoil("naca4412")
        )
    ]
)

# ==========================================
# 2. 2026 REAR WING (Active, No Beam Wing)
# Span: ~1.0m 
# ==========================================
rear_mainplane = asb.Wing(
    name="2026 Rear Wing Mainplane",
    symmetric=True,
    xsecs=[
        # Root (Center)
        asb.WingXSec(
            xyz_le=[3.3, 0.0, 0.85], # Sitting high at the back of the car
            chord=0.25, 
            twist=-8.0, 
            airfoil=asb.Airfoil("naca8412") # Aggressive camber
        ),
        # Tip
        asb.WingXSec(
            xyz_le=[3.3, 0.5, 0.90], 
            chord=0.20, 
            twist=-4.0, 
            airfoil=asb.Airfoil("naca4412")
        )
    ]
)

rear_flap = asb.Wing(
    name="2026 Active Rear Flap (DRS)",
    symmetric=True,
    xsecs=[
        # Root
        asb.WingXSec(
            xyz_le=[3.53, 0.0, 0.95], 
            chord=0.18, 
            twist=rear_flap_angle, # Dynamically controlled by Aero Mode
            airfoil=asb.Airfoil("naca4412")
        ),
        # Tip
        asb.WingXSec(
            xyz_le=[3.51, 0.5, 0.98], 
            chord=0.15, 
            twist=rear_flap_angle, 
            airfoil=asb.Airfoil("naca4412")
        )
    ]
)

# Assemble the 2026 car (Notice we leave out the banned Beam Wing)
f1_2026_car = asb.Airplane(
    name=f"F1 2026 Concept ({aero_mode})",
    wings=[front_mainplane, front_flap, rear_mainplane, rear_flap]
)

# ==========================================
# 3. HIGH-FIDELITY SOLVER SETUP
# ==========================================
# Testing at 80 m/s (approx 288 km/h or 180 mph)
op_point = asb.OperatingPoint(
    atmosphere=asb.Atmosphere(altitude=0), # Altitude in meters (0 = sea level)
    velocity=80.0,
    alpha=0.0 
)

# SOLVER A: Vortex Lattice Method (3D Downforce, Induced Drag, Wake Roll-up)
vlm = asb.VortexLatticeMethod(
    airplane=f1_2026_car,
    op_point=op_point,
    spanwise_resolution=16,  
    chordwise_resolution=16,
)
vlm_results = vlm.run()

# SOLVER B: AeroBuildup (2D Viscous Skin Friction & Profile Drag)
viscous_solver = asb.AeroBuildup(
    airplane=f1_2026_car,
    op_point=op_point
)
viscous_results = viscous_solver.run()

# ==========================================
# 4. RESULTS OUTPUT
# ==========================================
# ==========================================
# 4. RESULTS OUTPUT
# ==========================================
print(f"--- 2026 F1 AERO RESULTS: {aero_mode.upper()} ---")

# Extract the values from the NumPy arrays and convert them to standard floats
vlm_lift = float(np.sum(vlm_results['L']))
vlm_drag = float(np.sum(vlm_results['D']))
viscous_drag = float(np.sum(viscous_results['D']))

total_drag = vlm_drag + viscous_drag

# Lift is negative in AeroSandbox because it pushes down (Downforce)
print(f"Total Downforce:     {-vlm_lift:.2f} N")
print(f"Total Drag:          {total_drag:.2f} N")
print(f"Aerodynamic Efficiency (L/D): {-vlm_lift / total_drag:.2f}")

# Uncomment to visualize the 3D geometry and pressure!
# vlm.draw()
# ==========================================
# 5. VOLUMETRIC WIND STREAMLINES & VISUALIZATION
# ==========================================
print("Calculating full-height volumetric wind streamlines...")

# 1. Create a TALLER grid of "smoke wands" 1 meter in front of the car
# We increased the width slightly and dramatically increased the height!
y_seeds = np.linspace(-1.0, 1.0, 12)  # Width of the simulation volume (12 wands wide)
z_seeds = np.linspace(0.05, 1.1, 12)  # Height: From the floor (0.05m) up to OVER the rear wing (1.1m)
Y, Z = np.meshgrid(y_seeds, z_seeds)
X = np.full_like(Y, -1.0) # X-coordinate: -1.0 meters (in front of the nose)

# Stack them into a list of 3D coordinates (X, Y, Z)
seed_points = np.column_stack((X.flatten(), Y.flatten(), Z.flatten()))

# 2. Command the VLM solver to trace the wind from those points
vlm.calculate_streamlines(
    seed_points=seed_points,
    n_steps=200,      # Increased steps for a smoother 3D render
    length=10.0       # The wind lines will stretch 10 meters long
)

# 3. Draw the final high-fidelity simulation
print("Generating interactive browser plot...")
vlm.draw(
    backend="plotly", 
    show_kwargs={
        "title": f"2026 F1 Aero Volume (Full Car Height) - {aero_mode}",
    }
)
