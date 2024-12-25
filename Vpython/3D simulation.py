Web VPython 3.2

scene1 = canvas(Title='Test', x=0, y=0, width=800, height=800, background=color.black)

v = float(input('введите орбитальную скорость аппарата'))
dt = 0.1 # шаг интегрирования
rate_multiplier=900
rotation_vel = 2*pi
g=1.625
radius_pow = 2
mu = 4902.8 * (1000 ** 3) # Грав. параметр Луны - произведние гравитационной постоянной на массу Луны
k = 0
sat_size = 2000
sat_start_pos = vector(0,-1837000,0)
start_velocity = vector(v,0,0)
planet = sphere(pos=vector(0,0,0), radius=1737000, color = color.white)
satelite = sphere(pos=sat_start_pos, radius=sat_size, color=color.yellow, texture=textures.metal, make_trail=True)
satelite.velocity = start_velocity

scene1.camera.follow(satelite)
print(sat_start_pos)

oscillation = graph(title='График зависимости расстояния до поверхности луны от времени', xtitle='время', ytitle='Радиус', fast=False, width=500)
funct1 = gcurve(color=color.blue, width=4, markers=True, marker_color=color.orange, label='радиус')

k = 0

# Вращение происходит, фактически, вокруг точки (центра планеты), поэтому в каждой точке расчета нам нужно ускорение свободного падение давать по вектору, связываещему положение тела с центром планеты
t=0
while 1:
    rate(rate_multiplier/dt) # шаг интегрирования
    radius_vector=planet.pos-satelite.pos #задаем радиус вектор
    radius_vector_norm=radius_vector/radius_vector.mag # Нормализация (делим вектор на его длину)
    g = mu/(radius_vector.mag**2) #ускорение свободного падения (зависит от квадрата радиуса)
    g_vect = radius_vector_norm * g
    satelite.velocity += g_vect*dt # в каждом тике добавляем к скорости ускорение свободного падения, умноженное на шаг интегрирования
    satelite.pos += satelite.velocity*dt # в каждом тике добавляем к позиции скорость, умноженное на шаг интегрирования
    k+=1
    if k==2500:
        k = 0
        t+=1
        funct1.plot(t, radius_vector.mag - planet.radius) 

        
    
