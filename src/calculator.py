import pandas as pd
def load_sector_params(path="data/sector_te_params.csv"):
    """
    Loads techno-economic parameters for all sectors.
    Returns a pandas DataFrame.
    """
    return pd.read_csv(path)
def get_sector_route_params(df, sector, route):
    """
    Extract parameters for a specific sector and route.
    Example: sector='steel', route='DRI-H2'
    """
    row = df[(df["sector"] == sector) & (df["route"] == route)]
    if row.empty:
        raise ValueError(f"No parameters found for {sector}-{route}")
    return row.squeeze()
def compute_cost_per_ton(params, electricity_price, hydrogen_cost):
    """
    Computes local industrial production cost per tonne.

    Inputs:
    - params: row from sector_te_params.csv
    - electricity_price: $/MWh
    - hydrogen_cost: $/kg

    Returns a cost breakdown and total cost.
    """

    # Energy costs
    elec_cost = params["electricity_mwh_per_ton"] * electricity_price
    h2_cost = params["hydrogen_kg_per_ton"] * hydrogen_cost
    gas_cost = params["gas_gj_per_ton"] * 3  # placeholder: $3/GJ gas

    # CAPEX annualization (very simplified)
    capex_cost = params["capex_usd_per_ton"]

    # OPEX and labor
    opex_cost = params["opex_usd_per_ton"]
    labor_cost = params["labor_usd_per_ton"]

    total = elec_cost + h2_cost + gas_cost + capex_cost + opex_cost + labor_cost

    return {
        "electricity_cost": elec_cost,
        "hydrogen_cost": h2_cost,
        "gas_cost": gas_cost,
        "capex_cost": capex_cost,
        "opex_cost": opex_cost,
        "labor_cost": labor_cost,
        "total_cost": total
    }
def calculate_local_cost(sector, route, electricity_price, hydrogen_cost,
                         path="data/sector_te_params.csv"):
    """
    High-level wrapper: user provides sector, route, and energy prices.
    Returns cost breakdown and total cost.
    """
    df = load_sector_params(path)
    params = get_sector_route_params(df, sector, route)
    return compute_cost_per_ton(params, electricity_price, hydrogen_cost)
if __name__ == "__main__":
    # Example quick test
    result = calculate_local_cost(
        sector="steel",
        route="DRI-H2",
        electricity_price=60,  # $/MWh
        hydrogen_cost=4.5      # $/kg
    )
    print(result)

