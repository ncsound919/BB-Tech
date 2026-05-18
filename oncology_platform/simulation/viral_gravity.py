import numpy as np
from typing import Dict, List

class ViralGravitySimulation:
    """
    Simulation of the 'Viral Gravity Offense' (Volume 1: Viral Systems).
    Models high-transmission viral dynamics ('Steph Curry' phenotype) 
    where viral 'gravity' pulls host resources and healthy cells into the infection cascade,
    undergoing dynamic countermeasure defenses.
    """
    
    def __init__(self, 
                 initial_susceptible: float = 1e6,
                 initial_infected: float = 100.0,
                 gravity_coefficient: float = 2.5,
                 clearance_rate: float = 0.1):
        self.S0 = initial_susceptible
        self.I0 = initial_infected
        self.G = gravity_coefficient
        self.gamma = clearance_rate
        
    def simulate_infection_cascade(self, 
                                   days: int = 60, 
                                   countermeasure_day: int = 15,
                                   defense_potency: float = 0.6) -> Dict:
        """
        Run SIRS (Susceptible, Infected, Recovered, Stressed) infection cascade 
        with Steph Curry-style 'Gravity' dynamics.
        
        Gravity increases beta (infection rate) as a function of current infected density.
        """
        S = [self.S0]
        I = [self.I0]
        R = [0.0]
        Stressed = [0.0]
        
        N = self.S0 + self.I0
        
        # Base transmission rate
        beta_base = 0.05
        
        for t in range(1, days):
            # Dynamic 'Viral Gravity' factor pulls cells in
            # As infected population grows, infection probability increases nonlinearly
            gravity_pull = 1.0 + (self.G * (I[-1] / N))
            beta_dynamic = beta_base * gravity_pull
            
            # Apply defense (e.g. vaccine/antiviral countermeasure)
            if t >= countermeasure_day:
                beta_dynamic *= (1.0 - defense_potency)
                
            new_infections = beta_dynamic * S[-1] * I[-1] / N
            new_recoveries = self.gamma * I[-1]
            
            # Cellular stress due to high viral replication
            new_stress = 0.02 * I[-1]
            
            S_next = max(0.0, S[-1] - new_infections)
            I_next = max(0.0, I[-1] + new_infections - new_recoveries - new_stress)
            R_next = R[-1] + new_recoveries
            Stressed_next = Stressed[-1] + new_stress - (0.05 * Stressed[-1]) # slow recovery of stress
            
            S.append(S_next)
            I.append(I_next)
            R.append(R_next)
            Stressed.append(Stressed_next)
            
        # Compute baseline R0
        # R0 = beta * N / gamma
        r0_baseline = (beta_base * (1.0 + self.G)) / self.gamma
        r0_post_countermeasure = ((beta_base * (1.0 - defense_potency)) * (1.0 + self.G)) / self.gamma
        
        return {
            'days': list(range(days)),
            'susceptible': S,
            'infected': I,
            'recovered': R,
            'stressed_cells': Stressed,
            'r0_baseline': r0_baseline,
            'r0_post_countermeasure': r0_post_countermeasure,
            'peak_infection': max(I),
            'peak_day': int(np.argmax(I))
        }
