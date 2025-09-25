-- Script de migración de RegMed SQLite a SQL Server (Estructura Corregida)
-- Generado el: 2025-09-24 10:51:18.643717

-- Usar la base de datos existente Jomquer
USE Jomquer;
GO

-- Crear estructura de tablas basada en SQLite real

-- Tabla users
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(255) UNIQUE NOT NULL,
    hash NVARCHAR(MAX) NOT NULL,
    rol NVARCHAR(50) NOT NULL
);
GO

-- Tabla Pacientes (estructura completa)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pacientes' AND xtype='U')
CREATE TABLE Pacientes (
    usersId INT PRIMARY KEY,
    Usuario NVARCHAR(255),
    Contrasena NVARCHAR(255),
    NombreCompleto NVARCHAR(255),
    Expediente NVARCHAR(255),
    Nombre NVARCHAR(100),
    PrimerApellido NVARCHAR(100),
    SegundoApellido NVARCHAR(100),
    FechaNacimiento NVARCHAR(50),
    EntidadDeNacimiento NVARCHAR(10),
    SexoCURP INT,
    SexoBiologico INT,
    Genero NVARCHAR(50),
    CURP NVARCHAR(18),
    EstadoMental NVARCHAR(255),
    GrupoRH NVARCHAR(10),
    DiagnosticoPrimario NVARCHAR(255),
    CIEPrimario NVARCHAR(50),
    SegundoDiagnostico NVARCHAR(255),
    SegundoCIE NVARCHAR(50),
    TercerDiagnostico NVARCHAR(255),
    TercerCIE NVARCHAR(50),
    Domicilio NVARCHAR(500),
    eMailPaciente NVARCHAR(255),
    TelefonoPaciente NVARCHAR(20),
    WhatsAppPaciente NVARCHAR(20),
    NombreContactoTutor NVARCHAR(255),
    ParentescoContactoTutor NVARCHAR(100),
    TelefonoContactoTutor NVARCHAR(20),
    WhatsAppContactoTutor NVARCHAR(20),
    PrimerContacto INT,
    PacienteActivo INT DEFAULT 1,
    FechaUltimoMovimiento NVARCHAR(50),
    Alergico INT DEFAULT 0,
    RiesgoCaidas INT DEFAULT 0,
    RiesgoUlceras INT DEFAULT 0,
    FOREIGN KEY (usersId) REFERENCES users (id)
);
GO

-- Tabla sintomas (estructura real)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sintomas' AND xtype='U')
CREATE TABLE sintomas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date NVARCHAR(50),
    users_id INT,
    tipo NVARCHAR(MAX),
    duracion NVARCHAR(255),
    intensidad NVARCHAR(255),
    descripcion NVARCHAR(MAX),
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

-- Tabla eventos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='eventos' AND xtype='U')
CREATE TABLE eventos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date NVARCHAR(50),
    users_id INT,
    tipo INT,
    evento NVARCHAR(MAX),
    type INT,
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

-- Tabla planes_de_cuidados (estructura completa)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='planes_de_cuidados' AND xtype='U')
CREATE TABLE planes_de_cuidados (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    riesgo_caidas NVARCHAR(MAX),
    estado_mental NVARCHAR(MAX),
    riesgo_ulceras NVARCHAR(MAX),
    riesgo_pie_diabetico NVARCHAR(MAX),
    heridas NVARCHAR(MAX),
    estomas NVARCHAR(MAX),
    aseo NVARCHAR(MAX),
    medidas_posturales NVARCHAR(MAX),
    balance_liquidos NVARCHAR(MAX),
    dispositivos NVARCHAR(MAX),
    cuidados_via_aerea NVARCHAR(MAX),
    status NVARCHAR(50) DEFAULT 'Activo',
    comentarios NVARCHAR(MAX),
    dieta NVARCHAR(MAX),
    rehabilitacion NVARCHAR(MAX),
    alergico NVARCHAR(MAX),
    detecciones NVARCHAR(MAX),
    acciones NVARCHAR(MAX),
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

-- Tabla somatometria
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='somatometria' AND xtype='U')
CREATE TABLE somatometria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fecha NVARCHAR(50),
    peso FLOAT,
    talla FLOAT,
    imc FLOAT,
    circ_abdominal FLOAT,
    temp FLOAT,
    sistolica INT,
    diastolica INT,
    fcard INT,
    fresp INT,
    o2 INT,
    glucemia FLOAT,
    users_id INT,
    registrado_por INT,
    FOREIGN KEY (users_id) REFERENCES users (id),
    FOREIGN KEY (registrado_por) REFERENCES users (id)
);
GO

-- Tabla documentos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='documentos' AND xtype='U')
CREATE TABLE documentos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    tipo NVARCHAR(255),
    tema NVARCHAR(255),
    comentarios NVARCHAR(MAX),
    filename NVARCHAR(255),
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

-- Tabla prescripciones
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='prescripciones' AND xtype='U')
CREATE TABLE prescripciones (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    medicamento NVARCHAR(255),
    dosis NVARCHAR(100),
    cantidad NVARCHAR(100),
    via NVARCHAR(100),
    cada_cantidad NVARCHAR(100),
    cada_unidad NVARCHAR(100),
    unidad_medida NVARCHAR(100),
    desde NVARCHAR(50),
    durante_cantidad NVARCHAR(100),
    durante_unidad NVARCHAR(100),
    observaciones NVARCHAR(MAX),
    vigente NVARCHAR(10) DEFAULT 'Si',
    FOREIGN KEY (users_id) REFERENCES users (id)
);
GO

-- Insertar datos

-- Datos de tabla users
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (1, N'Mauricio', N'scrypt:32768:8:1$6AwRPhLn1SpbQ3dD$4c885d8c7ae94b2b310caae936bb1ee9b59c7a986af880f16290ade7807caae3d4d78a603632780d1893061ebea0a21c2c68c9ecae59efe5fee6ad6605ee440d', N'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (2, N'Enfermera', N'scrypt:32768:8:1$CNwynecym7G6jBjz$2e3a954c16e665f1b72595e0a0b3e18f3f7183ab22596187c69c65dde0bc8ed12b0c230b9d7fbc04601b1cda8e4ec25f3e8ae433eead85011b712c6e159ef2a3', N'enfermeria');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (3, N'Super', N'scrypt:32768:8:1$K1PZ0ErJp4RQbGnL$86dc00d05579742b3689a29226204ab03f301f00740594d5abfc93eb33b45e02587574905255161671b1aac22b66c829c24727e0f12dd5059b51db4cc07ac794', N'supervisor');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (4, N'Super2', N'scrypt:32768:8:1$fj7Z2uVPXA3Ot3Bk$7bad6e9cdd56a7d6a17572b1038a972943b097f5768a55a8b46be507b804a587a3ba8a7f2e33fd4dfdbafe3689932aa9542dc636c6f0b50c9742a07a7b5a890d', N'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (5, N'Mau', N'scrypt:32768:8:1$3zLjtIErDCZvumq0$e55d93810582a8a1d58e30d9c5adae07e3b6a8c065c6bb462fcb126dac67f912f60acd5724a05c3871d68b373bd4e4216c14d755e90bdd813c290de673c25289', N'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (6, N'Joe', N'scrypt:32768:8:1$GnHfNzD9nLhLfTTQ$19fbefcf6e09a65b4881a9fe4c2c09f14a68e044fb1dd95b5f85e59669474d0890ffa1ba253dfe144db98c752d10aacbf8a58271afc5c15ff2eed5e728eabc47', N'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (7, N'Juan', N'scrypt:32768:8:1$Ae1T9seiYjUzIdrz$bf6a0fd7014bca24a4cfbdebe7eb6f2752b5b2be643f3ba544dc68fcf36af79cd5fc5b0184bdd1c28e7e26340fd3c0b55734dd36138971067bb33f8dacc63391', N'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (8, N'R2D1', N'scrypt:32768:8:1$XMkzhu73Vou8gXyc$68bcbd575ea99d03d325bb124037cbb0d16ab3325555e461803407e01526021e04628774961f2fee1dff215a1627aa88de2753155bd7df91ac8334c7629bb706', N'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (9, N'John', N'scrypt:32768:8:1$7kgQkNdGhmbmOwql$1e95c3c38d48485f6823843b913d03e202d0cba40c2773d37456c131f7a5ee90d7fcb1b7ab972c630c2e2185fe6f48ddb9d09587d21b4ccda9f674d0e31ad93b', N'paciente');
SET IDENTITY_INSERT users OFF;
-- Fin datos users


-- Datos de tabla Pacientes
INSERT INTO Pacientes (usersId, Usuario, Contrasena, NombreCompleto, Expediente, Nombre, PrimerApellido, SegundoApellido, FechaNacimiento, EntidadDeNacimiento, SexoCURP, SexoBiologico, Genero, CURP, EstadoMental, GrupoRH, DiagnosticoPrimario, CIEPrimario, SegundoDiagnostico, SegundoCIE, TercerDiagnostico, TercerCIE, Domicilio, eMailPaciente, TelefonoPaciente, WhatsAppPaciente, NombreContactoTutor, ParentescoContactoTutor, TelefonoContactoTutor, WhatsAppContactoTutor, PrimerContacto, PacienteActivo, FechaUltimoMovimiento, Alergico, RiesgoCaidas, RiesgoUlceras) VALUES (1, NULL, NULL, N'Mauricio Derbez Derbez', NULL, N'Mauricio', N'Derbez', N'Derbez', N'1959-03-15', N'DF', NULL, 1, N'MASCULINO', N'DEPM590315HDFRNR04', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, N'', N'mauricio.derbez@gmail.com', N'9999007732', N'', NULL, NULL, NULL, NULL, NULL, 1, N'2025-09-11T13:32', 0, 1, 1);
INSERT INTO Pacientes (usersId, Usuario, Contrasena, NombreCompleto, Expediente, Nombre, PrimerApellido, SegundoApellido, FechaNacimiento, EntidadDeNacimiento, SexoCURP, SexoBiologico, Genero, CURP, EstadoMental, GrupoRH, DiagnosticoPrimario, CIEPrimario, SegundoDiagnostico, SegundoCIE, TercerDiagnostico, TercerCIE, Domicilio, eMailPaciente, TelefonoPaciente, WhatsAppPaciente, NombreContactoTutor, ParentescoContactoTutor, TelefonoContactoTutor, WhatsAppContactoTutor, PrimerContacto, PacienteActivo, FechaUltimoMovimiento, Alergico, RiesgoCaidas, RiesgoUlceras) VALUES (8, NULL, NULL, N'Ramiro Perz Duarte', NULL, N'Ramiro', N'Perz', N'Duarte', N'1998-09-15', NULL, NULL, 1, N'MASCULINO', N'', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, N'', N'', N'', N'', NULL, NULL, NULL, NULL, 1, 1, N'2025-09-18T19:21', 0, 0, 0);
INSERT INTO Pacientes (usersId, Usuario, Contrasena, NombreCompleto, Expediente, Nombre, PrimerApellido, SegundoApellido, FechaNacimiento, EntidadDeNacimiento, SexoCURP, SexoBiologico, Genero, CURP, EstadoMental, GrupoRH, DiagnosticoPrimario, CIEPrimario, SegundoDiagnostico, SegundoCIE, TercerDiagnostico, TercerCIE, Domicilio, eMailPaciente, TelefonoPaciente, WhatsAppPaciente, NombreContactoTutor, ParentescoContactoTutor, TelefonoContactoTutor, WhatsAppContactoTutor, PrimerContacto, PacienteActivo, FechaUltimoMovimiento, Alergico, RiesgoCaidas, RiesgoUlceras) VALUES (9, NULL, NULL, N'John F. Doe Ramirez', NULL, N'John F.', N'Doe', N'Ramirez', N'1965-06-15', NULL, NULL, 1, N'MASCULINO', N'', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, N'Parroquia 310, Col del Valle, Cd. México, 02020', N'pleboty@gmail.com', N'5578341813', N'5578341813', NULL, NULL, NULL, NULL, 1, 1, N'2025-09-20T09:43', 0, 0, 0);
-- Fin datos Pacientes


-- Datos de tabla sintomas
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES (N'2025-09-10 14:24:24.623034', 1, N'Neurológico: Dolor de cabeza, mareos, convulsiones, hormigueo, pérdida de fuerza, alteraciones de la memoria', N'1 minuto', N'Leve: Puede realizar actividades habituales.', N'Se me durmio la pierna a la hora de la comida');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES (N'2025-09-10 14:53:10.565926', 1, N'Neurológico: Dolor de cabeza, mareos, convulsiones, hormigueo, pérdida de fuerza, alteraciones de la memoria', N'1 minuto', N'Leve: Puede realizar actividades habituales.', N'Se me durmio la rodilla en el cine');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES (N'2025-09-10 20:46:05.181055', 1, N'Dolor de cabeza', N'media hora', N'Leve', N'dolor agudo en la nuca');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES (N'2025-09-10 21:44:43.422413', 1, N'Náusea', N'media hora', N'Leve', N'despues de andar en barco');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES (N'2025-09-11 19:29:19.351369', 1, N'Dolor de cabeza', N'1 minuto', N'Leve', N'das dsafsdf');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES (N'2025-09-18 12:08:49.798281', 6, N'Tos', NULL, NULL, N'Etuve tosiendo mucho . Empezo sin motivo y termino cuando tome agua.');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES (N'2025-09-20 09:45:57.660279', 9, N'Mareos', NULL, NULL, N'Desperté muy mareado. Tardé 20 minutos en poder pararme.');
-- Fin datos sintomas


-- Datos de tabla eventos
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES (N'2025-09-10 20:19:35.966592', 1, 1, N'Fui a la Farmacia de Similares y me recetaros paracetamol 10 mg por 3 dias', 1);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES (N'2025-09-10 20:19:57.158433', 1, 2, N'Autorización para mauricio.derbez@gmail.com', 0);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES (N'2025-09-10 21:45:06.087593', 1, 1, N'Estrés postraumático: xbxcbx', 1);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES (N'2025-09-18T12:35', 6, 1, N'Accidente de tránsito: Me atroppelló una señora con su bibicleta', 0);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES (N'2025-09-20T09:46', 9, 1, N'Enfermedad aguda: Rinitis. Durante el desayuno, me da rinitis', 0);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES (N'2025-09-20 09:50:11.755632', 9, 2, N'Autorización para mderbez@outlook.com', 0);
-- Fin datos eventos


-- Datos de tabla planes_de_cuidados
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, N'2025-09-11 19:51', N'', N'Alerta', N'', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, N'Baja', N'', NULL, NULL, NULL, N'Semanalmente aplicar escala Norton (úlceras por presión)', N'Temperatura 3 veces al dia, atender prescripciones, cambiar gasas en las mañanas');
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, N'2025-09-12 11:24', N'0', N'', N'0', N'', N'', N'', N'', N'', N'', N'', N'', N'Baja', N'\nSupervisor: Revisar, todo aparece sin valores', NULL, NULL, NULL, NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, N'2025-09-12 11:27', N'1', N'', N'1', N'', N'', N'', N'', N'', N'', N'', N'', N'Baja', N'\nSupervisor: revisar temperatura', NULL, NULL, NULL, NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, N'2025-09-12 11:58', N'1', N'estado mental', N'1', N'pie diabetico', N'heridas', N'estomas', N'aseo', N'postura', N'balance', N'dispositivos', N'via aérea', N'Aprobado', N'', NULL, NULL, NULL, NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, N'2025-09-15 11:01', N'1', N'Alerta', N'1', N'0', N'Moretones en cara producto de una caida nocturna', N'Ninguno', N'Por cuenta propia', N'Cambiar cada 2 horas de lugar', N'Normal', N'Sin dispositivos', N'Ejercicios con pelota', N'Aprobado', N'\nSupervisor: Revisar ultimos 4 datos\nEnfermera: \nSupervisor: Siguen sin datos\nSupervisor: nuevo comentario\nEnfermera: Nuevo intento\r\n\nSupervisor: va de nuevo\nEnfermera: ya esta\nSupervisor: 1revisar dispositivos médicos\nSupervisor: 1revisar dispositivos médicos', NULL, NULL, N'1', NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, N'2025-09-15 17:58', N'1', N'', N'1', N'0', N'', N'estomas', N'', N'', N'', N'', N'', N'Baja', N'revisar', NULL, NULL, NULL, NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, N'2025-09-17 18:26', N'1', N'Alerta', N'1', N'Si', N'Moretones en cara producto de una caida nocturna', N'estomas', N'Por cuenta propia', N'Cambiar cada 2 horas de lugar', N'normal', N'Ninguno', N'Sin problemas ', N'Aprobado', N'', NULL, NULL, NULL, N'Mensualmente UPP', N'Nuevo plan: toma de temperatura cada 6 horas, aplicar ');
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (9, N'2025-09-20 11:26', N'1', N'Alerta', N'1', N'Sí', N'Moretones en cara producto de una caida nocturna', N'Post-operación', N'Por cuenta propia', N'Cambiar de postura cada hora , sesiones de media hora sentado y media hora acostado durante 3 horas', N'1 litro de suero intravenoso cada 12 horas', N'Ninguno', N'Ejercicios con pelota', N'Aprobado', N'', NULL, NULL, NULL, N'Revisión semanal de riesgo de úlceras por presión', N'Toma de temperatura cada 8 horas, Toma de presión arterial en las mañanas Después de la operación, revisar estomas en cada cambio de turno');
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (9, N'2025-09-20 13:10', N'1', N'Alerta', N'1', N'Si', N'No', N'No', N'Por cuenta propia', N'Cambiar de postura cada hora , sesiones de media hora sentado y media hora acostado durante 3 horas', N'1 litro de suero intravenoso cada 12 horas', N'Sin dispositivos', N'Sin problemas reportados', N'Pendiente de revisión', N'', NULL, NULL, NULL, N'Revisar riesgo de ulceras por presión', N'Somatometria: 3 veces al dia.  Revisión y si procede, cambio de vendas postoperacion cada cambio de turno');
-- Fin datos planes_de_cuidados


-- Datos de tabla somatometria
INSERT INTO somatometria (fecha, peso, talla, imc, circ_abdominal, temp, sistolica, diastolica, fcard, fresp, o2, glucemia, users_id, registrado_por) VALUES (N'2025-09-19T11:43', 78.5, 177.0, NULL, N'', 37.9, 70, N'', N'', N'', 92, N'', 1, 1);
INSERT INTO somatometria (fecha, peso, talla, imc, circ_abdominal, temp, sistolica, diastolica, fcard, fresp, o2, glucemia, users_id, registrado_por) VALUES (N'2025-09-19T11:44', 77.0, 175.0, NULL, N'', 38.4, 60, 50, 120, 12, 92, N'', 1, 2);
INSERT INTO somatometria (fecha, peso, talla, imc, circ_abdominal, temp, sistolica, diastolica, fcard, fresp, o2, glucemia, users_id, registrado_por) VALUES (N'2025-09-20T09:48', 78.5, 177.0, NULL, 90.0, 38.2, 70, 60, 66, N'', 92, 120.0, 9, 9);
-- Fin datos somatometria


-- Datos de tabla documentos
INSERT INTO documentos (users_id, fecha, tipo, tema, comentarios, filename) VALUES (9, N'2025-09-20 10:34', N'Laboratorio - Sangre', N'Estudios de laboratorio por altos niveles de ácido úrico', N'Todo en rangos', N'Laboratorio___Salud_Digna.pdf');
-- Fin datos documentos


-- Datos de tabla prescripciones
INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, observaciones, vigente) VALUES (2, N'Espaven', N'5 mg', N'1', N'oral', N'6', N'horas', N'tabletas', N'20-09-2025', N'1', N'dias', NULL, N'Si');
INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, observaciones, vigente) VALUES (2, N'Espaven', N'7 mg', N'2', N'oral', N'2', N'horas', N'tabletas', N'20-09-2025', N'2', N'dias', NULL, N'Si');
INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, observaciones, vigente) VALUES (9, N'Espaven', N'7 mg', N'2', N'oral', N'6', N'horas', N'tabletas', N'20-09-2025', N'30', N'dias', NULL, N'Si');
INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, observaciones, vigente) VALUES (9, N'Aspirina', N'5 mg', N'1', N'oral', N'1', N'horas', N'tabletas', N'20-09-2025', N'12', N'dias', NULL, N'Si');
-- Fin datos prescripciones


GO
-- Migración completada