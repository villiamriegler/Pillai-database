CREATE TABLE IF NOT EXISTS bipacksedel_user_information (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_product_information (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_indication (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_caution_and_warnings (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_contraindication (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_caution (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_interaction (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_pregnancy (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_driving (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_substance_information (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_usage_and_administration (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_overdosage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_missed (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_withdrawal (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_side_effects (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_additionalMonitoringInfo (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_storage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_information_source (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_composition (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_appearance (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_prod_license (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_tradename (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_composition (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_product_form (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_clinical (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_pharmacological (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_pharmaceutical (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_prod_license (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_approval_number (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_approval_first_date (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_revision_date (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_indication (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_contraindication (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_dosage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_caution (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_interaction (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_pregnancy (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_breastfeeding (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_fertility (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_driving (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_side_effects (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_overdosage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_pharmacodynamic (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_pharmacokinetic (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_preclinical_info (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_composition (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_env_effect (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_handling_life_shelf_storage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bilder_och_delbarhet_delbarhets_information (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS miljoinformation_env_effect (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_composition (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_hazardous_properties (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_precautions_during_handling (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_accidental_release_measures (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_first_aid (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_more_info (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_name (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_user_information (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_product_information (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_indication (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_caution_and_warnings (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_contraindication (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_caution (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_interaction (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_pregnancy (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_driving (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_substance_information (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_usage_and_administration (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_overdosage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_missed (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_withdrawal (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_side_effects (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_additionalMonitoringInfo (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_storage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_information_source (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_composition (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_appearance (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_prod_license (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_tradename (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_composition (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_product_form (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_clinical (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_pharmacological (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_pharmaceutical (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_prod_license (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_approval_number (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_approval_first_date (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS produktresume_revision_date (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_indication (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_contraindication (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_dosage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_caution (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_interaction (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_pregnancy (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_breastfeeding (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_fertility (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_driving (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_side_effects (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_overdosage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_pharmacodynamic (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_pharmacokinetic (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_preclinical_info (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_composition (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_handling_life_shelf_storage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bilder_och_delbarhet_delbarhets_information (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_composition (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_hazardous_properties (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_precautions_during_handling (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_accidental_release_measures (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_first_aid (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skyddsinfo_more_info (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_name (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_incompatibility (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_env_effect (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS miljoinformation_env_effect (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fass_text_properties_medicine (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_children (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_interaction_food (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_usage_children (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_additional_sources (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_instructions_for_use (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_manufacturer (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_usage (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_directions_for_use (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_side_effects_children (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bipacksedel_action (
	nplID INT PRIMARY KEY,
	content TEXT NOT NULL
);

