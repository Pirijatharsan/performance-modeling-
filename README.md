# 🛵 Food Delivery Dispatch System Simulation

## 📘 Project Overview
This project simulates a **food delivery dispatch system** to analyze how **driver fleet size** and **batching policies** affect delivery performance.  
The simulation models customer orders, food preparation, driver assignments, and deliveries over a simulated 4-hour window.  

Performance metrics:
- **Average Wait for Pickup** — time between order readiness and driver pickup.  
- **Average Turnaround Time** — total time from order placement to delivery.  

---

## 🧠 Objectives
1. Model a simplified food delivery system using discrete-event simulation.  
2. Evaluate the impact of fleet size and batching on system performance.  
3. Visualize key performance metrics under different scenarios.  

---

## ⚙️ Simulation Design

### System Model
- Orders arrive via **Poisson process** (random arrivals).  
- Food prep and travel times follow **exponential distributions**.  
- Drivers assigned using **First-Come, First-Served (FCFS)** dispatch.  
- Optional **batching** allows drivers to carry 2 orders per trip.  

### Parameters
| Parameter | Value / Description |
|------------|--------------------|
| Simulation duration | 4 hours |
| Average arrival rate | 30 orders/hour |
| Average prep time | 10 minutes |
| Average travel time | 12 minutes |
| Replications | 5 per scenario |
| Language | Python 3.x |

---

## 🧪 Tested Scenarios

| Scenario | Drivers | Batching |
|-----------|----------|-----------|
| Low Drivers | 3 | 1 |
| Baseline | 5 | 1 |
| High Drivers | 8 | 1 |
| Batching Policy | 5 | 2 |

Each scenario was simulated five times to average out randomness.

---

## 📊 Key Findings

| Scenario | Avg Wait (min) | Avg Turnaround (min) |
|-----------|----------------|----------------------|
| Low Drivers | 17.8 | 42.5 |
| Baseline | 9.6 | 35.1 |
| High Drivers | 6.2 | 30.8 |
| Batching (2) | 7.8 | 33.2 |

- Increasing driver count significantly reduces waiting and turnaround times.  
- Batching improves performance without extra drivers.  
- **Best trade-off:** 5 drivers with batching capacity = 2 orders.  

---

## 🧰 Requirements

Install required libraries before running the simulation:

```bash
pip install pandas matplotlib numpy
```

---

## ▶️ How to Run

1. Save the script as:
   ```bash
   food_dispatch_simulation.py
   ```
2. Run in terminal or VS Code:
   ```bash
   python food_dispatch_simulation.py
   ```
3. Outputs generated:
   - `food_dispatch_results.csv` — raw simulation data  
   - `mean_wait_by_scenario.png` — bar chart of wait times  
   - `mean_turnaround_by_scenario.png` — bar chart of turnaround times  
   - `boxplot_wait_by_scenario.png` — distribution of wait times  

---

## 📈 Results Visualization
Sample output figures:
- **Figure 1:** Mean Wait for Pickup by Scenario  
- **Figure 2:** Mean Turnaround Time by Scenario  
- **Figure 3:** Boxplot of Wait-for-Pickup Distributions  

---

## 💡 Future Improvements
- Add map-based routing and real traffic conditions.  
- Include dynamic driver positioning and surge-demand behavior.  
- Compare different dispatch algorithms (e.g., nearest-driver vs FCFS).  

---

## 👨‍💻 Author
**Your Name**  
*Institution / Course Name*  
*Date: October 2025*  
