import streamlit as st

st.set_page_config(
    page_title="Sea Ice Preservation Simulator",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Sea Ice Preservation through Salinity Reduction")

st.markdown("""
## Welcome to the Sea Ice Preservation Simulator

This interactive tool allows you to explore how reducing ocean surface salinity 
could help preserve and expand sea ice formation in polar regions, particularly the Arctic.

### What You Can Do:

1. **Learn** about the relationship between salinity and sea ice formation
2. **Calculate** freshwater requirements for salinity reduction
3. **Simulate** potential ice expansion based on salinity changes
4. **Compare** different geoengineering approaches
5. **Save** your simulation scenarios and results to the database

### Why This Matters:

> "The preservation of sea ice is vital for maintaining Earth's climate balance and protecting delicate 
> marine ecosystems. By understanding the dynamics of salinity and its connection to sea ice formation, 
> we can explore possible interventions to preserve sea ice and mitigate the impacts of climate change."

Use the sidebar to navigate between different sections of the application.
""")

st.subheader("Key Concepts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Salinity and Ice Formation
    
    - Freshwater (lower salinity) has a higher freezing point than saltwater
    - When surface water salinity decreases, ice formation becomes easier
    - Lower salinity helps create stratification, with fresher water staying at the surface
    - This stratification insulates ice from warmer water below
    """)
    
with col2:
    st.markdown("""
    ### Climate Benefits of Sea Ice
    
    - Sea ice reflects sunlight (high albedo), reducing heat absorption
    - When ice melts, darker ocean water absorbs more heat (feedback loop)
    - Preserving ice helps maintain this reflectivity
    - Ice formation also affects ocean circulation patterns
    """)

st.subheader("Explore the Simulator")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    Navigate through the pages in the sidebar to explore different aspects of sea ice 
    preservation through salinity reduction. Each page focuses on a specific topic and 
    provides interactive tools to help you understand the concepts.

    **Get started by selecting a page from the sidebar!**
    """)

with col2:
    st.success("""
    ### New Database Feature!
    
    You can now save your simulation scenarios and results to a database for future reference.
    
    - Save your favorite parameter combinations
    - Track simulation history
    - Compare different approaches
    
    Check out the **Saved Simulations** page in the sidebar.
    """)
