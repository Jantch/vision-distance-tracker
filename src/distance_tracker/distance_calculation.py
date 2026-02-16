from pathlib import Path
import time as t


class DistanceCalculator:
    def __init__(self, constant = None, status = False, interval : float = 0.2):
        self.constant = constant
        self.if_calibrated = status
        self.last_dist = 0
        self.last_update_time = 0 # [s]
        self.update_interval = interval #[s]

    def dist_calc_calibration(self, eye_dist_pix : float, curr_dist : float | int):
        self.constant = (eye_dist_pix * curr_dist)
        self.if_calibrated = True

    def get_status(self):
        return self.if_calibrated

    def get_dist(self, eye_dist_pix : float) -> float:
        try:
            dist = self.constant / eye_dist_pix
            self.last_dist = dist
            return dist
        except ZeroDivisionError:
            return self.last_dist

    def get_constant(self) -> float:
        return self.constant

    def set_status(self, status : bool):
        self.if_calibrated = status

    def get_last_update_time(self) -> float:
        return self.last_update_time

    def time_update(self):
        self.last_update_time = t.time()

    def should_calculate(self) -> bool:
        return t.time() - self.last_update_time >= self.update_interval

def calibration(dist_calc, eye_dist_pix):
    curr_dist = float(input("Enter your current distance from the screen: "))
    while curr_dist < 0 or not isinstance(curr_dist, (float, int)):
        print("Please enter a valid distance (float or int, positive value).\n")
        curr_dist = float(input("Enter your current distance from the screen: "))

    dist_calc.dist_calc_calibration(eye_dist_pix, curr_dist)

def save_calibration(file_path, constant):
    file_path.write_text(str(constant))

def delete_calibration(file_path, constant):
    file_path.write_text("")