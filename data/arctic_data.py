import numpy as np
import pandas as pd

def generate_simulated_arctic_data(grid_size=100):
    """
    Generate simulated Arctic temperature and salinity data.
    
    This creates simplified model data for illustration purposes.
    In a real application, this would be replaced with actual data
    from sources like NOAA, NASA, or oceanographic institutions.
    
    Parameters:
    -----------
    grid_size : int
        Size of the grid for the simulation
        
    Returns:
    --------
    dict
        Dictionary containing temperature and salinity data arrays
    """
    # Center coordinates
    center_x = grid_size // 2
    center_y = grid_size // 2
    
    # Create temperature grid with colder center and warmer edges
    temperature = np.zeros((grid_size, grid_size))
    salinity = np.zeros((grid_size, grid_size))
    
    for i in range(grid_size):
        for j in range(grid_size):
            # Calculate distance from center
            distance = np.sqrt((i - center_x)**2 + (j - center_y)**2)
            normalized_distance = distance / (grid_size // 2)
            
            # Temperature increases with distance from pole
            # This is a very simplified model
            if normalized_distance <= 1.0:
                # Inside the Arctic circle
                temperature[i, j] = -10 + 15 * normalized_distance
                salinity[i, j] = 32 - 2 * (1 - normalized_distance)
            else:
                # Outside the Arctic circle
                temperature[i, j] = 5 + 5 * (normalized_distance - 1)
                salinity[i, j] = 35
    
    # Create circular mask for the Arctic Ocean
    y, x = np.ogrid[-grid_size//2:grid_size//2, -grid_size//2:grid_size//2]
    mask = x**2 + y**2 <= (grid_size//2)**2
    
    return {
        "temperature": temperature,
        "salinity": salinity,
        "mask": mask
    }

def get_arctic_facts():
    """
    Return a dictionary of facts about the Arctic Ocean.
    
    Returns:
    --------
    dict
        Dictionary of Arctic Ocean facts
    """
    return {
        "total_area": 14.0e6,  # km²
        "average_depth": 1038,  # m
        "volume": 18.75e6,  # km³
        "salinity_range": (30, 34),  # PSU
        "avg_temperature": -1.8,  # °C
        "sea_ice_minimum": 3.74e6,  # km² (2020 minimum)
        "sea_ice_maximum": 15.05e6,  # km² (2020 maximum)
        "main_rivers": ["Ob", "Yenisei", "Lena", "Mackenzie"]
    }

def get_salinity_reduction_examples():
    """
    Return examples of potential salinity reduction scenarios.
    
    Returns:
    --------
    list of dict
        List of example scenarios
    """
    return [
        {
            "name": "Small Regional Intervention",
            "area_km2": 100000,
            "depth_m": 10,
            "salinity_reduction": 2,
            "freshwater_km3": 6.67
        },
        {
            "name": "Medium Arctic Basin",
            "area_km2": 1000000,
            "depth_m": 10,
            "salinity_reduction": 2,
            "freshwater_km3": 66.7
        },
        {
            "name": "Large Scale Arctic-wide",
            "area_km2": 5640000,
            "depth_m": 10,
            "salinity_reduction": 2,
            "freshwater_km3": 376.0
        }
    ]

def get_geoengineering_comparison_data():
    """
    Return comparison data for various geoengineering approaches.
    
    Returns:
    --------
    pandas.DataFrame
        Dataframe with geoengineering comparison metrics
    """
    approaches = [
        "Salinity Reduction",
        "Ice Thickening",
        "Reflective Materials",
        "Undersea Barriers",
        "Cloud Seeding",
        "Geotextiles"
    ]
    
    # Metrics for each approach (1-10 scale, 10 being best)
    metrics = {
        "Effectiveness": [7, 6, 8, 7, 5, 4],
        "Feasibility": [5, 7, 6, 3, 6, 5],
        "Cost Efficiency": [4, 6, 5, 2, 7, 3],
        "Environmental Impact": [6, 7, 4, 5, 5, 6],
        "Technological Readiness": [4, 7, 6, 3, 8, 7],
        "Scalability": [6, 4, 7, 5, 6, 3]
    }
    
    df = pd.DataFrame(metrics, index=approaches)
    return df
