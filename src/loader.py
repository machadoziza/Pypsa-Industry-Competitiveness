import pandas as pd
import xarray as xr

def load_electricity_price(netcdf_path: str, node: str):
    """
    Loads marginal electricity price (LMP) for a given node
    from a PyPSA NetCDF result file.
    Returns the average price in $/MWh.
    """
    ds = xr.open_dataset(netcdf_path)
    if "marginal_price" not in ds:
        raise KeyError("NetCDF file missing 'marginal_price' variable.")

    prices = ds["marginal_price"].sel(bus=node).to_pandas()
    avg_price = prices.mean()

    return avg_price


def load_hydrogen_cost(csv_path: str):
    """
    Load hydrogen cost from a CSV file with column:
      hydrogen_cost_usd_per_kg
    If file does not exist, returns a placeholder cost.
    """
    try:
        df = pd.read_csv(csv_path)
        return df["hydrogen_cost_usd_per_kg"].iloc[0]
    except:
        # default placeholder until linked with PyPSA outputs
        return 2.5
