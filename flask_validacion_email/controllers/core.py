from winreg import FlushKey
from wsgiref.util import request_uri
from flask_validacion_email import app
#se importa el modelo que contiene la clase
from flask_validacion_email.models.emails import Email
#se importa las funciones de flask
from flask import render_template, redirect, request, session, flash
#se importan el modulo de fechas
from datetime import date


#Ruta Raiz carga una lista de diccionarios via GET render
@app.route('/')
def main_page():
  #tambien se devuelve la lista de diccionarios como una variable renderizada GET como practica
  return render_template('main.html')

#Ruta para Limpiar
@app.route('/limpiar')
def limpiar():
  session.clear()
  return redirect('/')


#Ruta por si el susuario volvio atras por un boton y no por el explorador
@app.route('/regreso')
def redirigir():
  print("ESTAMOS REDIRIGIENDO A INDEX!!!!")
  return redirect('/')


#Ruta para procesar ejecutando un metodo POST
@app.route('/grabar', methods=['POST'])
def procesar_email():

  #se caaptura la data el email
  data = {'email':request.form['email']}

  if 'enviar' in request.form:
   #si se presiono el boton tipo submit enviar
   if request.form['enviar'] == 'enviar':
     #se verifica si el email es valido, aparte de las validaciones del elemento html
     if not Email.validar(request.form):
         flash("Direccion email no valida o ya existe...","danger")
         return redirect('/')

     #se trata grabar el email
     try:
         Email.save(data)
         #se emite un mensaje flash exitoso
         flash("La direcion email que introdujo en valida, se grabo exitosamente!","success")
         #se emite un mensaje por consola exitoso
         print("email guardado exitosamente!",flush=True)
     except Exception as error:
         #se emite un mensaje flash de error
         flash(f"error guardando el email {error}","danger")
         #se emite un mensaje por consola de error
         print("Error guardando el email error: ",error,flush=True)

  if 'eliminar' in request.form:
   #si se presiono el boton tipo submit eliminar
   if request.form['eliminar'] == 'eliminar':
    #se debe verificar si el email existe en la base de datos
      #si existe se emite un mnesaje de error que no existe en la base de datos
      if not Email.validar_existe('email',data['email']):
        flash("La direcion email que introdujo no existe en la base de datos...","danger")
      else:  #si existe entonces se procede con la eliminacion
        #se trata de eleiminar el email
        try:
            Email.delete(data)
            #se emite un mensaje flash exitoso
            flash("Se ha eliminado el email exitosamente!","success")
            #se emite un mensaje por consola exitoso
            print("email eliminado exitosamente!",flush=True)
        except Exception as error:
            #se emite un mensaje flash de error
            flash(f"error eliminando el email {error}","danger")
            #se emite un mensaje por consola de error
            print("Error eliminando el email, erro: ",error,flush=True)


  #se redirige el POST hacia la pagina de checkout
  return redirect('/result')


#Ruta para el checkout
@app.route('/result')
def checkout():
  #se rederiza la pagina checkout
  diasemana = ['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
  meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

  today = diasemana[date.today().weekday()] + ', ' + str(date.today().day) + ' de ' + meses[date.today().month] + ' de ' + str(date.today().year)

  emails_enviados = Email.get_all()


  return render_template('enviados.html',hoy = today,emails_enviados=emails_enviados)


if __name__=="__main__":   # Asegúrate de que este archivo se esté ejecutando directamente y no desde un módulo diferente    
    app.run(debug=True)    # Ejecuta la aplicación en modo de depuración