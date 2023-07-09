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
    window.setFixedHeight(500)
    
    acts = activities.get_all_activities()

    for a in range(0,len(acts)):
        frame=QLabel(acts[a].name)
        frame.setWordWrap(True)
        frame.setFrameStyle(QFrame.Shape.Panel)
        frame.setLineWidth(1)
        layout.addWidget(frame, 0, a, 1 ,1)

    solver = ScheduleSolver(100)

    # def signal_handler(sig, frame):
    #     print('You pressed Ctrl+C!')
    #     sys.exit(0)

    # signal.signal(signal.SIGINT, signal_handler)

    sch = solver.solve().sch

    for col in range(0,sch.shape[1]):
        row = 0
        while row < sch.shape[0]:
            if row == -1:
                frame=QLabel()

            leg = sch[row,col]

            length = 0
            newleg = leg

            while np.equal(newleg,leg).all():
                length = length + 1
                row = row + 1

                if row >= sch.shape[0]:
                    break

                newleg = sch[row,col]

            frame = QLabel(str(leg))
            frame.setFrameStyle(QFrame.Shape.Panel)
            frame.setLineWidth(1)
            layout.addWidget(frame, row-length+1, col, length ,1)

            # row = row + 1

    window.setLayout(layout)
   
    # helloMsg.move(60, 15)



    
    window.show()

    print(sch)


    sys.exit(app.exec())