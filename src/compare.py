import pandas as pd
def load_global_benchmarks(path="data/global_benchmarks.csv"):
    """
    Loads global benchmark costs.
    Returns a pandas DataFrame.
    """
    return pd.read_csv(path)
def get_global_best_cost(df, sector, route):
    """
    Finds the minimum cost among all regions for the given sector and route.
    """
    subset = df[(df["sector"] == sector) & (df["route"] == route)]
    if subset.empty:
        raise ValueError(f"No global benchmark found for {sector}-{route}")
    return subset["cost_usd_per_ton"].min()
def compute_competitiveness(local_cost, global_cost):
    """
    Computes competitiveness index:
    <1.1 = competitive, 1.1-1.3 = at risk, >1.3 = uncompetitive
    """
    index = local_cost / global_cost
    if index < 1.1:
        status = "competitive"
    elif index <= 1.3:
        status = "at risk"
    else:
        status = "uncompetitive"
    return {"index": index, "status": status}
def evaluate_competitiveness(sector, route, local_cost,
                             benchmarks_path="data/global_benchmarks.csv"):
    """
    User-friendly function: input sector, route, local cost.
    Returns competitiveness index and status.
    """
    df = load_global_benchmarks(benchmarks_path)
    global_cost = get_global_best_cost(df, sector, route)
    return compute_competitiveness(local_cost, global_cost)
if __name__ == "__main__":
    # Example usage
    local_cost = 612  # USD/ton for DRI-H2 steel
    result = evaluate_competitiveness("steel", "DRI-H2", local_cost)
    print(result)
