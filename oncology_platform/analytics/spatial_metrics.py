import numpy as np
from scipy.spatial import Voronoi

class SpatialTumorAnalyzer:
    """
    Spatial pattern analysis using computational geometry
    
    Implements:
    - Voronoi tessellation for tumor architecture
    - Ripley's K-function for immune cell clustering
    - Cross-K for tumor-immune interactions
    """
    
    def __init__(self):
        self.voronoi_computed = False
        
    def compute_voronoi_tessellation(self, cell_positions: np.ndarray) -> Voronoi:
        """
        Compute Voronoi diagram from cell nuclei coordinates
        
        Args:
            cell_positions: Nx2 array of (x,y) coordinates
            
        Returns:
            scipy.spatial.Voronoi object
        """
        vor = Voronoi(cell_positions)
        self.voronoi_computed = True
        return vor
    
    def calculate_spatial_disorganization_index(self, vor: Voronoi) -> float:
        """
        Quantify entropy of Voronoi tessellation
        
        Healthy tissue: Regular hexagonal packing (low entropy)
        Malignant tissue: Irregular polygons (high entropy)
        
        Returns:
            Shannon entropy of polygon side distribution
        """
        # Count sides of each Voronoi polygon
        polygon_sides = []
        for region_idx in vor.regions:
            if -1 not in region_idx and len(region_idx) > 0:
                polygon_sides.append(len(region_idx))
        
        if not polygon_sides:
            return 0.0
            
        # Calculate Shannon entropy
        side_counts = np.bincount(polygon_sides)
        probabilities = side_counts / side_counts.sum()
        # Filter out 0 probabilities to prevent NaN in log
        probabilities = probabilities[probabilities > 0]
        entropy = -np.sum(probabilities * np.log2(probabilities))
        
        return entropy
    
    def ripleys_k_function(self, points: np.ndarray, 
                          radii: np.ndarray,
                          area: float) -> np.ndarray:
        """
        Ripley's K-function for point pattern analysis
        
        K(r) = (Area / n²) * Σ Σ I(d_ij < r)
        
        Args:
            points: Nx2 array of point coordinates
            radii: Array of distance thresholds
            area: Total area of observation window
            
        Returns:
            K(r) values for each radius
        """
        n = len(points)
        if n == 0:
            return np.zeros_like(radii)
            
        k_values = []
        
        for r in radii:
            count = 0
            for i in range(n):
                for j in range(i+1, n):
                    dist = np.linalg.norm(points[i] - points[j])
                    if dist < r:
                        count += 2  # Count both i→j and j→i
            
            k = (area / (n * n)) * count
            k_values.append(k)
        
        return np.array(k_values)
    
    def calculate_L_function(self, k_values: np.ndarray, 
                             radii: np.ndarray) -> np.ndarray:
        """
        Normalized Ripley's K (L-function)
        
        L(r) = sqrt(K(r) / π) - r
        
        L(r) > 0: Clustering (immune cells around tumor)
        L(r) = 0: Random distribution
        L(r) < 0: Dispersion (immune exclusion)
        """
        return np.sqrt(k_values / np.pi) - radii
