import sys
if __name__ == '__main__':
    filename = 'nboutput.txt'  # local
    # filename = sys.argv[0]
    correct_prediction, total_samples = 0, 0
    tp, tn, fp, fn = 0, 0, 0, 0
    with open(filename, "r") as read_ptr:
        results = read_ptr.readlines()
        for result in results:
            predicted_label, directory = result.split('C:')
            print(predicted_label, directory)
            if 'spam' in directory:
                ground_truth = 'spam'
            elif 'ham' in directory:
                ground_truth = 'ham'
            else:
                continue
            if ground_truth == predicted_label.strip():
                correct_prediction += 1
                if ground_truth == 'spam':
                    tp += 1
                elif ground_truth == 'ham':
                    tn += 1
            else:
                if ground_truth == 'spam' and predicted_label.strip() == 'ham':
                    fn += 1
                elif ground_truth == 'ham' and predicted_label.strip() == 'spam':
                    fp += 1
            total_samples += 1

    print("Accuracy", (correct_prediction/total_samples)*100)

    # calculate precision, recall, F1 score
    # calculating evalutions for spam
    s_precision = tp / (tp + fp)
    s_recall = tp / (tp + fn)
    s_f1 = 2 * (s_precision * s_recall) / (s_precision + s_recall)
    print("Spam Precision", s_precision)
    print("Spam Recall", s_recall)
    print("Spam F1 Score", s_f1)
    # calculating evaluations for ham
    h_precision = tn / (tn + fn)
    h_recall = tn / (tn + fp)
    h_f1 = 2 * (h_precision * h_recall) / (h_precision + h_recall)
    print("Ham Precision", h_precision)
    print("Ham Recall", h_recall)
    print("Ham F1 Score", h_f1)
