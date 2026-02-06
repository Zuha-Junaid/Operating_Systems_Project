Readers & Writers Problem with Writer's Priority

This repository contains a Python implementation of the classical Readers-Writers synchronization problem, specifically designed with writer priority to prevent writer starvation. Developed as an Operating Systems semester project, it demonstrates the practical application of thread coordination, mutual exclusion, and resource management.

🚀 Features

Writer Priority Mechanism: Implements logic that blocks new readers if a writer is waiting, ensuring writers are not starved by a continuous stream of readers.

Real-Time Visualization: A Streamlit-based web dashboard provides live metrics, execution logs, and thread state tracking.

Interactive Simulation: Adjust the number of readers, writers, and simulation duration through a Jupyter Notebook or web interface.

Data Consistency: Built-in verification to ensure shared data remains consistent across concurrent operations.

Efficient Resource Usage: Uses condition variables instead of busy waiting to save CPU cycles.

🧠 OS Concepts Applied

The project implements several core Operating System principles:

Multithreading: Managing concurrent execution using Python’s threading module.

Mutual Exclusion (Mutex): Protecting shared counters (reader_count, waiting_writers) from race conditions.

Condition Variables: Coordinating thread execution by allowing threads to sleep and wake up based on specific state changes.

Deadlock Prevention: Utilizing structured lock ordering and hierarchy to ensure the system never reaches a circular wait state.

🛠️ Tools & Technologies
Tool	Purpose
Python	Core programming language for implementation.

Threading	Python library used for creating and managing concurrent threads.

Streamlit	Framework used for the interactive web dashboard and real-time visualization.

Pandas	Used for data manipulation and exporting simulation logs to CSV.

Jupyter	Provides an educational, step-by-step execution environment.

💻 Installation & Usage

1. Requirements
   
Python 3.8+.

4GB RAM minimum.

2. Setup
   
Install required libraries

pip install streamlit pandas jupyter ipywidgets

4. Running the Simulation
   
Web Interface (Streamlit):

python -m streamlit run app.py

Educational Notebook:

jupyter notebook readers_writers.ipynb

📊 Results & Testing

The system has been tested under various configurations to ensure correctness:

Concurrency: Multiple readers can access the resource simultaneously, as verified by max_concurrent_readers stats.

Exclusivity: Writers maintain exclusive access; no readers or other writers can enter the critical section during a write.

Consistency: Final data values are verified against the total number of write operations (e.g., Final Data == Total Writes).
