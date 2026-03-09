# 🏁 Historical Analysis of Formula 1 Teams, Drivers and Decades (1950-2024)
Python - SQL - Streamlit (Python)

---

<div align="center">

https://github.com/user-attachments/assets/f6c6fc43-c7a0-48c4-8966-9f5b73c0b493


</div>

---

## Dataset

- Source: Kaggle -> https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020

- Period: 1950-2024

- **Tables:**

  - circuits - *Circuits where the F1 races*
  - constructor_results - *Constructors results by race*
  - constructor_standings - *Constructors standings after every race*
  - constructors - *Every constructor that has participated in the history*
  - driver_standings - *Drivers standings after every race*
  - drivers - *Every driver that has raced historically*
  - lap_times - *Lap times of every driver*
  - pit_stops - *Pit stops made by race by every driver*
  - qualifying - *Qualifying times of every driver by Grand Prix*
  - races - *Every race that ever took place*
  - results - *Drivers' results of every race*
  - seasons - *Seasons info*
  - sprint_results - *Sprint results of every driver*
  - status - *Describes how the driver finished the race (DNF, Finished, Accident, etc.)

 ---

## Technologies Used

- **Python**
    - Pandas
    - Streamlit

- **Database**
    - MariaDB / MySQL
    - SQLAlchemy
 
- **Visulizations**
    - Streamlit Bar and Line Chart
    - Plotly 

---

## 📂 Project Structure

- **src/**
  - __init__.py
  - db.py
  - decades.py
  - drivers.py
  - teams.py
- f1_app.py

You can check the documentation of each file inside of itself. Also note that the .sql file is the Database created from the downloaded file, manually.
In addition, you can download the .zip file with all the CSVs files that contain the data.

---

## Insights Identified 🔎

### 1 - Ferrari The Winningest Team 🏆

- Has won 15 Constructors Titles since its begginings.

- Team with most points, 10,820.

- Team with most races, nearly 2,500.

- Despite all the titles, we can see the irregularity in its points during the years.

  <img width="768" height="522" alt="image" src="https://github.com/user-attachments/assets/9038968c-f098-4d62-b5d4-98be136c8b2e" />

---

### 2 - Hamilton Feels Comfortable at Home 🏠

- Nearly 20 races and and average of a podium finish everytime he races there there.

- +300 points scored, the most he has scored in any circuit.

- Out of 18 races there, he has won 9, making it a 50% of wins in a single circuit. Outstanding.

<img width="912" height="733" alt="image" src="https://github.com/user-attachments/assets/f6534b28-74cb-44a7-bd37-5638ec244a21" />

---

### 3 - Schumacher's Era 🏎️

- Leader of the 90s and 00s in wins and total points.

- Outscored the second best driver of each decade by more than 200 points in the 1990s like in the 2000s.

- Won 7 titles in a span of 15 years (1991-2005).

#### Schumacher in the 90s

<img width="785" height="756" alt="image" src="https://github.com/user-attachments/assets/dcf7acd9-06c2-4759-b0df-16e6aa0aa4a2" />

---

#### Schumacher in the 00s

<img width="854" height="774" alt="image" src="https://github.com/user-attachments/assets/94eab3ed-e4bf-4916-ba17-0f5d4a4b62d1" />

---

## Download the Queries

In every section you have the option to download the views generated from the quieres I did as csv files. Download them and explore by yourself!

---

## 🧑‍💻 Author

Manuel Lombardi
Data Analyst & Software Developer

🔗 LinkedIn: https://www.linkedin.com/in/manuel-lombardi-572685341/

🐙 GitHub: https://github.com/ML13-DEV





