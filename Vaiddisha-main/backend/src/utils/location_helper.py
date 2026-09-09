# src/utils/location_helper.py
import gradio as gr
from country_state_city import Country, State, City

ALL_COUNTRIES = [c.name for c in Country.get_countries()]
DEFAULT_COUNTRY = "India"

def fetch_country_states(country_name: str) -> tuple[list[str], str]:
    if not country_name:
        return [], ""
    country_obj = next((c for c in Country.get_countries() if c.name == country_name), None)
    if not country_obj:
        return [], ""
    states = [s.name for s in State.get_states_of_country(country_obj.iso2)]
    return states, (states[0] if states else "")

def fetch_state_cities(country_name: str, state_name: str) -> tuple[list[str], str]:
    if not country_name or not state_name:
        return [], ""
    country_obj = next((c for c in Country.get_countries() if c.name == country_name), None)
    if not country_obj:
        return [], ""
    state_obj = next((s for s in State.get_states_of_country(country_obj.iso2) if s.name == state_name), None)
    if not state_obj:
        return [], ""
    cities = [c.name for c in City.get_cities_of_state(country_obj.iso2, state_obj.iso_code)]
    return cities, (cities[0] if cities else "")

INITIAL_STATES, DEFAULT_STATE = fetch_country_states(DEFAULT_COUNTRY)
INITIAL_CITIES, DEFAULT_CITY = fetch_state_cities(DEFAULT_COUNTRY, DEFAULT_STATE)

def get_states_for_country(country_name: str):
    states, default_st = fetch_country_states(country_name)
    cities, default_ct = fetch_state_cities(country_name, default_st)
    return (
        gr.update(choices=states, value=default_st),
        gr.update(choices=cities, value=default_ct)
    )

def get_cities_for_state(country_name: str, state_name: str):
    cities, default_ct = fetch_state_cities(country_name, state_name)
    return gr.update(choices=cities, value=default_ct)