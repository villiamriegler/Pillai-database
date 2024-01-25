-- File for database creation, 
-- Create tables, views etc 

CREATE TABLE IF NOT EXISTS product_name (
	nplID INT PRIMARY KEY,
	(P_NAME)product_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_leaflet (
    nplID INT PRIMARY KEY, 
    (PL)user_information
    (PL)product_information
    (PL)substance_information

    (PL)indication

    (PL)caution
    (PL)caution_and_warnings
    (PL)interaction
    
    (PL)missed

    (PL)side_effects
    (PL)withdrawal
    (PL)overdosage

    (PL)additionalMonitoringInfo

    (PL)storage

    (PL)appearance

    (PL)children
    (PL)pregnancy
    
    (PL)interaction
    (PL)interaction_food

    (PL)usage_and_administration
    (PL)instructions_for_use
    (PL)contraindication
    (PL)usage_children

    (PL)driving
);

CREATE TABLE IF NOT EXISTS summary_of_product_characteristics (
    nplID INT PRIMARY KEY,
    (SmPC)tradename 

    (SmPC)composition
    (SmPC)product_form
    
    (SmPC)clinical
    (SmPC)pharmacological
    (SmPC)pharmaceutical
    (SmPC)prod_license
    (SmPC)approval_number
    (SmPC)approval_first_date
    (SmPC)revision_date
);

CREATE TABLE IF NOT EXISTS fass_text (
    nplID INT PRIMARY KEY,
    (fass)indication
    (fass)contraindication
    (fass)dosage
    (fass)caution
    (fass)interaction
    (fass)pregnancy
    (fass)breastfeeding
    (fass)fertility
    (fass)driving
    (fass)side_effects
    (fass)overdosage
    (fass)pharmacodynamic
    (fass)pharmacokinetic 
    (fass)preclinical_info
    (fass)composition
    (fass)env_effect
    (fass)handling_life_shelf_storage
    (fass)incompatibility
    (fass)properties_medicine
);

CREATE TABLE IF NOT EXISTS skyddsinfo (
    nplID INT PRIMARY KEY,
    (Sydd)composition
    (Sydd)hazardous_properties
    (Sydd)precautions_during_handling
    (Sydd)accidental_release_measures
    (Sydd)first_aid
    (Sydd)more_info
);

CREATE TABLE IF NOT EXISTS divisability (
	nplID INT PRIMARY KEY,
	(Delbarhet)content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS miljoinformation_env_effect (
	nplID INT PRIMARY KEY,
	(Env)content TEXT NOT NULL
);


