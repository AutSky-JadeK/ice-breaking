import codecs
import numpy as np
from sklearn.model_selection import train_test_split

x = np.arange(1000)
print(x)
x_train, x_test = train_test_split(x, test_size=0.4, random_state=43)
x_test, x_valid = train_test_split(x_test, test_size=0.5, random_state=43)
print(x_train.shape)
print(x_test.shape)
print(x_valid.shape)
x_train = x_train.tolist()
x_test = x_test.tolist()
x_valid = x_valid.tolist()
print(x_train)
print(x_valid)
print(x_test)
train = codecs.open('train.txt', 'w', 'utf-8')
test = codecs.open('test.txt', 'w', 'utf-8')
valid = codecs.open('val.txt', 'w', 'utf-8')

with open('shuffled_all.txt', 'r', encoding='utf8') as f:
	i = 0
	for line in f.readlines():
		if i in x_train:
			train.write(line)
		if i in x_test:
			test.write(line)
		if i in x_valid:
			valid.write(line)
		i = i + 1
train.close()
test.close()
valid.close()