
CREATE TYPE LANGUAGE AS ENUM ('SV', 'EN');

CREATE TABLE IF NOT EXISTS leaflets (
    leaflet_id INT PRIMARY KEY,
    language LANGUAGE,
    text TEXT
);

CREATE TABLE IF NOT EXISTS products (
    ean VARCHAR(14) PRIMARY KEY,
    npl VARCHAR(14) NOT NULL UNIQUE,
    leaflet_id INT REFERENCES LEAFLETS,
    name VARCHAR(64) 
);




INSERT INTO leaflets (leaflet_id, language, text) VALUES (1, 'SV', 'X');
INSERT INTO leaflets (leaflet_id, language, text) VALUES (2, 'SV', 'Y');


INSERT INTO products (ean, npl, name, leaflet_id) VALUES ('07046260070127', '20010601000082', 'Alvedon®', 1);
INSERT INTO products (ean, npl, name, leaflet_id) VALUES ('07350099990328', '20170809000076', 'Magnesium EQL Pharma', 2);



