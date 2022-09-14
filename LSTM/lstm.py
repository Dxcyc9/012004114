from pickletools import optimize
import numpy
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import  pandas as pd
import  os
from keras.models import Sequential, load_model
from sklearn.preprocessing import MinMaxScaler
from keras import optimizers

def create_dataset(dataset, look_back):
#这里的look_back与timestep相同
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back)]
        dataX.append(a)
        dataY.append(dataset[i + look_back])
    return numpy.array(dataX),numpy.array(dataY)

dataframe1 = pd.read_excel('data.xlsx', usecols=[2])
dataframe2 = pd.read_excel('data.xlsx', usecols=[1])


dataset1 = dataframe1.values
dataset2 = dataframe2.values

# 将整型变为float
dataset1 = dataset1.astype('float32')
dataset2 = dataset2.astype('float32')
#归一化 
scaler = MinMaxScaler(feature_range=(0, 1))
dataset1 = scaler.fit_transform(dataset1)
dataset2 = scaler.fit_transform(dataset2)

# train_size = int(len(dataset) * 0.65)
trainlist = dataset1
testlist = dataset2



#训练数据太少 look_back并不能过大
look_back = 2
trainX,trainY  = create_dataset(trainlist,look_back)

testX,testY = create_dataset(testlist,look_back)

trainX = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = numpy.reshape(testX, (testX.shape[0], testX.shape[1] ,1 ))

# # create and fit the LSTM network
# model = Sequential()
# model.add(LSTM(4, input_shape=(None,1)))
# model.add(Dense(1))
# adam = optimizers.Adam(learning_rate=0.01, beta_1=0.9, beta_2=0.999, amsgrad=False)
# model.compile(loss='mean_squared_error', optimizer=adam)


# model.fit(trainX, trainY, epochs=30, batch_size=3, verbose=2)
# model.save(os.path.join("DATA","Test" + ".h5"))

# make predictions
model = load_model(os.path.join("DATA","Test" + ".h5"))
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

#反归一化
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)


testY = testY.astype(int)
testPredict = testPredict.astype(int)
testY = testY.reshape(-1)

print("选出偏差百分比大于20%的数据")
print("日期下标\t真实值\t预测值\t偏差百分比")

df1 = pd.DataFrame({'predict': testY})
df1.to_excel('predict.xlsx', sheet_name='Sheet1', index=False) # index false为不写入索引
for i in range(len(testY)-1):
    delta = (testY[i] - testPredict[i+1])/testY[i] * 100
    delta = abs(delta)
    if delta > 10:
        print(i,testY[i],testPredict[i+1],delta)

# plt.plot(trainY)
# plt.plot(trainPredict[1:])
# plt.show()
# plt.plot(testY)
# plt.plot(testPredict[1:])
# plt.show()
