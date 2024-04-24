CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    phone TEXT NOT NULL,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Email (para loguear)
Contraseña (hasheada)
Nombre
Apellido
Dirección de entrega (Campos: Calle/Avenida, Número, Piso / Departamento (Opcional), Localidad o Barrio, Provincia, Código Postal)
Última fecha de inicio de sesión (dato interno, nos puede servir para saber qué usuarios están más activos que otros. Es algo que se me acaba de ocurrir)
Teléfono de Contacto

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    wine TEXT NOT NULL,
    store TEXT NOT NULL,
    year TEXT NOT NULL,
    variety TEXT NOT NULL,
    origin TEXT NOT NULL,
    presentation TEXT NOT NULL
);

CREATE TABLE stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    product_id INT NOT NULL,
    stock INT NOT NULL,
    reserved INT NOT NULL,
    left INT NOT NULL,
    percentage TEXT NOT NULL DEFAULT '100%',
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE newsletter (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    email TEXT NOT NULL
);

INSERT INTO products (wine, store, year, variety, origin, presentation) VALUES ('Saint Felicien Bonarda', 'Catena Zapata', '2018', '100% Bonarda', 'El Mirador, Mendoza, Argentina', 'Botella de 750 ml en caja cerrada de 4 unidades');
INSERT INTO stock (product_id, stock, reserved, left) VALUES (1, 10, 0, 10);
