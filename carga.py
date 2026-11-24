import pyodbc
import pandas as pd

#Funcion para conectar a SQL Server
def conectar():
   conexion = pyodbc.connect(
       "DRIVER={ODBC Driver 18 for SQL Server};"
       "SERVER=.\\SQLEXPRESS;"
       "DATABASE=Proyecto_Programacion;"
       "Trusted_Connection=yes;"
       "TrustServerCertificate=yes;"
   )
   return conexion

#Funcion para leer los datos integrados
def leer_datos():
   #Leer el archivo CSV
   df = pd.read_csv("Datos_Integrados.csv")

   #Mostrar la informacion del archivo
   print("\nDatos integrados")
   print(df.head())

   #Mostrar la cantidad de registros y columnas
   print("\nCantidad de registros:", len(df))
   print("Cantidad de columnas:", len(df.columns))

   return df
#Funcion para transformar los datos para la tabla Valores
def preparar_valores(df):
   # Convertir las columnas de indicadores en filas
   df_valores = df.melt(
       id_vars=["Periodo"],
       var_name="Indicador",
       value_name="Valor"
   )

   #Mostrar los datos preparados
   print("\nDatos preparados para la tabla Valores")
   print(df_valores.head(15))

   #Mostrar la cantidad de registros
   print("\nCantidad de valores:", len(df_valores))


   return df_valores

#Funcion para relacionar los indicadores con sus identificadores
def relacionar_indicadores(df_valores):
   # Asignar el identificador correspondiente a cada indicador
   indicadores = {
       "INPC_General": 1,
       "INPC_Mercancias": 2,
       "INPC_Servicios": 3,
       "INPC_Agropecuarios": 4,
       "INPC_Energeticos_Gobierno": 5,
       "Nacimientos": 6,
       "Fecundidad": 7,
       "Consumo": 8,
       "Crecimiento_Consumo": 9,
       "Consumo_Porcentaje_PIB": 10
   }

   #Agregar la columna con los identificadores
   df_valores["IdIndicador"]= df_valores["Indicador"].map(indicadores)

   #Mostrar los datos relacionados
   print("\nDatos con identificadores de indicadores")
   print(df_valores.head(15))

   # Comprobar si existen identificadores vacios
   print("\nIdentificadores sin asignar:")
   print(df_valores["IdIndicador"].isnull().sum())
   return df_valores

#Funcion para relacionar los periodos con sus identificadores
def relacionar_periodos(df_valores, conexion):

   #Consultar los periodos registrados en SQL Server
   cursor= conexion.cursor()
   cursor.execute("SELECT IdPeriodo,  Anio FROM Periodos")

   #Obtener los resultados de la consulta
   datos_periodos=cursor.fetchall()

   #Convertir los resultados a tuplas
   datos_periodos = [tuple(fila) for fila in datos_periodos]

   #Crear un DataFrame con los periodos
   df_periodos =pd.DataFrame(
       datos_periodos,
       columns=["IdPeriodo", "Anio"]
   )

   #Relacionar los datos mediante el año
   df_valores=pd.merge(
       df_valores,
       df_periodos,
       left_on="Periodo",
       right_on="Anio",
       how="inner"
   )

   #Mostrar los datos relacionados
   print("\nDatos con identificadores de periodos")
   print(df_valores.head(15))

   #Comprobar si existen identificadores vacios
   print("\nIdentificadores de periodos sin asignar:")
   print(df_valores["IdPeriodo"].isnull().sum())

   #Mostrar la cantidad de registros
   print("\nCantidad de registros relacionados:", len(df_valores))

   #Cerrar el cursor
   cursor.close()
   return df_valores
#Funcion para insertar los valores en SQL Server
def insertar_valores(df_valores):
   conexion= conectar()       # Conectar a SQL
   cursor =conexion.cursor()  # Crear el cursor
   sql="""
   INSERT INTO Valores
   (IdPeriodo, IdIndicador, Valor)
   VALUES (?,?,?)
   """

   #Preparar los datos para insertar
   parametros= []

   for fila in df_valores.values:
       parametros.append((
           fila[4],  #IdPeriodo
           fila[3],  #IdIndicador
           fila[2]   # Valor
       ))

   #Insertar todos los registros
   cursor.executemany(sql, parametros)

   #Guardar los cambios
   conexion.commit()

   #Mostrar la cantidad de registros insertados
   print("\nRegistros insertados correctamente:",len(parametros))

   #Cerrar el cursor y la conexion
   cursor.close()
   conexion.close()

#Ejecutar las funciones
if __name__ == "__main__":

   conexion = conectar()
   print("Conexion realizada correctamente")
   df = leer_datos()
   df_valores =preparar_valores(df)
   df_valores=relacionar_indicadores(df_valores)
   df_valores = relacionar_periodos(df_valores, conexion)
   conexion.close()
   insertar_valores(df_valores)
