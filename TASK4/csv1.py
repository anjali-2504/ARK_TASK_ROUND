import numpy as np
np.set_printoptions(threshold=3)
np.set_printoptions(suppress=True)
from numpy import genfromtxt
import matplotlib.pyplot as plt
import math
from mpl_toolkits import mplot3d

def prediction(X_hat_t_1,P_t_1,F_t,B_t,U_t,Q_t):
    X_hat_t=F_t.dot(X_hat_t_1)+(B_t.dot(U_t).reshape(B_t.shape[0],-1) )
    P_t=np.diag(np.diag(F_t.dot(P_t_1).dot(F_t.transpose())))+Q_t
    return X_hat_t,P_t
    

def update(X_hat_t,P_t,Z_t,R_t,H_t):
    
    K_prime=P_t.dot(H_t.transpose()).dot( np.linalg.inv ( H_t.dot(P_t).dot(H_t.transpose()) +R_t ))  


    
    X_t=X_hat_t+K_prime.dot(Z_t-H_t.dot(X_hat_t))
    P_t=P_t-K_prime.dot(H_t).dot(P_t)
    Y_t=H_t.dot(X_t)

    
    return X_t,P_t,Y_t


acceleration=0
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
Z_Array=[[],[],[],[],[],[]]
x_Array=[[],[],[],[],[],[]]
y_Array=[[],[],[],[],[],[]]
xg=[]
yg=[]

fig = plt.figure()
axs = plt.axes(projection ='3d')
#fig, ax = plt.subplots(6)
for j in range(1):
    for i in range(100):
        r=(measurmens[i][0]**2+measurmens[i][1]**2+measurmens[i][2]**2)**(0.5)
       # print(r)
        alpha=math.acos(measurmens[i][0]/r)
        beta=math.acos(measurmens[i][1]/r)
        x=measurmens[i][0]
        y=measurmens[i][1]
        z=measurmens[i][2]


        Mat_Y_Measure=np.array([r,alpha,beta])
        a1=-(y**2+z**2)**0.5/r**2  
        a2= x*y/((r**2)*((y**2+z**2)**0.5))
        a3= x*z/((r**2)*((y**2+z**2)**0.5))
        b1=  x*y/((r**2)*((x**2+z**2)**0.5))
        b2=   -(x**2+z**2)**0.5/r**2  
        b3= y*z/((r**2)*((x**2+z**2)**0.5))
        H_mat=np.array([[x,y,z,0,0],[a1, a2  , a3 , 0 , -1],[b1 , b2 , b3 ,  -1 ,  0  ]]).reshape(3,5)
        
        noise=np.array([0.07,0.004,0.004])
      #  print(H_mat)
     #   print(Mat_Y_Measure-noise)


        X_state_t=np.linalg.lstsq(H_mat, Mat_Y_Measure -noise , rcond=None)[0]

      #  X_state_t= (np.linalg.inv(H_mat)).dot((Mat_Y_Measure -noise ))




      #  X_hat_t, P_hat_t = prediction(X_hat_t, P_t, F_t, B_t, U_t, Q_t)
       # print("Prediction:")
      #  print("X_hat_t:\n", X_hat_t, "\nP_t:\n", P_t)


        Z_t = measurmens[i][3*j:3*j+3].transpose()
        Z_t = Z_t.reshape(Z_t.shape[0], -1)

   # print(Z_t.shape)

      #  X_t, P_t,Y_t = update(X_hat_t, P_hat_t, Z_t, R_t, H_t)
       # print("Update:")
       # print("X_t:\n", X_t, "\nP_t:\n", P_t)
       # X_Array[j].append(Y_t[0])
      #  Y_Array[j].append(Y_t[1])
        print(X_state_t)
        X_Array[j].append(X_state_t[0])
        Y_Array[j].append(X_state_t[1])
        Z_Array[j].append(X_state_t[2])

      #  X_hat_t = X_t
     #   P_hat_t = P_t

       # print("=========================================")
   # print("Opencv Kalman Output:")
   # print("X_t:\n",opencvKalmanOutput[i])
    print(type(X_state_t))

    axs.plot3D(X_Array[j], Y_Array[j],Z_Array[j], 'green')
axs.set_title('3D line plot')
plt.show()
  #  ax[j].plot(x_Array[j],y_Array[j])

plt.xlabel("X")
plt.ylabel("Y")
  
