import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()
clf = svm.SVC()

X, y = digits.data[:-10], digits.target[:-10]

clf.fit(X, y)

idxOfDigit = -8
prediction = clf.predict(digits.data[[idxOfDigit]])
print("The algorithm thinks this is a: ", prediction)

plt.imshow(digits.images[idxOfDigit], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()