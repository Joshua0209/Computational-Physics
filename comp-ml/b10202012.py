import numpy as np
from libsvm.svmutil import *
np.random.seed(1126)


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


def features(samples):
    features = []
    for evt in samples:
        px = py = pz = E = 0.
        for p in evt:
            px += p[1]
            py += p[2]
            pz += p[3]
            E += (p[1]**2+p[2]**2+p[3]**2)**0.5
        M = (E**2 - (px**2+py**2+pz**2))**0.5
        features.append([len(evt), M, E, px, py, pz])
    return features


def valid_split(X, y, val_size):
    X, y = np.array(X), np.array(y)
    idx = np.random.permutation(len(X))
    x_train = X[idx[val_size:]]
    x_val = X[idx[:val_size]]
    y_train = y[idx[val_size:]]
    y_val = y[idx[:val_size]]
    return x_train, y_train, x_val, y_val


if __name__ == '__main__':
    sample_sig = load_samples('comp-ml\sample_hbb.csv')
    sample_bkg = load_samples('comp-ml\sample_q.csv')
    sample_test = load_samples('comp-ml\sample_test.csv')
    x_data = np.array(features(sample_sig) + features(sample_bkg))
    y_data = np.array([1]*len(sample_sig)+[0]*len(sample_bkg))
    x_test = np.array(features(sample_test))
    x_train, y_train, x_val, y_val = valid_split(x_data, y_data, 30000)
    print("split done.")
    params = f'-s 0 -t 2 -c 100 -g 1 -h 0'
    m = svm_train(y_train, x_train, params)
    svm_save_model('comp.model', m)
    p_label, p_acc, p_val = svm_predict(y_val, x_val, m)
    # p_test = svm_predict(m, x_test)
    # fout = open('my_predicts.csv', 'w')
    # fout.write("id,class\n")
    # for idx, p in enumerate(p_test):
    #     fout.write('%d,%d\n' % (idx, p > 0.5))
    # fout.close()
