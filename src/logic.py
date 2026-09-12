import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: file not found — {filepath}")
        return None


def clean_data(df):
    before = len(df)
    df["bytes"] = pd.to_numeric(df["bytes"], errors="coerce")
    df = df.dropna(subset=["src_ip", "bytes", "status"])
    after = len(df)
    dropped = before - after
    if dropped > 0:
        print(f"Warning: dropped {dropped} rows with missing or invalid data")
    return df


def analyze(df):
    totals = df.groupby("src_ip")["bytes"].sum()
    connection_counts= df.groupby("src_ip").size()
    top_talker = totals.idxmax()
    top_bytes = int(totals.max())

    failed = df[df["status"] == "failed"]
    failed_counts = failed["src_ip"].value_counts()

    failed_counts=failed_counts.reindex(connection_counts.index,fill_value=0)
    failure_rate = failed_counts / connection_counts


    suspicious_ips=[]
    for ip in connection_counts.index:
        if failed_counts[ip]>=3 and  failure_rate[ip] >=0.5:
            ip_rows=df[df["src_ip"]==ip]
            target_ports=ip_rows["dst_port"].unique().tolist()
            suspicious_ips.append({
                "ip":ip,
                "total_bytes": int(totals[ip]),
                "connections": int(connection_counts[ip]),
                "failed_attempts":int(failed_counts[ip]),
                "failure_rate":float(failure_rate[ip]),
                "target_ports": target_ports,
                "reason": "Repeated failed connections with high failure rate"


            })

            
    

    return {

        "top_talker": top_talker,
        "top_bytes": top_bytes,
        "failed_counts": failed_counts,
        "connection_counts": connection_counts,
        "failure_rate": failure_rate,
        "suspicious_ips":suspicious_ips
    }


def write_report(results, output_path="data/triage_report.txt"):
    """Write the analysis findings to a readable text report."""

    with open(output_path, "w") as f:
        f.write("=== NETWORK TRIAGE REPORT ===\n\n")

        f.write(
            f"Top talker (most bytes sent): {results['top_talker']} "
            f"({results['top_bytes']} bytes)\n\n"
        )

        f.write("Failed connection attempts per IP:\n")
        for ip, count in results["failed_counts"].items():
            f.write(f"  {ip}: {count} failed\n")

        f.write("\n=== SUSPICIOUS ACTIVITY ===\n")

        for item in results["suspicious_ips"]:
            f.write(f"\nIP: {item['ip']}\n")
            f.write(f"Total bytes: {item['total_bytes']}\n")
            f.write(f"Connections: {item['connections']}\n")
            f.write(f"Failed attempts: {item['failed_attempts']}\n")
            f.write(f"Failure rate: {item['failure_rate']:.0%}\n")
            f.write(f"Target ports: {item['target_ports']}\n")
            f.write(f"Reason: {item['reason']}\n")

    print(f"Report written to {output_path}")

def make_chart(df, output_path="data/top_talkers.png"):
    """Draw a bar chart of total bytes per IP and save it as an image."""

    totals = df.groupby("src_ip")["bytes"].sum().sort_values(ascending=False)

    totals.plot(
        kind="bar",
        title="Total Bytes Sent per IP"
    )

    plt.xlabel("Source IP")
    plt.ylabel("Total Bytes")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"Chart saved to {output_path}")

def make_failed_chart(results, output_path="data/failed_attempts.png"):
    """Draw a bar chart of failed connection attempts per IP."""

    failed_counts = results["failed_counts"]

    failed_counts.plot(
        kind="bar",
        title="Failed Connection Attempts per IP"
    )

    plt.xlabel("Source IP")
    plt.ylabel("Failed Attempts")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"Failed-attempt chart saved to {output_path}")