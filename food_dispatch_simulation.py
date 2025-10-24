"""
Food Delivery Dispatch System Simulation
----------------------------------------
Simulates a food delivery platform to study how
driver fleet size and batching policies affect:
 - Average wait-for-pickup time
 - Average total turnaround time


"""

import random
import math
import heapq
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --------------------------
# Simulation Components
# --------------------------

class Order:
    def __init__(self, order_id, t_order, prep_time, travel_time):
        self.order_id = order_id
        self.t_order = t_order
        self.prep_time = prep_time
        self.t_ready = t_order + prep_time
        self.travel_time = travel_time
        self.t_pickup = None
        self.t_delivered = None


def exponential(mean):
    """Generate exponential random variable."""
    return random.expovariate(1.0 / mean)


def run_simulation(sim_time_hours=4.0,
                   arrival_rate_per_hour=30.0,
                   prep_mean_minutes=10.0,
                   travel_mean_minutes=12.0,
                   n_drivers=5,
                   batching_max=1,
                   seed=None):
    """
    Discrete-event simulation for a food delivery dispatch system.
    """

    if seed is not None:
        random.seed(seed)

    # Time conversions
    sim_time = sim_time_hours * 60  # in minutes
    arrival_rate_per_minute = arrival_rate_per_hour / 60.0

    # State variables
    current_time = 0.0
    order_id = 0
    events = []  # (time, event_type, data)
    ready_orders = []
    available_drivers = list(range(n_drivers))
    active_orders = []

    # Schedule first order
    next_arrival = exponential(1.0 / arrival_rate_per_minute)
    heapq.heappush(events, (next_arrival, "new_order", None))

    orders = []

    # Run simulation loop
    while events:
        t, event, data = heapq.heappop(events)
        current_time = t

        # Stop condition
        if current_time > sim_time:
            break

        if event == "new_order":
            # Create new order
            prep_time = exponential(prep_mean_minutes)
            travel_time = exponential(travel_mean_minutes)
            order = Order(order_id, current_time, prep_time, travel_time)
            orders.append(order)

            # Schedule order ready event
            heapq.heappush(events, (order.t_ready, "order_ready", order))
            order_id += 1

            # Schedule next arrival
            next_arrival = current_time + exponential(1.0 / arrival_rate_per_minute)
            if next_arrival <= sim_time:
                heapq.heappush(events, (next_arrival, "new_order", None))

        elif event == "order_ready":
            ready_orders.append(data)
            # Dispatch if possible
            if available_drivers and ready_orders:
                dispatch_driver(current_time, events, available_drivers, ready_orders, batching_max)

        elif event == "driver_free":
            driver_id = data
            available_drivers.append(driver_id)
            if ready_orders:
                dispatch_driver(current_time, events, available_drivers, ready_orders, batching_max)

    # Simulation complete
    df = pd.DataFrame([{
        "order_id": o.order_id,
        "t_order": o.t_order,
        "t_ready": o.t_ready,
        "t_pickup": o.t_pickup,
        "t_delivered": o.t_delivered,
        "wait_time": (o.t_pickup - o.t_ready) if o.t_pickup else None,
        "turnaround_time": (o.t_delivered - o.t_order) if o.t_delivered else None
    } for o in orders if o.t_pickup is not None])

    return df


def dispatch_driver(current_time, events, available_drivers, ready_orders, batching_max):
    """Assign available driver to ready orders."""
    if not available_drivers:
        return

    driver_id = available_drivers.pop(0)
    batch_size = min(batching_max, len(ready_orders))
    assigned_orders = [ready_orders.pop(0) for _ in range(batch_size)]

    max_prep_delay = 0
    total_travel = 0
    for o in assigned_orders:
        o.t_pickup = current_time
        o.t_delivered = current_time + o.travel_time
        total_travel = max(total_travel, o.travel_time)
        max_prep_delay = max(max_prep_delay, o.t_pickup - o.t_ready)

    # Schedule driver free event
    heapq.heappush(events, (current_time + total_travel, "driver_free", driver_id))


# --------------------------
# Experiment Setup
# --------------------------

def run_experiments():
    scenarios = [
        {"name": "Low Drivers (3)", "n_drivers": 3, "batching_max": 1},
        {"name": "Baseline (5)", "n_drivers": 5, "batching_max": 1},
        {"name": "High Drivers (8)", "n_drivers": 8, "batching_max": 1},
        {"name": "Batching (5x2)", "n_drivers": 5, "batching_max": 2},
    ]

    all_results = []

    for sc in scenarios:
        for rep in range(5):
            df = run_simulation(
                sim_time_hours=4,
                arrival_rate_per_hour=30,
                prep_mean_minutes=10,
                travel_mean_minutes=12,
                n_drivers=sc["n_drivers"],
                batching_max=sc["batching_max"],
                seed=rep
            )
            df["scenario"] = sc["name"]
            df["rep"] = rep
            all_results.append(df)

    results = pd.concat(all_results, ignore_index=True)
    return results


# --------------------------
# Visualization
# --------------------------

def plot_results(results):
    summary = results.groupby("scenario").agg(
        mean_wait=("wait_time", "mean"),
        mean_turnaround=("turnaround_time", "mean"),
        std_wait=("wait_time", "std"),
        std_turn=("turnaround_time", "std")
    ).reset_index()

    print("\n--- SUMMARY RESULTS ---")
    print(summary)

    plt.figure(figsize=(8, 5))
    plt.bar(summary["scenario"], summary["mean_wait"], yerr=summary["std_wait"], capsize=5)
    plt.title("Mean Wait-for-Pickup by Scenario")
    plt.ylabel("Minutes")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("mean_wait_by_scenario.png")

    plt.figure(figsize=(8, 5))
    plt.bar(summary["scenario"], summary["mean_turnaround"], yerr=summary["std_turn"], capsize=5)
    plt.title("Mean Turnaround Time by Scenario")
    plt.ylabel("Minutes")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("mean_turnaround_by_scenario.png")

    plt.figure(figsize=(8, 5))
    results.boxplot(column="wait_time", by="scenario", grid=False)
    plt.title("Distribution of Wait Times by Scenario")
    plt.suptitle("")
    plt.ylabel("Minutes")
    plt.tight_layout()
    plt.savefig("boxplot_wait_by_scenario.png")

    plt.show()


# --------------------------
# Main Execution
# --------------------------

if __name__ == "__main__":
    results = run_experiments()
    results.to_csv("food_dispatch_results.csv", index=False)
    plot_results(results)
    print("\nSimulation complete! Charts and CSV have been saved.")
