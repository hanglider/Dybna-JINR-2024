import csv
from pathlib import Path
import json

def process_csv_data(file_path: str) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        data = []
        for row in  reader:
            name, gender, age, skills, company, salary, location, registered_date = row
            skills = skills.split(';')
            lat = float(location.split(';')[0])
            lon = float(location.split(';')[1])
            age = int(age)

            data_dict = {
                'name' : name,
                'gender' : gender,
                'age' : age,
                'skills' : skills,
                'company' : company,
                'salary' : salary,
                'location' : {
                    'lat' : lat,
                    'lon' : lon
                },
                'registered_date' : registered_date
            }
            data.append(data_dict)
    return data

def save_json(data:list[dict], file_path:str):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    main_dir = Path(r'C:\IT\JINR\Practics\data')
    results = [process_csv_data(file) for file in main_dir.iterdir()]
    save_json(results, "C:\IT\JINR\Practics\data\data.json")
