import pandas
import numpy
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plot

def remove_outlier(df_in: pandas.DataFrame, col_name: str):
    q1 = df_in[col_name].quantile(0.25)
    q3 = df_in[col_name].quantile(0.75)
    iqr = q3-q1 #Interquartile range
    fence_low  = q1-1.5*iqr
    fence_high = q3+1.5*iqr
    df_out = df_in.loc[(df_in[col_name] > fence_low) & (df_in[col_name] < fence_high)]
    return df_out

sp_data = pandas.read_csv('data/sp500-eps-3year.csv', delimiter=';', header=[0])
sp_data.dropna()


filter1 = remove_outlier(sp_data, 'eps')
filter2 = remove_outlier(filter1, 'year_return')
x = filter2['eps'].values.reshape(-1, 1)
y = filter2['year_return'].values

reg = LinearRegression()
reg.fit(x, y)

# The coefficients
print('Coefficients: \n', reg.coef_)

# The mean squared error
#print('Mean squared error: {}'.format(mean_squared_error(y_test, y_pred)))

# The coefficient of determination: 1 is perfect prediction
#print('Coefficient of determination: '.format(r2_score(y_test, y_pred))

# Plot outputs
plot.xlabel('3 Year EPS')
plot.ylabel('3 Year Returns')
plot.scatter(x, y,  color='black')
plot.plot(x, reg.predict(x), color='blue', linewidth=2)
plot.show()