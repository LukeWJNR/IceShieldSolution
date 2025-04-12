import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from utils.calculations import calculate_freezing_point, estimate_newly_frozen_area
from utils.visualizations import plot_arctic_map

st.title("Ice Expansion Simulation")

st.markdown("""
## Simulating Potential Ice Expansion

This page simulates how reducing surface ocean salinity could potentially expand sea ice coverage.
The simulation is based on the relationship between salinity, temperature, and freezing points.
""")

# Simulation parameters
st.subheader("Simulation Parameters")

col1, col2 = st.columns(2)

with col1:
    initial_salinity = st.slider("Initial salinity (PSU)", 30.0, 35.0, 32.0, 0.1)
    target_salinity = st.slider("Target salinity (PSU)", 28.0, initial_salinity-0.1, 30.0, 0.1)

with col2:
    grid_size = st.slider("Simulation grid size", 50, 200, 100, 10, 
                         help="Higher values give more detailed but slower simulations")
    
    season = st.selectbox("Season", ["Winter", "Spring", "Summer", "Fall"])

# Create simulated temperature and salinity data
st.subheader("Generating Simulated Arctic Data")

@st.cache_data
def generate_arctic_data(grid_size, season):
    """
    Generate simulated Arctic temperature and salinity data.
    
    In a real application, this would use actual data from sources like:
    - NOAA's Arctic data
    - NASA's satellite measurements
    - Oceanic research station data
    
    Here we create a simplified model with:
    - Colder temperatures near the center (North Pole)
    - A gradient of temperatures moving outward
    - Seasonal adjustments
    """
    # Temperature adjustments by season (very simplified)
    season_temp_adjust = {
        "Winter": -5.0,
        "Spring": -2.0,
        "Summer": 0.0,
        "Fall": -3.0
    }
    
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
            if normalized_distance <= 1.0:
                # Inside the Arctic circle
                temperature[i, j] = -10 + 15 * normalized_distance + season_temp_adjust[season]
                salinity[i, j] = initial_salinity - 2 * (1 - normalized_distance)
            else:
                # Outside the Arctic circle
                temperature[i, j] = 5 + 5 * (normalized_distance - 1)
                salinity[i, j] = initial_salinity
    
    # Create circular mask for the Arctic Ocean
    y, x = np.ogrid[-grid_size//2:grid_size//2, -grid_size//2:grid_size//2]
    mask = x**2 + y**2 <= (grid_size//2)**2
    
    return temperature, salinity, mask

# Generate data
temperature, salinity_data, arctic_mask = generate_arctic_data(grid_size, season)

# Apply mask to limit data to within the Arctic circle
temperature_masked = np.copy(temperature)
temperature_masked[~arctic_mask] = 10  # Set to a high value outside the Arctic

# Information about the simulation
st.info(f"""
This simulation creates a simplified model of the Arctic Ocean with:
- Temperature gradient from pole (colder) to edges (warmer)
- Season adjustment: {season}
- Initial freezing point: {calculate_freezing_point(initial_salinity):.2f}°C
- Target freezing point: {calculate_freezing_point(target_salinity):.2f}°C

The simulation shows where ice would form based on these conditions.
""")

# Run the simulation
results = estimate_newly_frozen_area(
    temperature_masked, 
    salinity_data,
    initial_salinity,
    target_salinity
)

# Display results
st.subheader("Simulation Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Currently Frozen Area", f"{results['currently_frozen_area']:,} km²")
    
with col2:
    st.metric("Newly Frozen Area", f"{results['newly_frozen_area']:,} km²")
    
with col3:
    st.metric("Total Frozen Area", f"{results['total_frozen_area']:,} km²", 
             delta=f"+{results['newly_frozen_area'] / results['currently_frozen_area'] * 100:.1f}%")

# Create and display visualization
st.markdown("### Arctic Ice Coverage Visualization")

arctic_map = plot_arctic_map(
    results['currently_frozen_map'],
    results['newly_frozen_map'],
    grid_size
)

st.pyplot(arctic_map)

st.caption("""
Note: This is a simplified simulation for educational purposes. Actual ice formation depends on many additional 
factors including ocean currents, wind patterns, and existing ice dynamics.
""")

# Show temperature distribution
st.subheader("Temperature Distribution")

fig, ax = plt.subplots(figsize=(10, 6))

# Plot temperature histogram only for points within the Arctic circle
arctic_temperatures = temperature[arctic_mask]
ax.hist(arctic_temperatures, bins=30, alpha=0.7)

# Add vertical lines for freezing points
initial_freezing = calculate_freezing_point(initial_salinity)
target_freezing = calculate_freezing_point(target_salinity)

ax.axvline(x=initial_freezing, color='blue', linestyle='--', 
           label=f'Current Freezing Point ({initial_freezing:.2f}°C)')
ax.axvline(x=target_freezing, color='green', linestyle='--', 
           label=f'New Freezing Point ({target_freezing:.2f}°C)')

# Shade the area between freezing points
ax.axvspan(target_freezing, initial_freezing, alpha=0.2, color='green',
          label=f'Newly Freezable Region ({initial_freezing-target_freezing:.2f}°C)')

ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Frequency')
ax.set_title('Arctic Temperature Distribution')
ax.legend()

st.pyplot(fig)

st.info(f"""
The area between the two vertical lines represents water that is currently above freezing temperature,
but would freeze if the salinity were reduced from {initial_salinity} PSU to {target_salinity} PSU.

This simplified model suggests that a {initial_salinity-target_salinity:.1f} PSU reduction in salinity 
could increase the frozen area by approximately {results['newly_frozen_area']:,} km².
""")

st.subheader("Real-World Considerations")
st.markdown("""
While this simulation provides a conceptual model of how salinity reduction could expand ice coverage,
real-world implementation would need to consider additional factors:

1. **Ocean Dynamics**: Currents, mixing, and stratification would affect how freshwater distributes
2. **Seasonal Timing**: Intervention would be most effective just before and during freezing seasons
3. **Regional Targeting**: Focusing on areas with temperatures just above freezing would maximize impact
4. **Feedback Effects**: New ice formation would create its own feedback by reflecting more sunlight
5. **Environmental Impacts**: Changes to salinity could affect marine ecosystems

The next page explores different geoengineering approaches that could be used to implement
salinity reduction or other ice preservation strategies.
""")
