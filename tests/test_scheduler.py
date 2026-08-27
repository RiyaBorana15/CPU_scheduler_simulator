import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from scheduler import Process, fcfs, sjf, srtf, round_robin, priority_scheduling


class TestFCFS(unittest.TestCase):
    def test_basic_order(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=4),
            Process("P2", arrival_time=1, burst_time=3),
        ]
        result, gantt = fcfs(procs)
        by_pid = {p.pid: p for p in result}
        self.assertEqual(by_pid["P1"].completion_time, 4)
        self.assertEqual(by_pid["P2"].completion_time, 7)


class TestSJF(unittest.TestCase):
    def test_shortest_runs_first_when_available(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=6),
            Process("P2", arrival_time=0, burst_time=2),
            Process("P3", arrival_time=0, burst_time=4),
        ]
        result, gantt = sjf(procs)
        order = [pid for pid, _, _ in gantt]
        self.assertEqual(order, ["P2", "P3", "P1"])


class TestSRTF(unittest.TestCase):
    def test_all_processes_complete(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=8),
            Process("P2", arrival_time=1, burst_time=4),
        ]
        result, gantt = srtf(procs)
        self.assertEqual(len(result), 2)
        for p in result:
            self.assertGreater(p.completion_time, 0)


class TestRoundRobin(unittest.TestCase):
    def test_quantum_slicing(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=5),
            Process("P2", arrival_time=0, burst_time=3),
        ]
        result, gantt = round_robin(procs, quantum=2)
        self.assertTrue(len(gantt) >= 4)
        total_run = sum(end - start for _, start, end in gantt)
        self.assertEqual(total_run, 8)


class TestPriority(unittest.TestCase):
    def test_lower_number_runs_first(self):
        procs = [
            Process("P1", arrival_time=0, burst_time=5, priority=3),
            Process("P2", arrival_time=0, burst_time=2, priority=1),
        ]
        result, gantt = priority_scheduling(procs)
        self.assertEqual(gantt[0][0], "P2")


if __name__ == "__main__":
    unittest.main()
