
# Data Analyst Final Project – Multi-Feature Streamlit Application

This project is a comprehensive **Data Analyst final project** developed **Streamlit**, integrating multiple data-related components into a single interactive web application.

The application combines:

* Interactive games
* Web scraping & database storage
* Dashboard integration
* Machine learning prediction

---


### 1. Interactive Games

The app includes three mini-games with user interaction and score tracking:

*  Rock-Paper-Scissors
*  Memory Game (multi-level)
*  Typing Speed Challenge

 Features:

* Multi-round gameplay
* Score tracking and ranking system
* Data stored in CSV files
* Replay functionality

---

### 2. Real-Time News Scraping & Database

This section collects and displays the latest news using web scraping.

Process:

* Scraping news from a website using **BeautifulSoup**
* Storing data in **SQL Server** using `pyodbc`
* Creating database and table automatically (if not exists)
* Displaying latest news داخل اپلیکیشن

Capabilities:

* Manual update button for refreshing news
* Persistent storage in database
* Structured data retrieval

---

###  3. Dashboard Integration

* Displays a Power BI dashboard (via link)
* Can be hosted on Power BI Report Server
* Provides visual insights and reporting

---

###  4. Machine Learning Model

A regression model predicts student exam scores based on various factors.

Model Details:

* Algorithm: Random Forest Regressor
* Preprocessing: One-Hot Encoding
* Evaluation Metric: Mean Absolute Error (MAE)

 Input Features:

* Study hours
* Attendance
* Sleep duration
* Motivation level
* Family income
* Teacher quality
* And more

 Output:

* Predicted exam score

---

###  5. User Guideline

A simple guide explaining each section of the application.

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* Scikit-learn
* BeautifulSoup
* Requests
* SQL Server (pyodbc)
* Joblib


---

##  Important Notes

* SQL Server must be installed and configured locally
* Update database connection string if needed

---


##  Author

Maryam Samie
Data Analyst

---

