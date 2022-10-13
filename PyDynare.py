#!/usr/bin/env python
# coding: utf-8

# In[93]:


import sympy as sy
import numpy as np
#parameters:
γ, δ, β, α, ρ_a, σ_a =sy.symbols("γ δ β α rho_A σ_A")
#external shock:
ϵ_a =sy.Symbol("ϵ_A")
#variables in t
c, inv, w, l, rk, k, t, λ, y, A, l =sy.symbols("c_t inv_t w_t l_t r^k_t k_t t λ_t y_t A_t l_t")
#variables in t+1
c1, inv1, w1, l1, rk1, k1, λ1, A1, l1 =sy.symbols("c_t+1 inv_t+1 w_t+1 l_t+1 r^k_t+1 k_t+1 λ_t+1 A_t+1 l_t+1 ")
#variables in t+2
c2, inv2, w2, l2, rk2, k2 =sy.symbols("c_t+2 inv_t+2 w_t+2 l_t+2 r^k_t+2 k_t+2")
#ECONOMY

yd=c+inv

#HOMES

#Utility funtion
U= β**t*(c**(1-γ)-1)/(1-γ)

#Capital movement
capital_movement= (1-δ)*k+inv-k1
capital_movement1= (1-δ)*k1+inv1-k2

#Investement
inv=sy.factor((sy.solve(capital_movement, inv)[0]),k)
inv1=sy.factor((sy.solve(capital_movement1, inv1)[0]),k)

#Budget
budget=w*l+k*rk-c-inv
budget1=w1*l1+k1*rk1-c1-inv1

#Lagrange:
lagrange=U+β**t*λ*budget+β**(t+1)*λ1*budget1

#First Order Condition
diff_c=(lagrange.diff(c)).simplify()
a=sy.solve(diff_c, λ)[0]
a1=a.subs(c,c1)
diff_k1=(lagrange.diff(k1))

#Euler equation
euler_eqtn=(diff_k1.subs(λ,a).subs(λ1,a1))

#Consumption
consumption=sy.solve(euler_eqtn, c)[0]

#FIRMS
#Tecnology
ys=A*k**α*l**(1-α)

#Profit equation
Π=ys-w*l-rk*k

#First Order Conditions
diff_l=Π.diff(l).simplify()
diff_k=Π.diff(k).simplify()

#cost of capital
r=sy.solve(diff_k,rk)[0]
r1=r.subs(k,k1).subs(A,A1).subs(l,l1)

#wages
w=sy.solve(diff_l,w)[0]

#Shock
A1= ρ_a*sy.log(A)+σ_a*ϵ_a
consumption=consumption.subs(rk1,r1)
euler_eqtn=euler_eqtn.subs(rk1,r1)

#Stationary states:
c_ss, k_ss, w_ss, rk_ss, y_ss, inv_ss =sy.symbols("c^* k^* w^* rk^* y^* inv^*")

k_ss=sy.solve(euler_eqtn.subs(c1,c_ss).subs(c,c_ss).subs(k1,k_ss),k_ss)[0]
inv_ss=inv.subs(k1, k_ss).subs(k,k_ss)
y_ss=ys.subs(k,k_ss)
c_ss=y_ss-inv_ss
l_ss=1
w_ss=w.subs(k,k_ss).subs(l,l_ss)
rk_ss=r.subs(k,k_ss).subs(l,l_ss)
A_ss=1



# In[115]:


k_ss=sy.lambdify([α,β,δ,A,l], k_ss)
inv_ss=sy.lambdify([α,β,δ,A,l], inv_ss)
y_ss=sy.lambdify([α,β,δ,A,l], y_ss)
c_ss=sy.lambdify([α,β,δ,A,l], c_ss)
w_ss=sy.lambdify([α,β,δ,A,l], w_ss)
rk_ss=sy.lambdify([α,β,δ,A,l], rk_ss)


ss= np.array([k_ss(α=0.33, β=0.99, δ=0.025, A_t=1, l_t=1), inv_ss(α=0.33, β=0.99, δ=0.025, A_t=1,l_t=1),
              y_ss(α=0.33, β=0.99, δ=0.025, A_t=1, l_t=1), c_ss(α=0.33, β=0.99, δ=0.025, A_t=1, l_t=1),
              w_ss(α=0.33, β=0.99, δ=0.025, A_t=1, l_t=1), rk_ss(α=0.33, β=0.99, δ=0.025, A_t=1, l_t=1),
              A_ss])
#DYNAMIC

#Cost of capital
rk=sy.lambdify([A,k,α,l],r)
#Wages=
w=sy.lambdify([A,k,α,l],w)
#Consumption
c=sy.lambdify([α,β,δ,k1,c1,γ,l1,A1], consumption)
#Investment
inv=sy.lambdify([k,δ,k1], inv)
#Economy
y=yd-ys
y=sy.lambdify([α,β,δ,A,k1,c1,γ,k],y)
#Tecnology shock
A1=sy.lambdify([ρ_a,σ_a, sy.ln(A)], A1)
#capital movement
k1=sy.lambdify([k,δ,k1], capital_movement)



consumption


# In[105]:


type(dynamic[0])
x_path= np.zeros((7,10))

for t in range (0,10):
    if t==0:
        x_path[:,t]=ss
    else:
        x_path[:,t]=x_path[:,t-1]+dynamic[:,]
    
x_path

