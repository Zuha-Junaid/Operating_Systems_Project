Readers & Writers Problem with Writer's Priority
Project Overview
This project implements the classical Readers-Writers synchronization problem with a specific focus on writer priority. Developed as an Operating Systems semester project, it demonstrates fundamental concurrency concepts such as mutual exclusion, thread synchronization, and starvation prevention.

The implementation provides two primary interfaces:


Streamlit Web Interface: A real-time dashboard for visualizing thread execution, system statistics, and interactive concept diagrams.


Jupyter Notebook: An educational platform designed for step-by-step understanding of synchronization mechanisms.

Key Features

Writer Priority: Prevents writer starvation by blocking new readers when a writer is waiting.


Real-time Visualization: Live logs, execution metrics (active readers, waiting writers), and interactive concurrency graphs.


Data Consistency: Automated verification to ensure shared_data matches the total number of successful writes.


Efficient Synchronization: Uses Python’s threading.Condition variables to avoid CPU-heavy busy waiting.

Operating System Concepts Applied
This project serves as a practical application of several OS core principles:


Multithreading: Managing concurrent execution of multiple reader and writer threads.


Mutual Exclusion: Utilizing Mutex locks to prevent race conditions on shared counters.


Condition Variables: Facilitating efficient thread signaling and waiting without wasting CPU cycles.


Deadlock & Starvation Prevention: Implementing lock ordering and priority logic to ensure system progress.

System Requirements

Python: version 3.8 or higher.


RAM: 4GB minimum.


Browser: Chrome, Firefox, or Edge (for Streamlit).

Installation & Usage
1. Install Dependencies
Bash
pip install streamlit pandas jupyter ipywidgets


2. Run the Streamlit Dashboard
Bash
streamlit run app.py

If the command is not found, use: python -m streamlit run app.py.

3. Run the Jupyter Notebook
Bash
jupyter notebook readers_writers.ipynb


Project Structure

app.py: The main Streamlit application file.


readers_writers.ipynb: Interactive Jupyter Notebook for step-by-step execution.


simulation_data.csv: Exported logs and metrics from the simulation.
