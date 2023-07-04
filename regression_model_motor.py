import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import matplotlib.pyplot as plt
import numpy as np

# Define the data points
data = {
    'Torque': [0.769537, 0.770006, 0.770148, 0.949985, 0.771563, 0.772835, 0.770847, 0.950502, 0.770764, 0.77116, 0.770259, 0.949734,0.767955,0.77092,0.77046,0.769617,0.770509,0.769985,0.949361,0.950258],
    'Speed': [4210.1, 4194.8, 5047.5, 4141.9, 4320, 4286.4, 5156.6, 4316.1, 4080.6, 4049.1, 4842.7, 3879.2, 3996.3, 4611.4, 4977.1, 4562, 4956.8, 5360.9, 4047.8, 4484.7],
    'Current': [2.38374, 12.39036, 2.42299, 2.91722, 2.35988, 2.33975, 2.34885, 2.8392, 2.41287, 2.41354, 2.40574, 2.91614, 2.41528, 2.50907, 2.42891 , 2.4979, 2.4271, 2.56641, 2.93291, 3.07592],
    'Voltage_meas': [2.99624, 2.99096, 3.30325, 3.28604, 2.9967, 2.99041, 3.30226, 3.28633, 2.99638, 2.98974, 3.30155, 3.28645, 2.99676, 2.99697, 2.98947, 2.98877, 3.30142, 3.30134, 3.28599, 3.28612],
    'Vacuum': [238, 238, 238, 238, 243, 243, 243, 243, 244, 244, 244, 244,243,247,243,247,243,247,243,247]
}

# Create a DataFrame from the data
test_data = [ 18, 17, 16, 15,13,12]
test_data_t = [19, 18, 17, 16, 15,14,13,12]
df = pd.DataFrame(data).drop(test_data_t)

#remove 

# Extract the independent variables (Torque, Speed, Current, Voltage_meas) and the target variable (Vacuum)
X = df[['Torque', 'Speed', 'Current', 'Voltage_meas']]
y = df['Vacuum']

# Apply polynomial feature transformation
poly_features = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly_features.fit_transform(X)

# Initialize and fit the polynomial regression model
model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(X_poly, y)

# # Predict vacuum for new input data
# new_data = {
#     'Torque': [0.767955,0.77092,0.77046,0.769617,0.770509,0.769985,0.949361,0.950258],
#     'Speed': [3996.3, 4611.4, 4977.1, 4562, 4956.8, 5360.9, 4047.8, 4484.7],
#     'Current': [2.41528, 2.50907, 2.42891 , 2.4979, 2.4271, 2.56641, 2.93291, 3.07592],
#     'Voltage_meas': [2.99676, 2.99697, 2.98947, 2.98877, 3.30142, 3.30134, 3.28599, 3.28612],
#     'Vacuum': [243,247,243,247,243,247,243,247]
# }

new_data =  pd.DataFrame(data).iloc[test_data]

new_X = pd.DataFrame(new_data)[['Torque', 'Speed', 'Current', 'Voltage_meas']]
new_X_poly = poly_features.transform(new_X)
predicted_vacuum = model.predict(new_X_poly)
print("Predicted Vacuum:", predicted_vacuum)

y=np.array(pd.DataFrame(new_data)[['Vacuum']])
# Plot the comparison between estimated and real vacuum
plt.figure(figsize=(8, 6))
plt.scatter(np.arange(len(y)), y, label='Real Vacuum', color='blue')
plt.scatter(np.arange(len(y)), predicted_vacuum, label='Estimated Vacuum', color='red')
plt.xlabel('Data Points')
plt.ylabel('Vacuum [mmHg]')
plt.title('Comparison between Estimated and Real Vacuum')
plt.legend()
plt.show()

# # Plot the error between y and predicted_vacuum
# error = y - np.array(predicted_vacuum)
# plt.figure(figsize=(8, 6))
# x=np.arange(len(error)+1)
# plt.scatter(x, error, label='Error', color='green')
# plt.xlabel('Data Points')
# plt.ylabel('Error')
# plt.title('Error between Real and Estimated Vacuum')
# plt.legend()
# plt.show()


