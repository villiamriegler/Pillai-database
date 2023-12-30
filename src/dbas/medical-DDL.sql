-- First implementation of NPL-database 
-- Some oboiusly irrelevant infromation from NPL is disregarded (may need a second look, to see what is actall irrelevant)
-- Tries to include as much possibly relevant information as possible 

-- All ids are copies from NPL and N:M relations follow from NPL-schema defenitions

-- Not verified for BCNF simply a first outtake for evaluation


CREATE TABLE pharmaceutical_form (
	mpaID: CHAR(6),
	sv_desc: VARCHAR(255),
	en_desc: VARCHAR(255),
	PRIMARY KEY(mpaID)
);

CREATE TABLE route_of_administration (
	mpaID: VARCHAR(4),
	sv_desc: VARCHAR(255),
	en_desc: VARCHAR(255),
	PRIMARY KEY(mpaID)
);

-- not storing adress line 1,2,3 or vat-no
CREATE TABLE organization (
	orgID: CHAR(18),
	name: VARCHAR(255) NOT NULL,
	country: VARCHAR(6) NOT NULL, -- Schema states 1-6 char, every actall record has 3 characters
	PRIMARY KEY(orgID)
);

CREATE TABLE organization_role(
	mpaID: VARCHAR(6),
	sv_role: VARCHAR(255),
	en_role: VARCHAR(255),
	PRIMARY KEY(mpaID)
);

CREATE TABLE product_class(
	mpaID: VARCHAR(3),
	sv_class: VARCHAR(255),
	en_class: VARCHAR(255),
	PRIMARY KEY(mpaID)
);

CREATE TABLE narcotic_class(
	mpaID: VARCHAR(2),
	sv_class: VARCHAR(255),
	en_class: VARCHAR(255),
	PRIMARY KEY(mpaID)
);

CREATE TABLE perscription( -- could be type enum
	mpaID: VARCHAR(1),
	sv_class: VARCHAR(255),
	en_class: VARCHAR(255),
	PRIMARY KEY(mpaID)
);

CREATE TABLE ingredient_role(
	mpaID: VARCHAR(4),
	sv_role: VARCHAR(255),
	en_role: VARCHAR(255),
	PRIMARY KEY (mpaID)
);

-- Does not include approvalnumber, (legalname, Historical name/legalname)
CREATE TABLE medecine (
	nplID: BIGINT,
	name: VARCHAR(255) NOT NULL,
	strength_text: VARCHAR(255),
	pharmaceutical_form: CHAR(6) NOT NULL,	
	product_class: VARCHAR(3) NOT NULL,
	perscription_status: VARCHAR(1) NOT NULL,
	narcotic_class: VARCHAR(2) NOT NULL,
	sale_stopped: BOOLEAN,
	PRIMARY KEY(nplID),
	CONSTRAINT fk_pharmaceutical_form
		FOREGIN KEY(pharmaceutical_form)
			REFERENCES pharmaceutical_form(mpaID),
	CONSTRAINT fk_product_class
		FOREGIN KEY(product_class)
			REFERENCES product_class(mpaID),
	CONSTRAINT fk_perscription_status
		FOREGIN KEY (perscription_status)
			REFERENCES perscription(mpaID),
	CONSTRAINT fk_narcotic_class
		FOREGIN KEY (narcotic_class)
			REFERENCES narcotic_class(mpaID)
); 

CREATE TABLE packages(
	medecineID: BIGINT,
	npl_packID: BIGINT,
	PRIMARY KEY(medecineID, npl_packID)
);

-- Placeholder see next comment
CREATE TABLE medecine_ingredients(
	medecineID: BIGINT,
	substanceID: CHAR(18), -- ID from NSL which I have yet to look at, i.e table not implemented
	ingredient_role: VARCHAR(4),
	PRIMARY KEY(medecineID, substanceID),
	CONSTRAINT fk_medecineID
		FOREGIN KEY(medecineID)
			REFERENCES medecine(nplID),
	CONSTRAINT fk_ingredient_role
		FOREGIN KEY (ingredient_role)
			REFERENCES ingredient_role(mpaID)
	-- FK to substance table
);

CREATE TABLE organization_medecine_map(
	medecineID: BIGINT,
	orgID: CHAR(18),
	org_role: VARCHAR(6),
	PRIMARY KEY(medecineID, orgID),
	CONSTRAINT fk_medecineID
		FOREGIN KEY (medecineID)
			REFERENCES medecine(nplID),
	CONSTRAINT fk_orgID
		FOREGIN KEY (orgID)
			REFERENCES organization(orgID),
	CONSTRAINT fk_org_role
		FOREGIN KEY(org_role)
			REFERENCES organization_role(mpaID)
);

CREATE TABLE route_of_administration_map (
	medecineID: BIGINT,
	route_of_administration: VARCHAR(4),
	PRIMARY KEY (medecineID, route_of_administration),
	CONSTRAINT fk_medecineID
		FOREGIN KEY(medecineID)
			REFERENCES medecine(nplID),
	CONSTRAINT fk_route_of_administration
		FOREGIN KEY(route_of_administration)
			REFERENCES route_of_administration(mpaID)
);

