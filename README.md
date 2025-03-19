# Activity Tracker

## Overview
**Activity Tracker** is a simple Python-based application designed to log and track daily activities. It provides a user-friendly interface using **Tkinter**, stores data in an **Excel** file, and displays activity logs in a **Treeview** widget.

## Features
- Start and stop activity tracking with a timer.
- Logs activities into an **Excel file**.
- Automatically creates an Excel file if one does not exist.
- Displays recorded activities in a **Treeview**.
- Designed for self-improvement and learning purposes using **Tkinter** and **Python Classes**.

## Motivation
There are many applications available for tracking daily activities, including Excel and macros. However, this project was created as a **learning experience** to explore:
- Python **Classes**
- **Tkinter** for GUI development
- **Excel automation** using OpenPyXL and Pandas

## Technologies Used
- **Python**
- **Tkinter** (for GUI)
- **Pandas** (for data handling)
- **OpenPyXL** (for Excel file operations)

## Installation
### Prerequisites
Ensure you have Python installed (>=3.6) and install the required libraries:
```sh
pip install pandas openpyxl
```

### Running the Application
Clone or download the repository and run the script:
```sh
python activity_tracker.py
```

## How It Works
1. **Enter an Activity Name** and press Enter to start the timer.
2. **Stop the Timer** when done; the activity is logged in the Excel file.
3. **View Activity Logs** in the Treeview widget.

## File Structure
- `activity_tracker.py` - Main script for the application.
- `activity_tracker_excel.xlsx` - Excel file that stores activity logs (created automatically if missing).

## Data Format
Each activity is stored in an **Excel file** with the following columns:
| Date | Activity | Start Time | Stop Time | Duration |
|------|---------|-----------|----------|----------|

## Contributions
This project was created as a personal learning endeavor by **Ashwani Bhati**. Contributions are welcome for feature enhancements!

## Acknowledgments
- **Corey Schafer** & **Codemy.com** for Python tutorials.
- **ChatGPT** for debugging assistance.

---
### Author: Ashwani Bhati

