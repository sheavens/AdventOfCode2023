"""Find the start position x,y,z and the velocity vx,vy,vz of a particle that
will collide with all other particles in the input data."""
# find the time at which particles intersect, and the distance aparat at that time.
# minimimise the differences usinf gradient descent.
import numpy as np
from scipy.optimize import minimize, dual_annealing
import matplotlib.pyplot as plt

testData = [
'19, 13, 30 @ -2,  1, -2',
'18, 19, 22 @ -1, -1, -2',
'20, 25, 34 @ -2, -2, -4',
'12, 31, 28 @ -1, -2, -1',
'20, 19, 15 @  1, -5, -3',
]

data = testData
testArea =[(7,7),(27,27)]

# read the data from input file day24_input.txt
with open('day24_input.txt') as f:
    data = f.read().splitlines()

lineList = []
for line in range(len(data)):
    p, v = data[line].split('@')
    x,y,z = p.split(',')
    vx, vy, vz = v.split(',')
    # Using point on line and vector representation
    lineList.append([np.array([int(x),int(y),int(z)]), np.array([int(vx),int(vy),int(vz)])]) 

def line_intersection(line1, line2):
    # Line 1: P1 + t * v1
    P1, v1 = line1
    P2, v2 = line2
    
    # Check if lines are parallel
    cross_product = np.cross(v1, v2)
    if np.allclose(cross_product, [0, 0, 0]):  # Lines are parallel
        return np.array([float('inf'), float('inf'), float('inf')]) 
    
    # Calculate parameters t1 and t2 for the intersection point
    A = np.vstack((v1, -v2)).T
    b = P2 - P1
    t1, t2 = np.linalg.lstsq(A, b, rcond=None)[0]
    
    # Calculate intersection point
    intersection_point = P1 + t1 * v1
    
    return intersection_point

# Example lines represented as (point_on_line, direction_vector)
""" line1 = (np.array([1, 2, 3]), np.array([2, 3, 4]))
line2 = (np.array([5, 6, 7]), np.array([1, 0, -1]))

intersection_point = line_intersection(line1, line2)

if intersection_point is not None:
    print("Intersection point:", intersection_point)
else:
    print("The lines are parallel and do not intersect.") """


def intersection(p1, p2, p3, p4):
    # return the intersection point of two lines
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    a1 = y2 - y1
    b1 = x1 - x2
    c1 = a1 * x1 + b1 * y1
    
    a2 = y4 - y3
    b2 = x3 - x4
    c2 = a2 * x3 + b2 * y3
    
    determinant = a1 * b2 - a2 * b1
    
    if determinant == 0:
        return None
    else:
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        return (x, y)

# Function to calculate the position of the projectile at a given time
def projectile_position(t, v_x, v_y, v_z, x_0, y_0, z_0):
    x = v_x * t + x_0
    y = v_y * t + y_0
    z = v_z * t + z_0 # no gravity -0.5 * 9.81 * t**2 +
    return x, y, z

# Function to calculate the distance between two points in 3D space
def distance(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# binary tree function to find the minimum distance apart of the projectile with another projectile.
# ... but quicker to calculate intersection point .. then the difference in times to that point? - not min dist tho'
def binary_search(projectile, other_projectile, tolerance=0.01):
    # projectile in form ([x, y, z], [vx, vy, vz])
    pt = projectile[0]
    vt = projectile[1]
    x, y, z = pt
    vx, vy, vz = vt
    pt2 = other_projectile[0]
    vt2 = other_projectile[1]
    x2, y2, z2 = pt2
    vx2, vy2, vz2 = vt2

    t = 0
    dt = 1
    while dt > tolerance:  # take it to half a nano second (and could meybe start with much larger dt and narrow it down)
        min_dist = float('inf')

        x_p, y_p, z_p = projectile_position(t, vx, vy, vz, x, y, z)
        xo_p, yo_p, zo_p = projectile_position(t, vx2, vy2, vz2, x2, y2, z2)
        dist = distance(x_p, y_p, z_p, xo_p, yo_p, zo_p)
        min_dist = min(min_dist, dist)

        min_dist_plus_dt = float('inf')
        x_p, y_p, z_p = projectile_position(t + dt, vx, vy, vz, x, y, z)
        xo_p, yo_p, zo_p = projectile_position(t + dt, vx2, vy2, vz2, x2, y2, z2)
        dist = distance(x_p, y_p, z_p, xo_p, yo_p, zo_p)
        min_dist_plus_dt = min(min_dist_plus_dt, dist)
        if min_dist_plus_dt < min_dist:
            t += dt
        else:
            dt /= 2
    return t, min_dist


# Loss function
def loss_function_example(v_x, v_y, v_z, x_0, y_0, z_0, other_projectiles):
    total_loss = 0
    for projectile in other_projectiles:
        x_p, y_p, z_p = projectile_position(projectile['time'], v_x, v_y, v_z, x_0, y_0, z_0)
        dist = distance(x_p, y_p, z_p, projectile['x'], projectile['y'], projectile['z'])
        total_loss += dist
    return total_loss

# Loss function
def loss_function(projectile_params, other_projectiles):
    projectile = [projectile_params[:3], projectile_params[3:]] # pack as 3 position ans 3 velocity valuesa
    total_loss = 0 # loss is the sum of the minimum distances between the projectile and the other projectiles
    for other in other_projectiles:
        t, min_dist = binary_search(projectile, other)
        total_loss += min_dist
    return total_loss

def intersections(Vs, projectiles):
    # projectiles is a list of lines at Pt, Vt
    # subtract the velocity of the snowball from the velocity other projectiles
    for i in range(len(projectiles)):
        Pt, Vtp = projectiles[i]
        projectiles[i] = Pt, Vtp-Vs
    # find the intersection points of the projectiles
    intersections = []
    for i in range(len(projectiles)):
        c = projectiles[i]
        for j in range(len(projectiles)):
            d = projectiles[j]
            if i == j : continue
            intersection = line_intersection(c, d)
            if intersection.any() == float('inf') : 
                print("No intersection")
                return float('inf')       
            else :
                intersections.append(intersection)
    return intersections

# Gradient descent function
def gradient_descent2(initial_velocity, projectiles, learning_rate, iterations):
    vt = initial_velocity.copy() # Vt: vx,vy,vz
    for i in range(iterations):
        grad = np.zeros(len(vt)) # gradient of the loss function with respect to each parameter (v_x, v_y, v_z, x_0, y_0, z_0
        
        for j in range(len(vt)): # loop throup the Vt compnqnts 
            vt_plus = vt.copy()
            vt_plus[j] -= 1 # 1e-5 # increase the velocity component by an integer amount (in this case)

            # adjust the velocity of the other projectiles to the relative velocity at the new values
            loss_plus_eps = loss_function2(vt_plus, projectiles)
            loss_current = loss_function2(vt, projectiles)

            grad[j] = (loss_plus_eps - loss_current) / 0.1 # 1e-5
        vt -= learning_rate * grad
        print("Iteration:", i, "Loss:", loss_current, vt)
    return vt

""" # adjust the velocity
np.array([1,1,1])

dvx = 0
dvy = 0
dvz = 0
for i in range(1000) :

    dvx = dvx -10 + 1
    dvy = dvy -10 + 1
    dvz = dvz -10 + 1

    ptSet = set()
    for p in lineList:
        Pt, Vtp = p
        p = Pt, Vtp - np.array([dvx,dvy,dvz])
        for t in range(20):
            Pt + Pt + Vtp -np.array([dvx,dvy,dvz])*t
            Pt = Pt + Vtp
            if Pt[0] in ptSet: # only looking at x for now
                print(Pt, t, p)
            ptSet.add(Pt[0]) """

    

def gradFunc(snowballVelocity, lineList):
    Vs = snowballVelocity
    # deduct the snowball velocity from the other projectiles
    for i in range(len(lineList)):
        Pt, Vtp = lineList[i]
        lineList[i] = Pt, Vtp - Vs

    # get a set of intersection points of the projectiles with each other
    intersection_points = []
    for line in lineList:
        a,b = line
        for line2 in lineList:
            c,d= line2
            if (a == c).all() and (b == d).all() : continue
            intersection = line_intersection(line, line2)
            if intersection is not None:
                intersection_points.append(intersection)

    # fit the intersection points to a straight line
    # calculate the standard deviation of the intersection points from the line
    # return the derivative of the standard deviation with respect to the snowball velocity
    # the gradient descent function will find the snowball velocity that minimizes the standard deviation
    # of the intersection points from the line

    # Calculate the slope and intercept of the line
    x = np.array([point[0] for point in intersection_points])
    y = np.array([point[1] for point in intersection_points])
    z = np.array([point[2] for point in intersection_points])
    A = np.vstack([x, y, z, np.ones(len(x))]).T
    m, c, p, q = np.linalg.lstsq(A, np.ones(len(x)), rcond=None)[0]

    # Calculate the standard deviation of the intersection points from the line
    std_dev = np.sqrt(np.mean((m*x + c*y + p*z + q - 1)**2))

    # Calculate the derivative of the standard deviation with respect to the snowball velocity
    d_std_dev_d_vx = np.mean(2*m*x + c*y + p*z + q)
    d_std_dev_d_vy = np.mean(m*x + 2*c*y + p*z + q)
    d_std_dev_d_vz = np.mean(m*x + c*y + 2*p*z + q)

    # return np.array([d_std_dev_d_vx, d_std_dev_d_vy, d_std_dev_d_vz]) 
    return  std_dev  


# Gradient descent function
def gradient_descent(vs, lineList , learning_rate, iterations):
    params = vs.copy()
    for i in range(iterations):
        grad = np.zeros(len(params)) # gradient of the loss function with respect to each parameter (v_x, v_y, v_z, x_0, y_0, z_0
        for j in range(len(params)): # loop throup the parameters 
            params_plus_eps = params.copy()
            params_plus_eps[j] += 1 # 1e-5 # increase the parameter by an integer amount (in this case)
            grad[j] = gradFunc(params, lineList) / 1e-2 # 1e-5
        params -= learning_rate * grad
    return params

# Example data for other projectiles
other_projectiles = [{'time': 3, 'x': 10, 'y': 5, 'z': 20}, {'time': 4, 'x': 15, 'y': 3, 'z': 18}]

# gradient_descent([10,10,10], lineList, 0.1, 1000)

def sgd(
    gradient, x, y, n_vars=None, start=None, learn_rate=0.1,
    decay_rate=0.0, batch_size=1, n_iter=50, tolerance=1e-06,
    dtype="float64", random_state=None
):
    # Checking if the gradient is callable
    if not callable(gradient):
        raise TypeError("'gradient' must be callable")

    # Setting up the data type for NumPy arrays
    dtype_ = np.dtype(dtype)

    # Converting x and y to NumPy arrays
    x, y = np.array(x, dtype=dtype_), np.array(y, dtype=dtype_)
    n_obs = x.shape[0]
    if n_obs != y.shape[0]:
        raise ValueError("'x' and 'y' lengths do not match")
    xy = np.c_[x.reshape(n_obs, -1), y.reshape(n_obs, 1)]

    # Initializing the random number generator
    seed = None if random_state is None else int(random_state)
    rng = np.random.default_rng(seed=seed)

    # Initializing the values of the variables
    vector = (
        rng.normal(size=int(n_vars)).astype(dtype_)
        if start is None else
        np.array(start, dtype=dtype_)
    )

    # Setting up and checking the learning rate
    learn_rate = np.array(learn_rate, dtype=dtype_)
    if np.any(learn_rate <= 0):
        raise ValueError("'learn_rate' must be greater than zero")

    # Setting up and checking the decay rate
    decay_rate = np.array(decay_rate, dtype=dtype_)
    if np.any(decay_rate < 0) or np.any(decay_rate > 1):
        raise ValueError("'decay_rate' must be between zero and one")

    # Setting up and checking the size of minibatches
    batch_size = int(batch_size)
    if not 0 < batch_size <= n_obs:
        raise ValueError(
            "'batch_size' must be greater than zero and less than "
            "or equal to the number of observations"
        )

    # Setting up and checking the maximal number of iterations
    n_iter = int(n_iter)
    if n_iter <= 0:
        raise ValueError("'n_iter' must be greater than zero")

    # Setting up and checking the tolerance
    tolerance = np.array(tolerance, dtype=dtype_)
    if np.any(tolerance <= 0):
        raise ValueError("'tolerance' must be greater than zero")

    # Setting the difference to zero for the first iteration
    diff = 0

    # Performing the gradient descent loop
    for _ in range(n_iter):
        # Shuffle x and y
        rng.shuffle(xy)

        # Performing minibatch moves
        for start in range(0, n_obs, batch_size):
            stop = start + batch_size
            x_batch, y_batch = xy[start:stop, :-1], xy[start:stop, -1:]

            # Recalculating the difference
            grad = np.array(gradient(x_batch, y_batch, vector), dtype_)
            diff = decay_rate * diff - learn_rate * grad

            # Checking if the absolute difference is small enough
            if np.all(np.abs(diff) <= tolerance):
                break

            # Updating the values of the variables
            vector += diff

    return vector if vector.shape else vector.item()
 

# set the intial params to be the minimum x, y, z and the maximum vx, vy,vz from input data
# find the minimum and maximum values for the x, y, z and vx, vy, vz
min_x = min([line[0][0] for line in lineList])
max_x = max([line[0][0] for line in lineList])
min_y = min([line[0][1] for line in lineList])
max_y = max([line[0][1] for line in lineList])
min_z = min([line[0][2] for line in lineList])
max_z = max([line[0][2] for line in lineList])
max_vx = max([line[1][0] for line in lineList])
min_vx = min([line[1][0] for line in lineList])
max_vy = max([line[1][1] for line in lineList])
min_vy = min([line[1][1] for line in lineList])
max_vz = max([line[1][2] for line in lineList])
min_vz = min([line[1][2] for line in lineList])

# Initial parameters and hyperparameters
tryLine = ([np.array([min_x,min_y,min_z]), np.array([max_vx,max_vy,max_vz])]) 


# result = minimize(loss_function2, np.array([max_vx,max_vy,max_vx]), args=(lineList,), method='L-BFGS-B', options={'disp': True, 'maxiter': 1000},)
# print(result)
#print([line_intersection(lineList[i], tryLine) for i in range(len(lineList))])
# derive a list of times of intersection 
# derive a list of distances at those times

### or.. calculate the minimum distance apart of the projectile with each of the list of projectiles.



# minimize the sum of distances between the projectile and the other projectiles
# the loss function is the sum of the distances between the projectile and the other projectiles

# Run gradient descent
#params = gradient_descent(initial_params, lineList, learning_rate, iterations)
#print("Optimal parameters:", params)


# params = gradient_descent2([-3,1,2], lineList[:4], learning_rate, iterations)
# print("Optimal parameters:", params)

# insight.  Imagine the snowball is stationary, and all other projectiles travel at the relative velocity.
# Since the snowball must collide with al other projectiles, the other projectiles must all
# intersect at the same point in space.
# So find the snowball velocity by finding the velocities of the other projectiles that
# intersect at the same point in space.
#
# Domt need all the projectiles?  Try with just 3 , which form up two colliding pairs.

# How to use the python gradient descent imported?  Need to supply input arrays and
# a function 'grad'.  The function 'grad' is the derivative of the loss function with respect to the parameters.
# The loss function is the std deviation of the points of interesection, for x . for y and for x.
# Solve by changing the velocity of the snowball, and finding the minimum std deviation of the points of intersection.
# The gradient descent function will find the minimum std deviation of the points of intersection, and the velocity of the snowball
 # ..or the intersection points are in a striagt line
# fit the intersection points to a striaght line.

""" def stdDev(arr) :
    # find the standard deviation of the input array
    mean = np.mean(arr)
    return np.sqrt(np.sum((arr - mean)**2) / len(arr))



stdDevSum = np.inf
minStdDevSum = np.inf
vs = np.array([-100,-100,-100])
for t in range(1000) : # at one time
    for dv in range(100) : # range of velocities
        vs = vs + np.array([10,10,10])
        xt = []
        yt = []
        zt = []
        for p in lineList[:10]:
            Pt, Vtp = p
            x,y,z = Pt
            vx, vy, vz = Vtp
            vsx, vsy, vsz = vs
            xt.append(x + (vx-vsx)*t)
            yt.append(y + (vy-vsy)*t)
            zt.append(z + (vz-vsz)*t) 

    stdDevSum = stdDev(xt) + stdDev(yt) + stdDev(zt)
    if stdDevSum < minStdDevSum:
        minStdDevSum = stdDevSum
        print(vs, stdDevSum) """
 


    # fit the intersection points to a straight line
    # calculate the standard deviation of the intersection points from the line
    # return the derivative of the standard deviation with respect to the snowball velocity
    # the gradient descent function will find the snowball velocity that minimizes the standard deviation
    # of the intersection points from the line

# now try own solution

def hitEmAll(lineList) :
    # !!! not working yet - putting n the known solution does not get stdDev 0
    learning_rate = 0.4
    tolerance = 1
    #snowball = tryLine
    # snowball = ([12,13,14], [-3,1,2])
    # snowball = ([24,13,10], [-3,1,2])
    snowball = ([24,13,10], [-161,-122,70])

    Ps, Vs = snowball
    x,y,z = Ps
    vx, vy, vz = Vs
    params = [x,y,z,vx,vy,vz]
    delta = [1,1,1,1,1,1]
    better = [1,1,1,1,1,1]
    dtx = []
    dty = []
    dtz = []
    sampleList = lineList[:5]
    lastStdDev = 1
    maxiter = 1000
    iter = 0
    while lastStdDev > 0.1 and iter < maxiter:
        iter += 1
        for p in range(len(params)):
            snowball = (np.array([params[0],params[1],params[2]]), np.array([params[3],params[4],params[5]]))
            Ps, Vs = snowball
            for i in range(len(sampleList)): # here on could be in loss function
                Pt, Vtp = sampleList[i]
                intersection = line_intersection(snowball, sampleList[i])
                if intersection.any() == float('inf') : 
                    print("No intersection", params)
                    continue 
                else :
                    # for a collision, both reach the intersection point at the same time.
                    # tx = delta x / vx
                    txs = 0 if Vs[0] == 0 else (intersection[0] - Ps[0]) / Vs[0]
                    txp = 0 if Vtp[0] == 0 else (intersection[0] - Pt[0]) / Vtp[0]
                    dtx.append(txs - txp)
                    tys = 0 if Vs[1] == 0 else (intersection[1] - Ps[1]) / Vs[1]
                    typ = 0 if Vtp[1] == 0 else (intersection[1] - Pt[1]) / Vtp[1]
                    dty.append(tys - typ)
                    tzs = 0 if Vs[2] == 0 else (intersection[2] - Ps[2]) / Vs[2]
                    tzp = 0 if Vtp[2] == 0 else (intersection[2] - Pt[2]) / Vtp[2]
                    dtz.append(tzs - tzp)

            stdDev = np.std(dtx)+np.std(dty)+np.std(dtz)


            if np.abs(stdDev) < tolerance:
                print("Solution found", params, stdDev, iter)
                return params

            delta[p] = (stdDev-lastStdDev) # trial and error multiplier

            # if the stdDev has improved (lowered), then change the paramter again in the same direction

            params[p] = params[p] + (delta[p])

            params[p] = params[p] -1*learning_rate * delta[p]/1000
            print(params, stdDev, delta[p])
        
        lastStdDev = stdDev
    return params, lastStdDev, iter

# print(hitEmAll(lineList))

# I now have two approaches to solve this.  I know that the test solution is obtained when the std dev is 
# a) randome start with binary search to narrow down. b) gradient decline

# 0.  I can use the scipy optimize minimize function to find the minimum std dev, and the snowball velocity.

def loss_function(params, sampleList=lineList) :
    snowball = (np.array([params[0],params[1],params[2]]), np.array([params[3],params[4],params[5]]))
    Ps, Vs = snowball
    dtx = []
    dty = []
    dtz = []
    for i in range(len(sampleList)): # here on could be in loss function
        Pt, Vtp = sampleList[i]
        intersection = line_intersection(snowball, sampleList[i])
        if intersection.any() == float('inf') : 
            print("No intersection", params)
            continue 
        else :
            # for a collision, both reach the intersection point at the same time.
            # tx = delta x / vx
            txs = 1 if Vs[0] == 0 else (intersection[0] - Ps[0]) / Vs[0]
            txp = 0 if Vtp[0] == 0 else (intersection[0] - Pt[0]) / Vtp[0]
            dtx.append(txs - txp)
            tys = 1 if Vs[1] == 0 else (intersection[1] - Ps[1]) / Vs[1]
            typ = 0 if Vtp[1] == 0 else (intersection[1] - Pt[1]) / Vtp[1]
            dty.append(tys - typ)
            tzs = 1 if Vs[2] == 0 else (intersection[2] - Ps[2]) / Vs[2]
            tzp = 0 if Vtp[2] == 0 else (intersection[2] - Pt[2]) / Vtp[2]
            dtz.append(tzs - tzp)

    stdDev = np.std(dtx)+np.std(dty)+np.std(dtz)
    print(stdDev)
    return stdDev, params

#initial_params = np.array([min_x, min_y, min_z, max_vx, max_vy, max_vz])  # initial guess 

#initial_params = np.array([10,10,10,10,10,10])  # initial guess  .. this almost got the test solution.  [23.39,13,10,-3,1,2] .. should be 24
# print(loss_function([24,13,10,-3,1,2], lineList)) # the test solution.


initial_params = np.array([max_x,max_y,max_z,min_vx*2,min_vy*2,min_vz*2]) 
# print(loss_function([-10000000000,10000000000,10000000000,-4000000,-29767,-27525], lineList))
#result = minimize(loss_function, initial_params, args=(lineList,), method='L-BFGS-B', options={'disp': True, 'ftol' : 1e-14, 'maxls' : 30},)



bounds = [(min_x, max_x), (min_y, max_y), (min_z, max_z), (min_vx, max_vx), (min_vy, max_vy), (min_vz, max_vz)]
# result = dual_annealing(loss_function, bounds, args=(lineList,), maxiter=1000, minimizer_kwargs=None, initial_temp=5230.0, restart_temp_ratio=2e-05, visit=2.62, accept=-5.0, maxfun=10000000.0, seed=None, no_local_search=False, callback=None, x0=None)
# print(result)

# from the Line list make three dictionaries, one for each x, y, z as keys and the corresponding vx, vy, vz as value. Sort the
#dictionaries by ascending x, y, z keys
x_dict = {}
y_dict = {}
z_dict = {}

print(max_x-min_x, max_y-min_y, max_z-min_z)
for line in lineList:
    x, y, z = line[0]
    vx, vy, vz = line[1]
    x_dict[x] = vx
    y_dict[y] = vy
    z_dict[z] = vz




x_dict = dict(sorted(x_dict.items(), key=lambda item: item[1]))
y_dict = dict(sorted(y_dict.items(), key=lambda item: item[1]))
z_dict = dict(sorted(z_dict.items(), key=lambda item: item[1]))


print(x_dict)

# chose a starting value for x, vx that has x higher than most of the line dictionany keys where vx is positive, and 



