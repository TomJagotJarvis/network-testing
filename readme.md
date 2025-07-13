# WiFi Speed and Latency Logger

A tool to log WiFi performance (local latency and internet speed) room-by-room, and visualize the results via an interactive web page.

---

## 🐍 Python Virtual Environment Setup (Recommended)
### ✅ Create a virtual environment and activate it
```
python3 -m venv .venv
source .venv/bin/activate
(.venv) your-machine:project-folder yourname$
```
### ❌ To deactivate the environment:
```
deactivate
```

---

## 📦 Requirements

- Python 3 (macOS recommended)
- macOS `networkquality` tool (built-in from macOS 12+)
- SQLite (built into Python)
- Browser (to view the chart and table)
- Chart.js (loaded via CDN in HTML)

---

## 🧪 How to Run the Script

Use the `wifi_test.py` script to log WiFi tests.

### ✅ Required argument:

- `--room`: The name of the room (e.g. `--room kitchen`)

### ✅ Optional arguments:

- `--runs`: Number of test repetitions (default = 1)
- `--wait`: Seconds to wait between each run (default = 1)

---

## 📌 Example Usage

### **Run one test in the kitchen:**
```
python wifi_test.py --room kitchen
```

### **Run 3 tests in the bedroom with 5 seconds between each:**
```
python wifi_test.py --room bedroom --runs 3 --wait 5
```

### **Run 10 tests in the living room sofa area quickly:**
```
python wifi_test.py --room living_room_sofa --runs 10 --wait 1
```

---

## 💾 Output Files

- `wifi_results.db` — SQLite database that stores all test results.
- `wifi_results.csv` — CSV export used by the web interface.

---

## 🌐 Viewing Results in the Browser

### Step 1: Start a simple web server

From the same directory as `index.html` and `wifi_results.csv`, run:

```
bash
python -m http.server
```

### Step 2: Open in your browser:

```
http://localhost:8000
```

---

## 📊 Features of the Web Interface

- 📈 Interactive bar chart (Chart.js)
- 📋 Data table with sortable columns
- 🧠 Toggle between **Average** and **95th Percentile**
- 🔁 Automatically updates from latest `wifi_results.csv`

---

## 📁 Recommended Project Structure

```
wifi-testing/
├── wifi_test.py
├── wifi_results.db
├── wifi_results.csv
├── index.html
├── README.md
```

---

## 🧠 Tips and Ideas

- Run the script in each room of your house to compare coverage.
- Combine this with signal metrics (RSSI, noise) using `airport -I` on macOS.
- Add local throughput testing with `iperf3` if desired.

---

Enjoy measuring and understanding your WiFi like a pro! 📶📊
