import numpy as np

class StackelbergTherapyOptimizer:
    """
    Stackelberg game model for adaptive therapy
    
    Leader: Physician chooses drug dose D(t)
    Follower: Tumor evolves resistance frequency f_r(t)
    
    Objective: Maximize time to progression (TTP)
    """
    
    def __init__(self):
        self.sensitive_fitness = 0.05
        self.resistant_fitness = 0.04  # Cost of resistance
        self.drug_kill_rate = 0.08
        self.alpha = 1.0  # Competition coefficient of R on S
        self.beta = 4.0   # Competition coefficient of S on R (strong suppression)
        
    def tumor_growth_ode(self, state, t, drug_dose):
        """
        Lotka-Volterra competition model with dynamic drug intervention
        
        dS/dt = r_s * S * (1 - (S + alpha * R)/K) - d * drug_dose * S
        dR/dt = r_r * R * (1 - (R + beta * S)/K)
        
        S: Sensitive cells
        R: Resistant cells
        """
        S, R = state
        K = 1e9  # Carrying capacity
        
        r_s = self.sensitive_fitness
        r_r = self.resistant_fitness
        d = self.drug_kill_rate
        
        # Prevent negative population values
        S = max(0.0, S)
        R = max(0.0, R)
        
        # Competitional growth
        dS = r_s * S * (1.0 - (S + self.alpha * R) / K) - d * drug_dose * S
        dR = r_r * R * (1.0 - (R + self.beta * S) / K)
        
        return [dS, dR]
    
    def adaptive_dosing_strategy(self, 
                                 current_tumor_size: float,
                                 target_size: float) -> float:
        """
        Adaptive therapy: Dose to maintain stable size
        
        Args:
            current_tumor_size: Current total cells
            target_size: Desired tumor burden (80% of baseline)
            
        Returns:
            Optimal drug dose
        """
        if current_tumor_size < target_size * 0.95:
            return 0.0  # Holiday - let sensitive cells grow back
        elif current_tumor_size > target_size * 1.05:
            return 1.0  # Full dose to shrink
        else:
            # Proportional control
            error = (current_tumor_size - target_size) / target_size
            dose = 0.5 + 0.5 * error  # PID-like control
            return max(0.0, min(1.0, dose))
    
    def calculate_time_to_progression(self, 
                                     dosing_strategy: str,
                                     simulation_days: int = 500) -> float:
        """
        Simulate TTP under different strategies
        
        Args:
            dosing_strategy: 'MTD' (Maximum Tolerated Dose) or 'ADAPTIVE'
            simulation_days: Simulation duration
            
        Returns:
            Time to progression (days)
        """
        # Initial conditions
        S = 1e8  # Sensitive cells
        R = 1e5  # Resistant cells (0.1% of total)
        
        baseline_size = S + R
        target_size = baseline_size * 0.8
        progression_threshold = baseline_size * 1.2  # 20% growth over baseline is progression
        
        dt = 1.0  # 1 day steps
        
        for day in range(simulation_days):
            current_size = S + R
            if current_size >= progression_threshold:
                return float(day)
                
            # Determine dose
            if dosing_strategy == 'MTD':
                dose = 1.0
            else:  # ADAPTIVE
                dose = self.adaptive_dosing_strategy(current_size, target_size)
                
            # Run simple Euler integration step
            dS, dR = self.tumor_growth_ode([S, R], day, dose)
            S += dS * dt
            R += dR * dt
            
            # Prevent negative populations
            S = max(0.0, S)
            R = max(0.0, R)
            
        return float(simulation_days)
