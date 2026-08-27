# CPU Scheduling Algorithms Simulator

A Computer Engineering / Operating Systems mini-project that implements
and compares the classic CPU scheduling algorithms taught in every OS
course. Written in pure Python (no external dependencies), with unit
tests and a console Gantt chart.

## Features

- **FCFS** — First Come First Serve
- **SJF** — Shortest Job First (non-preemptive)
- **SRTF** — Shortest Remaining Time First (preemptive)
- **Round Robin** — with configurable time quantum
- **Priority Scheduling** — non-preemptive, lower number = higher priority

For each algorithm the simulator prints:
- Completion time, turnaround time, and waiting time per process
- Average waiting time and average turnaround time
- An ASCII Gantt chart of execution order

## Project Structure

```
cpu-scheduler-simulator/
├── src/
│   ├── scheduler.py   # All scheduling algorithm implementations
│   └── main.py        # CLI entry point / demo runner
├── tests/
│   └── test_scheduler.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.8+

### Run the simulator
```bash
git clone <your-repo-url>
cd cpu-scheduler-simulator
python src/main.py
```

### Run the tests
```bash
python -m unittest discover -s tests -v
```

## Customizing the Workload

Edit `build_sample_processes()` in `src/main.py`:

```python
Process(pid="P1", arrival_time=0, burst_time=5, priority=2)
```

Add, remove, or change processes, then re-run `python src/main.py`.

## Sample Output

```
==================================================
 First Come First Serve (FCFS)
==================================================
PID   Arrival   Burst   Completion  Turnaround  Waiting
P1    0         5       5           5           0
P2    1         3       8           7           4
...
Average Waiting Time:    ...
Average Turnaround Time: ...
```

## Possible Extensions

- Multilevel Feedback Queue scheduling
- Read process lists from a CSV/JSON file
- Plot Gantt charts graphically with `matplotlib`
- Wrap the simulator in a small Flask/Streamlit web UI

## License

MIT — see [LICENSE](LICENSE).
