import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variables
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://99210041514:kareKARE@cluster0.8nxoygo.mongodb.net/conference_db?retryWrites=true&w=majority&appName=Cluster0")

print(f"Connecting to database using URI: {mongo_uri.replace(mongo_uri.split('@')[0], '[CREDENTIALS HIDDEN]')}")

try:
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    
    # Test the connection
    client.admin.command('ping')
    print("Connection successful!")
    
    # Get the database
    db = client.conference_db
    
    # Import Excel data
    print("Reading Excel file...")
    excel_path = r"C:\Users\kumar\Downloads\Index Page.xlsx"  # Note the 'r' prefix for raw string
    data = pd.read_excel(excel_path)
    
    # Check what columns we have
    print(f"Excel columns: {data.columns.tolist()}")
    
    # Clear existing proceedings data
    db.proceedings.delete_many({})
    print("Cleared existing proceedings data.")
    
    # Prepare proceedings data
    proceedings_data = []
    
    # Process each row in the Excel file
    for _, row in data.iterrows():
        # Extract data - adjust these column names to match your Excel file
        paper_id = str(row['Paper ID']) if 'Paper ID' in row else 'N/A'
        title = row['Paper Title'] if 'Paper Title' in row else 'Untitled Paper'
        authors = row['Author Names'] if 'Author Names' in row else 'Unknown Author'
        
        # Create document - omitting content as requested
        proceedings_data.append({
            "paper_id": paper_id,
            "title": title,
            "author": authors,
            "timestamp": datetime.now()
        })
    
    # Insert new proceedings data
    if proceedings_data:
        db.proceedings.insert_many(proceedings_data)
        print(f"Successfully added {len(proceedings_data)} papers to the database!")
    else:
        print("No data was found to import.")
    
    # Check what we now have in the database
    count = db.proceedings.count_documents({})
    print(f"Total papers in database: {count}")
    
    # List a few sample papers
    print("\nSample papers in database:")
    for paper in db.proceedings.find().limit(3):
        print(f"- {paper['title']} by {paper['author']}")

except Exception as e:
    print(f"An error occurred: {e}")
    
    # Additional troubleshooting information for Excel-related errors
    if "No such file or directory" in str(e):
        print("\nFile Error Troubleshooting:")
        print("1. Check if the Excel file path is correct")
        print("2. Make sure to use raw string (r prefix) or double backslashes in the path")
        print("3. Verify that the Excel file exists at the specified location")