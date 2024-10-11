import numpy as np
import pandas as pd
import csv
from pathlib import Path
import json
import os
main_dir = Path(r'data/csv_data')

# словарь с ключевыми словами по ядерной физике
high_energy_physics_terms = set([
    "quark", "quarks", "lepton", "leptons", "boson", "bosons", "Higgs", "Higgses", 
    "neutrino", "neutrinos", "photon", "photons", "gluon", "gluons", "proton", "protons", 
    "neutron", "neutrons", "electron", "electrons", "positron", "positrons", "antimatter", 
    "antimatters", "particle", "particles", "accelerator", "accelerators", "collider", 
    "colliders", "synchrotron", "synchrotrons", "hadron", "hadrons", "meson", "mesons", 
    "fermion", "fermions", "muon", "muons", "tau", "taus", "graviton", "gravitons", 
    "supersymmetry", "supersymmetries", "quantum", "quantums", "chromodynamics", 
    "strong_force", "strong_forces", "weak_force", "weak_forces", "electromagnetic_force", 
    "electromagnetic_forces", "standard_model", "standard_models", "quantum_field_theory", 
    "quantum_field_theories", "spontaneous_symmetry_breaking", "grand_unification", 
    "grand_unifications", "dark_matter", "dark_matters", "dark_energy", "dark_energies", 
    "cosmic_ray", "cosmic_rays", "black_hole", "black_holes", "string_theory", 
    "string_theories", "extra_dimension", "extra_dimensions", "tachyon", "tachyons", 
    "renormalization", "renormalizations", "loop_quantum_gravity", "loop_quantum_gravities", 
    "fermion", "fermions", "neutrino_oscillation", "neutrino_oscillations", "mass", "masses", 
    "energy", "energies", "feynman_diagram", "feynman_diagrams", "beta_decay", "beta_decays", 
    "big_bang", "big_bangs", "cosmology", "cosmologies", "superstring_theory", 
    "superstring_theories",
    "Black Hole physics",
    "Curved spacetime",
    "Experimental realizations",
    "Hawking radiation",
    "Massless scalar fields",
    "Quantum field theory",
    "Quantum many-body systems",
    "Static spacetime",
    "Quantum theory",
    "Bosonic fields",
    "Nonclassical effects",
    "Atom-field interaction",
    "Cavity Quantum Electrodynamics",
    "Wigner-Yanase skew information",
    "Jaynes-Cummings model",
    "Energy gap",
    "III-V semiconductors",
    "High electron mobility",
    "Magneto-transport characteristics",
    "Quantum optics",
    "Wave packets",
    "Quantum state transfers",
    "Topological charges",
    "Phase gradient",
    "Transverse planes",
    "X-Y model",
    
])

def find_articles(keywords: set, df: pd.DataFrame) -> pd.DataFrame:
    """
    Find articles in the DataFrame where at least 2 of the keywords are present in the "Ключевые слова указателя" column.

    Args:
    keywords (set): A set of keywords to search for.
    df (pd.DataFrame): The DataFrame to search in.

    Returns:
    pd.DataFrame: A new DataFrame containing only the rows where at least 2 of the keywords are present in the "Ключевые слова указателя" column.
    """
    # Convert the set of keywords to a list of lowercase strings
    keywords = [kw.lower() for kw in keywords]

    # Filter out rows with NaN values in the "Ключевые слова указателя" column and create a copy
    if 'Index Keywords' in df.columns:
        df.rename(columns={'Index Keywords': 'Ключевые слова указателя'}, inplace=True)
    
    try:
        df_filtered = df.dropna(subset=['Ключевые слова указателя']).copy()
    except:
        print('NO SUCH COLUMN Ключевые слова указателя')
    
    # Using .loc to safely modify the DataFrame
    df_filtered.loc[:, 'match_count'] = df_filtered['Ключевые слова указателя'].str.lower().str.findall('|'.join(keywords)).str.len()

    # Find rows where at least 2 keywords are present in the "Ключевые слова указателя" column
    mask = df_filtered['match_count'] >= 2

    # Return a new DataFrame containing only the matching rows
    return df_filtered[mask]

# Function to process each file
def process_file(file_path, organisations_dict):

    # Read CSV file
    # WARNING :  ТУТ ВЫЛЕЗАЕТ ОШИБКА
    # TODO
    df_current = pd.read_csv(file_path, low_memory=False)
    
    #df_current = df_current.drop(['Том', 'Выпуск','Страница начала','Страница окончания','Количество страниц','Статья №','Год','Идентификатор PubMed','Сокращенное название источника','Тип документа','СТАДИЯ ПУБЛИКАЦИИ','Open Access (открытый доступ)','CODEN','ISBN','Место проведения конференции','Дата конференции','Название конференции','Код конференции','Редакторы','Спонсоры','Адрес для корреспонденции','Текст о финансировании','Сведения о финансировании','Ссылка','Номера молекулярных последовательностей','Химические вещества/CAS','Фирменные наименования','Производители','DOI','ISSN','Язык оригинального документа','Источник','EID','Идентификатор автора(ов)'], axis=1)
    df_current = find_articles(keywords=high_energy_physics_terms,df=df_current)

            # Filter out rows with NaN values in the "Ключевые слова указателя" column and create a copy
    if 'Affiliations' in df_current.columns:
        df_current.rename(columns={'Affiliations': 'Организации'}, inplace=True)
        
    if 'Организации' in df_current.columns:
            # Split the organisations column by semicolon and explode it
            df_current = df_current.assign(Organisation=df_current['Организации'].str.split(';')).explode('Организации')
            # Strip whitespace from organisation names

            
            #Update count in organisations_df
            for org_list in df_current['Organisation']:
                for org in org_list:
                    if(org in organisations_dict):
                        organisations_dict[org.strip()] += 1
                    else:
                        organisations_dict[org.strip()] = 1
    
    return organisations_dict

def top_5_pairs(dictionary):
    # Сортируем словарь по значениям в порядке убывания и берём первые 5 пар
    top_pairs = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)[:5]
    
    return dict(top_pairs)

# Функция для рекурсивного поиска и обработки всех CSV файлов в директориях
# ПРОСТО НАПИСАНА ГПТ, МЫ ЕЩЕ НЕ УСПЕЛИ ЕЕ ИСПОЛЬЗОВАТЬ
def process_directory(directory_path):
    organisations_dict = dict()

    # Рекурсивно обходим папки
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                print(f"Обработка файла: {file_path}")
                organisations_dict = process_file(file_path, organisations_dict)


    # После обработки всех файлов, группируем результаты по организациям
    final_stats = top_5_pairs(organisations_dict)
    
    return final_stats

directory_path = './data/2024'

# Обработка всех файлов
top_organisations = process_directory(directory_path)
top_organisations

len(top_organisations)
top_organisations