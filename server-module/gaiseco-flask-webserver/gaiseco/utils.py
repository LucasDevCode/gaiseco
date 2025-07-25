from flask import flash
from flask import current_app

from threading import enumerate


def d(msg):
    n = len(str(msg))
    print("-"*n)
    print(str(msg))
    print("-"*n)


def start_first_thread():
    if len(current_app.config['THREADS']) > 0:
        t = current_app.config['THREADS'][0]
        
        if t.native_id == None:
            t.start()

            flash(t.name + ' iniciado...')
            
            d("Thread iniciada : " + t.name)


def check_first_thread_finish():
    if len(current_app.config['THREADS']) > 0:
        t = current_app.config['THREADS'][0]

        if t.native_id != None and t.is_alive() == False:
            current_app.config['THREADS'].remove(t)
            
            flash(t.name + ' finalizado!', 'success')

            d("Thread finalizada : " + t.name)

    