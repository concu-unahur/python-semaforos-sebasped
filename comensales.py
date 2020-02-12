import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Cocinero(threading.Thread):
  def __init__(self):
    super().__init__()
    self.name = 'Cocinero'

  def run(self):
    global platosDisponibles
    while (True):
      semaCoci.acquire()
      semaPlato.acquire() #el cocinero está reponiendo platos, asi que nadie puede comer
      try:
        time.sleep(1)
        logging.info('Reponiendo los platos...')
        platosDisponibles = 3
      finally:
        semaPlato.release()
        # pass

class Comensal(threading.Thread):
  def __init__(self, numero):
    super().__init__()
    self.name = f'Comensal {numero}'

  def run(self):
    global platosDisponibles
    
    semaPlato.acquire()
    try:
      if platosDisponibles>0:
          platosDisponibles -= 1
          time.sleep(1)
          logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')
      else:
        semaCoci.release()
    finally:
        semaPlato.release()

semaPlato = threading.Semaphore(1)
semaCoci = threading.Semaphore(1)

platosDisponibles = 3
semaCoci.acquire() # como hay platos, entonces que el cocinero espera

Cocinero().start()

for i in range(10):
  Comensal(i).start()

