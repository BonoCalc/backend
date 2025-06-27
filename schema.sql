-- schema.sql
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    correo VARCHAR(255) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    nombre VARCHAR(255),
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE configuracion (
    usuario_id INT PRIMARY KEY REFERENCES usuario(id),
    moneda_default VARCHAR(10),
    tipo_tasa_default VARCHAR(20),
    capitalizacion_default VARCHAR(10)
);

CREATE TABLE bono (
    id SERIAL PRIMARY KEY,
    valor_nominal BIGINT NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    frecuencia_pago VARCHAR NOT NULL,
    tipo_tasa VARCHAR,
    valor_tasa INT NOT NULL,
    capitalizacion INT,
    dias_base INT,
    prima_redencion INT,
    gracia_total_inicio INT,
    gracia_total_fin INT,
    gracia_parcial_inicio INT,
    gracia_parcial_fin INT,
    created_at DATE DEFAULT CURRENT_DATE,
    updated_at DATE DEFAULT CURRENT_DATE,
    usuario_id INT REFERENCES usuario(id)
);

CREATE TABLE flujos_caja (
    id SERIAL PRIMARY KEY,
    numero_cuota INT,
    fecha DATE,
    amortizacion INT,
    interes INT,
    cuota INT,
    saldo INT,
    bono_id INT REFERENCES bono(id)
);

CREATE TABLE valoraciones (
    id SERIAL PRIMARY KEY,
    fecha_valoracion DATE DEFAULT CURRENT_DATE,
    tcea FLOAT,
    trea FLOAT,
    duracion FLOAT,
    duracion_modificada FLOAT,
    convexidad FLOAT,
    precio_maximo FLOAT,
    origen_valoracion VARCHAR(10),
    valor_base FLOAT,
    precio_calculado FLOAT,
    tir_calculada FLOAT,
    bono_id INT REFERENCES bono(id)
);


