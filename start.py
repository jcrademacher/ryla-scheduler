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
    window.setFixedHeight(800)
    
    acts = activities.get_all_activities()
    num_legs = 12
    num_slots = 48

    for a in range(0,num_legs):
        frame=QLabel(str(a+1))
        frame.setWordWrap(True)
        frame.setFrameStyle(QFrame.Shape.Panel)
        frame.setLineWidth(1)
        layout.addWidget(frame, 0, a, 1 ,1)

    pop_size = 200
    solver = ScheduleSolver(pop_size,num_legs=num_legs,num_slots=num_slots)

    # def signal_handler(sig, frame):
    #     print('You pressed Ctrl+C!')
    #     sys.exit(0)

    # signal.signal(signal.SIGINT, signal_handler)

    (solution,fitnesses) = solver.solve()
    sch = solution.sch
    
    # sch = np.fromfile("schedules/schedule_pop100_ep10_mp50_i1000_07m-10d-23y_23H-36M-49S.bin",'uint32').reshape((20,5))
    # sch_obj = Schedule(num_legs=12)
    # sch = sch_obj.sch

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

            if adx == -1:
                name = "Break"
            else:
                name = acts[adx].name

            frame = QLabel(acts[adx].name)
            frame.setFrameStyle(QFrame.Shape.Panel)
            frame.setLineWidth(1)
            layout.addWidget(frame, row-length+1, col, length ,1)

            # row = row + 1

    window.setLayout(layout)
   
    # helloMsg.move(60, 15)

    from datetime import datetime
    now = datetime.now()

    date_str = now.strftime("%mm-%dd-%yy_%HH-%MM-%SS")
    fitnesses.astype("uint32").tofile(f"fitnesses/fitness_pop{pop_size}_ep{solver.elitist_pct}_mp{solver.mate_fitness_pct}_i{solver.max_iters}_{date_str}.bin")
    sch.astype("uint32").tofile(f"schedules/schedule_pop{pop_size}_ep{solver.elitist_pct}_mp{solver.mate_fitness_pct}_i{solver.max_iters}_{date_str}.bin")
    
    window.show()

    

    # print(sch_obj.get_leg_schedule(1))


    sys.exit(app.exec())