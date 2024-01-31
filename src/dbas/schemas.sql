-- File for database creation, 
-- Create tables, views etc 
-- File for database creation, 
-- Create tables, views etc 

CREATE TABLE IF NOT EXISTS product_name (
	nplID INT PRIMARY KEY,
	(P_NAME)product_name TEXT NOT NULL
);

CREATE TABLE general_info (
	nplID INT PRIMARY KEY,
    (SmPC)tradename 
    (PL)user_information
    (PL)product_information
    (PL)substance_information
    (fass)pharmacodynamic
    (fass)pharmacokinetic 
    (SmPC)pharmacological
    (SmPC)pharmaceutical
);


CREATE TABLE side_effects (
	nplID INT PRIMARY KEY,
    (PL)side_effects
    (PL)withdrawal
    (fass)fertility
    (fass)side_effects
);

CREATE TABLE interactions (
	nplID INT PRIMARY KEY,
    (PL)interaction
    (PL)interaction_food
    (fass)interaction
    (fass)incompatibility
);

CREATE TABLE warnings (
	nplID INT PRIMARY KEY,
    (PL)caution
    (PL)caution_and_warnings
    (PL)missed
    (fass)caution
    (Sydd)hazardous_properties
    (Sydd)precautions_during_handling
    (Sydd)accidental_release_measures
    (Sydd)first_aid
);

CREATE TABLE usage (
	nplID INT PRIMARY KEY,
    (PL)usage_and_administration
    (PL)instructions_for_use
    (PL)usage_children
    (fass)dosage
    (PL)overdosage
    (fass)overdosage
    (PL)driving
    (fass)driving
    (PL)children
    (PL)pregnancy
    (fass)pregnancy
    (fass)breastfeeding
);

CREATE TABLE appropriateness (
	nplID INT PRIMARY KEY,
    (PL)indication
    (fass)indication
    (PL)contraindication
    (fass)contraindication
);

CREATE TABLE storage (
	nplID INT PRIMARY KEY,
    (fass)handling_life_shelf_storage
    (PL)storage
);

CREATE TABLE properties (
	nplID INT PRIMARY KEY,
    (fass)properties_medicine
    (Sydd)composition
    (fass)composition
    (PL)appearance
    (SmPC)composition
    (SmPC)product_form
    (SmPC)clinical
);


CREATE TABLE IF NOT EXISTS divisability (
	nplID INT PRIMARY KEY,
	(Delbarhet)content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS miljoinformation_env_effect (
	nplID INT PRIMARY KEY,
	(Env)content TEXT 
    (fass)env_effect
);



