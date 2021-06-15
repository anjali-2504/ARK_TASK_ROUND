import numpy as np
np.set_printoptions(threshold=3)
np.set_printoptions(suppress=True)
from numpy import genfromtxt
import matplotlib.pyplot as plt
 
def prediction(X_hat_t_1,P_t_1,F_t,B_t,U_t,Q_t):
    X_hat_t=F_t.dot(X_hat_t_1)+(B_t.dot(U_t).reshape(B_t.shape[0],-1) )
    P_t=np.diag(np.diag(F_t.dot(P_t_1).dot(F_t.transpose())))+Q_t
    return X_hat_t,P_t
    
 
def update(X_hat_t,P_t,Z_t,R_t,H_t):
    
    K_prime=P_t.dot(H_t.transpose()).dot( np.linalg.inv ( H_t.dot(P_t).dot(H_t.transpose()) +R_t ))  
 
    #print("K:\n",K_prime)
    
    X_t=X_hat_t+K_prime.dot(Z_t-H_t.dot(X_hat_t))
    P_t=P_t-K_prime.dot(H_t).dot(P_t)
    Y_t=H_t.dot(X_t)   
    return X_t,P_t,Y_t

acceleration=0.5
delta_t=1/40#milisecond
 
measurmens = genfromtxt('Data1.csv', delimiter=',',skip_header=1)
 
#Transition matrix of the process from the state at k to the state at k + 1, and is assumed stationary over time, (nxm);
F_t=np.array([ [1 ,0,delta_t,0] , [0,1,0,delta_t] , [delta_t,0,1,0] , [0,0,0,1] ])
 
#Initial State cov
P_t= np.identity(4)*0.2
 
#Process cov
Q_t= np.identity(4)
 
#Control matrix
B_t=np.array( [ [0] , [0], [0] , [0] ])
 
#Control vector
U_t=acceleration
 
#Measurment Matrix
#H is the noiseless connection between the state vector and the measurement vector, and is assumed stationary over time
H_t = np.array([ [1, 0, 0, 0], [ 0, 1, 0, 0],[0,0,1,0]])
#Measurment cov
R_t= np.identity(3)*5
# Initial State
X_hat_t = np.array( [[0],[0],[0],[0]] )
X_Array=[[],[],[],[],[],[]]
Y_Array=[[],[],[],[],[],[]]
fig, axs = plt.subplots(6)
for j in range(6):
    for i in range(400):
        X_hat_t, P_hat_t = prediction(X_hat_t, P_t, F_t, B_t, U_t, Q_t)
        Z_t = measurmens[i][3*j:3*j+3].transpose()
        Z_t = Z_t.reshape(Z_t.shape[0], -1)
        X_t, P_t,Y_t = update(X_hat_t, P_hat_t, Z_t, R_t, H_t)
        X_Array[j].append(X_t[0])
        Y_Array[j].append(X_t[1])
        X_hat_t = X_t
        P_hat_t = P_t
    axs[j].plot(X_Array[j],Y_Array[j])
 
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Scatter Plot")
plt.show() 