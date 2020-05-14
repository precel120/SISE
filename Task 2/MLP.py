import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as pl
import excel

# Loading data
df = pd.read_csv('./dataset.csv')
data = df[['measurement x', 'measurement y', 'reference x', 'reference y']]
input_columns = ['measurement x', 'measurement y']
target_columns = ['reference x', 'reference y']
x = []
y = []
for it in range(data[input_columns[0]].__len__()):
    x.append([data[input_columns[0]][it], data[input_columns[1]][it]])
    y.append([data[target_columns[0]][it], data[target_columns[1]][it]])

# Splitting data into train and test
x_train, x_test = x[:-1541], x[-1540:]
y_train, y_test = y[:-1541], y[-1540:]

# Add previous time steps
prev_steps = 50
for it in range(x_train.__len__()):
    for j in range(prev_steps):
        x_train[it].append(x_train[it - j][0])
        x_train[it].append(x_train[it - j][1])

for it in range(x_test.__len__()):
    for j in range(prev_steps):
        x_test[it].append(x_test[it - j][0])
        x_test[it].append(x_test[it - j][1])

# Scaling input data
scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# Creating MLP model and training on data
mlp = MLPRegressor(hidden_layer_sizes=(30,), activation='relu', solver='adam', max_iter=500, verbose=True)
mlp.fit(x_train, y_train)

# Predictions and plotting
predict_train = mlp.predict(x_train)
print(type(predict_train))
print(mean_squared_error(y_train, predict_train))
predict_test = mlp.predict(x_test)
print(mean_squared_error(y_test, predict_test))
pl.clf()
pl.plot(predict_train[:, 0], predict_train[:, 1], 'g.', label='Train data')
pl.plot(predict_test[:, 0], predict_test[:, 1], 'b.', label='Test data')
pl.legend()
pl.show()

# Saving results to excel file
excel.add_results_to_main_excel(predict_test)
