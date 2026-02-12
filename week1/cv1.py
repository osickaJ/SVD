import numpy as np 
import matplotlib.pyplot as plt 

# A = np.array([[1,2,3], [4,5,6]])

# print(f"Original array A =\n {A};" )
# print(f"First element: {A[0,0]}")

# print(f"Size of the matrix A = {A.shape}")
# [m,n] = A.shape
# #A.reshape(n,m)
# print(f"Average of columns: {A.mean(axis = 0)}")
# print(f"Average of rows: {A.mean(axis = 1)}")
# print(f"Sum of rows: {A.sum(axis = 1)}") # min, max, std...


# # choice of the elements by : operator 
# print(f"Second column reversed : {A[::-1, 1]}")

# print(A[(A > 3) & (A < 5)])
# coords = np.argwhere((A > 3) & (A < 5))
# print(coords)  

# # operace s maticemi

# B = np.array([[1,2],[2,3]])
# C = np.array([[1,3],[5,6]])

# print(f"Matrix B: \n{B}")
# print(f"Matrix C: \n{C}")
# print(f"Sum of matrices: \n{B+C}")
# print(f"Product of matrices: \n{B@C}")
# print(f"Elementwise product of matrices:\n {B*C}")

# P = np.arange(0,1,0.02) #linspace in MATLAB
# print(P)
# Q = np.linspace(0,1,51)
# print(Q)
# np.append(Q,2)

# x = np.linspace(-2,2,21)
# y1 = np.exp(x)
# y2 = np.sin(x)
# fig = plt.figure()
# ax1 = fig.add_subplot(1,2,1)
# ax1.plot(x,y1,"go")
# ax2 = fig.add_subplot(1,2,2)
# ax2.plot(x,y2,"rx")
# plt.show()

x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)

# Define function
Z = np.cos(X) * np.sin(Y)

# Plot
fig = plt.figure(figsize=(8,5))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap = 'coolwarm')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("cos(x) * sin(y)")
plt.show()