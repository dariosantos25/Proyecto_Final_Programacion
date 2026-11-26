CREATE DATABASE Proyecto_Programacion
GO
USE Proyecto_Programacion
GO

-- Crear la tabla de fuentes
CREATE TABLE Fuentes (
    IdFuente INT IDENTITY(1,1) PRIMARY KEY,
    NombreFuente VARCHAR(100) NOT NULL UNIQUE,
    URLS VARCHAR(500) NOT NULL
)
GO
-- Crear la tabla de indicadores
CREATE TABLE Indicadores (
    IdIndicador INT IDENTITY(1,1) PRIMARY KEY,
    NombreIndicador VARCHAR(150) NOT NULL UNIQUE,
    UnidadMedida VARCHAR(100) NOT NULL,
    IdFuente INT NOT NULL,
    FOREIGN KEY (IdFuente) REFERENCES Fuentes(IdFuente)
)
GO
-- Crear la tabla de periodos
CREATE TABLE Periodos (
    IdPeriodo INT IDENTITY(1,1) PRIMARY KEY,
    Anio INT NOT NULL UNIQUE
)
GO
-- Crear la tabla de valores
CREATE TABLE Valores (
    IdPeriodo INT NOT NULL,
    IdIndicador INT NOT NULL,
    Valor DECIMAL(30,8) NOT NULL,
    PRIMARY KEY (IdPeriodo, IdIndicador),
    FOREIGN KEY (IdPeriodo) REFERENCES Periodos(IdPeriodo),
    FOREIGN KEY (IdIndicador) REFERENCES Indicadores(IdIndicador)
)
GO
-- Registrar las fuentes de información
INSERT INTO Fuentes (NombreFuente, URLS)
VALUES
('INEGI', 'https://www.inegi.org.mx/'),
('Banco Mundial', 'https://data.worldbank.org/')

GO
-- Registrar los indicadores del INEGI
INSERT INTO Indicadores (NombreIndicador, UnidadMedida, IdFuente)
VALUES
('INPC General', 'Indice', 1),
('INPC Mercancias', 'Indice', 1),
('INPC Servicios', 'Indice', 1),
('INPC Agropecuarios', 'Indice', 1),
('INPC Energeticos y tarifas autorizadas por el gobierno', 'Indice', 1),
('Nacimientos', 'Nacimientos registrados', 1)
GO
-- Registrar los indicadores del Banco Mundial
INSERT INTO Indicadores (NombreIndicador, UnidadMedida, IdFuente)
VALUES
('Fecundidad', 'Hijos por mujer', 2),
('Consumo', 'Moneda constante', 2),
('Crecimiento del consumo', 'Porcentaje anual', 2),
('Consumo como porcentaje del PIB', 'Porcentaje del PIB', 2)
GO

-- Registrar los años del proyecto
INSERT INTO Periodos (Anio)
VALUES
(2000),(2001),(2002),(2003),(2004),(2005),(2006),(2007),(2008),(2009),(2010),(2011),(2012),
(2013),(2014),(2015),(2016),(2017),(2018),(2019),(2020),(2021),(2022),(2023),(2024)
GO


SELECT * FROM Fuentes

SELECT * FROM Indicadores

select * from Valores

SELECT * FROM Periodos
ORDER BY Anio

SELECT
    IdPeriodo,
    IdIndicador,
    Valor
FROM Valores
ORDER BY
    IdPeriodo,
    IdIndicador