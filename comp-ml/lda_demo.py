import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


def load_samples(filename):
    print('load from', filename)
    fin = open(filename)
    lines = fin.readlines()
    idx_cur, samples, evt = -1, [], []
    for l in lines[1:]:
        idx, code, px, py, pz = l.split(',')
        if idx_cur != int(idx):
            idx_cur = int(idx)
            if len(evt) > 0:
                samples.append(evt)
                evt = []
        else:
            evt.append([int(code), float(px), float(py), float(pz)])
    samples.append(evt)
    print(len(samples), 'events loaded.')
    return samples


def prepare_features(samples):
    features = []
    for evt in samples:
        px = py = pz = E = 0.
        for p in evt:
            px += p[1]
            py += p[2]
            pz += p[3]
            E += (p[1]**2+p[2]**2+p[3]**2)**0.5
        M = (E**2 - (px**2+py**2+pz**2))**0.5
        features.append([len(evt), abs(M-125)])
    return features


sample_sig = load_samples('comp-ml\sample_hbb.csv')
sample_bkg = load_samples('comp-ml\sample_q.csv')
sample_test = load_samples('comp-ml\sample_test.csv')
x_train = np.array(prepare_features(sample_sig)+prepare_features(sample_bkg))
y_train = np.array([1]*len(sample_sig)+[0]*len(sample_bkg))
x_test = np.array(prepare_features(sample_test))

clf = LinearDiscriminantAnalysis()
f_train = clf.fit_transform(x_train, y_train)

p_test = clf.predict(x_test)
fout = open('my_predicts.csv', 'w')
fout.write("id,class\n")
for idx, p in enumerate(p_test):
    fout.write('%d,%d\n' % (idx, p > 0.5))
fout.close()

s_train = clf.score(x_train, y_train)
print('Performance (training):', s_train)

fig = plt.figure(figsize=(6, 9), dpi=80)
plt.subplot(3, 1, 1)
plt.hist(x_train[y_train == 0][:, 0], bins=50, color='y')
plt.hist(x_train[y_train == 1][:, 0], bins=50, color='g', alpha=0.5)
plt.subplot(3, 1, 2)
plt.hist(x_train[y_train == 0][:, 1], bins=50, color='y')
plt.hist(x_train[y_train == 1][:, 1], bins=50, color='g', alpha=0.5)
plt.subplot(3, 1, 3)
plt.hist(f_train[y_train == 0], bins=50, color='y')
plt.hist(f_train[y_train == 1], bins=50, color='g', alpha=0.5)
plt.show()
