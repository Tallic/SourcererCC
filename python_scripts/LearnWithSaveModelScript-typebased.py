import pandas as pd
import time as time
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import pickle

print("imports complete")
#path_train="./train/train.txt"
path_train="/scratch/mondego/local/farima/artifacts/train_exp/inputFiles/train_type3_1_fe.txt"
#path_test="./test/train_sample_100k.txt"
colNames=["block1", "block2", "isClone", "COMP", "NOCL", "NOS", "HLTH", "HVOC", "HEFF", "HBUG", "CREF", "XMET", "LMET", "NLOC", "NOC", "NOA", "MOD", 
"HDIF", "VDEC", "EXCT", "EXCR", "CAST", "TDN", "HVOL", "NAND", "VREF", "NOPR", "MDN", "NEXP", "LOOP",
"COMP_", "NOCL_", "NOS_", "HLTH_", "HVOC_", "HEFF_", "HBUG_", "CREF_", "XMET_", "LMET_", "NLOC_", "NOC_", "NOA_", "MOD_", "HDIF_", "VDEC_", "EXCT_", 
"EXCR_", "CAST_", "TDN_", "HVOL_", "NAND_", "VREF_", "NOPR_", "MDN_", "NEXP_", "LOOP_"]

#colNames=["block1", "block2", "isClone", "COMP", "NOCL", "NOS", "HLTH", "HVOC", "HEFF", "HBUG", "CREF", "XMET", "LMET", "NLOC", "NOC", "NOA", "MOD", 
#"HDIF", "VDEC", "EXCT", "EXCR", "CAST", "TDN", "HVOL", "NAND", "VREF", "NOPR", "MDN", "NEXP", "LOOP"]

clones_train = pd.read_csv(path_train, names=colNames, delimiter='~~', engine='python')
print("train set read complete")
#clones_test = pd.read_csv(path_test, names=colNames)
#print("test set read complete")

clones_train = clones_train.sample(frac=1).reset_index(drop=True) #shuffle data

array = clones_train.values
#X_train = array[:,[i for i in range(3,30+27) if i not in [4,4+27,5+27,8+27,13,13+27,14,14+27,16,16+27,23+27]]]
X_train = array[:,[i for i in range(3,30) if i not in [4,13,14,16]]]
Y_train = array[:,2]

#array = clones_test.values
#X_test = array[:,3:30]
#Y_test = array[:,2]


#Learn
clf = RandomForestClassifier(n_estimators=25, max_depth=20)
#clf = AdaBoostClassifier(base_estimator=DecisionTreeClassifier(max_depth=10, max_features='sqrt'), n_estimators=25)
#clf = DecisionTreeClassifier(max_depth=10, max_features='sqrt', min_samples_split=10, min_samples_leaf=5)
#clf = KNeighborsClassifier(n_neighbors=5)
start_time = time.time()
clf.fit(X_train, Y_train.astype(bool))
end_time=time.time()
print("time to build model: "+str((end_time-start_time)))
#Save model
filename = 'randfor_type31_25es20d_fe.sav'
pickle.dump(clf, open('./model_type/'+filename, 'wb'))
print("model saved")

#predict on this model
file_clonepair = open('./model_type/clonepairs_type31_20dfe.txt', 'w')
file_recall = open('./model_type/recall_type31_20dfe.txt', 'w')
file_falsepos=open('./model_type/falsepos_type31_20dfe.txt', 'w')
file_falseneg = open('./model_type/falseneg_type31_20dfe.txt', 'w')
clone_pairs = ''
falsepos=''
falseneg=''
start_time = time.time()
predictions = clf.predict(X_train)
end_time=time.time()
print("prediction complete! time taken: " + str(end_time- start_time))
file_recall.write(classification_report(Y_train.astype(bool), predictions))
file_recall.close()
for i in range(predictions.shape[0]):
    if predictions[i]:
        clone_pairs += (str(array[i][0]) + ',' + str(array[i][1]) + '\n')
        if not Y_train[i]:
            falsepos += (str(array[i][0]) + ',' + str(array[i][1]))
            for j in range(0, 30): # + 27):
                if j not in [0, 1, 2, 4, 4 + 27, 5 + 27, 8 + 27, 13, 13 + 27, 14, 14 + 27, 16, 16 + 27, 23 + 27]:
                    falsepos += ',' + str(array[i][j])
            falsepos = falsepos[:-1] + '\n'
    if not predictions[i]:
        if Y_train[i]:
            falseneg += (str(array[i][0]) + ',' + str(array[i][1]))
            for j in range(0, 30): # + 27):
                if j not in [0, 1, 2, 4, 4 + 27, 5 + 27, 8 + 27, 13, 13 + 27, 14, 14 + 27, 16, 16 + 27, 23 + 27]:
                    falseneg += ',' + str(array[i][j])
            falseneg = falseneg[:-1] + '\n'
file_clonepair.write(clone_pairs)
file_clonepair.close()
file_falsepos.write(falsepos)
file_falsepos.close()
file_falseneg.write(falseneg)
file_falseneg.close()


# load the model from disk
#start_time = time.time()
#loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.score(X_test, Y_test.astype(bool))
# print(result)
#predictions = loaded_model.predict(X_test)
#end_time=time.time()
#print("time to predict: "+str((end_time-start_time)))
#print(confusion_matrix(Y_test.astype(bool), predictions))
#print(classification_report(Y_test.astype(bool), predictions))