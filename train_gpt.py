# Import necessary libraries
import pandas as pd
from datasets import Dataset
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments

# Load the tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Set the padding token to be the same as the EOS token
tokenizer.pad_token = tokenizer.eos_token

# Define a function to load the dataset
def load_data(file_path):
    # Load the dataset from a CSV file
    dataset = Dataset.from_pandas(pd.read_csv(file_path))
    # Add a mock emergency_services column
    dataset = dataset.map(lambda x: {'emergency_services': ['Default Emergency Service'] * len(x['name'])})
    print("Loaded dataset columns:", dataset.column_names)  # Print the column names
    return dataset

# Define a function to combine relevant columns
def combine_columns(examples):
    # Get specialties from the examples
    specialties = examples.get('specialties', [])

    # If specialties is empty, return empty list
    if not specialties:
        return {'combined_text': [''] * len(specialties)}  # Return empty strings for combined_text

    # Combine specialties into a single text
    combined_texts = []
    for specialty in specialties:
        # Ensure that specialties is a string
        specialty_text = specialty if isinstance(specialty, str) else ' '.join(specialty)
        combined_texts.append(specialty_text.strip())

    return {'combined_text': combined_texts}

# Define a function to preprocess the dataset
def preprocess_data(dataset):
    # Check if the 'specialties' column exists
    if 'specialties' not in dataset.column_names:
        raise ValueError("The dataset must contain the 'specialties' column.")

    # Combine relevant columns
    dataset = dataset.map(combine_columns, batched=True)

    # Tokenize the combined text
    dataset = dataset.map(
        lambda examples: tokenizer(examples['combined_text'], truncation=True, padding='max_length', max_length=512),
        batched=True
    )

    # Set the labels to be the same as input_ids
    dataset = dataset.map(lambda x: {'labels': x['input_ids']})
    return dataset

# Main script execution
if __name__ == "__main__":
    # Load and preprocess data
    dataset = load_data("H:/hospital_project/cleaned_hospitals.csv")  # Replace with your actual dataset path
    dataset = preprocess_data(dataset)
    
    # Load the model
    model = GPT2LMHeadModel.from_pretrained(model_name)
    
    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",  # Changed from evaluation_strategy to eval_strategy
        learning_rate=5e-5,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    # Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=dataset,
    )

    # Start training
    trainer.train()
    
    # Save the trained model and tokenizer
    model.save_pretrained("./results/trained_model")
    tokenizer.save_pretrained("./results/trained_model")
