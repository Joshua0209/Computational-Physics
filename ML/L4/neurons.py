import random
import numpy as np

def sigma(z):
    return 0.5*(np.tanh(0.5*z)+1.)
def sigma_p(z):
    return sigma(z)*(1.-sigma(z))

class neurons(object):
    def __init__(self, shape):
        self.shape = shape
        self.v = [np.zeros((n,1)) for n in shape]
        self.z = [np.zeros((n,1)) for n in shape[1:]]
        self.w = [np.random.randn(n,m) for n,m in zip(shape[1:],shape[:-1])]
        self.b = [np.random.randn(n,1) for n in shape[1:]]
        self.delw = [np.zeros(w.shape) for w in self.w]
        self.delb = [np.zeros(b.shape) for b in self.b]

    def predict(self, x):
        self.v[0] = x.reshape(self.v[0].shape)
        for l in range(len(self.shape)-1):
            self.z[l] = np.dot(self.w[l],self.v[l])+self.b[l]
            self.v[l+1] = sigma(self.z[l])
        return self.v[-1]

    def gradient(self, y):
        for l in range(len(self.shape)-2,-1,-1):
            if l==len(self.shape)-2:
                  delta = (self.v[-1]-y.reshape(self.v[-1].shape))*sigma_p(self.z[l])
            else: delta = np.dot(self.w[l+1].T,self.delb[l+1])*sigma_p(self.z[l])
            self.delb[l] = delta
            self.delw[l] = np.dot(delta,self.v[l].T)

    def fit(self, x_data, y_data, epochs, batch_size, eta):
        samples = list(zip(x_data, y_data))
        for ep in range(epochs):
            print('Epoch: %d/%d' % (ep+1,epochs))
            random.shuffle(samples)
            sum_delw = [np.zeros(w.shape) for w in self.w]
            sum_delb = [np.zeros(b.shape) for b in self.b]
            batch_count = 0
            for x,y in samples:
                self.predict(x)
                self.gradient(y)
                for l in range(len(self.shape)-1):
                    sum_delw[l] += self.delw[l]
                    sum_delb[l] += self.delb[l]
                batch_count += 1
                if batch_count>=batch_size or (x is samples[-1][0]):
                    for l in range(len(self.shape)-1):
                        self.w[l] -= eta/batch_count*sum_delw[l]
                        self.b[l] -= eta/batch_count*sum_delb[l]
                        sum_delw[l],sum_delb[l] = 0.,0.
                    batch_count = 0
            ret = self.evaluate(x_data, y_data)
            print('Loss: %.4f, Acc: %.4f' % ret)

    def evaluate(self, x_data, y_data):
        loss, cnt = 0., 0.
        for x,y in zip(x_data, y_data):
            self.predict(x)
            loss += ((self.v[-1]-y.reshape(self.v[-1].shape))**2).sum()
            if np.argmax(self.v[-1])==np.argmax(y): cnt += 1.
        loss /= 2.*len(x_data)
        return loss, cnt/len(x_data)

