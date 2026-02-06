import streamlit as st
import time
import threading
import random
from datetime import datetime
import pandas as pd
import queue

st.set_page_config(page_title="Readers-Writers Problem", layout="wide")
st.title("📚 Readers–Writers Problem (Writer Priority) - Live Simulation")
st.caption("Professional real-time dashboard with moving graphs and live logs! 🔥")

class ReadersWritersProblem:
    def __init__(self):
        self.reader_count = 0
        self.waiting_writers = 0
        self.resource_lock = threading.Lock()
        self.mutex = threading.Lock()
        self.can_read = threading.Condition(self.mutex)
        self.can_write = threading.Condition(self.mutex)
        self.shared_data = 0
        self.logs = []
        self.metrics_queue = queue.Queue()
        self.stats = {'total_reads': 0, 'total_writes': 0, 'max_concurrent_readers': 0}

    def log_event(self, event):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {event}"
        self.logs.append(log_entry)

    def update_metrics(self):
        self.metrics_queue.put({
            'time': time.time(),
            'readers': self.reader_count,
            'waiting_writers': self.waiting_writers,
            'shared_data': self.shared_data
        })

    def reader(self, reader_id, end_time):
        while time.time() < end_time:
            with self.mutex:
                while self.waiting_writers > 0:
                    self.log_event(f"🟡 Reader {reader_id} WAITING (Writer priority)")
                    self.can_read.wait()
                self.reader_count += 1
                self.stats['max_concurrent_readers'] = max(self.stats['max_concurrent_readers'], self.reader_count)
            self.log_event(f"📖 Reader {reader_id} READING | Data = {self.shared_data} | Readers = {self.reader_count}")
            self.stats['total_reads'] += 1
            self.update_metrics()
            time.sleep(random.uniform(1, 2))
            with self.mutex:
                self.reader_count -= 1
                self.log_event(f"✅ Reader {reader_id} finished | Readers = {self.reader_count}")
                if self.reader_count == 0:
                    self.can_write.notify()
            self.update_metrics()
            time.sleep(random.uniform(2, 4))

    def writer(self, writer_id, end_time):
        while time.time() < end_time:
            with self.mutex:
                self.waiting_writers += 1
                self.log_event(f"⏳ Writer {writer_id} WAITING | Waiting Writers = {self.waiting_writers}")
                while self.reader_count > 0:
                    self.can_write.wait()
                self.waiting_writers -= 1
            with self.resource_lock:
                old = self.shared_data
                self.log_event(f"✍️ Writer {writer_id} WRITING | Old = {old}")
                self.shared_data += 1
                time.sleep(random.uniform(1.5, 2.5))
                self.log_event(f"💾 Writer {writer_id} finished | New = {self.shared_data}")
                self.stats['total_writes'] += 1
            with self.mutex:
                self.can_read.notify_all()
            self.update_metrics()
            time.sleep(random.uniform(3, 5))

# Session state for simulation control
if 'running' not in st.session_state:
    st.session_state.running = False
    st.session_state.rw = None
    st.session_state.metrics = []

# Controls
col1, col2, col3 = st.columns(3)
num_readers = col1.slider("Number of Readers", 1, 10, 3)
num_writers = col2.slider("Number of Writers", 1, 5, 2)
duration = col3.slider("Duration (seconds)", 5, 30, 15, step=5)

if st.button("🚀 Start Live Simulation", type="primary"):
    st.session_state.running = True
    st.session_state.rw = ReadersWritersProblem()
    st.session_state.metrics = []
    st.session_state.start_time = time.time()

    # Start threads
    end_time = time.time() + duration
    threads = []
    for i in range(num_readers):
        t = threading.Thread(target=st.session_state.rw.reader, args=(i+1, end_time))
        threads.append(t)
        t.start()
    for i in range(num_writers):
        t = threading.Thread(target=st.session_state.rw.writer, args=(i+1, end_time))
        threads.append(t)
        t.start()
    st.session_state.threads = threads

# Placeholders
log_placeholder = st.empty()
metrics_placeholder = st.empty()
chart_placeholder = st.empty()
status_placeholder = st.empty()

if st.session_state.running:
    rw = st.session_state.rw
    start_time = st.session_state.start_time

    # Collect metrics
    while not rw.metrics_queue.empty():
        st.session_state.metrics.append(rw.metrics_queue.get())

    # Update UI
    with log_placeholder.container():
        st.subheader("📜 Live Logs")
        st.text("\n".join(rw.logs[-20:]))  # Show last 20 logs

    if st.session_state.metrics:
        latest = st.session_state.metrics[-1]
        with metrics_placeholder.container():
            st.subheader("📊 Current Status")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Shared Data", latest['shared_data'])
            c2.metric("Active Readers", latest['readers'])
            c3.metric("Waiting Writers", latest['waiting_writers'])
            c4.metric("Total Writes", rw.stats['total_writes'])

        df = pd.DataFrame(st.session_state.metrics)
        df['time'] = df['time'] - start_time
        df = df.set_index('time')
        with chart_placeholder.container():
            st.subheader("📈 Real-time Graph")
            st.line_chart(df[['readers', 'waiting_writers', 'shared_data']])

    status_placeholder.info("⏳ Simulation running... Updating live!")

    # Check if simulation ended
    if time.time() - start_time >= duration + 5:
        st.session_state.running = False
        status_placeholder.success("🎉 Simulation Completed!")
        st.balloons()

        st.subheader("📊 Final Results")
        col1, col2 = st.columns(2)
        col1.metric("Total Reads", rw.stats['total_reads'])
        col2.metric("Total Writes", rw.stats['total_writes'])
        st.metric("Max Concurrent Readers", rw.stats['max_concurrent_readers'])
        st.metric("Final Shared Data", rw.shared_data)

        df_logs = pd.DataFrame({"log": rw.logs})
        st.download_button("📥 Download Logs CSV", df_logs.to_csv(index=False).encode(), "simulation_logs.csv")

    else:
        time.sleep(0.5)
        st.rerun()

else:
    st.info("Set parametrs and Press Start Button to run the simulation.")

# ==================== CONCEPT DIAGRAMS SECTION ====================
st.markdown("---")
st.markdown("### 📚 Concept Diagrams & Explanation")

# Create tabs for different concepts
tab1, tab2, tab3, tab4 = st.tabs([
    "🔄 Problem Overview", 
    "🎯 Writer Priority Logic", 
    "🔐 Synchronization Mechanisms",
    "📊 Architecture Diagram"
])

with tab1:
    st.markdown("#### 🔄 Readers-Writers Problem Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **The Challenge:**
        - Multiple **Readers** can read simultaneously
        - **Writers** need exclusive access
        - Without priority: Writers may starve
        - With Writer Priority: Prevents writer starvation
        
        **Key Rules:**
        1. ✅ Multiple readers can read at the same time
        2. ❌ Only ONE writer can write at a time
        3. ❌ No readers allowed when writer is writing
        4. 🎯 Writers get priority over new readers
        """)
    
    with col2:
        st.markdown("""
        ```
        ┌─────────────────────────┐
        │   Shared Resource       │
        │   (Database/File)       │
        └───────────┬─────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    Reader 1    Reader 2    Writer 1
       📖          📖          ✍️
    (READ)      (READ)     (WRITE)
    
    ✅ Readers can work together
    ❌ Writer needs exclusive access
        ```
        """)

with tab2:
    st.markdown("#### 🎯 Writer Priority Logic")
    
    st.markdown("""
    **How Writer Priority Works:**
    
    When a writer requests access:
    1. Increment `waiting_writers` counter
    2. New readers check this counter
    3. If `waiting_writers > 0`, new readers WAIT
    4. Writer waits for current readers to finish
    5. Writer gets exclusive access
    6. After writing, readers can proceed
    """)
    
    st.code("""
# Reader Entry Check (Key Part!)
with self.mutex:
    while self.waiting_writers > 0:  # ⭐ Writer Priority Check
        # Block new readers if writer is waiting
        self.can_read.wait()
    
    # No writers waiting, proceed
    self.reader_count += 1
    """, language="python")
    
    st.markdown("""
    **Flow Diagram:**
    ```
    Reader Arrives
         │
         ▼
    Check waiting_writers
         │
    ┌────┴────┐
    │ > 0 ?   │
    └────┬────┘
         │
    YES  │  NO
    ┌────▼────────┐      ┌─────────────┐
    │ WAIT/BLOCK  │      │ Enter Read  │
    │  (Priority  │      │   Section   │
    │  to Writer) │      │     📖      │
    └─────────────┘      └─────────────┘
    ```
    """)

with tab3:
    st.markdown("#### 🔐 Synchronization Mechanisms Used")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Mutex (Lock)**
        - Protects shared counters
        - `reader_count`
        - `waiting_writers`
        
        **2. Resource Lock**
        - Controls access to shared data
        - Ensures exclusive write access
        
        **3. Condition Variables**
        - `can_read`: Signals readers
        - `can_write`: Signals writers
        """)
    
    with col2:
        st.markdown("""
        **Synchronization Flow:**
        ```
        ┌─────────────────┐
        │  Mutex Lock     │
        │  (Protects)     │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  reader_count   │
        │  waiting_writers│
        └─────────────────┘
        
        ┌─────────────────┐
        │ Resource Lock   │
        │  (Controls)     │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Shared Data    │
        │  (Database)     │
        └─────────────────┘
        ```
        """)
    
    st.markdown("""
    **Critical Section Protection:**
    
    | Thread Type | Entry Condition | Exit Action |
    |-------------|----------------|-------------|
    | **Reader** | `waiting_writers == 0` | Decrement `reader_count` |
    | **Writer** | `reader_count == 0` | Notify waiting readers |
    """)

with tab4:
    st.markdown("#### 📊 Complete System Architecture")
    
    st.markdown("""
    ```
    ┌──────────────────────────────────────────────────────────────┐
    │                   APPLICATION LAYER                          │
    │              (Streamlit/Jupyter Interface)                   │
    └────────────────────────────┬─────────────────────────────────┘
                                 │
    ┌────────────────────────────▼─────────────────────────────────┐
    │              THREAD MANAGEMENT LAYER                         │
    │  ┌────────────────┐              ┌────────────────┐          │
    │  │ Reader Threads │              │ Writer Threads │          │
    │  │   📖 📖 📖    │              │     ✍️ ✍️      │          │
    │  └────────┬───────┘              └────────┬───────┘          │
    └───────────┼──────────────────────────────┼──────────────────┘
                │                              │
    ┌───────────▼──────────────────────────────▼──────────────────┐
    │         SYNCHRONIZATION PRIMITIVES LAYER                     │
    │                                                               │
    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
    │  │ Mutex Lock   │  │Resource Lock │  │  Condition   │      │
    │  │ (reader_     │  │ (exclusive   │  │  Variables   │      │
    │  │  count,      │  │  write       │  │  (can_read,  │      │
    │  │  waiting_    │  │  access)     │  │   can_write) │      │
    │  │  writers)    │  │              │  │              │      │
    │  └──────────────┘  └──────────────┘  └──────────────┘      │
    └────────────────────────────┬─────────────────────────────────┘
                                 │
    ┌────────────────────────────▼─────────────────────────────────┐
    │                  SHARED RESOURCE LAYER                       │
    │                                                               │
    │              ┌──────────────────────────┐                    │
    │              │    Shared Data (DB)      │                    │
    │              │    reader_count = 0      │                    │
    │              │    waiting_writers = 0   │                    │
    │              │    shared_data = 0       │                    │
    │              └──────────────────────────┘                    │
    └──────────────────────────────────────────────────────────────┘
    ```
    """)
    
    st.markdown("#### 🔄 Execution Flow")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Reader Execution:**
        ```
        START
          ↓
        Acquire Mutex
          ↓
        Check waiting_writers
          ↓
        ┌─NO─→ Increment reader_count
        │       ↓
        │     If first reader:
        │       Acquire resource_lock
        │       ↓
        │     Release Mutex
        │       ↓
        │     READ DATA 📖
        │       ↓
        │     Acquire Mutex
        │       ↓
        │     Decrement reader_count
        │       ↓
        │     If last reader:
        │       Release resource_lock
        │       ↓
        │     Release Mutex
        │       ↓
        │     END
        │
        └─YES→ WAIT (Writer Priority)
                ↓
              (Loop back)
        ```
        """)
    
    with col2:
        st.markdown("""
        **Writer Execution:**
        ```
        START
          ↓
        Acquire Mutex
          ↓
        Increment waiting_writers 🎯
          ↓
        Release Mutex
          ↓
        Acquire resource_lock
        (Waits for readers)
          ↓
        Acquire Mutex
          ↓
        Decrement waiting_writers
          ↓
        Release Mutex
          ↓
        WRITE DATA ✍️
          ↓
        Release resource_lock
          ↓
        Acquire Mutex
          ↓
        Notify all waiting readers
          ↓
        Release Mutex
          ↓
        END
        ```
        """)

# Add explanation section
st.markdown("---")
st.markdown("### 💡 Key Concepts Explained")

expander1 = st.expander("🔍 What is Writer Priority?")
expander1.markdown("""
**Writer Priority** means that once a writer signals its intent to write (by incrementing `waiting_writers`):
- New readers are **blocked** from entering
- Current readers can **finish** their work
- Writer gets access as soon as all current readers are done
- This prevents writer **starvation**

**Without Writer Priority:** If readers keep arriving continuously, a writer might wait forever!
""")

expander2 = st.expander("🔐 Why Use Mutex and Locks?")
expander2.markdown("""
**Mutex (Mutual Exclusion Lock):**
- Protects shared variables like `reader_count` and `waiting_writers`
- Ensures only one thread modifies these at a time
- Prevents race conditions

**Resource Lock:**
- Ensures exclusive access to the shared data
- Writers hold this lock alone
- First reader acquires it, last reader releases it

**Without these:** Data corruption, race conditions, and unpredictable behavior!
""")

expander3 = st.expander("⚡ How Does Condition Variable Work?")
expander3.markdown("""
**Condition Variables** (`can_read`, `can_write`) allow threads to:
1. **Wait** for a specific condition
2. **Signal** other threads when condition changes
3. Avoid busy-waiting (CPU efficient)

**Example:**
```python
# Reader waits if writer has priority
while self.waiting_writers > 0:
    self.can_read.wait()  # Sleep until notified

# Writer notifies readers after writing
self.can_read.notify_all()  # Wake up all waiting readers
```
""")

expander4 = st.expander("📊 What Prevents Deadlock?")
expander4.markdown("""
**Deadlock Prevention Strategies Used:**

1. **Lock Ordering:** Always acquire locks in same order
2. **No Circular Wait:** Linear lock acquisition hierarchy
3. **Resource Release:** All locks eventually released
4. **Timeout Mechanisms:** (Can be added for production)

**In Our Implementation:**
- Readers and writers follow predictable patterns
- No thread holds multiple locks simultaneously for long
- Condition variables handle waiting efficiently
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Operating Systems Project</strong> | Readers-Writers Problem with Writer Priority</p>
    <p>Presented by: ZUHA JUNAID</p>
    <p>Supervisor: Mam AMMARA</p>
</div>
""", unsafe_allow_html=True)