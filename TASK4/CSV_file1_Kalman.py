import numpy as np
np.set_printoptions(threshold=3)
np.set_printoptions(suppress=True)
from numpy import genfromtxt
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def prediction(X_hat_t_1,P_t_1,F_t,B_t,U_t_1,Q_t):
    X_hat_t=F_t.dot(X_hat_t_1)+(B_t.dot(U_t_1).reshape(B_t.shape[0],-1) )
    P_t=np.diag(np.diag(F_t.dot(P_t_1).dot(F_t.transpose())))+Q_t
    return X_hat_t,P_t
    

def update(X_hat_t,P_t,Z_t,R_t,H_t):
    
    #6x3
    K_prime=P_t.dot(H_t.transpose()).dot( np.linalg.inv (H_t.dot(P_t).dot(H_t.transpose()) +R_t)) 


    X_t=X_hat_t+K_prime.dot(Z_t-H_t.dot(X_hat_t))
    P_t=(P_t-K_prime.dot(H_t).dot(P_t)).dot((np.identity(6)-K_prime.dot(H_t)).transpose()) + K_prime.dot(R_t.dot(K_prime.transpose()))   
    return X_t,P_t


delta_t=1

measurmens = genfromtxt('Data1.csv', delimiter=',',skip_header=1)
#6x6
F_t=np.array([[1 ,0,0,0,0,0] , [0,1,0,0,0,0] , [0,0,1,0,0,0] , [delta_t,0,0,1,0,0],[0,delta_t,0,0,1,0],[0,0,delta_t,0,0,1] ])

#6x6
P_t= np.identity(6)*20.0

#6x6
Q_t= np.identity(6)

#6x3
B_t=np.array([[0.5*(delta_t)*delta_t,0.0,0.0 ],[0.0,0.5*(delta_t**2),0.0],[0.0,0.0,0.5*(delta_t**2)],[delta_t,0,0],[0,delta_t,0],[0,0,delta_t]])

#3x1
U_t=np.array([[0],[0.02],[0.01]])

#3x6
H_t = np.array([[1, 0, 0, 0,0,0], [0,1, 0, 0,0,0],[0,0,1,0,0,0]])

#3x3
R_t= np.identity(3)*1

#6x1
X_hat_t_1= np.array( [[0],[-1],[-1],[0],[0],[0]] )

X_Array=[[]]

Y_Array=[[]]

Z_Array=[[]]

fig = plt.figure()
axs = plt.axes(projection ='3d')

for j in range(1):
    for i in range(50):
    
        X_hat_t, P_hat_t = prediction(X_hat_t_1, P_t, F_t, B_t, U_t, Q_t)
        Z_t = measurmens[i][3*j:3*j+3].transpose()
        Z_t = Z_t.reshape(Z_t.shape[0], -1)
        X_t, P_t = update(X_hat_t, P_hat_t, Z_t, R_t, H_t)
        print(U_t)
        ''' print(X_t)
        print()
        print(Z_t)
        print()
        print("---------------------------")'''
        X_Array[j].append(1*X_t[0][0])
        Y_Array[j].append(1*X_t[1][0])
        Z_Array[j].append(1*X_t[2][0])
        i+=1
        x1=measurmens[i-1][3*j:3*j+3]
        x2=measurmens[i][3*j:3*j+3]
        x3=measurmens[i+1][3*j:3*j+3]
        x120=x2[0]-x1[0]
        x230=x3[0]-x2[0]
        xa0=(x230-x120)/delta_t**2
        x121=x2[1]-x1[1]
        x231=x3[1]-x2[1]
        xa1=(x231-x121)/delta_t**2
        x122=x2[2]-x1[2]
        x232=x3[2]-x2[2]
        xa2=(x232-x122)/delta_t**2
       # print(xa0,xa1,xa2)
        U_t=np.array([[xa0],[xa1],[xa2]])
        

        X_hat_t = X_t
        P_hat_t = P_t

    axs.plot3D(X_Array[j], Y_Array[j],Z_Array[j], 'green')


axs.set_title('3D line plot')
plt.show() 
