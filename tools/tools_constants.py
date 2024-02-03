# Retriever tool
few_shots_examples = {
    "Le dernier nom de modèle de montre rappelé": """ SELECT noms_des_modeles_ou_references
                FROM rappel_conso_table
                WHERE LOWER(nom_de_la_marque_du_produit) LIKE '%montre%'
                   OR LOWER(noms_des_modeles_ou_references) LIKE '%montre%'
                ORDER BY date_de_publication DESC
                LIMIT 1;
                """,
    "Y a-t-il des voitures Tesla rappelés actuellement ?": """SELECT COUNT(*) FROM rappel_conso_table WHERE LOWER(nom_de_la_marque_du_produit) LIKE '%tesla%' AND date_de_fin_de_la_procedure_de_rappel IS NULL""",
}

retriever_tool_description = (
    "The 'sql_get_few_shot' tool is designed for efficient and accurate retrieval of "
    "SQL query examples closely related to a given user query. It identifies the most "
    "relevant pre-defined SQL query from a curated set."
)

# Other tools

COLUMNS_DESCRIPTIONS = {
    "reference_fiche": "primary key of the database and unique identifier in the database. ",
    "nom_de_la_marque_du_produit": "A string representing the Name of the product brand. Example: Apple, Carrefour, etc ... When you filter by this column,you must use LOWER() function to make the comparison case insensitive and you must use LIKE operator to make the comparison fuzzy.",
    "noms_des_modeles_ou_references": "Names of the models or references. Can be used to get specific infos about the product. Example: iPhone 12, etc, candy X, product Y, bread, butter ...",
    "identification_des_produits": "Identification of the products. For instance it may represent the sales lot.",
    "date_debut_commercialisation": "the date when the product first became available for sale to the public.",
    "date_fin_commercialisation": "the date when the product was officially ceased to be available for sale.",
    "temperature_de_conservation": "Storage temperature",
    "informations_complementaires": "Additional information that can be useful about the risks, who to call, what to do, etc...",
    "zone_geographique_de_vente": "Geographical area of sale",
    "distributeurs": "The distributors of the recalled product. When you filter by this column,you must use LOWER() function to make the comparison case insensitive and you must use LIKE operator to make the comparison fuzzy. ",
    "motif_du_rappel": "Reason for recall. Such as the presence of a foreign body, a pathogen, a toxic element, etc ...",
    "risques_pour_le_consommateur": "the potential risks or hazards associated with the recalled product for consumers.",
    "recommandations_sante": "Health recommendations",
    "numero_de_contact": "Contact number",
    "modalites_de_compensation": "Compensation arrangements",
    "date_de_fin_de_la_procedure_de_rappel": "End date of the recall procedure",
    "liens_vers_les_images": "Links to images",
    "lien_vers_la_liste_des_produits": "Link to the list of products",
    "lien_vers_la_liste_des_distributeurs": "Link to the list of distributors",
    "lien_vers_affichette_pdf": "Link to the PDF poster",
    "lien_vers_la_fiche_rappel": "Link to the recall sheet",
    "date_de_publication": "Publication date",
}
