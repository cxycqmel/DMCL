import sys
import json

# epoch 40
# {'accuracy': 0.8267272727272728, 'out_of_scope_recall': 0.308, 'out_of_scope_precision': 0.9005847953216374, 'in_scope_accuracy': 0.942, 'all_recalls': [1.0, 0.9, 0.9666666666666667, 0.0, 0.9, 0.8666666666666667, 0.9666666666666667, 1.0, 1.0, 0.9, 1.0, 0.9666666666666667, 0.9, 0.9, 0.9333333333333333, 1.0, 1.0, 1.0, 1.0, 0.9, 0.9666666666666667, 0.9666666666666667, 0.9666666666666667, 1.0, 0.9333333333333333, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9333333333333333, 0.9666666666666667, 0.9666666666666667, 1.0, 0.7666666666666667, 1.0, 1.0, 0.9, 0.9, 0.8666666666666667, 0.9333333333333333, 0.9333333333333333, 0.9666666666666667, 0.9666666666666667, 1.0, 0.9333333333333333, 0.8333333333333334, 1.0, 1.0, 1.0, 0.9, 0.9666666666666667, 1.0, 1.0, 1.0, 1.0, 0.9333333333333333, 1.0, 0.9333333333333333, 0.9666666666666667, 0.9, 0.7666666666666667, 0.9, 0.9333333333333333, 0.9, 1.0, 1.0, 0.9666666666666667, 0.9666666666666667, 0.9, 0.9, 0.9333333333333333, 0.9666666666666667, 1.0, 0.9666666666666667, 0.9666666666666667, 1.0, 0.9, 1.0, 1.0, 0.8333333333333334, 1.0, 1.0, 1.0, 1.0, 0.9666666666666667, 0.9666666666666667, 0.9666666666666667, 0.9666666666666667, 0.8333333333333334, 0.8666666666666667, 0.9666666666666667, 0.8666666666666667, 0.9, 0.9333333333333333, 0.8, 0.9333333333333333, 0.9666666666666667, 0.9666666666666667, 1.0, 1.0, 1.0, 0.8333333333333334, 0.6333333333333333, 0.9333333333333333, 0.9666666666666667, 1.0, 0.9666666666666667, 1.0, 1.0, 0.9666666666666667, 0.9333333333333333, 1.0, 1.0, 1.0, 0.8, 1.0, 0.9666666666666667, 1.0, 1.0, 0.9333333333333333, 0.9666666666666667, 0.9666666666666667, 0.9666666666666667, 0.9666666666666667, 0.9, 0.9666666666666667, 0.9333333333333333, 0.9, 0.9666666666666667, 0.8, 0.8333333333333334, 1.0, 0.9333333333333333, 0.9666666666666667, 0.9333333333333333, 1.0, 1.0, 1.0, 1.0, 0.9666666666666667, 1.0, 1.0, 0.7333333333333333, 0.9666666666666667, 0.9666666666666667, 0.8666666666666667, 1.0, 1.0, 0.7666666666666667]}

def main():
  all_accs = []
  all_precs = []
  all_recalls = []
  all_f1s = []
  all_metrics = []
  v_all_accs = []
  v_all_precs = []
  v_all_recalls = []
  v_all_f1s = []
  v_all_metrics = []
  fname = sys.argv[1]
  valid_fname = sys.argv[2]
  with open(fname) as fin, open(valid_fname) as vfin:
    for line in fin:
      if line.startswith("epoch"):
        key = line.strip()
      else:
        metrics = json.loads(line.replace("'", '"'))
        in_scope_acc = metrics['in_scope_accuracy']
        prec = metrics['out_of_scope_precision']
        recall = metrics['out_of_scope_recall']
        f1 = 2*prec*recall/(prec+recall+1e-12)
        metrics['out_of_scope_f1'] = f1
  
        all_accs.append(in_scope_acc)
        all_precs.append(prec)
        all_recalls.append(recall)
        all_f1s.append(f1)
        all_metrics.append(metrics)
  
    for line in vfin:
      if line.startswith("epoch"):
        key = line.strip()
      else:
        metrics = json.loads(line.replace("'", '"'))
        in_scope_acc = metrics['in_scope_accuracy']
        prec = metrics['out_of_scope_precision']
        recall = metrics['out_of_scope_recall']
        f1 = 2*prec*recall/(prec+recall+1e-12)
        metrics['out_of_scope_f1'] = f1
  
        v_all_accs.append(in_scope_acc)
        v_all_precs.append(prec)
        v_all_recalls.append(recall)
        v_all_f1s.append(f1)
        v_all_metrics.append(metrics)
 
  if len(v_all_metrics) != len(all_metrics):
    return 
  
  max_acc = max(v_all_accs)
  max_acc_index = v_all_accs.index(max_acc)
  max_f1 = max(v_all_f1s)
  max_f1_index = v_all_f1s.index(max_f1)
  
  print("max in scope accuracy: ", all_accs[max_acc_index], " at epoch [{}]".format(max_acc_index+1))
  print("out_of_scope_f1: ", all_metrics[max_acc_index]['out_of_scope_f1'])
  print("max out scope f1: ", all_f1s[max_f1_index], " at epoch [{}]".format(max_f1_index+1))
  print("in_scope_accuracy: ", all_metrics[max_f1_index]['in_scope_accuracy'])

if __name__ == "__main__":
  main()
