import pandas as pd

#Integrar los archivos transformados en una sola tabla
def integrar_datos():
   #Cargar los archivos transformados
   df_inpc= pd.read_csv("Inpc_Preparado.csv")
   df_nacimientos =pd.read_csv("Nacimientos_Transformados.csv")
   df_fecundidad= pd.read_csv("Fecundidad_Transformada.csv")
   df_consumo= pd.read_csv("Consumo_Transformado.csv")
   df_crecimiento =pd.read_csv("Crecimiento_Consumo_Transformado.csv")
   df_consumo_pib =pd.read_csv("Consumo_Pib_Transformado.csv")

   #Cambiar los nombres de las columnas
   df_nacimientos.rename(columns={"Valor":"Nacimientos"},inplace=True)
   df_fecundidad.rename(columns={"Valor": "Fecundidad"}, inplace=True)
   df_consumo.rename(columns={"Valor":"Consumo"},inplace=True)
   df_crecimiento.rename(columns=  {"Valor":"Crecimiento_Consumo"},inplace=True)
   df_consumo_pib.rename(columns={"Valor":"Consumo_Porcentaje_PIB"}, inplace=True)

   # Elimina las columnas de indicadores
   df_nacimientos.drop(columns=["Indicador"], inplace=True)
   df_fecundidad.drop(columns=["Indicador"],inplace=True)
   df_consumo.drop(columns=["Indicador"],inplace=True)
   df_crecimiento.drop(columns=["Indicador"],inplace=True)
   df_consumo_pib.drop(columns=["Indicador"], inplace=True)

   #Integrar los archivos mediante el año
   df =pd.merge(df_inpc, df_nacimientos, on="Periodo", how="inner")
   df= pd.merge(df,df_fecundidad,on="Periodo", how="inner")
   df= pd.merge(df, df_consumo, on="Periodo",how="inner")
   df =pd.merge(df,df_crecimiento,on="Periodo",how="inner")
   df=pd.merge(df,df_consumo_pib, on="Periodo",how="inner")

   # Ordenar los datos por año
   df.sort_values("Periodo", inplace=True)

   # Reiniciar los indices
   df.reset_index(inplace=True, drop=True)

   # Comprobar si los nacimientos tienen valores decimales
   print("\nRevision de nacimientos")
   print("Parte decimal de los valores:")
   print(df["Nacimientos"] % 1)

   # Convertir nacimientos a numeros enteros
   if (df["Nacimientos"] % 1 == 0).all():
       df["Nacimientos"] = df["Nacimientos"].astype(int)

   # Mostrar los datos integrados
   print("\nDatos integrados")
   print(df.dtypes)
   print(df.head())
   print(df.tail())
   print("Cantidad de registros:", len(df))
   print("Cantidad de columnas:", len(df.columns))

   # Revisar valores nulos
   print("\nRevision de valores nulos")
   print(df.isnull().sum())

   # Revisar registros duplicados completos
   print("\nRevision de registros duplicados")
   print("Registros duplicados:", df.duplicated().sum())

   # Revisar años duplicados
   print("\nRevision de años duplicados")
   print("Años duplicados:", df["Periodo"].duplicated().sum())

   if df["Periodo"].duplicated().sum() > 0:
       print(df[df.duplicated(subset=["Periodo"], keep=False)])
   else:
       print("No existen años duplicados")

   # Revisar los años registrados
   print("\nAños registrados")
   print(df["Periodo"].unique())

   # Contar registros por año
   print("\nCantidad de registros por año")
   print(df["Periodo"].value_counts().sort_index())

   # Obtener estadisticas descriptivas
   print("\nEstadisticas descriptivas")
   print(df.describe())

   # Guardar los datos integrados
   df.to_csv("Datos_Integrados.csv", index=False, encoding="utf-8-sig")

# Ejecutar la integración
if __name__ == "__main__":
   integrar_datos()
