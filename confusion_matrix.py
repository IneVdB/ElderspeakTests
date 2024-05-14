from sklearn.metrics import ConfusionMatrixDisplay

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import pandas as pd

true = pd.read_csv('tagged_csv/true.csv', header=None)
predict = pd.read_csv('tagged_csv/predict_new.csv', header=None)

y_true = true[1].tolist()
y_pred = predict[1].tolist()

labels = ["CVNW", "NONE", "TSW", "VKW"]


cm = confusion_matrix(y_true, y_pred)
print(cm)

accuracy = accuracy_score(y_true, y_pred)
print(accuracy)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot()
plt.show()

#old 0.9270754287448778
#new 0.9921460009106086
