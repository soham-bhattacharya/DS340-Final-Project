import sys
sys.path.append('/home/giancos/git/SoccerDataset/B_Detection/ActivityNet/Evaluation')
from eval_proposal import ANETproposal

import matplotlib.pyplot as plt
import numpy as np
import json

# %matplotlib inline



def run_evaluation(ground_truth_filename, proposal_filename, 
                   max_avg_nr_proposals=100, 
                   tiou_thresholds=np.linspace(0.5, 0.95, 10),
                   subset='validation'):

    anet_proposal = ANETproposal(ground_truth_filename, proposal_filename,
                                 tiou_thresholds=tiou_thresholds,
                                 max_avg_nr_proposals=max_avg_nr_proposals,
                                 subset=subset, verbose=True, check_status=True)
    anet_proposal.evaluate()
    
    recall = anet_proposal.recall
    average_recall = anet_proposal.avg_recall
    average_nr_proposals = anet_proposal.proposals_per_video
    
    return (average_nr_proposals, average_recall, recall)

def plot_metric(average_nr_proposals, average_recall, recall, tiou_thresholds=np.linspace(0.5, 0.95, 10)):

    fn_size = 14
    plt.figure(num=None, figsize=(6, 5))
    ax = plt.subplot(1,1,1)
    
    colors = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9']

    area_under_curve = np.zeros_like(tiou_thresholds)
    for i in range(recall.shape[0]):
        area_under_curve[i] = np.trapz(recall[i], average_nr_proposals)

    for idx, tiou in enumerate(tiou_thresholds[::2]):
        ax.plot(average_nr_proposals, recall[2*idx,:], color=colors[idx+1],
                label="tiou=[" + str(tiou) + "], area=" + str(int(area_under_curve[2*idx]*100)/100.), 
                linewidth=4, linestyle='--', marker=None)

    # Plots Average Recall vs Average number of proposals.
    ax.plot(average_nr_proposals, average_recall, color=colors[0],
            label="tiou = 0.5:0.05:0.95," + " area=" + str(int(np.trapz(average_recall, average_nr_proposals)*100)/100.), 
            linewidth=4, linestyle='-', marker=None)

    handles, labels = ax.get_legend_handles_labels()
    ax.legend([handles[-1]] + handles[:-1], [labels[-1]] + labels[:-1], loc='best')
    
    plt.ylabel('Average Recall', fontsize=fn_size)
    plt.xlabel('Average Number of Proposals per Video', fontsize=fn_size)
    plt.grid(b=True, which="both")
    plt.ylim([0, 1.0])
    plt.setp(plt.axes().get_xticklabels(), fontsize=fn_size)
    plt.setp(plt.axes().get_yticklabels(), fontsize=fn_size)

    plt.show()






# %%time

uniform_average_nr_proposals_valid, uniform_average_recall_valid, uniform_recall_valid = run_evaluation(
    "labels_Delta_60.csv",
    "predictions_Thesh_1.csv",
    max_avg_nr_proposals=100,
    tiou_thresholds=np.linspace(0.5, 0.95, 10),
    # tiou_thresholds=np.linspace(0.5, 0., 2),
    subset='validation')

plot_metric(uniform_average_nr_proposals_valid, uniform_average_recall_valid, uniform_recall_valid)
