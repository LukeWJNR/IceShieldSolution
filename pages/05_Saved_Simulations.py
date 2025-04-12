import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utils.database import (
    get_scenarios, get_scenario, save_scenario, update_scenario, delete_scenario,
    get_results, save_result
)
from utils.calculations import calculate_freshwater_required, estimate_newly_frozen_area
from utils.visualizations import plot_arctic_map

st.title("Saved Simulations")

st.markdown("""
## Manage Your Simulation Scenarios

This page allows you to save, load, and manage your simulation scenarios.
You can save interesting configurations for future reference or comparison.
""")

# Tabs for different operations
tab1, tab2, tab3 = st.tabs(["Saved Scenarios", "Save Current Scenario", "History"])

# Tab 1: View and load saved scenarios
with tab1:
    st.subheader("Your Saved Scenarios")
    
    try:
        # Get all saved scenarios
        scenarios = get_scenarios()
        
        if not scenarios:
            st.info("You don't have any saved scenarios yet. Use the 'Save Current Scenario' tab to create one.")
        else:
            # Convert to DataFrame for display
            df = pd.DataFrame(scenarios)
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            
            # Display only relevant columns
            display_df = df[['id', 'name', 'initial_salinity', 'target_salinity', 'area_km2', 'depth_m', 'created_at']]
            st.dataframe(display_df, use_container_width=True)
            
            # Select scenario to view details or load
            selected_id = st.selectbox("Select scenario to view or load:", 
                                      options=[s['id'] for s in scenarios],
                                      format_func=lambda x: next((s['name'] for s in scenarios if s['id'] == x), str(x)))
    except Exception as e:
        st.error(f"Error retrieving saved scenarios: {e}")
        st.info("Database connection issue. Please try again later.")
        scenarios = []
        
        if selected_id:
            selected_scenario = next((s for s in scenarios if s['id'] == selected_id), None)
            
            if selected_scenario:
                # Display scenario details
                st.subheader(f"Scenario: {selected_scenario['name']}")
                
                if selected_scenario['description']:
                    st.markdown(selected_scenario['description'])
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Initial Salinity", f"{selected_scenario['initial_salinity']} PSU")
                    
                with col2:
                    st.metric("Target Salinity", f"{selected_scenario['target_salinity']} PSU")
                    
                with col3:
                    st.metric("Surface Area", f"{selected_scenario['area_km2']:,.0f} km²")
                
                # Actions for the selected scenario
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Load Parameters", key="load_params"):
                        # Store in session state to use in other pages
                        st.session_state['initial_salinity'] = selected_scenario['initial_salinity']
                        st.session_state['target_salinity'] = selected_scenario['target_salinity']
                        st.session_state['area_km2'] = selected_scenario['area_km2']
                        st.session_state['depth_m'] = selected_scenario['depth_m']
                        st.session_state['season'] = selected_scenario['season']
                        st.session_state['grid_size'] = selected_scenario['grid_size']
                        
                        st.success("Parameters loaded! Navigate to other pages to use them.")
                
                with col2:
                    if st.button("Delete", key="delete_scenario"):
                        if delete_scenario(selected_id):
                            st.experimental_rerun()
                
                with col3:
                    favorite = selected_scenario['is_favorite']
                    new_favorite = st.checkbox("Favorite", value=favorite)
                    
                    if new_favorite != favorite:
                        update_scenario(selected_id, is_favorite=new_favorite)
                        st.experimental_rerun()
                
                # Show simulation results for this scenario
                results = get_results(scenario_id=selected_id)
                
                if results:
                    st.subheader("Previous Simulation Results")
                    
                    results_df = pd.DataFrame(results)
                    results_df['run_at'] = pd.to_datetime(results_df['run_at']).dt.strftime('%Y-%m-%d %H:%M')
                    
                    # Display core metrics
                    display_cols = ['run_at', 'freshwater_volume_km3', 'newly_frozen_area', 'total_frozen_area']
                    st.dataframe(results_df[display_cols], use_container_width=True)

# Tab 2: Save current scenario
with tab2:
    st.subheader("Save Current Simulation")
    
    # Get current parameters from session state or use defaults
    current_initial_salinity = st.session_state.get('initial_salinity', 32.0)
    current_target_salinity = st.session_state.get('target_salinity', 30.0)
    current_area_km2 = st.session_state.get('area_km2', 100000.0)
    current_depth_m = st.session_state.get('depth_m', 10.0)
    current_season = st.session_state.get('season', 'Winter')
    current_grid_size = st.session_state.get('grid_size', 100)
    
    # Form for saving scenario
    with st.form("save_scenario_form"):
        name = st.text_input("Scenario Name", value=f"Scenario {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        description = st.text_area("Description (optional)", value="")
        
        col1, col2 = st.columns(2)
        
        with col1:
            initial_salinity = st.slider("Initial salinity (PSU)", 30.0, 35.0, float(current_initial_salinity), 0.1)
            target_salinity = st.slider("Target salinity (PSU)", 28.0, initial_salinity-0.1, float(current_target_salinity), 0.1)
        
        with col2:
            area = st.number_input("Surface area (km²)", 
                                  min_value=1000.0, 
                                  max_value=14000000.0, 
                                  value=float(current_area_km2), 
                                  step=10000.0)
            
            depth = st.slider("Surface layer depth (m)", 
                             min_value=1.0, 
                             max_value=50.0, 
                             value=float(current_depth_m), 
                             step=1.0)
        
        col1, col2 = st.columns(2)
        
        with col1:
            season = st.selectbox("Season", ["Winter", "Spring", "Summer", "Fall"], 
                                 index=["Winter", "Spring", "Summer", "Fall"].index(current_season) if current_season in ["Winter", "Spring", "Summer", "Fall"] else 0)
        
        with col2:
            grid_size = st.slider("Simulation grid size", 50, 200, int(current_grid_size), 10)
        
        is_favorite = st.checkbox("Mark as favorite")
        
        submit_button = st.form_submit_button("Save Scenario")
        
        if submit_button:
            # Save to database
            scenario_id = save_scenario(
                name=name,
                description=description,
                initial_salinity=initial_salinity,
                target_salinity=target_salinity,
                area_km2=area,
                depth_m=depth,
                season=season,
                grid_size=grid_size,
                is_favorite=is_favorite
            )
            
            if scenario_id:
                st.success(f"Scenario '{name}' saved successfully!")
                
                # Also save the current results if we have them
                if 'freshwater_volume_km3' in st.session_state:
                    save_result(
                        scenario_id=scenario_id,
                        freshwater_volume_km3=st.session_state.get('freshwater_volume_km3'),
                        currently_frozen_area=st.session_state.get('currently_frozen_area'),
                        newly_frozen_area=st.session_state.get('newly_frozen_area'),
                        total_frozen_area=st.session_state.get('total_frozen_area'),
                        percent_global_desal=st.session_state.get('percent_global_desal'),
                        plants_needed=st.session_state.get('plants_needed'),
                        energy_twh_total=st.session_state.get('energy_twh_total')
                    )
            else:
                st.error("Failed to save scenario.")

# Tab 3: History of simulations
with tab3:
    st.subheader("Simulation History")
    
    # Get recent simulation results
    results = get_results(limit=20)
    
    if not results:
        st.info("No simulation history found. Run some simulations first.")
    else:
        # Convert to DataFrame for display
        df = pd.DataFrame(results)
        df['run_at'] = pd.to_datetime(df['run_at']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Display results
        st.dataframe(df[[
            'id', 'scenario_id', 'run_at', 'freshwater_volume_km3', 
            'newly_frozen_area', 'total_frozen_area', 'percent_global_desal'
        ]], use_container_width=True)
        
        # Select result to view details
        if len(results) > 0:
            selected_result_id = st.selectbox("Select result to view details:", 
                                           options=[r['id'] for r in results],
                                           format_func=lambda x: f"Result {x} - {next((r['run_at'] for r in results if r['id'] == x), '')}")
            
            if selected_result_id:
                selected_result = next((r for r in results if r['id'] == selected_result_id), None)
                
                if selected_result:
                    # Display details
                    st.subheader(f"Result Details (ID: {selected_result_id})")
                    
                    # Core metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Freshwater Volume", f"{selected_result['freshwater_volume_km3']:.1f} km³")
                    
                    if selected_result['newly_frozen_area']:
                        with col2:
                            st.metric("Newly Frozen Area", f"{selected_result['newly_frozen_area']:,.0f} km²")
                        
                        with col3:
                            st.metric("Total Frozen Area", f"{selected_result['total_frozen_area']:,.0f} km²")
                    
                    # Implementation metrics
                    if selected_result['percent_global_desal'] and selected_result['plants_needed'] and selected_result['energy_twh_total']:
                        st.subheader("Implementation Requirements")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("% Global Desalination", f"{selected_result['percent_global_desal']:.1f}%")
                        
                        with col2:
                            st.metric("Plants Required", f"{selected_result['plants_needed']:.0f}")
                        
                        with col3:
                            st.metric("Energy (TWh)", f"{selected_result['energy_twh_total']:.0f}")
                    
                    # Show detailed results if available
                    if selected_result['detailed_results'] and isinstance(selected_result['detailed_results'], dict):
                        detailed = selected_result['detailed_results']
                        
                        if 'river_comparisons' in detailed and isinstance(detailed['river_comparisons'], dict):
                            st.subheader("River Comparisons")
                            
                            river_df = pd.DataFrame({
                                'Water Source': list(detailed['river_comparisons'].keys()),
                                'Percentage': list(detailed['river_comparisons'].values())
                            })
                            
                            st.bar_chart(river_df.set_index('Water Source'))

# Add a divider
st.markdown("---")

# Information about the database functionality
st.subheader("About Saved Simulations")
st.markdown("""
This database functionality allows you to:

1. **Save and manage scenarios**: Store your simulation parameters for future use
2. **Track simulation history**: Review past results and compare approaches
3. **Share configurations**: Export your scenarios to collaborate with others

The database stores all your simulation parameters, allowing you to quickly switch 
between different scenarios without having to re-enter all values each time.
""")