import streamlit as st
import numpy as np
from utils.visualizations import plot_freezing_point_curve, plot_ice_albedo_feedback
from utils.calculations import calculate_freezing_point

st.title("Salinity and Sea Ice Formation")

st.markdown("""
## The Relationship Between Salinity and Sea Ice

Salinity is a critical factor in sea ice formation. This page explains how salinity affects freezing points
and how reducing salinity could help preserve and expand sea ice.
""")

# Freezing point curve
st.subheader("How Salinity Affects Freezing Point")
st.markdown("""
Freshwater freezes at 0°C, but seawater freezes at lower temperatures due to dissolved salts.
The relationship between salinity and freezing point is approximately linear:

**The higher the salinity, the lower the freezing point.**

The interactive chart below shows this relationship:
""")

freezing_curve = plot_freezing_point_curve(0, 40)
st.plotly_chart(freezing_curve, use_container_width=True)

# Interactive freezing point calculator
st.subheader("Freezing Point Calculator")
st.markdown("""
Use this calculator to see how changes in salinity affect the freezing point of seawater.
""")

col1, col2 = st.columns(2)

with col1:
    initial_salinity = st.slider("Initial salinity (PSU)", 30.0, 35.0, 32.0, 0.1)
    initial_freezing_point = calculate_freezing_point(initial_salinity)
    st.metric("Freezing point", f"{initial_freezing_point:.2f}°C")

with col2:
    target_salinity = st.slider("Target salinity after reduction (PSU)", 28.0, initial_salinity, 30.0, 0.1)
    target_freezing_point = calculate_freezing_point(target_salinity)
    st.metric("New freezing point", f"{target_freezing_point:.2f}°C")
    
st.info(f"""
By reducing the salinity from {initial_salinity} PSU to {target_salinity} PSU, 
the freezing point would increase from {initial_freezing_point:.2f}°C to {target_freezing_point:.2f}°C.

This {target_freezing_point - initial_freezing_point:.2f}°C increase in the freezing point 
means that water would freeze at a higher temperature, potentially allowing more ice to form.
""")

# Arctic salinity information
st.subheader("Arctic Ocean Salinity")
st.markdown("""
The Arctic Ocean has unique salinity characteristics compared to other oceans:

- **Mean Arctic Ocean salinity**: Typically ranges from 30 to 34 PSU
- **Global average ocean salinity**: About 35 PSU

The Arctic has lower salinity because of:
1. Large freshwater input from rivers (like the Ob, Lena, and Mackenzie)
2. Melting ice in summer
3. Limited evaporation due to cold temperatures
4. Limited exchange with saltier oceans

This naturally lower salinity makes the Arctic more conducive to ice formation than other oceans.
""")

# Ice-Albedo Feedback
st.subheader("The Ice-Albedo Feedback Loop")
st.markdown("""
Sea ice plays a critical role in Earth's climate system through the ice-albedo feedback mechanism:

- **Albedo** is a measure of reflectivity
- Ice has high albedo (reflects sunlight)
- Ocean water has low albedo (absorbs sunlight)

When sea ice melts, more ocean is exposed, absorbing more heat, which causes more ice to melt. 
This creates a positive feedback loop accelerating warming.

By preserving and expanding sea ice through salinity reduction, we can help maintain
Earth's reflectivity and slow down warming.
""")

feedback_diagram = plot_ice_albedo_feedback()
st.plotly_chart(feedback_diagram, use_container_width=True)

st.subheader("Why Focus on Salinity?")
st.markdown("""
Reducing salinity is a potentially promising approach to sea ice preservation because:

1. **It works with natural processes**: It enhances the ocean's natural freezing mechanism
2. **Scalability potential**: It could be applied across regions with varying interventions
3. **Reversibility**: Unlike some geoengineering approaches, its effects are not permanent
4. **Complements other strategies**: It can work alongside other climate mitigation efforts

The next sections will explore the practical aspects of implementing salinity reduction and its potential impact.
""")
