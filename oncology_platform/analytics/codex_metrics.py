import numpy as np
from scipy.integrate import simpson

class CodexScout:
    """
    Calculates the biological 'box score' metrics based on the 
    Basketball-to-Biotech Mapping Framework.
    """

    def calculate_TER(self, proliferation_rate: float, stress_division: float, apoptosis_rate: float) -> float:
        """
        Calculates Tumor Efficiency Rating (TER).
        Weights derived from source documentation:
        - FG (Normal Division) = 1.65
        - 3P (Stress Division) = 2.65
        - TOV (Apoptosis) = -1.04
        """
        FG = 1.65 * proliferation_rate
        ThreeP = 2.65 * stress_division
        TOV = -1.04 * apoptosis_rate
        
        ter_score = FG + ThreeP + TOV 
        return ter_score

    def calculate_RO(self, gravity: float, breadth: float, pace: float, drtg: float) -> float:
        """
        Calculates Therapeutic Invasion Index (RO).
        Target: RO > 1.0 for self-propagating cure.
        Formula: RO = (Gravity * Breadth * Pace) / DRtg
        """
        if drtg == 0: 
            return float('inf')
        return (gravity * breadth * pace) / drtg

    def calculate_flow(self, initiative: float, time_points: np.ndarray, concentration_values: np.ndarray, d_max: float) -> float:
        """
        Calculates Pharmacokinetic Tempo (Flow).
        Formula: I * min(D_max / D, 1).
        Uses Numerical Integration (Simpson's Rule) for Delay (D).
        """
        # Integrate velocity over time to get Delay D = ∫ v(t) dt
        D = simpson(concentration_values, x=time_points)
        if D == 0:
            return 0.0
        
        # Calculate Flow Score
        flow_score = initiative * min(d_max / D, 1)
        return flow_score

    def check_trueness(self, binding_accuracy: float, baseline_noise: float, system_noise: float) -> float:
        """
        Calculates Target Fidelity (Trueness).
        Formula: A = k * (A / (B + N) - 1).
        Threshold: Must be > 0.60 to avoid genetic meltdown.
        """
        k = 1.0 # Scaling constant
        denominator = baseline_noise + system_noise
        if denominator == 0:
            return 0.0
        score = k * (binding_accuracy / denominator - 1)
        return score
