import argparse
import subprocess
import sqlite3
import datetime
import time

DB_PATH = "wifi_results.db"
CSV_PATH = "wifi_results.csv"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS wifi_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            room TEXT,
            local_latency_ms REAL,
            internet_download_mbps REAL,
            internet_upload_mbps REAL
        )
    """
    )
    conn.commit()
    conn.close()


def get_local_latency(router_ip="192.168.1.254"):
    try:
        output = subprocess.check_output(["ping", "-c", "4", router_ip])
        lines = output.decode().split("\n")
        summary_line = [
            line for line in lines if "round-trip" in line or "rtt" in line
        ][0]
        avg_latency = summary_line.split("/")[4]  # min/avg/max/stddev
        return float(avg_latency)
    except Exception as e:
        print(f"Error in ping: {e}")
        return None


def get_internet_speed():
    try:
        output = subprocess.check_output(["networkquality"]).decode()
        download = upload = None
        for line in output.splitlines():
            if "Downlink capacity" in line:
                download = float(line.split(":")[1].strip().split(" ")[0])
            if "Uplink capacity" in line:
                upload = float(line.split(":")[1].strip().split(" ")[0])
        return download, upload
    except Exception as e:
        print(f"Error parsing networkquality output: {e}")
        return None, None


def log_result(room, latency, download, upload):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO wifi_tests (timestamp, room, local_latency_ms, internet_download_mbps, internet_upload_mbps)
        VALUES (?, ?, ?, ?, ?)
    """,
        (datetime.datetime.now().isoformat(), room, latency, download, upload),
    )
    conn.commit()
    conn.close()


def export_csv():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM wifi_tests").fetchall()
    headers = [description[0] for description in c.description]
    conn.close()

    with open(CSV_PATH, "w") as f:
        f.write(",".join(headers) + "\n")
        for row in rows:
            f.write(",".join(str(x) for x in row) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WiFi testing and logging tool")
    parser.add_argument(
        "--room", required=True, help="Room where the test is being performed"
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of times to repeat the test (default: 1)",
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=1,
        help="Wait time in seconds between test runs (default: 1)",
    )

    args = parser.parse_args()

    init_db()

    for i in range(args.runs):
        print(f"Run {i+1}/{args.runs} in '{args.room}'...")

        latency = get_local_latency()
        download, upload = get_internet_speed()

        print(f"  Local latency: {latency} ms")
        print(f"  Download: {download} Mbps")
        print(f"  Upload: {upload} Mbps")

        log_result(args.room, latency, download, upload)

        if i < args.runs - 1:
            time.sleep(args.wait)

    export_csv()
    print("Results saved to database and exported to wifi_results.csv.")
