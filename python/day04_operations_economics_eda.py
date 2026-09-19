from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"data/processed/namma_yatri_bengaluru_cleaned.csv"
OUTPUT=ROOT/"data/processed/day04_operations_economics_summary.csv"
FIGURES=ROOT/"reports/figures/day04"
FIGURES.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(INPUT)
wards=df[df["Ward"].astype(str).str.strip()!="Bangalore Total"].copy()
for c in ["Bookings","Completed_Trips","Cancelled_Bookings","Booking_Cancellation_Rate","Average_Distance_Per_Trip_Km","Average_Fare_Per_Trip","Drivers_Earnings","Distance_Travelled_Km","Conversion_Rate"]:
    wards[c]=pd.to_numeric(wards[c],errors="coerce")
wards["Completion_Rate_From_Bookings"]=np.where(wards.Bookings>0,wards.Completed_Trips/wards.Bookings*100,np.nan)
wards["Cancellation_Rate_Calculated"]=np.where(wards.Bookings>0,wards.Cancelled_Bookings/wards.Bookings*100,np.nan)
wards["Estimated_Fare_Revenue"]=wards.Completed_Trips*wards.Average_Fare_Per_Trip
wards["Estimated_Earnings_Per_Completed_Trip"]=np.where(wards.Completed_Trips>0,wards.Drivers_Earnings/wards.Completed_Trips,np.nan)
wards["Estimated_Distance_Per_Completed_Trip_Km"]=np.where(wards.Completed_Trips>0,wards.Distance_Travelled_Km/wards.Completed_Trips,np.nan)
cols=["Ward","Bookings","Completed_Trips","Cancelled_Bookings","Booking_Cancellation_Rate","Completion_Rate_From_Bookings","Average_Distance_Per_Trip_Km","Average_Fare_Per_Trip","Drivers_Earnings","Distance_Travelled_Km","Estimated_Fare_Revenue","Estimated_Earnings_Per_Completed_Trip","Estimated_Distance_Per_Completed_Trip_Km"]
wards[cols].to_csv(OUTPUT,index=False)
for col,xlabel,title,name in [("Booking_Cancellation_Rate","Booking Cancellation Rate (%)","Top 10 Wards by Booking Cancellation Rate","top10_cancellation_rate.png"),("Average_Fare_Per_Trip","Average Fare per Trip","Top 10 Wards by Average Fare per Trip","top10_average_fare.png")]:
    p=wards.nlargest(10,col).sort_values(col)
    plt.figure(figsize=(10,6)); plt.barh(p.Ward,p[col]); plt.xlabel(xlabel); plt.ylabel("Ward"); plt.title(title); plt.tight_layout(); plt.savefig(FIGURES/name,dpi=160); plt.close()
plt.figure(figsize=(8,6)); plt.scatter(wards.Average_Distance_Per_Trip_Km,wards.Average_Fare_Per_Trip,alpha=.65); plt.xlabel("Average Distance per Trip (km)"); plt.ylabel("Average Fare per Trip"); plt.title("Average Distance vs Average Fare"); plt.tight_layout(); plt.savefig(FIGURES/"distance_vs_fare.png",dpi=160); plt.close()
plt.figure(figsize=(8,6)); plt.scatter(wards.Completed_Trips,wards.Drivers_Earnings,alpha=.65); plt.xlabel("Completed Trips"); plt.ylabel("Drivers' Earnings"); plt.title("Completed Trips vs Drivers' Earnings"); plt.tight_layout(); plt.savefig(FIGURES/"completed_trips_vs_earnings.png",dpi=160); plt.close()
print(f"Saved {OUTPUT}")
