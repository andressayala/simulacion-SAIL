# Unmanned-Surface-Vehicle

This repository contains the research, mathematical modeling, and control system design developed for a custom Unmanned Surface Vehicle (USV). 

## Repository Structure

### SymPy Dynamic Models
This section focuses on the derivation of analytical equations of motion for USVs, as well as the evaluation of various control schemes:

* **`USV - Dynamics.ipynb`**
  Explores the 2D planar dynamics of three simplified USV structural configurations. This analysis was used to select an optimal design based on performance heuristics, resulting in a monohull configuration equipped with a single thruster and steering mechanism.

* **`USV_model.py`**
  Implements a reusable Python class interface for the selected USV dynamic model, simplifying simulation and control integration.

* **`USV - PD Control.ipynb`**
  Implements and evaluates a cascaded PD (Proportional-Derivative) control architecture for vessel positioning and trajectory tracking.

* **`USV - MIMO Control 1 & 2.ipynb`**
  Exploration of Full-State Feedback (FSFB) multi-input multi-output control strategies, including Pole Placement and Linear Quadratic Regulator (LQR) methods. *(Note: Current implementations showed limited performance).*

* **`USV - NDI Control.ipynb`**
  Implements a Nonlinear Dynamic Inversion (NDI) controller to natively handle the non-linear system dynamics of a USV.

---

### MuJoCo Dynamic Models
Encompasses the code and configurations used to implement and simulate the USV model within the MuJoCo physics engine:

* **`USV - MuJoCo.ipynb`**
  Contains an initial 3D physics approximation of the selected USV monohull model in MuJoCo.

* **`USV - Water Simulation.ipynb`**
  Explores methods for simulating fluid dynamics within MuJoCo. Results indicate that while hydrostatic (buoyancy) forces are straightforward to model, hydrodynamic drag and lift forces, critical for high-speed maneuvering, present significant modeling challenges in rigid-body engines.

* **`USV - MuJoCo Control.ipynb`**
  Integrates hydrostatic forces with the vehicle model and tests a cascaded PD control scheme. *Current limitation:* Orientation instability was observed, likely due to MuJoCo's default freejoint quaternion representation. Future iterations may replace the freejoint with explicit hinge/prismatic joints to read Euler states directly.

* **`USV - MuJoCo 3 DoF RL.ipynb`**
  Trains a Reinforcement Learning policy network to navigate a simplified 3-DoF USV model to a target position.

---

### Motor Characterization
Contains experimental data and analysis used to evaluate thruster performance for a physical prototype:

* **`Motor Characterization.ipynb`**
  Processes thrust bench data and fits performance curves for two candidate brushless motors equipped with custom 3D-printed propellers operating underwater.