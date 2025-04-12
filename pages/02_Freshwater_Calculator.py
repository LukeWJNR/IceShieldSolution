import streamlit as st
import numpy as np
import pandas as pd
from utils.calculations import calculate_freshwater_required, calculate_desalination_metrics
from utils.visualizations import plot_freshwater_requirements

st.title("Freshwater Requirements Calculator")

st.markdown("""
## How Much Freshwater Would Be Needed?

Reducing ocean salinity requires adding freshwater to dilute the salt concentration.
This calculator helps you estimate the amount of freshwater needed for different scenarios
and explores the feasibility of various approaches to providing this freshwater.
""")

# Input parameters
st.subheader("Input Parameters")

col1, col2 = st.columns(2)

with col1:
    initial_salinity = st.slider("Initial salinity (PSU)", 30.0, 35.0, 32.0, 0.1)
    target_salinity = st.slider("Target salinity (PSU)", 28.0, initial_salinity-0.1, 30.0, 0.1)

with col2:
    area = st.number_input("Surface area (km²)", 
                          min_value=1000.0, 
                          max_value=14000000.0, 
                          value=100000.0, 
                          step=10000.0,
                          help="The Arctic Ocean is approximately 14 million km²")
    
    depth = st.slider("Surface layer depth (m)", 
                     min_value=1.0, 
                     max_value=50.0, 
                     value=10.0, 
                     step=1.0,
                     help="Depth of the surface layer to be diluted")

# Calculate freshwater requirements
if initial_salinity <= target_salinity:
    st.error("Target salinity must be lower than initial salinity for dilution to occur.")
else:
    results = calculate_freshwater_required(initial_salinity, target_salinity, area, depth)
    
    st.subheader("Freshwater Requirements")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Seawater Volume", f"{results['seawater_volume_km3']:.1f} km³")
        
    with col2:
        st.metric("Freshwater Needed", f"{results['freshwater_volume_km3']:.1f} km³")
        
    with col3:
        st.metric("% of Global Desalination", f"{results['percent_global_desal']:.1f}%", 
                 delta="annual capacity" if results['percent_global_desal'] < 100 else "years of capacity")
    
    # Visualization
    st.plotly_chart(plot_freshwater_requirements(results), use_container_width=True)
    
    # Comparison with natural water sources
    st.subheader("Comparison with Natural Water Sources")
    
    river_df = pd.DataFrame({
        'Water Source': ['Freshwater Required'] + list(results['river_comparisons'].keys()),
        'Percentage': [100] + list(results['river_comparisons'].values())
    })
    
    st.bar_chart(river_df.set_index('Water Source'), height=400)
    
    st.markdown(f"""
    The required freshwater volume ({results['freshwater_volume_km3']:.1f} km³) represents:
    
    - {results['river_comparisons']['Amazon River']:.1f}% of the annual Amazon River discharge
    - {results['river_comparisons']['Rhine River']:.1f}% of the annual Rhine River discharge
    - {results['river_comparisons']['Mississippi River']:.1f}% of the annual Mississippi River discharge
    """)
    
    # Desalination requirements
    st.subheader("Desalination Requirements")
    
    desal_metrics = calculate_desalination_metrics(results['freshwater_volume_km3'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Large Desalination Plants", f"{desal_metrics['plants_needed']:.0f}")
        
    with col2:
        st.metric("Energy Required", f"{desal_metrics['energy_twh_total']:.0f} TWh")
        
    with col3:
        st.metric("Tanker Trips", f"{desal_metrics['tanker_trips']:,.0f}", 
                 help="Using Very Large Crude Carriers (VLCCs)")
    
    # Cost information
    st.subheader("Estimated Costs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Plant Construction", f"${desal_metrics['plant_cost_billion']:.1f} billion")
        
    with col2:
        st.metric("Operational Costs", f"${desal_metrics['operational_cost_billion']:.1f} billion")
    
    st.info("""
    These are rough estimates based on current desalination technologies and costs.
    Actual costs would vary based on location, technology, and scale.
    """)
    
    # Alternative approaches
    st.subheader("Alternative Approaches")
    
    st.markdown("""
    While desalination is one approach to generating freshwater, there are other potential methods:
    
    1. **River Diversion**: Rerouting some freshwater from rivers that flow into other oceans
    2. **Targeted Seasonal Release**: Releasing reservoir water during critical ice formation periods
    3. **Mobile Desalination Ships**: Purpose-built vessels that desalinate water on-site
    4. **Ice Thickening**: Pumping water onto existing ice to increase its volume
    
    Each approach has different costs, benefits, and environmental considerations.
    """)
