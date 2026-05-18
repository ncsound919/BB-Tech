from dataclasses import dataclass
from typing import Dict

@dataclass
class TERComponents:
    """Tumor Efficiency Rating Components (Basketball → Biology)"""
    field_goals: float = 0.0        # Standard mitotic divisions
    three_pointers: float = 0.0     # Division under stress (hypoxia/chemo)
    assists: float = 0.0            # Paracrine signaling (VEGF, etc.)
    offensive_rebounds: float = 0.0 # Autophagy/metabolic scavenging
    turnovers: float = 0.0          # Apoptosis/necrosis
    personal_fouls: float = 0.0     # Deleterious mutations
    
    # Weights from NBA PER formula
    WEIGHTS = {
        'fg': 1.65,
        '3p': 2.65,
        'ast': 0.67,
        'orb': 0.79,
        'tov': -1.04,
        'pf': -0.35
    }

class TumorEfficiencyCalculator:
    """
    Calculate Tumor Efficiency Rating (TER)
    Adapted from John Hollinger's Player Efficiency Rating
    
    TER quantifies malignant potential per cell cycle
    """
    
    def __init__(self):
        self.league_average_pace = 100  # Cell cycles per unit time
        
    def calculate_ter(self, components: TERComponents, 
                      cell_cycle_time: float) -> float:
        """
        Calculate composite TER score
        
        Args:
            components: TERComponents with biological events
            cell_cycle_time: Duration of cell cycle (analogous to minutes played)
            
        Returns:
            Tumor Efficiency Rating (normalized to league average = 15.0)
        """
        if cell_cycle_time == 0:
            return 0.0
            
        unadjusted_ter = (
            components.WEIGHTS['fg'] * components.field_goals +
            components.WEIGHTS['3p'] * components.three_pointers +
            components.WEIGHTS['ast'] * components.assists +
            components.WEIGHTS['orb'] * components.offensive_rebounds +
            components.WEIGHTS['tov'] * components.turnovers +
            components.WEIGHTS['pf'] * components.personal_fouls
        )
        
        # Normalize by cell cycle time (per-minute rating)
        ter_per_cycle = unadjusted_ter / cell_cycle_time
        
        # Adjust to league average (15.0 standard)
        adjusted_ter = ter_per_cycle * (self.league_average_pace / 100)
        
        return adjusted_ter
    
    def classify_malignancy(self, ter: float) -> str:
        """Classify tumor aggressiveness by TER threshold"""
        if ter > 25:
            return "ELITE_MALIGNANT"  # MVP-level threat
        elif ter > 20:
            return "HIGH_AGGRESSIVE"
        elif ter > 15:
            return "MODERATE"
        else:
            return "LOW_AGGRESSIVE"
