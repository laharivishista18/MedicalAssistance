import os
from zipfile import ZipFile
import pandas as pd

def extract_csv_from_zip(zip_file_path, csv_file_name, output_dir):
    """Extracts a CSV file from a ZIP archive."""
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extract(csv_file_name, output_dir)

def load_dataset(csv_file_path):
    """Loads the dataset from a CSV file."""
    return pd.read_csv(csv_file_path)

def display_symptoms(symptoms):
    """Displays symptoms divided into six columns."""
    num_columns = 6
    num_symptoms = len(symptoms)
    symptoms_per_column = num_symptoms // num_columns + (num_symptoms % num_columns > 0)  # Ceiling division
    for i in range(symptoms_per_column):
        for j in range(i, len(symptoms), symptoms_per_column):
            print(f"{j + 1}. {symptoms[j]:<30}", end='\t')
        print()

def user_select_symptoms(symptoms):
    """Allows the user to select symptoms."""
    selected_symptoms = []
    while True:
        display_symptoms(symptoms)
        user_input = input("Enter the numbers corresponding to the selected symptoms (separated by commas): ")
        selected_indices = [int(idx) - 1 for idx in user_input.split(',') if idx.isdigit()]
        if all(idx >= 0 and idx < len(symptoms) for idx in selected_indices):
            selected_symptoms = [symptoms[idx] for idx in selected_indices]
            break
        else:
            print("Invalid input. Please enter valid numbers corresponding to the selected symptoms.")
    return selected_symptoms

def find_related_diseases(selected_symptoms, dataset):
    """Finds related diseases based on selected symptoms."""
    related_diseases = set()
    for _, row in dataset.iterrows():
        if any(row[symptom] == 1 for symptom in selected_symptoms):
            related_diseases.add(row['prognosis'])
    return related_diseases

def main():
    zip_file_path = "/content/Training.csv.zip"
    csv_file_name = "Training.csv"
    output_dir = "/content/"

    # Extract CSV from ZIP
    extract_csv_from_zip(zip_file_path, csv_file_name, output_dir)

    # Load dataset
    csv_file_path = os.path.join(output_dir, csv_file_name)
    dataset = load_dataset(csv_file_path)

    # Get all symptoms from the dataset
    symptoms = dataset.columns[1:-1].tolist()

    # First level of user input
    print("\n--- Level 1 ---")
    selected_symptoms_1 = user_select_symptoms(symptoms)
    related_diseases_1 = find_related_diseases(selected_symptoms_1, dataset)

    # Display related diseases for level 1
    print("\nDiseases related to the selected symptoms (Level 1):")
    if related_diseases_1:
        for disease in sorted(related_diseases_1):
            print(disease)
    else:
        print("No related diseases found.")

    # Second level of user input
    # Add similar code for other levels of user input

if __name__ == "__main__":
    main()
