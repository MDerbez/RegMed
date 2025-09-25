-- Script de migración de RegMed SQLite a SQL Server
-- Generado el: 2025-09-24 10:32:13.823911

-- Crear estructura de tablas
-- Tabla users
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(255) UNIQUE NOT NULL,
    hash NVARCHAR(255) NOT NULL,
    rol NVARCHAR(50) NOT NULL
);

-- Tabla Pacientes
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pacientes' AND xtype='U')
CREATE TABLE Pacientes (
    UsersId INT PRIMARY KEY,
    NombreCompleto NVARCHAR(255),
    Nombre NVARCHAR(100),
    PrimerApellido NVARCHAR(100),
    SegundoApellido NVARCHAR(100),
    FechaNacimiento NVARCHAR(50),
    EntidadDeNacimiento NVARCHAR(10),
    SexoBiologico NVARCHAR(50),
    Genero NVARCHAR(50),
    CURP NVARCHAR(18),
    Domicilio NVARCHAR(500),
    eMailPaciente NVARCHAR(255),
    TelefonoPaciente NVARCHAR(20),
    WhatsAppPaciente NVARCHAR(20),
    PacienteActivo INT DEFAULT 1,
    FechaUltimoMovimiento NVARCHAR(50),
    FOREIGN KEY (UsersId) REFERENCES users (id)
);

-- Tabla planes_de_cuidados
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='planes_de_cuidados' AND xtype='U')
CREATE TABLE planes_de_cuidados (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    acciones NVARCHAR(MAX),
    detecciones NVARCHAR(MAX),
    estado_mental NVARCHAR(MAX),
    riesgo_caidas NVARCHAR(MAX),
    riesgo_ulceras NVARCHAR(MAX),
    riesgo_pie_diabetico NVARCHAR(MAX),
    heridas NVARCHAR(MAX),
    estomas NVARCHAR(MAX),
    aseo NVARCHAR(MAX),
    medidas_posturales NVARCHAR(MAX),
    balance_liquidos NVARCHAR(MAX),
    dispositivos NVARCHAR(MAX),
    cuidados_via_aerea NVARCHAR(MAX),
    comentarios NVARCHAR(MAX),
    status NVARCHAR(50) DEFAULT 'Activo',
    FOREIGN KEY (users_id) REFERENCES users (id)
);

-- Tabla sintomas
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sintomas' AND xtype='U')
CREATE TABLE sintomas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date NVARCHAR(50),
    users_id INT,
    tipo NVARCHAR(100),
    descripcion NVARCHAR(MAX),
    FOREIGN KEY (users_id) REFERENCES users (id)
);

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

-- Tabla somatometria
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='somatometria' AND xtype='U')
CREATE TABLE somatometria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    peso FLOAT,
    talla FLOAT,
    circ_abdominal FLOAT,
    temp FLOAT,
    sistolica INT,
    diastolica INT,
    fcard INT,
    fresp INT,
    o2 FLOAT,
    glucemia FLOAT,
    registrado_por INT,
    FOREIGN KEY (users_id) REFERENCES users (id),
    FOREIGN KEY (registrado_por) REFERENCES users (id)
);

-- Tabla documentos
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='documentos' AND xtype='U')
CREATE TABLE documentos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    users_id INT,
    fecha NVARCHAR(50),
    tema NVARCHAR(255),
    tipo NVARCHAR(100),
    comentarios NVARCHAR(MAX),
    filename NVARCHAR(255),
    FOREIGN KEY (users_id) REFERENCES users (id)
);

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
    vigente NVARCHAR(10) DEFAULT 'Si',
    FOREIGN KEY (users_id) REFERENCES users (id)
);

-- Insertar datos

-- Datos de tabla users
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (1, 'Mauricio', 'scrypt:32768:8:1$6AwRPhLn1SpbQ3dD$4c885d8c7ae94b2b310caae936bb1ee9b59c7a986af880f16290ade7807caae3d4d78a603632780d1893061ebea0a21c2c68c9ecae59efe5fee6ad6605ee440d', 'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (2, 'Enfermera', 'scrypt:32768:8:1$CNwynecym7G6jBjz$2e3a954c16e665f1b72595e0a0b3e18f3f7183ab22596187c69c65dde0bc8ed12b0c230b9d7fbc04601b1cda8e4ec25f3e8ae433eead85011b712c6e159ef2a3', 'enfermeria');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (3, 'Super', 'scrypt:32768:8:1$K1PZ0ErJp4RQbGnL$86dc00d05579742b3689a29226204ab03f301f00740594d5abfc93eb33b45e02587574905255161671b1aac22b66c829c24727e0f12dd5059b51db4cc07ac794', 'supervisor');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (4, 'Super2', 'scrypt:32768:8:1$fj7Z2uVPXA3Ot3Bk$7bad6e9cdd56a7d6a17572b1038a972943b097f5768a55a8b46be507b804a587a3ba8a7f2e33fd4dfdbafe3689932aa9542dc636c6f0b50c9742a07a7b5a890d', 'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (5, 'Mau', 'scrypt:32768:8:1$3zLjtIErDCZvumq0$e55d93810582a8a1d58e30d9c5adae07e3b6a8c065c6bb462fcb126dac67f912f60acd5724a05c3871d68b373bd4e4216c14d755e90bdd813c290de673c25289', 'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (6, 'Joe', 'scrypt:32768:8:1$GnHfNzD9nLhLfTTQ$19fbefcf6e09a65b4881a9fe4c2c09f14a68e044fb1dd95b5f85e59669474d0890ffa1ba253dfe144db98c752d10aacbf8a58271afc5c15ff2eed5e728eabc47', 'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (7, 'Juan', 'scrypt:32768:8:1$Ae1T9seiYjUzIdrz$bf6a0fd7014bca24a4cfbdebe7eb6f2752b5b2be643f3ba544dc68fcf36af79cd5fc5b0184bdd1c28e7e26340fd3c0b55734dd36138971067bb33f8dacc63391', 'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (8, 'R2D1', 'scrypt:32768:8:1$XMkzhu73Vou8gXyc$68bcbd575ea99d03d325bb124037cbb0d16ab3325555e461803407e01526021e04628774961f2fee1dff215a1627aa88de2753155bd7df91ac8334c7629bb706', 'paciente');
SET IDENTITY_INSERT users OFF;
SET IDENTITY_INSERT users ON;
INSERT INTO users (id, username, hash, rol) VALUES (9, 'John', 'scrypt:32768:8:1$7kgQkNdGhmbmOwql$1e95c3c38d48485f6823843b913d03e202d0cba40c2773d37456c131f7a5ee90d7fcb1b7ab972c630c2e2185fe6f48ddb9d09587d21b4ccda9f674d0e31ad93b', 'paciente');
SET IDENTITY_INSERT users OFF;
-- Fin datos users


-- Datos de tabla Pacientes
INSERT INTO Pacientes (usersId, Usuario, Contrasena, NombreCompleto, Expediente, Nombre, PrimerApellido, SegundoApellido, FechaNacimiento, EntidadDeNacimiento, SexoCURP, SexoBiologico, Genero, CURP, EstadoMental, GrupoRH, DiagnosticoPrimario, CIEPrimario, SegundoDiagnostico, SegundoCIE, TercerDiagnostico, TercerCIE, Domicilio, eMailPaciente, TelefonoPaciente, WhatsAppPaciente, NombreContactoTutor, ParentescoContactoTutor, TelefonoContactoTutor, WhatsAppContactoTutor, PrimerContacto, PacienteActivo, FechaUltimoMovimiento, Alergico, RiesgoCaidas, RiesgoUlceras) VALUES (1, NULL, NULL, 'Mauricio Derbez Derbez', NULL, 'Mauricio', 'Derbez', 'Derbez', '1959-03-15', 'DF', NULL, 1, 'MASCULINO', 'DEPM590315HDFRNR04', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', 'mauricio.derbez@gmail.com', '9999007732', '', NULL, NULL, NULL, NULL, NULL, 1, '2025-09-11T13:32', 0, 1, 1);
INSERT INTO Pacientes (usersId, Usuario, Contrasena, NombreCompleto, Expediente, Nombre, PrimerApellido, SegundoApellido, FechaNacimiento, EntidadDeNacimiento, SexoCURP, SexoBiologico, Genero, CURP, EstadoMental, GrupoRH, DiagnosticoPrimario, CIEPrimario, SegundoDiagnostico, SegundoCIE, TercerDiagnostico, TercerCIE, Domicilio, eMailPaciente, TelefonoPaciente, WhatsAppPaciente, NombreContactoTutor, ParentescoContactoTutor, TelefonoContactoTutor, WhatsAppContactoTutor, PrimerContacto, PacienteActivo, FechaUltimoMovimiento, Alergico, RiesgoCaidas, RiesgoUlceras) VALUES (8, NULL, NULL, 'Ramiro Perz Duarte', NULL, 'Ramiro', 'Perz', 'Duarte', '1998-09-15', NULL, NULL, 1, 'MASCULINO', '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', '', '', '', NULL, NULL, NULL, NULL, 1, 1, '2025-09-18T19:21', 0, 0, 0);
INSERT INTO Pacientes (usersId, Usuario, Contrasena, NombreCompleto, Expediente, Nombre, PrimerApellido, SegundoApellido, FechaNacimiento, EntidadDeNacimiento, SexoCURP, SexoBiologico, Genero, CURP, EstadoMental, GrupoRH, DiagnosticoPrimario, CIEPrimario, SegundoDiagnostico, SegundoCIE, TercerDiagnostico, TercerCIE, Domicilio, eMailPaciente, TelefonoPaciente, WhatsAppPaciente, NombreContactoTutor, ParentescoContactoTutor, TelefonoContactoTutor, WhatsAppContactoTutor, PrimerContacto, PacienteActivo, FechaUltimoMovimiento, Alergico, RiesgoCaidas, RiesgoUlceras) VALUES (9, NULL, NULL, 'John F. Doe Ramirez', NULL, 'John F.', 'Doe', 'Ramirez', '1965-06-15', NULL, NULL, 1, 'MASCULINO', '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Parroquia 310, Col del Valle, Cd. México, 02020', 'pleboty@gmail.com', '5578341813', '5578341813', NULL, NULL, NULL, NULL, 1, 1, '2025-09-20T09:43', 0, 0, 0);
-- Fin datos Pacientes


-- Datos de tabla planes_de_cuidados
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, '2025-09-11 19:51', '', 'Alerta', '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'Baja', '', NULL, NULL, NULL, 'Semanalmente aplicar escala Norton (úlceras por presión)', 'Temperatura 3 veces al dia, atender prescripciones, cambiar gasas en las mañanas');
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, '2025-09-12 11:24', '0', '', '0', '', '', '', '', '', '', '', '', 'Baja', '
Supervisor: Revisar, todo aparece sin valores', NULL, NULL, NULL, NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, '2025-09-12 11:27', '1', '', '1', '', '', '', '', '', '', '', '', 'Baja', '
Supervisor: revisar temperatura', NULL, NULL, NULL, NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, '2025-09-12 11:58', '1', 'estado mental', '1', 'pie diabetico', 'heridas', 'estomas', 'aseo', 'postura', 'balance', 'dispositivos', 'via aérea', 'Aprobado', '', NULL, NULL, NULL, NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, '2025-09-15 11:01', '1', 'Alerta', '1', '0', 'Moretones en cara producto de una caida nocturna', 'Ninguno', 'Por cuenta propia', 'Cambiar cada 2 horas de lugar', 'Normal', 'Sin dispositivos', 'Ejercicios con pelota', 'Aprobado', '
Supervisor: Revisar ultimos 4 datos
Enfermera: 
Supervisor: Siguen sin datos
Supervisor: nuevo comentario
Enfermera: Nuevo intento

Supervisor: va de nuevo
Enfermera: ya esta
Supervisor: 1revisar dispositivos médicos
Supervisor: 1revisar dispositivos médicos', NULL, NULL, '1', NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, '2025-09-15 17:58', '1', '', '1', '0', '', 'estomas', '', '', '', '', '', 'Baja', 'revisar', NULL, NULL, NULL, NULL, NULL);
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (1, '2025-09-17 18:26', '1', 'Alerta', '1', 'Si', 'Moretones en cara producto de una caida nocturna', 'estomas', 'Por cuenta propia', 'Cambiar cada 2 horas de lugar', 'normal', 'Ninguno', 'Sin problemas ', 'Aprobado', '', NULL, NULL, NULL, 'Mensualmente UPP', 'Nuevo plan: toma de temperatura cada 6 horas, aplicar ');
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (9, '2025-09-20 11:26', '1', 'Alerta', '1', 'Sí', 'Moretones en cara producto de una caida nocturna', 'Post-operación', 'Por cuenta propia', 'Cambiar de postura cada hora , sesiones de media hora sentado y media hora acostado durante 3 horas', '1 litro de suero intravenoso cada 12 horas', 'Ninguno', 'Ejercicios con pelota', 'Aprobado', '', NULL, NULL, NULL, 'Revisión semanal de riesgo de úlceras por presión', 'Toma de temperatura cada 8 horas, Toma de presión arterial en las mañanas Después de la operación, revisar estomas en cada cambio de turno');
INSERT INTO planes_de_cuidados (users_id, fecha, riesgo_caidas, estado_mental, riesgo_ulceras, riesgo_pie_diabetico, heridas, estomas, aseo, medidas_posturales, balance_liquidos, dispositivos, cuidados_via_aerea, status, comentarios, dieta, rehabilitacion, alergico, detecciones, acciones) VALUES (9, '2025-09-20 13:10', '1', 'Alerta', '1', 'Si', 'No', 'No', 'Por cuenta propia', 'Cambiar de postura cada hora , sesiones de media hora sentado y media hora acostado durante 3 horas', '1 litro de suero intravenoso cada 12 horas', 'Sin dispositivos', 'Sin problemas reportados', 'Pendiente de revisión', '', NULL, NULL, NULL, 'Revisar riesgo de ulceras por presión', 'Somatometria: 3 veces al dia.  Revisión y si procede, cambio de vendas postoperacion cada cambio de turno');
-- Fin datos planes_de_cuidados


-- Datos de tabla sintomas
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES ('2025-09-10 14:24:24.623034', 1, 'Neurológico: Dolor de cabeza, mareos, convulsiones, hormigueo, pérdida de fuerza, alteraciones de la memoria', '1 minuto', 'Leve: Puede realizar actividades habituales.', 'Se me durmio la pierna a la hora de la comida');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES ('2025-09-10 14:53:10.565926', 1, 'Neurológico: Dolor de cabeza, mareos, convulsiones, hormigueo, pérdida de fuerza, alteraciones de la memoria', '1 minuto', 'Leve: Puede realizar actividades habituales.', 'Se me durmio la rodilla en el cine');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES ('2025-09-10 20:46:05.181055', 1, 'Dolor de cabeza', 'media hora', 'Leve', 'dolor agudo en la nuca');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES ('2025-09-10 21:44:43.422413', 1, 'Náusea', 'media hora', 'Leve', 'despues de andar en barco');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES ('2025-09-11 19:29:19.351369', 1, 'Dolor de cabeza', '1 minuto', 'Leve', 'das dsafsdf');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES ('2025-09-18 12:08:49.798281', 6, 'Tos', NULL, NULL, 'Etuve tosiendo mucho . Empezo sin motivo y termino cuando tome agua.');
INSERT INTO sintomas (date, users_id, tipo, duracion, intensidad, descripcion) VALUES ('2025-09-20 09:45:57.660279', 9, 'Mareos', NULL, NULL, 'Desperté muy mareado. Tardé 20 minutos en poder pararme.');
-- Fin datos sintomas


-- Datos de tabla eventos
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES ('2025-09-10 20:19:35.966592', 1, 1, 'Fui a la Farmacia de Similares y me recetaros paracetamol 10 mg por 3 dias', 1);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES ('2025-09-10 20:19:57.158433', 1, 2, 'Autorización para mauricio.derbez@gmail.com', 0);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES ('2025-09-10 21:45:06.087593', 1, 'Estrés postraumático', 'xbxcbx', 1);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES ('2025-09-18T12:35', 6, 'Accidente de tránsito', 'Me atroppelló una señora con su bibicleta', 0);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES ('2025-09-20T09:46', 9, 'Enfermedad aguda', 'Rinitis. Durante el desayuno, me da rinitis', 0);
INSERT INTO eventos (date, users_id, tipo, evento, type) VALUES ('2025-09-20 09:50:11.755632', 9, 2, 'Autorización para mderbez@outlook.com', 0);
-- Fin datos eventos


-- Datos de tabla somatometria
INSERT INTO somatometria (fecha, peso, talla, imc, circ_abdominal, temp, sistolica, diastolica, fcard, fresp, o2, glucemia, users_id, registrado_por) VALUES ('2025-09-19T11:43', 78.5, 177.0, NULL, '', 37.9, 70, '', '', '', 92, '', 1, 1);
INSERT INTO somatometria (fecha, peso, talla, imc, circ_abdominal, temp, sistolica, diastolica, fcard, fresp, o2, glucemia, users_id, registrado_por) VALUES ('2025-09-19T11:44', 77.0, 175.0, NULL, '', 38.4, 60, 50, 120, 12, 92, '', 1, 2);
INSERT INTO somatometria (fecha, peso, talla, imc, circ_abdominal, temp, sistolica, diastolica, fcard, fresp, o2, glucemia, users_id, registrado_por) VALUES ('2025-09-20T09:48', 78.5, 177.0, NULL, 90.0, 38.2, 70, 60, 66, '', 92, 120.0, 9, 9);
-- Fin datos somatometria


-- Datos de tabla documentos
INSERT INTO documentos (users_id, fecha, tipo, tema, comentarios, filename) VALUES (9, '2025-09-20 10:34', 'Laboratorio - Sangre', 'Estudios de laboratorio por altos niveles de ácido úrico', 'Todo en rangos', 'Laboratorio___Salud_Digna.pdf');
-- Fin datos documentos


-- Datos de tabla prescripciones
INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, observaciones, vigente) VALUES (2, 'Espaven', '5 mg', '1', 'oral', '6', 'horas', 'tabletas', '20-09-2025', '1', 'dias', NULL, 'Si');
INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, observaciones, vigente) VALUES (2, 'Espaven', '7 mg', '2', 'oral', '2', 'horas', 'tabletas', '20-09-2025', '2', 'dias', NULL, 'Si');
INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, observaciones, vigente) VALUES (9, 'Espaven', '7 mg', '2', 'oral', '6', 'horas', 'tabletas', '20-09-2025', '30', 'dias', NULL, 'Si');
INSERT INTO prescripciones (users_id, medicamento, dosis, cantidad, via, cada_cantidad, cada_unidad, unidad_medida, desde, durante_cantidad, durante_unidad, observaciones, vigente) VALUES (9, 'Aspirina', '5 mg', '1', 'oral', '1', 'horas', 'tabletas', '20-09-2025', '12', 'dias', NULL, 'Si');
-- Fin datos prescripciones

