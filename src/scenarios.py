import yaml
def load_scenarios(path="data/scenario_settings.yaml"):
    """
    Load scenario multipliers from YAML file.
    Returns a dictionary of scenarios.
    """
    with open(path, "r") as f:
        scenarios = yaml.safe_load(f)
    return scenarios["scenarios"]
def apply_scenario(local_cost, scenario_name, path="data/scenario_settings.yaml"):
    """
    Adjusts local cost based on a scenario:
    - tariff_multiplier
    - cbam_cost_addition
    - shipping_cost_usd_per_ton
    """
    scenarios = load_scenarios(path)
    
    if scenario_name not in scenarios:
        raise ValueError(f"Scenario {scenario_name} not found")
    
    s = scenarios[scenario_name]
    
    adjusted_cost = local_cost * s["tariff_multiplier"] + s["cbam_cost_addition"] + s["shipping_cost_usd_per_ton"]
    
    return adjusted_cost
if __name__ == "__main__":
    base_cost = 500
    scenario_name = "fragmented"
    adjusted = apply_scenario(base_cost, scenario_name)
    print(f"Base cost: {base_cost}, Scenario: {scenario_name}, Adjusted cost: {adjusted}")
