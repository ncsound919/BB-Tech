import numpy as np
from typing import Dict, List

class JordanCancerModel:
    """
    Simulation of the 'Jordan Cancer Model' (Volume 3: Malignancies & Takeovers).
    Models high-pace clonal expansion ('Michael Jordan' phenotype) where a dominant,
    extremely efficient malignant clone monopolizes microenvironmental space and resources,
    leading to competitive suppression and eventual systemic takeover.
    """
    
    def __init__(self,
                 initial_sensitive: float = 1e5,
                 initial_resistant: float = 100.0,
                 carrying_capacity: float = 1e8,
                 sensitive_growth_rate: float = 0.4,
                 resistant_growth_rate: float = 0.2):
        self.S0 = initial_sensitive
        self.R0 = initial_resistant
        self.K = carrying_capacity
        self.r_s = sensitive_growth_rate
        self.r_r = resistant_growth_rate
        
    def simulate_clonal_takeover(self,
                                 days: int = 150,
                                 dosing_strategy: str = 'MTD',
                                 dose_potency: float = 0.8) -> Dict:
        """
        Simulate clonal competition and calculate the Host Takeover Index (HTI).
        
        MTD immediately wipes out sensitive cells, releasing the resistant Jordan clone 
        from competitive resource suppression (competitive release).
        """
        S = [self.S0]
        R = [self.R0]
        HTI = [0.0]
        
        # Competition coefficients (Lotka-Volterra dynamics)
        # Sensitive cells are highly dominant over space, blocking resistant ones
        alpha_sr = 2.0  # sensitive impact on resistant
        alpha_rs = 1.0  # resistant impact on sensitive
        
        for t in range(1, days):
            current_S = S[-1]
            current_R = R[-1]
            total_pop = current_S + current_R
            
            # Apply therapy dosing
            s_kill = 0.0
            r_kill = 0.0
            if dosing_strategy == 'MTD':
                # Continuous maximum dosage kills sensitive cells at a very high rate
                s_kill = dose_potency * current_S
                r_kill = 0.05 * dose_potency * current_R # resistant has low kill rate
            elif dosing_strategy == 'ADAPTIVE':
                # Adaptive dosing is pulsed: only dosing when tumor grows beyond threshold
                if total_pop > 0.4 * self.K:
                    s_kill = 0.4 * dose_potency * current_S
                    r_kill = 0.02 * dose_potency * current_R
                    
            # Compute growth differentials
            growth_S = self.r_s * current_S * (1.0 - (current_S + alpha_rs * current_R) / self.K)
            growth_R = self.r_r * current_R * (1.0 - (current_R + alpha_sr * current_S) / self.K)
            
            next_S = max(0.0, current_S + growth_S - s_kill)
            next_R = max(0.0, current_R + growth_R - r_kill)
            
            # Prevent pop exceeding capacity
            if next_S + next_R > self.K:
                scale = self.K / (next_S + next_R)
                next_S *= scale
                next_R *= scale
                
            # Host Takeover Index (HTI) = percentage of total carrying capacity captured by cancer
            hti_t = ((next_S + next_R) / self.K) * 100.0
            
            S.append(next_S)
            R.append(next_R)
            HTI.append(hti_t)
            
        # Determine day of progression (progression defined as tumor reaching 50% capacity)
        progression_day = -1
        for idx, h in enumerate(HTI):
            if h >= 50.0:
                progression_day = idx
                break
                
        return {
            'days': list(range(days)),
            'sensitive_population': S,
            'resistant_population': R,
            'host_takeover_index': HTI,
            'progression_day': progression_day if progression_day != -1 else days,
            'final_takeover_pct': HTI[-1]
        }
