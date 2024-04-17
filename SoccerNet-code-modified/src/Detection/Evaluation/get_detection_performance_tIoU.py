import argparse
import numpy as np
import pandas as pd

from eval_detection import ANETdetection

def main(ground_truth_filename, prediction_filename,
         subset='validation', tiou_thresholds=np.linspace(0.5, 0.95, 10),
         verbose=True, check_status=True):

    anet_detection = ANETdetection(ground_truth_filename, prediction_filename,
                                   subset=subset, tiou_thresholds=tiou_thresholds,
                                   verbose=verbose, check_status=True)
    res = anet_detection.evaluate()
    return res

def parse_input():
    description = ('This script allows you to evaluate the ActivityNet '
                   'detection task which is intended to evaluate the ability '
                   'of  algorithms to temporally localize activities in '
                   'untrimmed video sequences.')
    p = argparse.ArgumentParser(description=description)
    p.add_argument('--ground_truth_filename',
                   help='Full path to json file containing the ground truth.')
    p.add_argument('--prediction_filename',
                   help='Full path to json file containing the predictions.')
    p.add_argument('--subset', default='validation',
                   help=('String indicating subset to evaluate: '
                         '(training, validation)'))
    p.add_argument('--tiou_thresholds', type=float, default=np.linspace(0.5, 0.95, 10),
                   help='Temporal intersection over union threshold.')
    p.add_argument('--verbose', type=bool, default=True)
    p.add_argument('--check_status', type=bool, default=True)
    return p.parse_args()

if __name__ == '__main__':
    args = parse_input()

    for k, DeltaGT in enumerate(range(30,0,-5)):
        for i, tIoU in enumerate(range(100,50,-5)):
        # DeltaGT = 60

            for j, WaterShedThresh in enumerate(range(95,0,-5)):
                # WaterShedThresh = 0.
                try:
                    args.verbose = True
                    args.ground_truth_filename = "../Results/labels_Delta_" + str(DeltaGT) + ".json"
                    args.prediction_filename = "../Results/predictions_Thesh_" + str(WaterShedThresh) + ".json"
                    print(tIoU/100.0)
                    args.tiou_thresholds = np.linspace(tIoU/100.0, tIoU/100.0, 1)
                    res = main(**vars(args))
                    print(res)

                    csv_file = "Results_Detection_Delta"+str(DeltaGT)+".csv"
                    print("saving results to csv file") 
                    df =  pd.read_csv(csv_file, index_col=0)
                    df.set_value(tIoU,str(WaterShedThresh),res)
                    df.to_csv(csv_file, sep=',', encoding='utf-8')
                    # print(DeltaGT, WaterShedThresh, res)
                except:
                    print("issue in :")
                    print("tIoU ", tIoU)
                    print("DeltaGT ",  DeltaGT)
                    print("WaterShedThresh ", WaterShedThresh)
