from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "namma_yatri_bengaluru_cleaned.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "day03_demand_eda.txt"
SUMMARY_FILE = PROJECT_ROOT / "data" / "processed" / "day03_ward_demand_summary.csv"
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def format_number(value):
    return f"{value:,.0f}"


def save_bar_chart(data, value_col, title, filename):
    chart_data = data.sort_values(value_col, ascending=True).tail(10)
    plt.figure(figsize=(10, 6))
    plt.barh(chart_data["Ward"], chart_data[value_col])
    plt.title(title)
    plt.xlabel(value_col.replace("_", " "))
    plt.ylabel("Ward")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / filename, dpi=160)
    plt.close()


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    ward_df = df.loc[~df["Is_Bangalore_Total"]].copy()

    demand_cols = ["Searches", "Bookings", "Completed_Trips"]
    summary = ward_df[["Ward", *demand_cols, "Conversion_Rate"]].copy()
    summary["Booking_to_Search_Rate"] = summary["Bookings"] / summary["Searches"] * 100
    summary["Completion_to_Search_Rate"] = summary["Completed_Trips"] / summary["Searches"] * 100
    summary["Completion_Rate_From_Bookings"] = summary["Completed_Trips"] / summary["Bookings"] * 100
    summary.to_csv(SUMMARY_FILE, index=False)

    top_searches = ward_df.nlargest(10, "Searches")[["Ward", "Searches"]]
    top_bookings = ward_df.nlargest(10, "Bookings")[["Ward", "Bookings"]]
    top_completed = ward_df.nlargest(10, "Completed_Trips")[["Ward", "Completed_Trips"]]

    low_searches = ward_df.nsmallest(10, "Searches")[["Ward", "Searches"]]
    low_bookings = ward_df.nsmallest(10, "Bookings")[["Ward", "Bookings"]]
    low_completed = ward_df.nsmallest(10, "Completed_Trips")[["Ward", "Completed_Trips"]]

    total_searches = ward_df["Searches"].sum()
    total_bookings = ward_df["Bookings"].sum()
    total_completed = ward_df["Completed_Trips"].sum()

    search_concentration_top10 = top_searches["Searches"].sum() / total_searches * 100
    booking_concentration_top10 = top_bookings["Bookings"].sum() / total_bookings * 100
    completed_concentration_top10 = top_completed["Completed_Trips"].sum() / total_completed * 100

    corr_search_booking = ward_df["Searches"].corr(ward_df["Bookings"])
    corr_search_completed = ward_df["Searches"].corr(ward_df["Completed_Trips"])

    highest_conversion = ward_df.nlargest(10, "Conversion_Rate")[["Ward", "Conversion_Rate", "Searches", "Bookings"]]
    lowest_conversion = ward_df.nsmallest(10, "Conversion_Rate")[["Ward", "Conversion_Rate", "Searches", "Bookings"]]

    save_bar_chart(ward_df, "Searches", "Top 10 Wards by Searches", "day03_top_wards_by_searches.png")
    save_bar_chart(ward_df, "Bookings", "Top 10 Wards by Bookings", "day03_top_wards_by_bookings.png")
    save_bar_chart(ward_df, "Completed_Trips", "Top 10 Wards by Completed Trips", "day03_top_wards_by_completed_trips.png")

    plt.figure(figsize=(9, 6))
    plt.scatter(ward_df["Searches"], ward_df["Bookings"], alpha=0.65)
    plt.title("Ward-Level Searches vs Bookings")
    plt.xlabel("Searches")
    plt.ylabel("Bookings")
    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "day03_searches_vs_bookings.png", dpi=160)
    plt.close()

    report = []
    report.append("DAY 3 - DEMAND EXPLORATORY DATA ANALYSIS")
    report.append("=" * 55)
    report.append("")
    report.append("Purpose")
    report.append("-------")
    report.append("Explore how Namma Yatri activity varies across Bengaluru wards, using")
    report.append("searches, bookings, completed trips, and conversion rate.")
    report.append("")
    report.append("Dataset scope")
    report.append("--------------")
    report.append(f"Rows in cleaned dataset: {len(df):,}")
    report.append(f"Actual wards analysed: {len(ward_df):,}")
    report.append("Bangalore Total row excluded from ward comparisons: Yes")
    report.append("Important limitation: the dataset is all-time ward-level aggregate data.")
    report.append("It does not contain dates, timestamps, or individual ride records.")
    report.append("")

    report.append("1. Overall ward-level activity")
    report.append("-------------------------------")
    report.append(f"Total searches across the 244 wards: {format_number(total_searches)}")
    report.append(f"Total bookings across the 244 wards: {format_number(total_bookings)}")
    report.append(f"Total completed trips across the 244 wards: {format_number(total_completed)}")
    report.append("")

    report.append("2. Top 10 wards by searches")
    report.append("----------------------------")
    report.append(top_searches.to_string(index=False))
    report.append("")

    report.append("3. Top 10 wards by bookings")
    report.append("----------------------------")
    report.append(top_bookings.to_string(index=False))
    report.append("")

    report.append("4. Top 10 wards by completed trips")
    report.append("----------------------------------")
    report.append(top_completed.to_string(index=False))
    report.append("")

    report.append("5. Lowest 10 wards by searches")
    report.append("-------------------------------")
    report.append(low_searches.to_string(index=False))
    report.append("")

    report.append("6. Lowest 10 wards by bookings")
    report.append("-------------------------------")
    report.append(low_bookings.to_string(index=False))
    report.append("")

    report.append("7. Lowest 10 wards by completed trips")
    report.append("--------------------------------------")
    report.append(low_completed.to_string(index=False))
    report.append("")

    report.append("8. Demand concentration")
    report.append("------------------------")
    report.append(f"Top 10 wards share of searches: {search_concentration_top10:.2f}%")
    report.append(f"Top 10 wards share of bookings: {booking_concentration_top10:.2f}%")
    report.append(f"Top 10 wards share of completed trips: {completed_concentration_top10:.2f}%")
    report.append("")

    report.append("9. Relationship between activity measures")
    report.append("------------------------------------------")
    report.append(f"Correlation: searches vs bookings = {corr_search_booking:.4f}")
    report.append(f"Correlation: searches vs completed trips = {corr_search_completed:.4f}")
    report.append("Correlation indicates association, not causation.")
    report.append("")

    report.append("10. Highest conversion-rate wards")
    report.append("---------------------------------")
    report.append(highest_conversion.to_string(index=False))
    report.append("")

    report.append("11. Lowest conversion-rate wards")
    report.append("--------------------------------")
    report.append(lowest_conversion.to_string(index=False))
    report.append("")

    report.append("12. What this tells us")
    report.append("----------------------")
    report.append("- Demand is geographically uneven: some wards generate substantially more searches and bookings than others.")
    report.append("- Searches, bookings, and completed trips should be treated as related but distinct demand/activity measures.")
    report.append("- Conversion rate adds a quality/efficiency dimension; high activity does not automatically mean high conversion.")
    report.append("- The top-10 concentration figures quantify how much activity is concentrated in the busiest wards.")
    report.append("- The results support ward-level demand and operational analysis in Power BI.")
    report.append("")

    report.append("13. What we cannot conclude")
    report.append("-----------------------------")
    report.append("- We cannot identify peak hours, weekdays, months, or seasonality because there is no time field.")
    report.append("- We cannot analyse individual routes or pickup/drop locations because this is ward-level aggregate data.")
    report.append("- We cannot claim that a ward causes higher demand based only on these correlations.")
    report.append("- We should not invent demographic, traffic, weather, income, or service-level explanations without additional data.")
    report.append("")

    report.append("14. Files created")
    report.append("------------------")
    report.append(f"Summary CSV: {SUMMARY_FILE.relative_to(PROJECT_ROOT)}")
    report.append("Figures:")
    report.append("- reports/figures/day03_top_wards_by_searches.png")
    report.append("- reports/figures/day03_top_wards_by_bookings.png")
    report.append("- reports/figures/day03_top_wards_by_completed_trips.png")
    report.append("- reports/figures/day03_searches_vs_bookings.png")

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print("Day 3 demand EDA completed.")
    print(f"Report: {REPORT_FILE}")
    print(f"Summary: {SUMMARY_FILE}")
    print(f"Figures: {FIGURE_DIR}")


if __name__ == "__main__":
    main()
