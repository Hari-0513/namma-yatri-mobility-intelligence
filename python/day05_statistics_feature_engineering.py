from pathlib import Path
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/"data/processed/namma_yatri_bengaluru_cleaned.csv"
OUTPUT=ROOT/"data/processed/day05_statistical_features.csv"
df=pd.read_csv(INPUT)
w=df[df["Ward"].astype(str).str.strip()!="Bangalore Total"].copy()
for c in ["Searches","Bookings","Completed_Trips","Cancelled_Bookings","Booking_Cancellation_Rate","Conversion_Rate","Drivers_Earnings","Average_Distance_Per_Trip_Km","Average_Fare_Per_Trip","Distance_Travelled_Km"]:
    w[c]=pd.to_numeric(w[c],errors="coerce")
w["Completion_Rate_From_Bookings"]=np.where(w.Bookings>0,w.Completed_Trips/w.Bookings*100,np.nan)
w["Fare_Per_Km"]=np.where(w.Average_Distance_Per_Trip_Km>0,w.Average_Fare_Per_Trip/w.Average_Distance_Per_Trip_Km,np.nan)
w["Earnings_Per_Completed_Trip"]=np.where(w.Completed_Trips>0,w.Drivers_Earnings/w.Completed_Trips,np.nan)
w["Distance_Per_Completed_Trip_Km"]=np.where(w.Completed_Trips>0,w.Distance_Travelled_Km/w.Completed_Trips,np.nan)
w["Booking_to_Search_Rate"]=np.where(w.Searches>0,w.Bookings/w.Searches*100,np.nan)
for c in ["Searches","Bookings","Completed_Trips","Conversion_Rate","Booking_Cancellation_Rate","Average_Fare_Per_Trip","Average_Distance_Per_Trip_Km","Drivers_Earnings"]:
    w[c+"_Percentile"]=w[c].rank(pct=True)*100
w["Demand_Quartile"]=pd.qcut(w["Searches"],4,labels=["Low","Moderate","High","Very High"])
w["Conversion_Quartile"]=pd.qcut(w["Conversion_Rate"],4,labels=["Low","Moderate","High","Very High"])
w["Cancellation_Quartile"]=pd.qcut(w["Booking_Cancellation_Rate"],4,labels=["Low","Moderate","High","Very High"])
w.to_csv(OUTPUT,index=False)
print(f"Saved: {OUTPUT}")