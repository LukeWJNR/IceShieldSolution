"""
Database module for the Sea Ice Preservation Simulator.

This module handles all database interactions for storing simulation
scenarios, results, and user favorites.
"""
import os
import json
import datetime
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database connection string from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class SimulationScenario(Base):
    """
    Stores simulation scenarios with parameters for salinity reduction simulations.
    """
    __tablename__ = 'simulation_scenarios'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Simulation parameters
    initial_salinity = Column(Float, nullable=False)
    target_salinity = Column(Float, nullable=False)
    area_km2 = Column(Float, nullable=False)
    depth_m = Column(Float, nullable=False)
    season = Column(String(20), nullable=True)
    
    # Optional parameters for more complex simulations
    grid_size = Column(Integer, default=100)
    is_favorite = Column(Boolean, default=False)

class SimulationResult(Base):
    """
    Stores results from simulations for historical tracking and comparison.
    """
    __tablename__ = 'simulation_results'
    
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer, nullable=False)
    run_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Core results
    freshwater_volume_km3 = Column(Float, nullable=False)
    currently_frozen_area = Column(Float, nullable=True)
    newly_frozen_area = Column(Float, nullable=True)
    total_frozen_area = Column(Float, nullable=True)
    
    # Additional metrics
    percent_global_desal = Column(Float, nullable=True)
    plants_needed = Column(Integer, nullable=True)
    energy_twh_total = Column(Float, nullable=True)
    
    # Serialized detailed results (JSON)
    detailed_results = Column(Text, nullable=True)

class GeoEngineeringApproach(Base):
    """
    Stores information about different geoengineering approaches for comparison.
    """
    __tablename__ = 'geoengineering_approaches'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Metrics (1-10 scale)
    effectiveness = Column(Integer, nullable=False)
    feasibility = Column(Integer, nullable=False)
    cost_efficiency = Column(Integer, nullable=False)
    environmental_impact = Column(Integer, nullable=False)
    technological_readiness = Column(Integer, nullable=False)
    scalability = Column(Integer, nullable=False)
    
    # Additional details
    methods = Column(Text, nullable=True)  # JSON list
    advantages = Column(Text, nullable=True)  # JSON list
    challenges = Column(Text, nullable=True)  # JSON list

# Database initialization function
def init_db():
    """
    Initialize the database by creating all tables if they don't exist.
    """
    Base.metadata.create_all(engine)
    
    # Add default geoengineering approaches if the table is empty
    session = Session()
    if session.query(GeoEngineeringApproach).count() == 0:
        default_approaches = [
            GeoEngineeringApproach(
                name="Salinity Reduction",
                description="Reducing the salinity of surface water to increase its freezing point and promote ice formation.",
                effectiveness=7,
                feasibility=5,
                cost_efficiency=4,
                environmental_impact=6,
                technological_readiness=4,
                scalability=6,
                methods=json.dumps(["Freshwater addition", "Desalination ships", "River diversion"]),
                advantages=json.dumps(["Works with natural freezing processes", "Potentially reversible", "Could be targeted regionally"]),
                challenges=json.dumps(["Requires large volumes of freshwater", "Logistical complexity", "Ocean mixing challenges"]),
            ),
            GeoEngineeringApproach(
                name="Ice Thickening",
                description="Pumping water onto the surface of ice sheets to freeze and thicken the ice.",
                effectiveness=6,
                feasibility=7,
                cost_efficiency=6,
                environmental_impact=7,
                technological_readiness=7,
                scalability=4,
                methods=json.dumps(["Surface pumping systems", "Renewable energy-powered pumps"]),
                advantages=json.dumps(["Directly adds ice mass", "Proven in small-scale tests", "Relatively straightforward technology"]),
                challenges=json.dumps(["Energy requirements", "Limited to existing ice areas", "Coverage limitations"]),
            ),
            GeoEngineeringApproach(
                name="Reflective Materials",
                description="Spreading reflective materials on ice surfaces to increase albedo and reduce melting.",
                effectiveness=8,
                feasibility=6,
                cost_efficiency=5,
                environmental_impact=4,
                technological_readiness=6,
                scalability=7,
                methods=json.dumps(["Glass microbeads", "Reflective films", "Engineered particles"]),
                advantages=json.dumps(["Could reduce melting by up to 30%", "Immediate effect", "Adaptable to different regions"]),
                challenges=json.dumps(["Environmental concerns", "Material dispersion", "Potential ecological impacts"]),
            ),
            GeoEngineeringApproach(
                name="Undersea Barriers",
                description="Constructing underwater curtains or barriers to block warm ocean currents from reaching ice shelves.",
                effectiveness=7,
                feasibility=3,
                cost_efficiency=2,
                environmental_impact=5,
                technological_readiness=3,
                scalability=5,
                methods=json.dumps(["Floating curtains", "Seabed anchored barriers", "Thermal screens"]),
                advantages=json.dumps(["Targets a major cause of ice shelf melting", "Could protect critical glaciers", "Long-lasting"]),
                challenges=json.dumps(["Enormous engineering challenge", "Very high costs", "Potential navigation impacts"]),
            ),
            GeoEngineeringApproach(
                name="Cloud Seeding",
                description="Enhancing snowfall over ice sheets by seeding clouds with substances like silver iodide.",
                effectiveness=5,
                feasibility=6,
                cost_efficiency=7,
                environmental_impact=5,
                technological_readiness=8,
                scalability=6,
                methods=json.dumps(["Aircraft dispersal", "Ground-based generators", "Drone systems"]),
                advantages=json.dumps(["Builds on existing technology", "Could increase ice accumulation", "Relatively low cost"]),
                challenges=json.dumps(["Weather dependency", "Uncertain efficacy", "Limited geographical application"]),
            ),
            GeoEngineeringApproach(
                name="Geotextiles",
                description="Wrapping glaciers in protective films or geotextiles to insulate them and reduce heat absorption.",
                effectiveness=4,
                feasibility=5,
                cost_efficiency=3,
                environmental_impact=6,
                technological_readiness=7,
                scalability=3,
                methods=json.dumps(["Insulating blankets", "Reflective covers", "Biodegradable films"]),
                advantages=json.dumps(["Demonstrated effectiveness in small areas", "Targeted protection", "Removable"]),
                challenges=json.dumps(["Scaling limitations", "Material requirements", "Visual impact"]),
            ),
        ]
        session.add_all(default_approaches)
        session.commit()
    session.close()

# Scenario operations
def save_scenario(name, description, initial_salinity, target_salinity, area_km2, depth_m, season, grid_size=100, is_favorite=False):
    """
    Save a simulation scenario to the database.
    
    Returns:
        The ID of the saved scenario.
    """
    session = Session()
    scenario = SimulationScenario(
        name=name,
        description=description,
        initial_salinity=initial_salinity,
        target_salinity=target_salinity,
        area_km2=area_km2,
        depth_m=depth_m,
        season=season,
        grid_size=grid_size,
        is_favorite=is_favorite
    )
    session.add(scenario)
    session.commit()
    scenario_id = scenario.id
    session.close()
    return scenario_id

def get_scenarios(favorite_only=False):
    """
    Get all simulation scenarios from the database.
    
    Args:
        favorite_only: If True, only return favorite scenarios.
        
    Returns:
        List of scenario dictionaries.
    """
    session = Session()
    query = session.query(SimulationScenario)
    if favorite_only:
        query = query.filter(SimulationScenario.is_favorite == True)
    scenarios = [
        {
            'id': s.id,
            'name': s.name,
            'description': s.description,
            'initial_salinity': s.initial_salinity,
            'target_salinity': s.target_salinity,
            'area_km2': s.area_km2,
            'depth_m': s.depth_m,
            'season': s.season,
            'grid_size': s.grid_size,
            'is_favorite': s.is_favorite,
            'created_at': s.created_at,
            'modified_at': s.modified_at
        }
        for s in query.all()
    ]
    session.close()
    return scenarios

def get_scenario(scenario_id):
    """
    Get a specific simulation scenario by ID.
    
    Returns:
        Scenario dictionary or None if not found.
    """
    session = Session()
    scenario = session.query(SimulationScenario).filter(SimulationScenario.id == scenario_id).first()
    if not scenario:
        session.close()
        return None
    
    result = {
        'id': scenario.id,
        'name': scenario.name,
        'description': scenario.description,
        'initial_salinity': scenario.initial_salinity,
        'target_salinity': scenario.target_salinity,
        'area_km2': scenario.area_km2,
        'depth_m': scenario.depth_m,
        'season': scenario.season,
        'grid_size': scenario.grid_size,
        'is_favorite': scenario.is_favorite,
        'created_at': scenario.created_at,
        'modified_at': scenario.modified_at
    }
    session.close()
    return result

def update_scenario(scenario_id, **kwargs):
    """
    Update a simulation scenario.
    
    Args:
        scenario_id: ID of the scenario to update
        **kwargs: Fields to update
        
    Returns:
        True if successful, False if scenario not found
    """
    session = Session()
    scenario = session.query(SimulationScenario).filter(SimulationScenario.id == scenario_id).first()
    if not scenario:
        session.close()
        return False
    
    for key, value in kwargs.items():
        if hasattr(scenario, key):
            setattr(scenario, key, value)
    
    scenario.modified_at = datetime.datetime.utcnow()
    session.commit()
    session.close()
    return True

def delete_scenario(scenario_id):
    """
    Delete a simulation scenario.
    
    Returns:
        True if deleted, False if not found
    """
    session = Session()
    scenario = session.query(SimulationScenario).filter(SimulationScenario.id == scenario_id).first()
    if not scenario:
        session.close()
        return False
    
    session.delete(scenario)
    session.commit()
    session.close()
    return True

# Result operations
def save_result(scenario_id, freshwater_volume_km3, currently_frozen_area=None, newly_frozen_area=None, 
               total_frozen_area=None, percent_global_desal=None, plants_needed=None, 
               energy_twh_total=None, detailed_results=None):
    """
    Save simulation results to the database.
    
    Args:
        scenario_id: ID of the scenario used for this simulation
        freshwater_volume_km3: Volume of freshwater required
        currently_frozen_area: Currently frozen area in km²
        newly_frozen_area: Newly frozen area in km²
        total_frozen_area: Total frozen area in km²
        percent_global_desal: Percentage of global desalination capacity
        plants_needed: Number of desalination plants needed
        energy_twh_total: Total energy required in TWh
        detailed_results: JSON string with detailed results
        
    Returns:
        The ID of the saved result
    """
    session = Session()
    result = SimulationResult(
        scenario_id=scenario_id,
        freshwater_volume_km3=freshwater_volume_km3,
        currently_frozen_area=currently_frozen_area,
        newly_frozen_area=newly_frozen_area,
        total_frozen_area=total_frozen_area,
        percent_global_desal=percent_global_desal,
        plants_needed=plants_needed,
        energy_twh_total=energy_twh_total,
        detailed_results=json.dumps(detailed_results) if detailed_results else None
    )
    session.add(result)
    session.commit()
    result_id = result.id
    session.close()
    return result_id

def get_results(scenario_id=None, limit=10):
    """
    Get simulation results from the database.
    
    Args:
        scenario_id: Optional ID to filter results by scenario
        limit: Maximum number of results to return
        
    Returns:
        List of result dictionaries
    """
    session = Session()
    query = session.query(SimulationResult)
    if scenario_id:
        query = query.filter(SimulationResult.scenario_id == scenario_id)
    
    query = query.order_by(SimulationResult.run_at.desc()).limit(limit)
    
    results = [
        {
            'id': r.id,
            'scenario_id': r.scenario_id,
            'run_at': r.run_at,
            'freshwater_volume_km3': r.freshwater_volume_km3,
            'currently_frozen_area': r.currently_frozen_area,
            'newly_frozen_area': r.newly_frozen_area,
            'total_frozen_area': r.total_frozen_area,
            'percent_global_desal': r.percent_global_desal,
            'plants_needed': r.plants_needed,
            'energy_twh_total': r.energy_twh_total,
            'detailed_results': json.loads(r.detailed_results) if r.detailed_results else None
        }
        for r in query.all()
    ]
    session.close()
    return results

# Geoengineering approach operations
def get_geoengineering_approaches():
    """
    Get all geoengineering approaches from the database.
    
    Returns:
        List of approach dictionaries
    """
    session = Session()
    approaches = [
        {
            'id': a.id,
            'name': a.name,
            'description': a.description,
            'effectiveness': a.effectiveness,
            'feasibility': a.feasibility,
            'cost_efficiency': a.cost_efficiency,
            'environmental_impact': a.environmental_impact,
            'technological_readiness': a.technological_readiness,
            'scalability': a.scalability,
            'methods': json.loads(a.methods) if a.methods else [],
            'advantages': json.loads(a.advantages) if a.advantages else [],
            'challenges': json.loads(a.challenges) if a.challenges else []
        }
        for a in session.query(GeoEngineeringApproach).all()
    ]
    session.close()
    return approaches

# Initialize database on module import
init_db()