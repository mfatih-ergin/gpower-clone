import csv
import os

oracle_scenarios = [
    # --- A-PRIORI (N hesaplama) ---
    # Standart ve dengeli (ratio = 1)
    {"id": "V01", "mode": "a-priori", "tails": 1, "d": 0.5, "alpha": 0.05, "power": 0.95, "ratio": 1.0, "n1": "", "n2": ""},
    {"id": "V02", "mode": "a-priori", "tails": 2, "d": 0.5, "alpha": 0.05, "power": 0.95, "ratio": 1.0, "n1": "", "n2": ""},
    {"id": "V03", "mode": "a-priori", "tails": 2, "d": 0.2, "alpha": 0.05, "power": 0.80, "ratio": 1.0, "n1": "", "n2": ""},
    {"id": "V04", "mode": "a-priori", "tails": 2, "d": 0.8, "alpha": 0.05, "power": 0.80, "ratio": 1.0, "n1": "", "n2": ""},
    {"id": "V05", "mode": "a-priori", "tails": 1, "d": 0.3, "alpha": 0.01, "power": 0.90, "ratio": 1.0, "n1": "", "n2": ""},
    {"id": "V06", "mode": "a-priori", "tails": 2, "d": 0.6, "alpha": 0.01, "power": 0.99, "ratio": 1.0, "n1": "", "n2": ""},
    {"id": "V07", "mode": "a-priori", "tails": 2, "d": 1.0, "alpha": 0.05, "power": 0.85, "ratio": 1.0, "n1": "", "n2": ""},
    {"id": "V08", "mode": "a-priori", "tails": 1, "d": 0.4, "alpha": 0.05, "power": 0.80, "ratio": 1.0, "n1": "", "n2": ""},

    # Dengesiz gruplar (ratio != 1) - kritik ödev testi
    {"id": "V09", "mode": "a-priori", "tails": 2, "d": 0.5, "alpha": 0.05, "power": 0.80, "ratio": 2.0, "n1": "", "n2": ""},
    {"id": "V10", "mode": "a-priori", "tails": 2, "d": 0.5, "alpha": 0.05, "power": 0.80, "ratio": 0.5, "n1": "", "n2": ""},
    {"id": "V11", "mode": "a-priori", "tails": 1, "d": 0.5, "alpha": 0.05, "power": 0.90, "ratio": 1.5, "n1": "", "n2": ""},
    {"id": "V12", "mode": "a-priori", "tails": 2, "d": 0.3, "alpha": 0.01, "power": 0.85, "ratio": 3.0, "n1": "", "n2": ""},
    {"id": "V13", "mode": "a-priori", "tails": 2, "d": 0.7, "alpha": 0.05, "power": 0.95, "ratio": 0.75, "n1": "", "n2": ""},
    {"id": "V14", "mode": "a-priori", "tails": 1, "d": 0.25, "alpha": 0.05, "power": 0.80, "ratio": 1.25, "n1": "", "n2": ""},

    # Sınır değerler (Boundary values)
    {"id": "V15", "mode": "a-priori", "tails": 2, "d": 0.1, "alpha": 0.05, "power": 0.80, "ratio": 1.0, "n1": "", "n2": ""}, # çok küçük etki
    {"id": "V16", "mode": "a-priori", "tails": 2, "d": 1.5, "alpha": 0.05, "power": 0.99, "ratio": 1.0, "n1": "", "n2": ""}, # çok büyük etki
    {"id": "V17", "mode": "a-priori", "tails": 1, "d": 0.5, "alpha": 0.001, "power": 0.99, "ratio": 1.0, "n1": "", "n2": ""}, # çok katı alpha
    {"id": "V18", "mode": "a-priori", "tails": 2, "d": 0.8, "alpha": 0.05, "power": 0.999, "ratio": 1.0, "n1": "", "n2": ""}, # aşırı yüksek güç
    {"id": "V19", "mode": "a-priori", "tails": 2, "d": 0.5, "alpha": 0.05, "power": 0.80, "ratio": 4.0, "n1": "", "n2": ""}, # aşırı dengesiz oran
    {"id": "V20", "mode": "a-priori", "tails": 1, "d": 0.5, "alpha": 0.05, "power": 0.80, "ratio": 0.25, "n1": "", "n2": ""}, # aşırı dengesiz ters oran

    # --- POST-HOC (Güç hesaplama) ---
    {"id": "V21", "mode": "post-hoc", "tails": 1, "d": 0.5, "alpha": 0.05, "power": "", "ratio": "", "n1": 88, "n2": 88},
    {"id": "V22", "mode": "post-hoc", "tails": 2, "d": 0.5, "alpha": 0.05, "power": "", "ratio": "", "n1": 64, "n2": 64},
    {"id": "V23", "mode": "post-hoc", "tails": 2, "d": 0.2, "alpha": 0.05, "power": "", "ratio": "", "n1": 100, "n2": 100},
    {"id": "V24", "mode": "post-hoc", "tails": 2, "d": 0.8, "alpha": 0.01, "power": "", "ratio": "", "n1": 30, "n2": 30},
    {"id": "V25", "mode": "post-hoc", "tails": 1, "d": 0.4, "alpha": 0.05, "power": "", "ratio": "", "n1": 50, "n2": 100}, # dengesiz örneklem
    {"id": "V26", "mode": "post-hoc", "tails": 2, "d": 0.6, "alpha": 0.05, "power": "", "ratio": "", "n1": 20, "n2": 40},
    {"id": "V27", "mode": "post-hoc", "tails": 2, "d": 1.2, "alpha": 0.01, "power": "", "ratio": "", "n1": 15, "n2": 15},
    {"id": "V28", "mode": "post-hoc", "tails": 1, "d": 0.15, "alpha": 0.05, "power": "", "ratio": "", "n1": 200, "n2": 200},
    {"id": "V29", "mode": "post-hoc", "tails": 2, "d": 0.5, "alpha": 0.05, "power": "", "ratio": "", "n1": 5, "n2": 5}, # küçük sınır örneklem
    {"id": "V30", "mode": "post-hoc", "tails": 2, "d": 0.3, "alpha": 0.001, "power": "", "ratio": "", "n1": 150, "n2": 300}
]

out_path = r"c:\Users\Pc\OneDrive\Desktop\Yazılım Gerçekleme ve Test Ödev 5\oracle\oracle_inputs.csv"
fieldnames = ["id", "mode", "tails", "d", "alpha", "power", "ratio", "n1", "n2", "expected_ncp", "expected_critical_t", "expected_df", "expected_n1", "expected_n2", "expected_n_total", "expected_actual_power"]

with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in oracle_scenarios:
        writer.writerow(row)

print("Created oracle template with 30 scenarios at:", out_path)
