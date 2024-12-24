import matplotlib.pyplot as plt

import krpc
import time
import csv
import matplotlib.pyplot as plt
def main():
    # Подключение к серверу kRPC
    conn = krpc.connect(name='Space M')

    # Получение информации об активном "судне"
    vessel = conn.space_center.active_vessel
  
    #получение информации о небесном теле - Луне
    body = vessel.orbit.body 

    #Открытие csv файла
    w_file = open("KSP data.csv", mode="w", encoding="UTF-8")
    fieldnames = ['Time since maneuver start', 'Periasis', 'Velocity']
    writer = csv.DictWriter(w_file, fieldnames=fieldnames)
    writer.writeheader()   
    # Инициализация списков для хранения данных
    velocity_data = []
    time_data = []
    periasis_data = [] 

    try:
        # Ждем, пока не зарабоатет двигатель Луны-25 
        while vessel.control.throttle == 0:
          print(conn.space_center.ut, vessel.control.throttle)
          time.sleep(0.5)
        # Маневр начался. Считываем данные, пока работает двигатель
        time_start = round(conn.space_center.ut, 2) 
        while vessel.control.throttle > 0:  
          # Получение текущего  времени
          cur_time = round(conn.space_center.ut, 2)
          time_since_m = cur_time - time_start  
          # Получение текущей скорости
          velocity = round(vessel.flight(body.orbital_reference_frame).speed, 5)
          # Получение текущего перигея
          periasis = round(vessel.orbit.periapsis_altitude,5)
          # Запись данных
          velocity_data.append(velocity)
          periasis_data.append(periasis)
          time_data.append(round(time_since_m, 2))
          print(time_since_m, cur_time,velocity, vessel.orbit.time_to_apoapsis, vessel.control.throttle)
          # Задержка перед следующим измерением
          time.sleep(1) 


    except KeyboardInterrupt:
        print('Программа завершена пользователем.')

    finally:
        # Закрытие соединения с сервером kRPC
        conn.close()
        #Запись полученных данных в csv файл, закрытие файла
        for n in range(len(time_data)):
            writer.writerow({'Time since maneuver start': time_data[n], 'Periasis': periasis_data[n],'Velocity': velocity_data[n]})
        w_file.close()

    # Инициализация списков для построения графиков, описание констант
    F = 375.0 # тяга двигателя
    m = 1750.0 # Масса Луны-25
    V2 = 1633.0 # Скорость на круговой орбите
    t_engine = 84
    G1 = 100000.0 # Апогей
    R = 1737700.0 # Радиус Луны
    mu = 4902.8 * (1000 ** 3) # гравитаицонная постоянная
    peri_ot_V = []
    peri_ot_t = []
    Scorost = []
    Time = []
    V1 = []
    time2 = []                                                      

    # Инициализируем функции, вычисляющие данные, основанные на мат модели
                             
    def VotT(t,m,V2,F):
        return (m * V2 - F * t) / m
    
    def G2V(R, G1, m, mu, V):
        return (((R + G1) * 2 * mu) / (2*mu  - ((R + G1) * (V**2)))) - 2 * R - G1

    def G2R(R, G1, m, mu, V2,t):
        return (((R + G1) * 2 * mu* (m**2)) / (2*(m**2)*mu  - (R + G1)*(m*V2 - F*t)**2)) - 2 * R - G1


    # Циклы, вычисляющие необходимые зависимости
    
    for Vi in range(1634, 1606, -1):   
        peri_ot_V.append(G2V(R,G1,m,mu,Vi))
        Scorost.append(Vi)

    for t in range(0, 127):
        peri_ot_t.append(G2R(R,G1,m,mu,V2,t))
        Time.append(t)

    for t in range(t_engine + 1):
        time2.append(t)
        V1.append(VotT(t,m,V2,F))
    #Построение графиков
        
    plt.plot(Time, peri_ot_t, label="Данные из Мат. модели", lw=2.2)
    plt.plot(time_data, periasis_data, label="Данные из KSP", lw=2.2)
    plt.xlabel('Время (секунды)')
    plt.ylabel('Перигей (метры)')
    plt.title('График зависимости перигея от времени работы двигателя')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.plot(Scorost, peri_ot_V, label="Данные из Мат. модели", lw=2.2)
    plt.plot(velocity_data, periasis_data, label="Данные из KSP", lw=2.3)
    plt.xlabel('Скорость аппарата (м/c)')
    plt.ylabel('Перигей (метры)')
    plt.title('График зависимости Перигея от орбитальной скорости аппарата')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.plot(time2, V1, label="Данные из Мат. модели", lw=2.2)
    plt.plot(time_data, velocity_data, label="Данные из KSP", lw=2.3)
    plt.xlabel('Время работы двигателя (c)')
    plt.ylabel('Скорость аппарата (м/c)')
    plt.title('График зависимости орбитальной скорости аппарата от времени работы двигателя')
    plt.grid(True)
    plt.legend()
    plt.show()
        

if __name__ == '__main__':
   main()


