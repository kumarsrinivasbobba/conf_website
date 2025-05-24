from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variables
mongo_uri = os.getenv("MONGO_URI")

# If no environment variable is found, use a default (replace with your credentials)
if not mongo_uri:
    print("Warning: No MONGO_URI found in environment variables. Using default connection string.")
    # Make sure to remove the angle brackets around the password
    mongo_uri = "mongodb+srv://99210041514:kareKARE@cluster0.8nxoygo.mongodb.net/conference_db?retryWrites=true&w=majority&appName=Cluster0"

print(f"Connecting to database using URI: {mongo_uri.replace(mongo_uri.split('@')[0], '[CREDENTIALS HIDDEN]')}")

try:
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    
    # Test the connection
    client.admin.command('ping')
    print("Connection successful!")
    
    # Get the database
    db = client.conference_db
    
    # Clear existing data (optional)
    db.proceedings.delete_many({})
    db.conference_state.delete_many({})
    print("Cleared existing data.")
    
    # Add conference state
    db.conference_state.insert_one({
        "id": "main",
        "is_launched": False,
        "launched_at": None
    })
    print("Added conference state.")
    
    # Sample proceedings
    sample_proceedings = [
        {
            "title": "Advances in Artificial Intelligence and Machine Learning",
            "content": "This paper explores recent developments in AI and machine learning, focusing on natural language processing and computer vision applications. We demonstrate how these technologies are being integrated into various industries and discuss their potential impact on future innovation.",
            "author": "Dr. Sarah Johnson",
            "timestamp": datetime.now() - timedelta(hours=2)
        },
        {
            "title": "Sustainable Computing: Reducing Carbon Footprint in Data Centers",
            "content": "Our research presents innovative approaches to reducing energy consumption in large-scale data centers. We propose a hybrid cooling system that combines traditional methods with renewable energy sources, resulting in a 45% reduction in overall carbon emissions.",
            "author": "Prof. Michael Chen",
            "timestamp": datetime.now() - timedelta(hours=1, minutes=30)
        },
        {
            "title": "Blockchain Applications in Supply Chain Management",
            "content": "This study examines how blockchain technology can enhance transparency and security in global supply chains. We present a case study of implementation in the pharmaceutical industry, demonstrating improved traceability and reduced counterfeit products.",
            "author": "Dr. Amelia Rodriguez",
            "timestamp": datetime.now() - timedelta(hours=1)
        },
        {
            "title": "Quantum Computing: Current State and Future Directions",
            "content": "Our paper provides a comprehensive overview of quantum computing advancements and challenges. We discuss recent experimental results in quantum supremacy and analyze potential applications in cryptography, optimization problems, and material science.",
            "author": "Dr. James Wilson",
            "timestamp": datetime.now() - timedelta(minutes=30)
        },
        {
            "title": "Human-Computer Interaction in Virtual Reality Environments",
            "content": "This research investigates novel interaction paradigms in immersive VR environments. We present findings from user studies that evaluated natural gesture recognition systems and haptic feedback mechanisms, offering design guidelines for more intuitive VR interfaces.",
            "author": "Prof. Lisa Zhang",
            "timestamp": datetime.now() - timedelta(minutes=15)
        }
    ]
    
    # Insert sample proceedings
    db.proceedings.insert_many(sample_proceedings)
    print("Added sample proceedings.")
    
    print("\nSample data has been successfully added to the database!")

except Exception as e:
    print(f"An error occurred: {e}")
    
    # Additional troubleshooting information
    if "bad auth" in str(e):
        print("\nAuthentication Error Troubleshooting:")
        print("1. Check if your MongoDB Atlas username and password are correct")
        print("2. Make sure there are NO angle brackets (<>) around your password")
        print("3. Verify that your MongoDB user has the right permissions")
        print("4. Check if your IP address is whitelisted in MongoDB Atlas")
        print("\nTo fix in MongoDB Atlas:")
        print("- Go to Security > Database Access to verify credentials")
        print("- Go to Network Access to check IP whitelist")