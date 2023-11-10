from schedule import Schedule
from solver import ScheduleSolver
import activities
import sys
import numpy as np
import signal

from threading import Thread

# 1. Import QApplication and all the required widgets
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QFrame

# Run the app
if __name__ == "__main__":

    # pop_size = 100

    # schedules = []

    # for i in range(0,pop_size):
    #     sch = Schedule()
    #     schedules.append(sch)

    app = QApplication([])

    layout = QGridLayout()
    layout.setHorizontalSpacing(0)
    layout.setVerticalSpacing(0)

    window = QWidget()
    window.setWindowTitle("PyQt App")
    # window.setFixedHeight(800)
    
    acts = activities.get_all_activities()
    num_legs = 8
    num_slots = 8

    for a in range(0,num_legs):
        frame=QLabel(str(a+1))
        frame.setWordWrap(True)
        frame.setFrameStyle(QFrame.Shape.Panel)
        frame.setLineWidth(1)
        layout.addWidget(frame, 0, a, 1 ,1)

    pop_size = 40
    solver = ScheduleSolver(pop_size,num_legs=num_legs,num_slots=num_slots)

    def signal_handler(sig, frame):
        solver.exit()

    signal.signal(signal.SIGINT, signal_handler)

    # solver.exit()
    (solution,fitnesses) = solver.solve()
    
    sch = solution.sch

    solution.print_summary()
    
    # sch = np.fromfile("schedules/schedule_pop10_ep10_mp50_i1000_07m-11d-23y_11H-17M-56S.bin",'uint32').reshape((num_slots,num_legs))
    # sch_obj = Schedule(num_legs=12)
    # sch = sch_obj.sch

    act_lengths = activities.get_activities_mapped(lambda a: a.length)

    # sch = solution.expand()
    overlaps = solution.get_overlaps()

    for col in range(0,sch.shape[1]):
        row = 0
        while row < sch.shape[0]:
            if row == -1:
                frame=QLabel()

            
            adx = sch[row,col]

            length = 0
            newadx = adx

            while newadx == adx:
                length = length + 1
                row = row + 1

                if row >= sch.shape[0]:
                    break

                newadx = sch[row,col]


            name = f"{acts[adx].name} (l={length})"

            frame = QLabel(name)

            if overlaps[row-length:row,col].any():
                frame.setStyleSheet("background-color: red")

            frame.setFrameStyle(QFrame.Shape.Panel)
            frame.setWordWrap(True)
            frame.setLineWidth(1)
            layout.addWidget(frame, row-length+1, col, length ,1)

            # row = row + 1

    window.setLayout(layout)
   
    # helloMsg.move(60, 15)

    from datetime import datetime
    now = datetime.now()

    # date_str = now.strftime("%mm-%dd-%yy_%HH-%MM-%SS")
    # fitnesses.astype("uint32").tofile(f"fitnesses/fitness_pop{pop_size}_ep{solver.elitist_pct}_mp{solver.mate_fitness_pct}_i{solver.max_iters}_{date_str}.bin")
    # sch.astype("uint32").tofile(f"schedules/schedule_pop{pop_size}_ep{solver.elitist_pct}_mp{solver.mate_fitness_pct}_i{solver.max_iters}_{date_str}.bin")
    
    window.show()
   
    sys.exit(app.exec())