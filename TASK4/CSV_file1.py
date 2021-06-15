import numpy as np
np.set_printoptions(threshold=3)
np.set_printoptions(suppress=True)
from numpy import genfromtxt
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def prediction(X_hat_t,V_hat_t,A_hat_t):
    X_pred_t=X_hat_t+V_hat_t*delta_t+A_hat_t*delta_t**2/2
    V_pred_t=V_hat_t+A_hat_t*delta_t
    A_pred_t=A_hat_t
   # P_pred_t=P_hat_t
    return X_pred_t,V_pred_t,A_pred_t
    

def update(X_pred_t,V_pred_t,A_pred_t,Z_mes):
  
    X_estimate_t=(X_pred_t)+ (alpha*(Z_mes-X_pred_t))
    V_estimate_t=X_pred_t+beta*(Z_mes-X_pred_t)/(delta_t**2)
    A_estimate_T=A_pred_t+0.5*gamma*(Z_mes-X_pred_t)/(delta_t**2)
    
    return X_estimate_t,V_estimate_t,A_estimate_T
alpha=0.5
beta=0.4
gamma=0.1

delta_t=1#milisecond

measurmens = genfromtxt('Data1.csv', delimiter=',',skip_header=1)


X_hat_t = np.array([[0],[-1],[-1]])
V_hat_t=np.array([[0.5],[0.5],[0.5]])
A_hat_t=np.array([[0.01],[0.01],[-9.8]])

X_Array=[[]]
Y_Array=[[]]
Z_Array=[[]]
x_Array=[[]]
y_Array=[[]]
z_Array=[[]]

fig = plt.figure(2)
axs = plt.axes(projection ='3d')

for j in range(1):
    for i in range(100):
        X_pred_t, V_pred_t,A_pred_t = prediction(X_hat_t,V_hat_t,A_hat_t)

        Z_t = measurmens[i][3*j:3*j+3].transpose()
        Z_t = Z_t.reshape(Z_t.shape[0], -1)
        X_estimate_t,V_estimate_t,A_estimate_T = update(X_pred_t,V_pred_t,A_pred_t,Z_t)
        X_Array[j].append(X_estimate_t[0][0])
        Y_Array[j].append(X_estimate_t[1][0])
        Z_Array[j].append(X_estimate_t[2][0])
        print(Z_t)
        x_Array[j].append(Z_t[0][0])
        y_Array[j].append(Z_t[1][0])
        z_Array[j].append(Z_t[2][0])
        X_hat_t=X_estimate_t
        V_hat_t=V_estimate_t
        A_hat_t=A_estimate_T

    axs.plot3D(X_Array[j], Y_Array[j],Z_Array[j], 'green')
    axs.plot3D(x_Array[j], y_Array[j],z_Array[j], 'blue')
axs.set_title('3D line plot geeks for geeks')
plt.show() 
