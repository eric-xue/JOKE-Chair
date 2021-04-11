import pandas as pd
import sys

POSTURES = ["proper", "lean_forward", "lean_right", "lean_left", "slouch", "right_leg_cross", "left_leg_cross"]


def generate_data_set(filename):
    data_set = pd.DataFrame()
    for posture in POSTURES:
        df = pd.read_csv("data/{}.csv".format(posture))
        data_set = pd.concat([data_set, df[:1000]]).reset_index(drop=True)

    data_set.to_csv("data/{}.csv".format(filename), index=False)

    exit(0)



if __name__ == "__main__":
    generate_data_set(sys.argv[1])