# Task Graph

TG-001: GT-001 bootstrap

Nodes:
- T1: Create charter and policy artifacts
- T2: Create intake and product artifacts
- T3: Create engineering artifacts and task graph
- T4: Create execution artifacts and work order
- T5: Create knowledge artifacts
- T6: Create evaluation artifacts
- T7: Create state layer artifacts
- T8: Create evolution artifacts
- T9: Create bootstrap artifacts
- T10: Write run summary and evaluation trace

Edges:
- T1 -> T2 -> T3 -> T4 -> T6 -> T10
- T5 and T7 and T8 and T9 run in parallel after T3
