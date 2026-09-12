from logic import (
    load_data,
    clean_data,
    analyze,
    write_report,
    make_chart,
    make_failed_chart
)


def main():
    """Run the full network triage pipeline: load, clean, analyze, report, chart."""
    df = load_data("data/connections.csv")

    if df is None:
        print("No data loaded. Exiting.")
        return

    df = clean_data(df)
    results = analyze(df)

    write_report(results)

    make_chart(df)
    make_failed_chart(results)

    


if __name__ == "__main__":
    main()