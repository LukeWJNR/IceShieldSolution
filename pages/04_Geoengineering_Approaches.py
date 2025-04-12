import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
from utils.visualizations import plot_geoengineering_comparison
from utils.database import get_geoengineering_approaches

st.title("Geoengineering Approaches")

st.markdown("""
## Comparing Methods for Sea Ice Preservation

Various geoengineering approaches have been proposed to preserve sea ice and slow the impacts of climate change.
This page compares these different methods, with a focus on salinity reduction techniques.
""")

# Overview of approaches
st.subheader("Overview of Geoengineering Approaches")

# Fetch geoengineering approaches from the database
try:
    db_approaches = get_geoengineering_approaches()
    
    # Convert database data into a dictionary format for easier use in the UI
    approaches = {}
    for approach in db_approaches:
        approaches[approach['name']] = {
            "description": approach['description'],
            "methods": approach['methods'],
            "advantages": approach['advantages'],
            "challenges": approach['challenges'],
            # Additional metrics from database
            "effectiveness": approach['effectiveness'],
            "feasibility": approach['feasibility'],
            "cost_efficiency": approach['cost_efficiency'],
            "environmental_impact": approach['environmental_impact'],
            "technological_readiness": approach['technological_readiness'],
            "scalability": approach['scalability']
        }
except Exception as e:
    st.error(f"Error retrieving data from database: {e}")
    st.info("Using default data as a fallback.")
    # The get_geoengineering_approaches function has a built-in fallback that will return 
    # default data if the database is unavailable, so the error should be handled gracefully.

# Display comparison chart
st.plotly_chart(plot_geoengineering_comparison(), use_container_width=True)

# Tabs for each approach
st.subheader("Detailed Approach Information")
tabs = st.tabs(list(approaches.keys()))

for i, (approach, info) in enumerate(approaches.items()):
    with tabs[i]:
        st.markdown(f"### {approach}")
        st.markdown(info["description"])
        
        # Add metrics scorecard at the top
        st.subheader("Metrics")
        metric_cols = st.columns(6)
        
        metrics = [
            ("Effectiveness", info["effectiveness"]),
            ("Feasibility", info["feasibility"]),
            ("Cost Efficiency", info["cost_efficiency"]),
            ("Environmental Impact", info["environmental_impact"]),
            ("Tech Readiness", info["technological_readiness"]),
            ("Scalability", info["scalability"])
        ]
        
        for idx, (metric_name, metric_value) in enumerate(metrics):
            with metric_cols[idx]:
                st.metric(metric_name, f"{metric_value}/10")
        
        # Add details in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Methods")
            for method in info["methods"]:
                st.markdown(f"- {method}")
                
            st.markdown("#### Advantages")
            for advantage in info["advantages"]:
                st.markdown(f"- {advantage}")
        
        with col2:
            st.markdown("#### Challenges")
            for challenge in info["challenges"]:
                st.markdown(f"- {challenge}")

# Focus on salinity reduction
st.subheader("Salinity Reduction Methods")

st.markdown("""
Let's explore specific approaches to implementing salinity reduction in more detail:
""")

# Salinity reduction methods
salinity_methods = {
    "Desalination Ships": {
        "description": "Purpose-built vessels equipped with desalination technology that can produce freshwater directly in the Arctic.",
        "capacity": "500,000 m³/day per large ship",
        "requirements": "Energy source (nuclear, diesel), intake systems, RO modules, distribution systems",
        "cost": "$500M - $2B per ship",
        "feasibility": "Technically viable but requires fleet development"
    },
    "River Diversion": {
        "description": "Redirecting portions of freshwater from rivers that flow into other oceans toward the Arctic.",
        "capacity": "Varies by river system, potentially massive volumes",
        "requirements": "Canal systems, pumping stations, international agreements",
        "cost": "Multi-billion dollar infrastructure projects",
        "feasibility": "Major engineering and geopolitical challenges"
    },
    "Seasonal Meltwater Capture": {
        "description": "Capturing and storing meltwater during summer for strategic release during ice formation season.",
        "capacity": "Limited by storage capacity, potentially billions of cubic meters",
        "requirements": "Reservoirs, distribution systems, pumping infrastructure",
        "cost": "Varies by scale",
        "feasibility": "More practical for targeted regional interventions"
    },
    "Subsurface Water Movement": {
        "description": "Using submarine systems to bring deeper, less saline water to the surface in strategic locations.",
        "capacity": "Depends on system size and deployment",
        "requirements": "Submarine technology, energy systems, precise monitoring",
        "cost": "High technology development costs",
        "feasibility": "Requires significant research and development"
    }
}

# Display salinity reduction methods
method_df = pd.DataFrame(salinity_methods).T.reset_index()
method_df.columns = ["Method", "Description", "Capacity", "Requirements", "Cost", "Feasibility"]

st.dataframe(method_df, use_container_width=True, hide_index=True)

# Case study: Desalination Ships
st.subheader("Case Study: Arctic Desalination Ships")

st.markdown("""
Desalination ships represent one of the more innovative approaches to implementing salinity reduction.
Let's explore what this might look like in practice:
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### Ship Design Concept
    
    A fleet of purpose-built desalination vessels could:
    
    - Be converted from oil tankers or LNG carriers
    - Include modular desalination units
    - Use nuclear power (similar to icebreakers)
    - Operate seasonally in strategic locations
    - Produce and distribute freshwater directly
    
    Each large ship could produce ~500,000 m³ of freshwater daily.
    """)

with col2:
    st.markdown("""
    #### Operational Strategy
    
    The most effective deployment would:
    
    - Target areas with temperatures just above freezing
    - Operate during early freezing season (Fall)
    - Create strategic freshwater "lenses" at the surface
    - Monitor and adjust based on real-time conditions
    - Work in coordination with climate monitoring systems
    
    Ships could have dual purpose for emergency water supply.
    """)

# Deployment considerations
st.subheader("Deployment Considerations")

st.markdown("""
Any geoengineering approach, including salinity reduction, would need to consider:
""")

considerations = {
    "Environmental Impact": [
        "Effects on marine ecosystems",
        "Potential changes to circulation patterns",
        "Impacts on local weather systems",
        "Secondary effects on biological productivity"
    ],
    "Legal and Governance": [
        "International agreements on Arctic interventions",
        "Regulatory frameworks for ocean modification",
        "Cross-border effects and responsibilities",
        "Monitoring and verification systems"
    ],
    "Economic Factors": [
        "Initial investment requirements",
        "Operational costs and maintenance",
        "Comparison with other climate mitigation strategies",
        "Potential economic benefits (like shipping route preservation)"
    ],
    "Technical Feasibility": [
        "Scaling challenges and limitations",
        "Energy requirements and sources",
        "Technological readiness levels",
        "Monitoring and adjustment capabilities"
    ]
}

cols = st.columns(4)

for i, (category, points) in enumerate(considerations.items()):
    with cols[i]:
        st.markdown(f"#### {category}")
        for point in points:
            st.markdown(f"- {point}")

# Final thoughts
st.subheader("Path Forward")

st.markdown("""
The complex challenge of preserving sea ice will likely require multiple complementary approaches, 
potentially including salinity reduction alongside other strategies. A recommended path forward would include:

1. **Small-scale field trials** to test different methodologies
2. **Comprehensive monitoring systems** to evaluate impacts
3. **International coordination** for governance and implementation
4. **Continued investment** in climate mitigation alongside geoengineering
5. **Adaptive approach** that evolves based on results and observations

Sea ice preservation represents one potential tool in addressing climate change, but should be 
viewed as a component of broader climate action rather than a standalone solution.
""")
