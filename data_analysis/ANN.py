import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from random import sample
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

def scale_data(frame):
    cols = frame.columns
    frame = pd.DataFrame(sc.fit_transform(frame))
    frame.columns = cols
    
    return frame

def construct_confusion(truth, prediction):
    #Construct Confusion matrix
    confusion = np.array([[0,0],[0,0]])
    for i in range(0, len(truth)):
        if (truth[i] == 0):
            if prediction[i] == 0:
                confusion[0,0] += 1
            else:
                confusion[0,1] += 1
        else:
            if prediction[i] == 0:
                confusion[1,0] += 1
            else:
                confusion[1,1] += 1
                
    return confusion/len(truth)

def print_confusion(confusion):
    print("\n   Predicted Class")
    print("      0  |   1")
    print("0 | %.2f | %.2f |"%(confusion[0,0], confusion[0,1]))
    print("1 | %.2f | %.2f |\n"%(confusion[1,0], confusion[1,1]))

def print_accuracy(trained_model, X, X_test, Y, Y_test):
    prediction = trained_model.predict(X)
    truth = Y.to_numpy()
    diff = truth - prediction

    confusion_train = construct_confusion(truth, prediction)

    print("Training Accuracy: %.2f%%"%(100 - np.sum(np.abs(diff))*100/len(truth)))
    print_confusion(confusion_train)

    prediction = trained_model.predict(X_test)
    truth = Y_test.to_numpy()
    diff = truth - prediction

    confusion_test = construct_confusion(truth, prediction)

    print("Test Accuracy: %.2f%%"%(100 - np.sum(np.abs(diff))*100/len(truth)))
    print_confusion(confusion_test)

    print("In-Sample Percent Survivor: %.2f%%"%((confusion_train[1,1]*100)/(confusion_train[1,1]+confusion_train[1,0])))
    print("In-Sample Percent Fatality: %.2f%%"%((confusion_train[0,0]*100)/(confusion_train[0,1]+confusion_train[0,0])))
    print("Out-Sample Percent Survivor: %.2f%%"%((confusion_test[1,1]*100)/(confusion_test[1,1]+confusion_test[1,0])))
    print("Out-Sample Percent Fatality: %.2f%%"%((confusion_test[0,0]*100)/(confusion_test[0,1]+confusion_test[0,0])))

def split_train_and_test(full_dataset, percent_split):
	if not(percent_split > 0 and percent_split < 1):
		print("Invalid Split: Value must be between 0 and 1")
		return None
	
	data_points = full_dataset.shape[0]

	#Create Training_list
	training_list = sample(range(data_points), int(percent_split*data_points))
	training_list.sort()

	#Create Test List
	full = [x for x in range(0,data_points)]
	full_set = set(full)
	test_list = list(full_set - set(training_list))
	test_list.sort()

	training_set = full_dataset.iloc[training_list]
	test_set = full_dataset.iloc[test_list]

	training_set.reset_index(inplace=True, drop=True)
	test_set.reset_index(inplace=True, drop=True)

	if (training_set.shape[0] + test_set.shape[0]) == data_points:
		print("Good Split")
		return {'training_set':training_set, 'test_set': test_set}
	else:
		print("Whoops! BAD SPLIT. Not sure what happened :/")
		return None

def print_set_info(full_set, X, X_test, Y, Y_test):
	print("\nTrain Set Size: %.2f%%"%(X.shape[0]*100/full_set.shape[0]))
	print("Test Set Size:  %.2f%%"%(X_test.shape[0]*100/full_set.shape[0]))

	success = np.sum(full_set['Success'].to_numpy())
	total = len(full_set['Success'].to_numpy())
	print("\nOverall Success:   %.5f%%"%(success*100/total))

	success = np.sum(Y.to_numpy())
	total = len(Y.to_numpy())
	print("Training Success:  %.5f%%"%(success*100/total))

	success = np.sum(Y_test.to_numpy())
	total = len(Y_test.to_numpy())
	print("Test Success:      %.5f%%"%(success*100/total))
    

features = [
	'Duration',
	'acousticness',
	'danceability',
	'energy', 
	'instrumentalness',
	'key',
	'liveness',
	'loudness',
	'mode',
	'speechiness',
	'tempo',
	'time_signature',
	'valence'
]
target = 'Success'

data_file = "../data/full_dataset.csv"
big_frame = pd.read_csv(data_file, index_col=False)
big_frame = big_frame.astype({'Success': int})
print(big_frame.info())

"""data_sets = split_train_and_test(big_frame, 0.7)
training_set = data_sets['training_set']
test_set = data_sets['test_set']

X = training_set[features]
X = scale_data(X)
Y = training_set[target]

X_test = test_set[features]
X_test = scale_data(X_test)
Y_test = test_set[target]

print_set_info(big_frame, X, X_test, Y, Y_test)

clf = MLPClassifier(
        hidden_layer_sizes = (5000,),
        solver='adam',
        activation='logistic',
	batch_size = 500,#int(0.1*X.shape[0]),
        learning_rate='adaptive',
        learning_rate_init=1,
        verbose=True,
        momentum=0.9,
	alpha = 0.1,
        max_iter = 10000,
        random_state=1
    )

clf.fit(X,Y)
print_accuracy(clf, X, X_test, Y, Y_test)"""


