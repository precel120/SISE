import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import mean_squared_error


def parse_data(file_path):
    df = pd.read_csv(file_path)
    return df[['measurement x', 'measurement y', 'reference x', 'reference y']]


data = parse_data('./dataset.csv')
input_columns = ['measurement x', 'measurement y']
target_columns = ['reference x', 'reference y']
x = []
y = []
for it in range(data[input_columns[0]].__len__()):
    x.append([data[input_columns[0]][it], data[input_columns[1]][it]])
    y.append([data[target_columns[0]][it], data[target_columns[1]][it]])

x_train, x_test = x[:-1541], x[-1540:]
y_train, y_test = y[:-1541], y[-1540:]

scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

mlp = MLPRegressor(hidden_layer_sizes=(2, 2, 2), activation='relu', solver='adam', max_iter=400)
mlp.fit(x_train, y_train)

predict_train = mlp.predict(x_train)
print(np.sqrt(mean_squared_error(y_train, predict_train)))
predict_test = mlp.predict(x_test)
print(np.sqrt(mean_squared_error(y_test, predict_test)))
