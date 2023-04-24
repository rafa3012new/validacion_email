#la idea de esta clase es poder grabar las friendships
from flask_validacion_email.config.mysqlconnection import connectToMySQL
from flask_validacion_email.utils.regex import REGEX_CORREO_VALIDO
from flask import flash

BASE_DATOS="validacion_email"

# modelar la clase después de la tabla friendships de nuestra base de datos
class Email:
    def __init__( self , data ):
        self.id= data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def validar_existe(cls, campo, valor):
        query = f"SELECT count(*) as contador FROM emails WHERE email = %({campo})s;"
        data = { campo : valor }
        results = connectToMySQL(BASE_DATOS).query_db(query, data)
        return results[0]['contador'] > 0


    @classmethod
    def validar(cls, data):

        is_valid = True
        #se crea una variable no_create para evitar la sobre escritura de la variable is_valid
        #pero a la vez se vean todos los errores al crear el usuario
        #y no tener que hacer un return por cada error
        no_create = is_valid

        if 'email' in data:
            if not REGEX_CORREO_VALIDO.match(data['email']):
                # flash('El correo no es válido', 'error')
                is_valid = False

            if is_valid == False: no_create = False

            if cls.validar_existe('email', data['email']):
                # flash('el correo ya fue ingresado', 'error')
                is_valid = False

            if is_valid == False: no_create = False


        return no_create



    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        # asegúrate de llamar a la función connectToMySQL con el esquema al que te diriges
        results = connectToMySQL(BASE_DATOS).query_db(query)
        print("estos son los resultados ", results,flush=True)
        # crear una lista vacía para agregar nuestras instancias de friendships
        datos = []
        # Iterar sobre los resultados de la base de datos y crear instancias de friendships con cls
        for dato in results:
            datos.append(cls(dato))
        return datos

    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_by_id(cls,data):
        #armar la consulta con cadenas f
        query = 'SELECT * FROM emails where id = %(id)s;'
        results = connectToMySQL(BASE_DATOS).query_db( query, data)
        #devolver el primer registro de los resultados si resultados devuelve algo sino que devuelva None
        return cls(results[0]) if len(results) > 0 else None


    @classmethod
    def save(cls, data):
        query = "INSERT INTO emails (email) VALUES ( %(email)s);"
        # data es un diccionario que se pasará al método de guardar desde server.py
        datos = connectToMySQL(BASE_DATOS).query_db( query, data)
        return datos


    @classmethod
    def delete(cls, data):
        query = "DELETE FROM emails WHERE email = %(email)s;"
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        return resultado