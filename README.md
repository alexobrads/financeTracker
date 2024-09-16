# Finance Tracker

## Overview

This project is a personal endeavour aimed at creating a data visualisation dashboard for tracking spending and mortgage repayments. It serves as a practical exercise to gain hands-on experience with Dash building.

## Key Features

- **Interactive Dashboards**: Utilize Dash to create dynamic and interactive visualizations.
- **Custom Styling**: Apply CSS to enhance the look and feel of the dashboard.
- **Callback Functions**: Implement callbacks to create responsive and real-time updates on the dashboard.

## Technologies Used

- **Dash**: A Python framework for building analytical web applications.
- **CSS**: For custom styling and enhanced UI.
- **Pandas**: For data manipulation and analysis.
- **Plotly**: For creating interactive plots.

## Getting Started

### Prerequisites

- Python 3.11.6
- Pip (Python package manager)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/finance-tracker.git
    ```
2. Navigate to the project directory:
    ```sh
    cd finance-tracker
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Application

1. At the moment this project only handles statements from a single banking entity, if you want to use it yourself you will need to adjust etl.process_statements.py

2. Execute the following command to start the server:
    ```sh
    python app.py
    ```
3. Open your web browser and visit: http://127.0.0.1:8050/


Feel free to reach out if you have any questions or suggestions!