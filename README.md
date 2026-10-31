# 🚆 AI-Based Intelligent Ticket & Passenger Reconciliation System

An AI-powered intelligent system designed to automate ticket verification, passenger detection, counting, and reconciliation in public transportation systems using Artificial Intelligence, Computer Vision, and OCR.

## 📌 Project Overview

The AI-Based Intelligent Ticket & Passenger Reconciliation System aims to improve passenger monitoring and ticket verification in railway and bus transportation.

The system uses OCR technology to extract passenger details from tickets and AI-based object detection to identify and count passengers through camera feeds. It compares the actual passenger count with ticket booking records to identify discrepancies and generate reconciliation reports.

## 🎯 Objectives

- Automate ticket verification.
- Detect and count passengers in real time.
- Compare booked passengers with actual passenger counts.
- Identify ticket and passenger discrepancies.
- Improve transportation security and efficiency.
- Generate automated passenger reconciliation reports.

## ✨ Key Features

- 🎫 AI-based ticket scanning and verification.
- 🔍 OCR-based passenger information extraction.
- 👥 Real-time passenger detection and counting.
- 🤖 AI-based passenger reconciliation.
- 📊 Dashboard for passenger monitoring.
- 🗄️ Database management for ticket records.
- 📑 Automated discrepancy reports.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| OpenCV | Image processing |
| YOLO | Passenger detection |
| Tesseract OCR | Ticket text extraction |
| Flask / Streamlit | Web interface |
| MySQL / SQLite | Database management |
| Machine Learning | Intelligent analysis |

## ⚙️ System Workflow

1. **Ticket Upload:** User uploads or scans a passenger ticket.
2. **Text Extraction:** OCR extracts ticket information.
3. **Passenger Detection:** Camera feed is processed using AI.
4. **Passenger Counting:** The system detects and counts passengers.
5. **Reconciliation:** Actual passenger counts are compared with booking records.
6. **Discrepancy Detection:** Mismatches are identified.
7. **Report Generation:** Results are displayed on the dashboard.

## 📂 Project Structure

```text
AI-Ticket-Passenger-Reconciliation/
│
├── app.py
├── requirements.txt
├── README.md
│
├── dataset/
│   ├── tickets/
│   └── passenger_images/
│
├── models/
│   └── yolov8_model.pt
│
├── modules/
│   ├── ticket_ocr.py
│   ├── passenger_detection.py
│   ├── passenger_count.py
│   └── reconciliation.py
│
├── database/
│   └── database.py
│
├── static/
├── templates/
└── reports/
```

## 🚀 Installation and Setup

**Step 1: Clone the repository**

```bash
git clone https://github.com/your-username/AI-Ticket-Passenger-Reconciliation.git
```

**Step 2: Navigate to the project folder**

```bash
cd AI-Ticket-Passenger-Reconciliation
```

**Step 3: Create a virtual environment**

```bash
python -m venv venv
```

**Step 4: Activate the virtual environment**

Windows:

```bash
venv\Scripts\activate
```

**Step 5: Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 6: Run the application**

```bash
streamlit run app.py
```

## 📊 Expected Output

- Extracted passenger ticket details.
- Real-time passenger count.
- Ticket and passenger reconciliation results.
- Discrepancy notifications.
- Passenger monitoring dashboard.
- Reconciliation reports.

## 🏢 Applications

- Indian Railways
- Public Transportation Systems
- Bus Transportation
- Smart Ticket Management
- Passenger Monitoring Systems

## 🔮 Future Scope

- Integration with railway reservation databases.
- Real-time CCTV integration.
- Advanced AI-based anomaly detection.
- Mobile application for ticket verification.
- Cloud-based passenger monitoring.

## 👨‍💻 Project Information

**Project Name:** AI-Based Intelligent Ticket & Passenger Reconciliation System

**Domain:** Artificial Intelligence and Machine Learning

**Programming Language:** Python

**Project Type:** Final Year Engineering Project

## 📜 License

This project is intended for educational and research purposes.

---

⭐ If you find this project useful, consider giving the repository a star!
