import sys
import pandas as pd
import numpy as np
import itertools
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, f1_score
from tpot_metrics import balanced_accuracy_score
from sklearn.pipeline import make_pipeline

dataset = sys.argv[1]

# Read the data set into memory
input_data = pd.read_csv(dataset, compression='gzip', sep='\t').sample(frac=1., replace=False, random_state=42)

for (min_weight_fraction_leaf, max_features, criterion) in itertools.product(np.arange(0., 0.51, 0.05),
                                                                             [0.1, 0.25, 0.5, 0.75, 'sqrt', 'log2', None],
                                                                             ['gini', 'entropy']):
    features = input_data.drop('class', axis=1).values.astype(float)
    labels = input_data['class'].values

    try:
        # Create the pipeline for the model
        clf = make_pipeline(StandardScaler(),
                            DecisionTreeClassifier(min_weight_fraction_leaf=min_weight_fraction_leaf,
                                                   max_features=max_features,
                                                   criterion=criterion,
                                                   random_state=324089))
        # 10-fold CV score for the pipeline
        cv_predictions = cross_val_predict(estimator=clf, X=features, y=labels, cv=10)
        accuracy = accuracy_score(labels, cv_predictions)
        macro_f1 = f1_score(labels, cv_predictions, average='macro')
        balanced_accuracy = balanced_accuracy_score(labels, cv_predictions)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        continue

    param_string = ''
    param_string += 'min_weight_fraction_leaf={},'.format(min_weight_fraction_leaf)
    param_string += 'max_features={},'.format(max_features)
    param_string += 'criterion={}'.format(criterion)

    out_text = '\t'.join([dataset.split('/')[-1][:-7],
                          'DecisionTreeClassifier',
                          param_string,
                          str(accuracy),
                          str(macro_f1),
                          str(balanced_accuracy)])

    print(out_text)
    sys.stdout.flush()
