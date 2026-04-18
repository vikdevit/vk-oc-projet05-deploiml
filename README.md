## Git Commit Convention

We follow Conventional Commits:

- feat: new feature
- fix: bug fix
- chore: maintenance tasks
- model: ML model changes
- test: testing

Example:
feat(api): add prediction endpoint

## Etape Feature Building 
### Structure df_joint
0   id                                            1470 non-null   int64   
 1   age                                           1470 non-null   int64   
 2   genre                                         1470 non-null   str     
 3   revenu_mensuel                                1470 non-null   int64   
 4   statut_marital                                1470 non-null   str     
 5   departement                                   1470 non-null   str     
 6   poste                                         1470 non-null   str     
 7   nombre_experiences_precedentes                1470 non-null   int64   
 8   nombre_total_annees_experience                1470 non-null   int64   
 9   nombre_total_annees_dans_l_entreprise         1470 non-null   int64   
 10  nombre_total_annees_dans_le_poste_actuel      1470 non-null   int64   
 11  satisfaction_salarie_environnement            1470 non-null   int64   
 12  note_evaluation_precedente                    1470 non-null   int64   
 13  niveau_hierarchique_poste                     1470 non-null   int64   
 14  satisfaction_salarie_nature_travail           1470 non-null   int64   
 15  satisfaction_salarie_equipe                   1470 non-null   int64   
 16  satisfaction_salarie_equilibre_pro_perso      1470 non-null   int64   
 17  note_evaluation_actuelle                      1470 non-null   int64   
 18  heures_supplementaires                        1470 non-null   str     
 19  precedent_pourcentage_d_augmentation          1470 non-null   int64   
 20  satisfaction_moyenne                          1470 non-null   float64 
 21  satisfaction_bin                              1470 non-null   category     
 23  nombre_participation_pee                      1470 non-null   int64   
 24  nombre_de_formations_suivies                  1470 non-null   int64   
 25  distance_domicile_travail                     1470 non-null   int64   
 26  niveau_education                              1470 non-null   int64   
 27  domaine_etude                                 1470 non-null   str     
 28  frequence_deplacement                         1470 non-null   str     
 29  nombre_d_annees_depuis_la_derniere_promotion  1470 non-null   int64   
 30  nombre_d_annees_sous_le_responsable_actuel    1470 non-null   int64   

### Structure JSON pour input
{
  "employees": [
    {
      "id": 1 (int64)
      "age": 34, (int64)
      "genre": "m", (m ou f (str))
      "revenu_mensuel": 3200, (int64)
      "statut_marital": "celibataire",   (celibataire', 'mariee', 'divorcee)
      "departement": "commercial",   (commercial', 'consulting', 'ressources_humaines )
      "poste": "manager", (cadre_commercial',  'assistant_de_direction','consultant', 'tech_lead', 'manager', 'senior_manager', 'representant_commercial','directeur_technique', 'ressources_humaines')
      "nombre_experiences_precedentes": 3,
      "nombre_total_annees_experience": 5,
      "nombre_total_annees_dans_l_entreprise": 4,
      "nombre_total_annees_dans_le_poste_actuel": 2,
      "satisfaction_salarie_environnement": 3, (1, 2,3 ou 4)
      "satisfaction_salarie_nature_travail": 4, (1, 2,3 ou 4)
      "satisfaction_salarie_equipe": 3, (1, 2,3 ou 4)
      "satisfaction_salarie_equilibre_pro_perso": 3,
      "note_evaluation_precedente": 4, (1, 2,3 ou 4)
      "niveau_hierarchique_poste": 2, (1, 2,3, 4 ou 5)
      "note_evaluation_actuelle": 4, (1, 2, 3 ou 4)
      "heures_supplementaires": "oui", (oui, non)
      "precedent_pourcentage_d_augmentation": 10, (entre 11 et 25 int 64),
     "nombre_participation_pee": 2, (1, 2 ou 3)
      "nombre_de_formations_suivies": 3, (0, 1, 2,3,4,5 ou 6)
      "distance_domicile_travail": 10, (1 à 30 int64)
      "niveau_education": 3, (1, 2, 3,4,5 int64)
      "domaine_etude": "autre", ('infra_et_cloud','autre','transformation_digitale', 'marketing','entrepreunariat' ou'ressources_humaines']
      "frequence_deplacement": "frequent", ('occasionnel', 'frequent'ou 'aucun)
      "nombre_d_annees_depuis_la_derniere_promotion": 2, (entre 0 et 15 int64)
      "nombre_d_annees_sous_le_responsable_actuel": 1 (entre 0 et 20 int64)
    },
   
   etc.

### pour encodage des variables catégorielles 
# Encodage des variables catégorielles
créer colonnes 
poste_assistant_de_direction                  1470 non-null   bool    
 27  poste_cadre_commercial                        1470 non-null   bool    
 28  poste_consultant                              1470 non-null   bool    
 29  poste_directeur_technique                     1470 non-null   bool    
 30  poste_manager                                 1470 non-null   bool    
 31  poste_other                                   1470 non-null   bool    
 32  poste_representant_commercial                 1470 non-null   bool    
 33  poste_senior_manager                          1470 non-null   bool    
 34  poste_tech_lead                               1470 non-null   bool  
 donc si poste pas cadre_comemrcial, consultant, directeur_techinuqe, manage,r representant_comemrcial, senio_manager ou tech_lead alors va dans poste_other
 
departement_commercial                        1470 non-null   bool    
 36  departement_consulting                        1470 non-null   bool    
 37  departement_other  
donc si departmeent = ressources_hulaines alors va dans deprtement_other

domaine_etude_autre                           1470 non-null   bool    
 39  domaine_etude_entrepreunariat                 1470 non-null   bool    
 40  domaine_etude_infra_et_cloud                  1470 non-null   bool    
 41  domaine_etude_marketing                       1470 non-null   bool    
 42  domaine_etude_other                           1470 non-null   bool    
 43  domaine_etude_transformation_digitale         1470 non-null   bool   
 donc si domaine_etude = resosurces_humaines alors va dans domaine_etude_other
 
 44  genre_f                                       1470 non-null   bool    
 45  genre_m                                       1470 non-null   bool

 heures_supplementaires_non                    1470 non-null   bool    
 47  heures_supplementaires_oui                    1470 non-null   bool    

   frequence_deplacement_aucun                   1470 non-null   bool    
 49  frequence_deplacement_frequent                1470 non-null   bool    
 50  frequence_deplacement_occasionnel             1470 non-null   bool    

 51  niveau_education_1                            1470 non-null   bool    
 52  niveau_education_2                            1470 non-null   bool    
 53  niveau_education_3                            1470 non-null   bool    
 54  niveau_education_4                            1470 non-null   bool    
 55  niveau_education_other                        1470 non-null   bool   
 donc si niveau_deudcation ) 5 alors va dans niveau_education_other
