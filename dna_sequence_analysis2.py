# -*- coding: utf-8 -*-
"""DNA Sequence Analysis2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qEqVXoOu0yp_DXmPBhTSfRTDB-kSPgYt

# **Human Data**
"""

from google.colab import drive
drive.mount('/content/drive')

pip install biopython

# Commented out IPython magic to ensure Python compatibility.
from ast import increment_lineno
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from IPython.display import Image
import Bio
from Bio.Seq import Seq
from Bio.SeqUtils import GC
plt.style.use('seaborn-darkgrid')
# %matplotlib inline

"""# **EDA**"""

labels = ['G protein coupled receptors','Tyrosine Kinase','Tyrosine phosphatase','Synthetase','Synthase','Ion channel','Transcription Factor']

Image('/content/drive/MyDrive/_results_.jpeg')

import os
os.chdir("/content/drive/MyDrive")

human= pd.read_table('human_data.txt')
human.head(3500)

human.info()

human.describe()

human["class"].value_counts()

seq = Seq(human["sequence"][0])
print(seq)

print(f" Complement : {seq.complement()} \n")
print(f"Reverse Complement :  {seq.reverse_complement()} " )

print("GC% :\t" + str(GC(seq)))

sns.barplot(x=human["class"].value_counts().sort_index(),y=labels)
plt.title("Class frequency for human data")
plt.xlabel('Frequency')
plt.ylabel('Protein class')
#plt.style.use('dark_background')
plt.show()

plt.figure(figsize=(6,6))
font_dict=font = {'family': 'serif',
        'color':  'Black',
        'size': 20,
        }
a=np.random.random(7)
cs=cm.Set1(np.arange(7)/7.)
plt.pie(human["class"].value_counts().sort_index(),labels=labels,autopct='%1.1f%%',colors=cs,startangle=90)
plt.axis('equal')
plt.title("Human data Protein class",fontdict=font_dict)
#plt.style.use('dark_background')
plt.show()

human['sequence'][20]

def noise_check(arr):
    d=[]
    count = 0
    for i in range(0,len(arr)):
        for j in arr['sequence'][i]:
            if j!='A' and j!='T' and j!='C' and j!='G':
                count = count + 1
                d.append(j)
    if count>0:
        print(d)
        print('Noise Count',count)
    else:
        print('No noise')

noise_check(human)

def remove_noise(arr):
  for i in range (0,len(arr)):
    arr['sequence'][i]=arr['sequence'][i].replace('N','')

remove_noise(human)

noise_check(human)

def missing_check(arr):
    classat=[]
    seqat=[]
    count = 0
    for i in range(0,len(arr)):
        if arr['sequence'][i]=='':
            seqat.append(i)
            count = count + 1
        if arr['class'][i]=='' or arr['class'][i]>6:
            classat.append(i)
            count = count + 1
    if count==0:
        print('No missing value')
    else:
        print('missing count = ',count)

missing_check(human)

human['class'].value_counts().sort_index().plot.bar()
#plt.style.use('dark_background')

y=human.loc[:,'class'].values

"""# **Classifiers**"""

from sklearn.feature_extraction.text import CountVectorizer

documents = [
    "This is the first document.",
    "And My name is Manoj Dey.",
    "And team members are Sayantika Das,Koustubh Manjumdar,Madhushree Ghosh .",
    "Is this our first Prject ?"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()
print("Matrix of token counts:")
print(X.toarray())
print("\nFeature names:")
print(feature_names)

def getKmers(sequence, size=6):
    return [sequence[x:x+size].lower() for x in range(len(sequence) - size + 1)]
cv = CountVectorizer(ngram_range=(4,4))

human['Words']=human.apply(lambda X: getKmers(X['sequence']),axis=1)
human=human.drop('sequence',axis =1)

human.head()

human["in_string"] =human['Words'].apply(lambda x:  ' '.join(x))

human[["Words","in_string"]]

print(human['Words'][0])

human_texts = list(human['Words'])
for item in range(len(human_texts)):
    human_texts[item] = ' '.join(human_texts[item])

X_h = cv.fit_transform(human_texts)
y_h = human.iloc[:, 0].values

print(X_h.shape,y_h.shape)

i=0
for key,value in cv.vocabulary_.items():
    print(f"{key} : {value}")
    i+=1
    if i>10:break

(human_texts[1])

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import xgboost as xgb
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import *

from sklearn.model_selection import train_test_split
X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_h,y_h,test_size = 0.25,random_state=42)

dtree_h = DecisionTreeClassifier()
dtree_h.fit(X_train_h,y_train_h)
dtree_h_pred = dtree_h.predict(X_test_h)
print(confusion_matrix(y_test_h, dtree_h_pred))
print(classification_report(y_test_h, dtree_h_pred))

rf_h = RandomForestClassifier(n_estimators=400)
rf_h.fit(X_train_h,y_train_h)
rf_h_pred = rf_h.predict(X_test_h)
print(confusion_matrix(y_test_h, rf_h_pred))
print(classification_report(y_test_h, rf_h_pred))

xgb_h = xgb.XGBClassifier()
xgb_h.fit(X_train_h,y_train_h)
xgb_h_pred = xgb_h.predict(X_test_h)
print(confusion_matrix(y_test_h, xgb_h_pred))
print(classification_report(y_test_h,xgb_h_pred))

NB_h = MultinomialNB(alpha=0.1)
NB_h.fit(X_train_h,y_train_h)
NB_h_pred = NB_h.predict(X_test_h)
print(confusion_matrix(y_test_h, NB_h_pred))
print(classification_report(y_test_h,NB_h_pred))

AdaB_h = AdaBoostClassifier(n_estimators=400)
AdaB_h.fit(X_train_h,y_train_h)
AdaB_h_pred = AdaB_h.predict(X_test_h)
print(confusion_matrix(y_test_h, AdaB_h_pred))
print(classification_report(y_test_h, AdaB_h_pred))

MLP_h = MLPClassifier(alpha=1)
MLP_h.fit(X_train_h,y_train_h)
MLP_h_pred = MLP_h.predict(X_test_h)
print(confusion_matrix(y_test_h, MLP_h_pred))
print(classification_report(y_test_h, MLP_h_pred))

SVC_h = SVC()
SVC_h.fit(X_train_h,y_train_h)
SVC_h_pred = SVC_h.predict(X_test_h)
print(confusion_matrix(y_test_h, SVC_h_pred))
print(classification_report(y_test_h, SVC_h_pred))

plt.figure(figsize=(10,5))
scores=["Naive Bayes","Random Forest","Decision Tree","svm","AdaBoostClassifier","neural_network","xgboost"]
accscore=[98,92,80,81,51,95,90]
f1score=[99,95,87,88,68,98,93]
w=0.2
bar1=np.arange(len(scores))
bar2=[i+w for i in bar1]

plt.bar(bar1,accscore,w,label="accuracy")
plt.bar(bar2,f1score,w,label="f1score")
plt.xticks(bar1, scores)
plt.legend()
plt.title("Comparision Between Models")
#plt.style.use('dark_background')
plt.show()

from sklearn.model_selection import train_test_split
X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_h,
                                                    y_h,
                                                    test_size = 0.20,
                                                    random_state=42)
nb_ =MultinomialNB(alpha=0.01)
nb_.fit(X_train_h, y_train_h)

y_pred = nb_.predict(X_test_h)
print(pd.crosstab(pd.Series(y_test_h, name='Actual'), pd.Series(y_pred, name='Predicted')))

import pickle

filename = 'finalized_model.sav'
pickle.dump(nb_, open(filename, 'wb'))

plt.figure(figsize=(7,6))
sns.heatmap(pd.crosstab(pd.Series(y_test_h, name='Actual'), pd.Series(y_pred, name='Predicted')),cmap="YlGnBu",annot=True,fmt='d')
#plt.style.use('dark_background')

"""# **For Chimpanzee**"""

pip install biopython

# Commented out IPython magic to ensure Python compatibility.
from ast import increment_lineno
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from IPython.display import Image
import Bio
from Bio.Seq import Seq
from Bio.SeqUtils import GC
plt.style.use('seaborn-darkgrid')
# %matplotlib inline

labels = ['G protein coupled receptors','Tyrosine Kinase','Tyrosine phosphatase','Synthetase','Synthase','Ion channel','Transcription Factor']

Image('/content/drive/MyDrive/chimp_dna.png')

chimpanzee = pd.read_table('chimp_data.txt')
chimpanzee.head(3500)

chimpanzee.info()

chimpanzee.describe()

chimpanzee["class"].value_counts()

seq = Seq(chimpanzee["sequence"][0])
print(seq)

print(f" Complement : {seq.complement()} \n")
print(f"Reverse Complement :  {seq.reverse_complement()} " )

print("GC% :\t" + str(GC(seq)))

sns.barplot(x=chimpanzee["class"].value_counts().sort_index(),y=labels)
plt.title("Class frequency for chimpanzee data")
plt.xlabel('Frequency')
plt.ylabel('Protein class')
#plt.style.use('dark_background')
plt.show()

plt.figure(figsize=(6,6))
font_dict=font = {'family': 'serif',
        'color':  'Black',
        'size': 20,
        }
a=np.random.random(7)
cs=cm.Set1(np.arange(7)/7.)
plt.pie(chimpanzee["class"].value_counts().sort_index(),labels=labels,autopct='%1.1f%%',colors=cs,startangle=90)
plt.axis('equal')
plt.title("Chimpanzee data Protein class",fontdict=font_dict)
#plt.style.use('dark_background')
plt.show()

chimpanzee['sequence'][20]

def noise_check(arr):
    d=[]
    count = 0
    for i in range(0,len(arr)):
        for j in arr['sequence'][i]:
            if j!='A' and j!='T' and j!='C' and j!='G':
                count = count + 1
                d.append(j)
    if count>0:
        print(d)
        print('Noise Count',count)
    else:
        print('No noise')

noise_check(chimpanzee)

def remove_noise(arr):
  for i in range (0,len(arr)):
    arr['sequence'][i]=arr['sequence'][i].replace('N','')

remove_noise(chimpanzee)

noise_check(chimpanzee)

def missing_check(arr):
    classat=[]
    seqat=[]
    count = 0
    for i in range(0,len(arr)):
        if arr['sequence'][i]=='':
            seqat.append(i)
            count = count + 1
        if arr['class'][i]=='' or arr['class'][i]>6:
            classat.append(i)
            count = count + 1
    if count==0:
        print('No missing value')
    else:
        print('missing count = ',count)

missing_check(chimpanzee)

chimpanzee['class'].value_counts().sort_index().plot.bar()
#plt.style.use('dark_background')

y=chimpanzee.loc[:,'class'].values

"""# **Classifiers**"""

from sklearn.feature_extraction.text import CountVectorizer

documents = [
    "This is the first document.",
    "And My name is Manoj Dey.",
    "And team members are Sayantika Das,Koustubh Manjumdar,Madhushree Ghosh .",
    "Is this our first Prject ?"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()
print("Matrix of token counts:")
print(X.toarray())
print("\nFeature names:")
print(feature_names)

def getKmers(sequence, size=6):
    return [sequence[x:x+size].lower() for x in range(len(sequence) - size + 1)]
cv = CountVectorizer(ngram_range=(4,4))

chimpanzee['Words']=chimpanzee.apply(lambda X: getKmers(X['sequence']),axis=1)
chimpanzee=chimpanzee.drop('sequence',axis =1)

chimpanzee.head()

chimpanzee["in_string"] =chimpanzee['Words'].apply(lambda x:  ' '.join(x))

chimpanzee[["Words","in_string"]]

print(chimpanzee['Words'][0])

chimpanzee_texts1 = list(chimpanzee['Words'])
for item in range(len(chimpanzee_texts1)):
    chimpanzee_texts1[item] = ' '.join(chimpanzee_texts1[item])

X_c = cv.fit_transform( chimpanzee_texts1)
y_c = chimpanzee.iloc[:, 0].values

print(X_c.shape,y_c.shape)

i=0
for key,value in cv.vocabulary_.items():
    print(f"{key} : {value}")
    i+=1
    if i>10:break

(chimpanzee_texts1[1])

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import xgboost as xgb
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import *

from sklearn.model_selection import train_test_split
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_c,y_c,test_size = 0.25,random_state=42)

dtree_c = DecisionTreeClassifier()
dtree_c.fit(X_train_c,y_train_c)
dtree_c_pred = dtree_c.predict(X_test_c)
print(confusion_matrix(y_test_c, dtree_c_pred))
print(classification_report(y_test_c, dtree_c_pred))

rf_c = RandomForestClassifier(n_estimators=400)
rf_c.fit(X_train_c,y_train_c)
rf_c_pred = rf_c.predict(X_test_c)
print(confusion_matrix(y_test_c, rf_c_pred))
print(classification_report(y_test_c, rf_c_pred))

xgb_c = xgb.XGBClassifier()
xgb_c.fit(X_train_c,y_train_c)
xgb_c_pred = xgb_c.predict(X_test_c)
print(confusion_matrix(y_test_c, xgb_c_pred))
print(classification_report(y_test_c,xgb_c_pred))

NB_c = MultinomialNB(alpha=0.1)
NB_c.fit(X_train_c,y_train_c)
NB_c_pred = NB_c.predict(X_test_c)
print(confusion_matrix(y_test_c, NB_c_pred))
print(classification_report(y_test_c,NB_c_pred))

AdaB_c = AdaBoostClassifier(n_estimators=400)
AdaB_c.fit(X_train_c,y_train_c)
AdaB_c_pred = AdaB_c.predict(X_test_c)
print(confusion_matrix(y_test_c, AdaB_c_pred))
print(classification_report(y_test_c, AdaB_c_pred))

MLP_c = MLPClassifier(alpha=1)
MLP_c.fit(X_train_c,y_train_c)
MLP_c_pred = MLP_c.predict(X_test_c)
print(confusion_matrix(y_test_c, MLP_c_pred))
print(classification_report(y_test_c, MLP_c_pred))

SVC_c = SVC()
SVC_c.fit(X_train_c,y_train_c)
SVC_c_pred = SVC_c.predict(X_test_c)
print(confusion_matrix(y_test_c, SVC_c_pred))
print(classification_report(y_test_c, SVC_c_pred))

plt.figure(figsize=(10,5))
scores=["Naive Bayes","Random Forest","Decision Tree","svm","AdaBoostClassifier","neural_network","xgboost"]
accscore=[90,82,77,75,47,91,86]
f1score=[98,100,90,85,60,99,95]
w=0.2
bar1=np.arange(len(scores))
bar2=[i+w for i in bar1]

plt.bar(bar1,accscore,w,label="accuracy")
plt.bar(bar2,f1score,w,label="f1score")
plt.xticks(bar1, scores)
plt.legend()
plt.title("Comparision Between Models")
#plt.style.use('dark_background')
plt.show()

from sklearn.model_selection import train_test_split
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_c,
                                                    y_c,
                                                    test_size = 0.20,
                                                    random_state=42)
nb_ =MultinomialNB(alpha=0.01)
nb_.fit(X_train_c, y_train_c)

y_pred = nb_.predict(X_test_c)
print(pd.crosstab(pd.Series(y_test_c, name='Actual'), pd.Series(y_pred, name='Predicted')))

import pickle

filename = 'finalized_model.sav'
pickle.dump(nb_, open(filename, 'wb'))

plt.figure(figsize=(7,6))
sns.heatmap(pd.crosstab(pd.Series(y_test_c, name='Actual'), pd.Series(y_pred, name='Predicted')),cmap="YlGnBu",annot=True,fmt='d')
#plt.style.use('dark_background')

"""# **Human VS Chimpanzee**"""

Image('/content/drive/MyDrive/sequence-alignment_med.jpeg')

"""# **For Dog DNA Analysis**"""

labels = ['G protein coupled receptors','Tyrosine Kinase','Tyrosine phosphatase','Synthetase','Synthase','Ion channel','Transcription Factor']

Image('/content/drive/MyDrive/dog_dna.jpg')

dog = pd.read_table('dog.txt')
dog.head(3500)

dog.info()

dog.describe()

dog["class"].value_counts()

seq = Seq(dog["sequence"][0])
print(seq)

print(f" Complement : {seq.complement()} \n")
print(f"Reverse Complement :  {seq.reverse_complement()} " )

print("GC% :\t" + str(GC(seq)))

sns.barplot(x=dog["class"].value_counts().sort_index(),y=labels)
plt.title("Class frequency for dog data")
plt.xlabel('Frequency')
plt.ylabel('Protein class')
#plt.style.use('dark_background')
plt.show()

plt.figure(figsize=(6,6))
font_dict=font = {'family': 'serif',
        'color':  'Black',
        'size': 20,
        }
a=np.random.random(7)
cs=cm.Set1(np.arange(7)/7.)
plt.pie(dog["class"].value_counts().sort_index(),labels=labels,autopct='%1.1f%%',colors=cs,startangle=90)
plt.axis('equal')
plt.title("Dog data Protein class",fontdict=font_dict)
#plt.style.use('dark_background')
plt.show()

dog['sequence'][20]

def noise_check(arr):
    d=[]
    count = 0
    for i in range(0,len(arr)):
        for j in arr['sequence'][i]:
            if j!='A' and j!='T' and j!='C' and j!='G':
                count = count + 1
                d.append(j)
    if count>0:
        print(d)
        print('Noise Count',count)
    else:
        print('No noise')

noise_check(dog)

def remove_noise(arr):
  for i in range (0,len(arr)):
    arr['sequence'][i]=arr['sequence'][i].replace('N','')

remove_noise(dog)

noise_check(dog)

def missing_check(arr):
    classat=[]
    seqat=[]
    count = 0
    for i in range(0,len(arr)):
        if arr['sequence'][i]=='':
            seqat.append(i)
            count = count + 1
        if arr['class'][i]=='' or arr['class'][i]>6:
            classat.append(i)
            count = count + 1
    if count==0:
        print('No missing value')
    else:
        print('missing count = ',count)

missing_check(dog)

dog['class'].value_counts().sort_index().plot.bar()
#plt.style.use('dark_background')

y=dog.loc[:,'class'].values

"""# **Classifiers**"""

from sklearn.feature_extraction.text import CountVectorizer

documents = [
    "This is the first document.",
    "And My name is Manoj Dey.",
    "And team members are Sayantika Das,Koustubh Manjumdar,Madhushree Ghosh .",
    "Is this our first Prject ?"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()
print("Matrix of token counts:")
print(X.toarray())
print("\nFeature names:")
print(feature_names)

def getKmers(sequence, size=6):
    return [sequence[x:x+size].lower() for x in range(len(sequence) - size + 1)]
cv = CountVectorizer(ngram_range=(4,4))

dog['Words']=dog.apply(lambda X: getKmers(X['sequence']),axis=1)
dog=dog.drop('sequence',axis =1)

dog.head()

dog["in_string"] =dog['Words'].apply(lambda x:  ' '.join(x))

dog[["Words","in_string"]]

print(dog['Words'][0])

dog_texts1 = list(dog['Words'])
for item in range(len(dog_texts1)):
    dog_texts1[item] = ' '.join(dog_texts1[item])

X_d = cv.fit_transform( dog_texts1)
y_d = dog.iloc[:, 0].values

print(X_d.shape,y_d.shape)

i=0
for key,value in cv.vocabulary_.items():
    print(f"{key} : {value}")
    i+=1
    if i>10:break

(dog_texts1[1])

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import xgboost as xgb
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import *

from sklearn.model_selection import train_test_split
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_d,y_d,test_size = 0.25,random_state=42)

dtree_d = DecisionTreeClassifier()
dtree_d.fit(X_train_d,y_train_d)
dtree_d_pred = dtree_d.predict(X_test_d)
print(confusion_matrix(y_test_d, dtree_d_pred))
print(classification_report(y_test_d, dtree_d_pred))

rf_d = RandomForestClassifier(n_estimators=400)
rf_d.fit(X_train_d,y_train_d)
rf_d_pred = rf_d.predict(X_test_d)
print(confusion_matrix(y_test_d, rf_d_pred))
print(classification_report(y_test_d, rf_d_pred))

xgb_d = xgb.XGBClassifier()
xgb_d.fit(X_train_d,y_train_d)
xgb_d_pred = xgb_d.predict(X_test_d)
print(confusion_matrix(y_test_d, xgb_d_pred))
print(classification_report(y_test_d,xgb_d_pred))

NB_d = MultinomialNB(alpha=0.1)
NB_d.fit(X_train_d,y_train_d)
NB_d_pred = NB_d.predict(X_test_d)
print(confusion_matrix(y_test_d, NB_d_pred))
print(classification_report(y_test_d,NB_d_pred))

AdaB_d = AdaBoostClassifier(n_estimators=400)
AdaB_d.fit(X_train_d,y_train_d)
AdaB_d_pred = AdaB_d.predict(X_test_d)
print(confusion_matrix(y_test_d, AdaB_d_pred))
print(classification_report(y_test_d, AdaB_d_pred))

MLP_d = MLPClassifier(alpha=1)
MLP_d.fit(X_train_d,y_train_d)
MLP_d_pred = MLP_d.predict(X_test_d)
print(confusion_matrix(y_test_d, MLP_d_pred))
print(classification_report(y_test_d, MLP_d_pred))

SVC_d = SVC()
SVC_d.fit(X_train_d,y_train_d)
SVC_d_pred = SVC_d.predict(X_test_d)
print(confusion_matrix(y_test_d, SVC_d_pred))
print(classification_report(y_test_d, SVC_d_pred))

plt.figure(figsize=(10,5))
scores=["Naive Bayes","Random Forest","Decision Tree","svm","AdaBoostClassifier","neural_network","xgboost"]
accscore=[68,56,49,49,38,59,64]
f1score=[83,86,76,58,86,71,89]
w=0.2
bar1=np.arange(len(scores))
bar2=[i+w for i in bar1]

plt.bar(bar1,accscore,w,label="accuracy")
plt.bar(bar2,f1score,w,label="f1score")
plt.xticks(bar1, scores)
plt.legend()
plt.title("Comparision Between Models")
#plt.style.use('dark_background')
plt.show()

from sklearn.model_selection import train_test_split
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_d,
                                                    y_d,
                                                    test_size = 0.20,
                                                    random_state=42)
nb_ =MultinomialNB(alpha=0.01)
nb_.fit(X_train_d, y_train_d)

y_pred = nb_.predict(X_test_d)
print(pd.crosstab(pd.Series(y_test_d, name='Actual'), pd.Series(y_pred, name='Predicted')))

import pickle

filename = 'finalized_model.sav'
pickle.dump(nb_, open(filename, 'wb'))

plt.figure(figsize=(7,6))
sns.heatmap(pd.crosstab(pd.Series(y_test_d, name='Actual'), pd.Series(y_pred, name='Predicted')),cmap="YlGnBu",annot=True,fmt='d')
#plt.style.use('dark_background')

"""# **Human VS Dog**"""

Image('/content/drive/MyDrive/humanDNAvsdogDNA.jpg')

"""# **Calculating The Sequence of Dog DNA**"""

Image('/content/drive/MyDrive/dog_dna_calculation.jpg')

