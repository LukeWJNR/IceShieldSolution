import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.calculations import calculate_freezing_point

def plot_freezing_point_curve(min_salinity=0, max_salinity=40):
    """
    Plot the relationship between salinity and freezing point.
    
    Parameters:
    -----------
    min_salinity : float
        Minimum salinity value for the plot
    max_salinity : float
        Maximum salinity value for the plot
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object containing the freezing point curve
    """
    # Generate salinity values
    salinity_values = np.linspace(min_salinity, max_salinity, 100)
    
    # Calculate corresponding freezing points
    freezing_points = [calculate_freezing_point(s) for s in salinity_values]
    
    # Create the plot
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=salinity_values, 
            y=freezing_points,
            mode='lines',
            name='Freezing Point',
            line=dict(color='blue', width=3)
        )
    )
    
    # Add annotations for notable points
    fig.add_annotation(
        x=35, y=calculate_freezing_point(35),
        text="Global Average Ocean (35 PSU)",
        showarrow=True,
        arrowhead=1
    )
    
    fig.add_annotation(
        x=32, y=calculate_freezing_point(32),
        text="Typical Arctic Ocean (30-34 PSU)",
        showarrow=True,
        arrowhead=1
    )
    
    fig.add_annotation(
        x=0, y=calculate_freezing_point(0),
        text="Freshwater (0 PSU)",
        showarrow=True,
        arrowhead=1
    )
    
    # Set axis labels and title
    fig.update_layout(
        title="Relationship Between Salinity and Freezing Point",
        xaxis_title="Salinity (PSU)",
        yaxis_title="Freezing Point (°C)",
        hovermode="x unified"
    )
    
    return fig

def plot_freshwater_requirements(results):
    """
    Create a bar chart showing the freshwater requirements compared to various references.
    
    Parameters:
    -----------
    results : dict
        Dictionary containing calculation results
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object containing the bar chart
    """
    # Extract river comparison data
    river_data = {
        'Freshwater Required': results['freshwater_volume_km3'],
        'Annual Amazon River Flow': 5500,
        'Annual Mississippi River Flow': 580,
        'Annual Rhine River Flow': 70,
        'Global Annual Desalination Capacity': 36.5
    }
    
    # Create the plot
    fig = go.Figure()
    
    for name, value in river_data.items():
        fig.add_trace(
            go.Bar(
                x=[name],
                y=[value],
                name=name
            )
        )
    
    # Set axis labels and title
    fig.update_layout(
        title="Freshwater Volume Required Compared to Natural Sources (km³)",
        yaxis_title="Volume (km³)",
        height=500
    )
    
    return fig

def plot_arctic_map(currently_frozen, newly_frozen, grid_size=100):
    """
    Create a visualization of the Arctic with currently frozen and newly frozen areas.
    
    Parameters:
    -----------
    currently_frozen : numpy.ndarray
        Binary array indicating currently frozen areas
    newly_frozen : numpy.ndarray
        Binary array indicating newly frozen areas
    grid_size : int
        Size of the grid for visualization
        
    Returns:
    --------
    matplotlib.figure.Figure
        Matplotlib figure containing the Arctic map
    """
    # Create a simplified Arctic map visualization
    # In a real application, you would use actual geographical data
    
    # Create a circular mask to represent the Arctic Ocean
    y, x = np.ogrid[-grid_size//2:grid_size//2, -grid_size//2:grid_size//2]
    mask = x**2 + y**2 <= (grid_size//2)**2
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot the base map (ocean)
    ax.imshow(np.ones((grid_size, grid_size))*0.8, cmap='Blues', vmin=0, vmax=1)
    
    # Plot currently frozen areas
    frozen_map = np.zeros((grid_size, grid_size))
    frozen_map[currently_frozen & mask] = 1
    ax.imshow(frozen_map, cmap='Greys', alpha=0.7, vmin=0, vmax=1)
    
    # Plot newly frozen areas
    new_frozen_map = np.zeros((grid_size, grid_size))
    new_frozen_map[newly_frozen & mask] = 1
    ax.imshow(new_frozen_map, cmap='Greens', alpha=0.7, vmin=0, vmax=1)
    
    # Add legend elements
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='lightgrey', alpha=0.7, label='Currently Frozen'),
        Patch(facecolor='lightgreen', alpha=0.7, label='Newly Frozen Area'),
        Patch(facecolor='lightblue', label='Ocean')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Set title and remove axis ticks
    ax.set_title('Arctic Sea Ice: Current and Potential Expansion')
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig

def plot_geoengineering_comparison():
    """
    Create a comparison chart of different geoengineering approaches.
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object containing the comparison chart
    """
    # Import here to avoid circular imports
    from utils.database import get_geoengineering_approaches
    
    # Get approaches from database
    approaches_data = get_geoengineering_approaches()
    
    # Create lists to store data
    approaches = []
    effectiveness = []
    feasibility = []
    cost_efficiency = []
    environmental_impact = []
    technological_readiness = []
    scalability = []
    
    # Extract data from database results
    for approach in approaches_data:
        approaches.append(approach['name'])
        effectiveness.append(approach['effectiveness'])
        feasibility.append(approach['feasibility'])
        cost_efficiency.append(approach['cost_efficiency'])
        environmental_impact.append(approach['environmental_impact'])
        technological_readiness.append(approach['technological_readiness'])
        scalability.append(approach['scalability'])
    
    # Create the plot
    fig = go.Figure()
    
    # Define categories for the radar chart
    categories = ['Effectiveness', 'Feasibility', 'Cost Efficiency', 
                 'Environmental Impact', 'Tech Readiness', 'Scalability']
    
    # Add traces for each approach
    for i, approach in enumerate(approaches):
        fig.add_trace(
            go.Scatterpolar(
                r=[effectiveness[i], feasibility[i], cost_efficiency[i], 
                   environmental_impact[i], technological_readiness[i], 
                   scalability[i], effectiveness[i]],  # Close the loop by repeating the first point
                theta=categories + [categories[0]],
                fill='toself',
                name=approach
            )
        )
    
    # Set layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        title="Comparison of Geoengineering Approaches",
        height=600
    )
    
    return fig

def plot_ice_albedo_feedback():
    """
    Create a visualization of the ice-albedo feedback loop.
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure object containing the visualization
    """
    # Define the nodes and their positions
    nodes = {
        "Sea Ice": {"x": 0, "y": 0},
        "Surface Albedo": {"x": -1, "y": -1},
        "Solar Energy Absorption": {"x": 1, "y": -1},
        "Surface Temperature": {"x": 0, "y": -2},
    }
    
    # Create the plot
    fig = go.Figure()
    
    # Add nodes
    for node, pos in nodes.items():
        fig.add_trace(
            go.Scatter(
                x=[pos["x"]], 
                y=[pos["y"]],
                mode='markers+text',
                marker=dict(size=30, color='lightblue'),
                text=node,
                textposition="middle center",
                name=node
            )
        )
    
    # Add arrows
    arrows = [
        # Positive feedback loop (clockwise)
        {"from": "Sea Ice", "to": "Surface Albedo", "label": "+", "color": "blue"},
        {"from": "Surface Albedo", "to": "Solar Energy Absorption", "label": "-", "color": "blue"},
        {"from": "Solar Energy Absorption", "to": "Surface Temperature", "label": "+", "color": "red"},
        {"from": "Surface Temperature", "to": "Sea Ice", "label": "-", "color": "red"},
    ]
    
    for arrow in arrows:
        start = nodes[arrow["from"]]
        end = nodes[arrow["to"]]
        
        # Calculate the midpoint for the annotation
        mid_x = (start["x"] + end["x"]) / 2
        mid_y = (start["y"] + end["y"]) / 2
        
        # Add arrow
        fig.add_annotation(
            x=end["x"],
            y=end["y"],
            ax=start["x"],
            ay=start["y"],
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor=arrow["color"]
        )
        
        # Add label
        fig.add_annotation(
            x=mid_x,
            y=mid_y,
            text=arrow["label"],
            showarrow=False,
            font=dict(size=20, color=arrow["color"])
        )
    
    # Set layout
    fig.update_layout(
        title="Ice-Albedo Feedback Loop",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-2, 2]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-3, 1],
            scaleanchor="x",
            scaleratio=1
        ),
        showlegend=False,
        height=500
    )
    
    return fig
