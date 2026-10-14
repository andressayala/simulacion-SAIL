import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import PillowWriter

from sympy import symbols, rad, Matrix, solve, lambdify, pprint
from sympy.physics.mechanics import dynamicsymbols, ReferenceFrame

class USV_Model():
    def __init__(self, m=5, l=1, c=1):
        self.m = m
        self.l = l
        self.c = c
        
        self.model = self.create_dynamic_model()
        self.dynamics = self.lambdify_dynamic_model(self.model, self.m, self.l, self.c)
    
    def create_dynamic_model(self):
        x_1, x_2, theta = dynamicsymbols('x_1, x_2, theta')
        u_1, u_2 = symbols('u_1, u_2')
        N = ReferenceFrame('N')

        B = N.orientnew('B', 'Axis', (theta, N.z))
        M = B.orientnew('M', 'Axis', (rad(90) + u_2, B.z))

        xipos = x_1*N.x + x_2*N.y
        xivel = xipos.dt(N)
        xiacc = xivel.dt(N)

        m, l, c = symbols('m, l, c')

        sumF = u_1*M.x -c*(xivel) - m*xiacc

        sumM = (-l/2*B.y).cross(u_1*M.x) -c*theta.diff()*B.z - m*l**2/12*theta.diff().diff()*B.z
        
        sumFx = sumF.dot(N.x)
        sumFy = sumF.dot(N.y)
        sumMz = sumM.dot(N.z)

        eqs = [sumFx, sumFy, sumMz]
        vars = [x_1.diff().diff(), x_2.diff().diff(), theta.diff().diff()]

        slns = solve(eqs, vars)

        model = Matrix([slns[x_1.diff().diff()], slns[x_2.diff().diff()], slns[theta.diff().diff()]])
        model.simplify()
        return model
    
    def lambdify_dynamic_model(self, system_dynamics, m_value, l_value, c_value):
        x_1, x_2, theta = dynamicsymbols('x_1, x_2, theta')
        u_1, u_2 = symbols('u_1, u_2')
        m, l, c = symbols('m, l, c')
        
        params = {m:m_value, l:l_value, c:c_value}
        dynamics = lambdify([[x_1, x_2, theta, x_1.diff(), x_2.diff(), theta.diff()], u_1, u_2], system_dynamics.subs(params), 'numpy')
        dynamics_fun = lambda q, u_1, u_2 : dynamics(q, u_1, u_2).squeeze()
        
        return dynamics_fun
    
    def change_params(self, m, l, c):
        self.m = m
        self.l = l
        self.c = c
        
    def get_dynamics(self):
        return self.dynamics
    
    def linearize_dynamic_model(self, q, u):
        m, l, c = symbols('m, l, c')
        u_1, u_2 = symbols('u_1, u_2')
        x_1, x_2, theta = dynamicsymbols('x_1, x_2, theta')

        params = {m: self.m, l: self.l, c:self.c}

        states = Matrix([x_1, x_2, theta, x_1.diff(), x_2.diff(), theta.diff()])
        inputs = Matrix([u_1, u_2])        

        A_sym = Matrix([x_1.diff(), x_2.diff(), theta.diff(), self.model[0], self.model[1], self.model[2]])
        B_sym = Matrix([x_1.diff(), x_2.diff(), theta.diff(), self.model[0], self.model[1], self.model[2]])

        A_sym = A_sym.subs(params).jacobian(states)
        B_sym = B_sym.subs(params).jacobian(inputs)

       
        eq_point = {x_1: q[0], x_2:q[1], theta:q[2], x_1.diff():q[3], x_2.diff():q[4], theta.diff():q[5], u_1: u[0], u_2: u[1]}
        
        A_num = np.array(A_sym.subs(eq_point), dtype=float)
        B_num = np.array(B_sym.subs(eq_point), dtype=float)


        
        return A_num, B_num
        
    
    def animate(self, qq, dt, filename='anim.gif', FPS=24, dpi=80, window_size=10):

        fig, ax = plt.subplots()
        com = ax.scatter([], [], label='com')

        ax.grid()
        ax.legend()
        ax.set_xlim(-window_size, window_size)
        ax.set_ylim(-window_size, window_size)
        ax.set_aspect('equal')

        ax.set(xlabel='$x$ Axis ($m$)', ylabel='$y$ Axis ($m$)')

        sample_rate = int(1/(dt*FPS))
        writer = PillowWriter(fps=FPS)

        with writer.saving(fig, filename, dpi):
            for i in range(0, len(qq), sample_rate):

                com.set_offsets([[(qq[i, 0]), (qq[i, 1])]])

                fig.canvas.draw()
                writer.grab_frame()

        plt.close(fig)