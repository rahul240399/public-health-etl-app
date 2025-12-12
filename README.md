# Public health ETL app

## 1. Project Overview
The **Public health ETL app** is an visualisation tool developed for epidemiological analysis. It interfaces with the **World Health Organization (WHO) GHO OData API** to retrieve public health indicators—specifically **Life Expectancy** stats.

The system is designed to solve the problem of "cryptic data" by implementing an **ETL (Extract, Transform, Load)** pipeline that cleanses raw API codes (e.g., `GBR`, `MLE`) into human-readable formats (e.g., `United Kingdom`, `Male`) and stores them in a relational **SQLite** database for offline analysis.

### Key Features
* **Dynamic Data Ingestion:** Fetches real time data from WHO OData endpoints.
* **Data Cleaning Engine:** Automatically maps ISO country codes and dimension codes to readable names.
* **Relational Storage:** Persists data using a Relational Schema for efficient querying.
* **Web Dashboard:** A Flask based app to view, filter, and analyse health trends.

---

## 2. Technical Architecture
The application follows a strict **Model View Controller (MVC)** design pattern to ensure modularity and testability.

### 2.1 The MVC Structure
* **Model (Data Layer):** Handles business logic, database interactions, and API connections.
    * *Key Components:* `HealthDatabase` (SQLite Manager), `WhoApiClient` (Requests), `DataCleaner` (Logic).
* **View (Presentation Layer):** Displays data to the user via a web browser.
    * *Key Components:* HTML Templates,CSS and js.
* **Controller (Application Layer):** manages the flow between the Model and View.
    * *Key Components:* `app.py` (Flask Routes).

### 2.2 Tech Stack
* **Language:** Python 3.x
* **Framework:** Flask (Web), Unittest (Testing)
* **Database:** SQLite3
* **External API:** WHO GHO OData API

---

## 3. Database Design (Schema)
The project uses a **Relational Schema** using SQL.

### Table 1: `countries` (Dimension Table)
Acts as the central lookup for geographic data.
* `code` (PK, TEXT): ISO Country Code (e.g., 'GBR')
* `name` (TEXT): Readable Name (e.g., 'United Kingdom')
* `region` (TEXT): WHO Region (e.g., 'Europe')

### Table 2: `health_data` (Fact Table)
Stores the quantitative health statistics.
* `id` (PK, INTEGER): Unique Record ID.
* `country_code` (FK, TEXT): Linked to `countries.code`.
* `year` (INTEGER): Time dimension.
* `sex` (TEXT): Categorical dimension ('Male', 'Female', 'Both').
* `value` (REAL): The specific health indicator value.
* `indicator` (TEXT): The name of the metric (e.g., 'Life Expectancy').

---

## 4. Requirements Analysis
*Analysed using MoSCoW and FURPS+ methodologies.*

### 4.1 MoSCoW Prioritisation
* **Must Have:** Fetching data from Endpoint: https://ghoapi.azureedge.net/api/WHOSIS_000001, Cleaning Logic (GBR -> UK), Database persistence, Basic Web UI, Unit Tests (TDD).
* **Should Have:** Region based mapping, Filtering by Year/Sex, Error handling for API timeouts.
* **Could Have:** CSV Export functionality, Visual Charts (Bar/Line).
* **Won't Have:** Predictive AI modelling, User Authentication.

### 4.2 FURPS+ Quality Attributes
* **Functionality:** Capability to join data from three distinct API sources.
* **Usability:** Browser based interface accessible to business users.
* **Reliability:** Transactions used for DB operations to prevent corruption.
* **Performance:** Caching strategy used to reduce network dependency.
* **Supportability:** Code adheres to PEP8 standards with comprehensive Docstrings.

---

## 5. Development Methodology
The project strictly follows **Test Driven Development (TDD)** principles.

Tests cover:
* Database Schema validation.
* Data Cleaning logic (Edge cases for invalid codes).
* API Response parsing.

---

## 6. Setup and Installation


1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the application: `python app.py`
