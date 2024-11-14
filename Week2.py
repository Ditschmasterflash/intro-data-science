import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("umsatzdaten_gekuerzt.csv")

warengruppen_map = {
    1: "Brot",
    2: "Brötchen",
    3: "Croissant",
    4: "Konditorei",
    5: "Kuchen",
    6: "Saisonbrot",
}

df["Produktgruppe"] = df["Warengruppe"].map(warengruppen_map)

print(df.head())

umsatz_per_day = df.groupby("Datum")["Umsatz"].sum().reset_index()
print(umsatz_per_day)

umsatz_per_day["Day"] = pd.to_datetime(umsatz_per_day["Datum"]).dt.strftime("%A")
day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
umsatz_per_day["Day"] = pd.Categorical(
    umsatz_per_day["Day"], categories=day_order, ordered=True
)
umsatz_per_day = umsatz_per_day.sort_values("Day")
print(umsatz_per_day)

mean_values = umsatz_per_day.groupby("Day")["Umsatz"].mean().reindex(day_order)
sem_values = umsatz_per_day.groupby("Day")["Umsatz"].sem().reindex(day_order)

plt.figure(figsize=(10, 6))
confidence_interval = 1.96 * sem_values  # 95% confidence interval
plt.bar(day_order, mean_values, yerr=confidence_interval, capsize=5)
plt.title("Average Daily Sales with 95% Confidence Interval")
plt.xlabel("Day of Week")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
