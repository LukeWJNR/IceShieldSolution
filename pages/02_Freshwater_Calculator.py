import streamlit as st
import numpy as np
import pandas as pd
from utils.calculations import calculate_freshwater_required, calculate_desalination_metrics
from utils.visualizations import plot_freshwater_requirements
from utils.database import save_result, save_scenario

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

# Store parameters in session state for other pages to access
st.session_state['initial_salinity'] = initial_salinity
st.session_state['target_salinity'] = target_salinity
st.session_state['area_km2'] = area
st.session_state['depth_m'] = depth

# Calculate freshwater requirements
if initial_salinity <= target_salinity:
    st.error("Target salinity must be lower than initial salinity for dilution to occur.")
else:
    results = calculate_freshwater_required(initial_salinity, target_salinity, area, depth)
    
    # Store results in session state for saving to database later
    st.session_state['freshwater_volume_km3'] = results['freshwater_volume_km3']
    st.session_state['percent_global_desal'] = results['percent_global_desal']
    
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
    
    # Add a divider
    st.markdown("---")
    
    # Save results section
    st.subheader("Save This Scenario")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scenario_name = st.text_input("Scenario Name", value=f"Freshwater Scenario {initial_salinity}->{target_salinity} PSU")
    
    with col2:
        save_button = st.button("Save Results to Database")
        
    if save_button:
        # Store desalination metrics in session state
        st.session_state['plants_needed'] = desal_metrics['plants_needed']
        st.session_state['energy_twh_total'] = desal_metrics['energy_twh_total']
        
        # Save the scenario
        scenario_id = save_scenario(
            name=scenario_name,
            description=f"Salinity reduction from {initial_salinity} to {target_salinity} PSU over {area:,.0f} km² area with {depth}m depth.",
            initial_salinity=initial_salinity,
            target_salinity=target_salinity,
            area_km2=area,
            depth_m=depth,
            season="N/A",
            grid_size=100
        )
        
        # Save the results
        if scenario_id:
            result_id = save_result(
                scenario_id=scenario_id,
                freshwater_volume_km3=results['freshwater_volume_km3'],
                percent_global_desal=results['percent_global_desal'],
                plants_needed=desal_metrics['plants_needed'],
                energy_twh_total=desal_metrics['energy_twh_total'],
                detailed_results={
                    'river_comparisons': results['river_comparisons'],
                    'seawater_volume_km3': results['seawater_volume_km3']
                }
            )
            
            st.success("Scenario and results saved successfully! View them in the 'Saved Simulations' page.")
        else:
            st.error("Failed to save scenario.")
