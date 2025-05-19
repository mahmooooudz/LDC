LDC Technical Assessment - RAG Chatbot System
Overview
This project implements a Retrieval-Augmented Generation (RAG) chatbot system that answers questions about HR policies. The system consists of three main components:

Python Backend - A FastAPI application that uses a RAG approach to process queries and retrieve relevant information from HR policy documents.
.NET Web API - An ASP.NET Core application that serves as the frontend service, handling user queries, forwarding them to the Python backend, and logging interactions.
SQL Database - A SQL Server database that stores all user queries and chatbot responses.

Repository Structure
LDC/
├── ChatbotAPI/            # .NET Web API project
│   ├── Controllers/       # API endpoints
│   ├── Models/            # Data models
│   ├── Repositories/      # Database access
│   ├── Services/          # Business logic
│   └── appsettings.json   # Configuration
├── python-backend/        # Python RAG implementation
│   ├── data/              # HR policy documents
│   ├── app.py             # FastAPI server
│   ├── document_processor.py
│   ├── rag_pipeline.py
│   └── requirements.txt   # Python dependencies
└── sql-schema.sql         # Database schema
Architecture
The system follows a three-tier architecture:
Client -> .NET Web API -> Python Backend -> HR Policy Documents
                |
                v
           SQL Database

Client Layer: End users submit queries via HTTP requests to the .NET Web API.
API Layer: The .NET Web API receives queries, forwards them to the Python backend, logs interactions, and returns responses.
Processing Layer: The Python backend implements a RAG pipeline that processes documents, retrieves relevant content, and generates responses.
Storage Layer: The SQL database stores all interactions for tracking and analysis.

Setup Instructions
Prerequisites

Python 3.10+ with pip
.NET 7.0+ SDK
SQL Server 2019+
SQL Server Management Studio (SSMS) or similar tool

1. Database Setup

Open SQL Server Management Studio and connect to your SQL Server instance
Execute the sql-schema.sql script to create the database, tables, and stored procedures
Verify that the following objects were created:

ChatbotDB database
UserQueries table
ChatbotResponses table
ChatInteractions view
LogChatInteraction stored procedure



2. Python Backend Setup

Navigate to the python-backend directory
Install required packages:
pip install -r requirements.txt

Ensure the HR policy documents are in the data folder:

HR_Policy_Dataset1.txt
HR_Policy_Dataset2.txt


Start the Python backend:
python app.py

The server will run on http://localhost:8000

3. .NET Web API Setup

Navigate to the ChatbotAPI directory
Update the connection string in appsettings.json to point to your SQL Server instance
Build and run the API:
dotnet build
dotnet run

The API will run on http://localhost:5149

Testing the System
Using Swagger UI

Open a web browser and navigate to http://localhost:5149/swagger
Locate the POST /api/Chat endpoint
Click "Try it out"
Enter a query in JSON format:
json{
  "query": "What is the maternity leave policy?"
}

Click "Execute"
Observe the response containing information from the HR policy

Sample Queries
Try these example queries to test the system:

"What is the maternity leave policy?"
"How many days of annual leave do I get?"
"What are the working hours at XYZ Company?"
"Tell me about health insurance benefits"
"What happens if I want to resign?"

Verifying Database Logging
After testing queries, check the database to confirm interactions were logged:

Open SQL Server Management Studio
Connect to your SQL Server instance
Execute the following query:
sqlSELECT q.QueryID, q.QueryText, q.Timestamp,
       r.ResponseID, r.ResponseText, r.Timestamp
FROM ChatbotDB.dbo.UserQueries q
JOIN ChatbotDB.dbo.ChatbotResponses r ON q.QueryID = r.QueryID
ORDER BY q.Timestamp DESC;

Verify that all your test interactions appear in the results

Implementation Details
Python Backend (RAG Implementation)
The Python backend implements a RAG pipeline using the following components:

Document Processor (document_processor.py)

Loads HR policy documents
Splits documents into chunks based on sections and subsections
Maintains document metadata for traceability


RAG Pipeline (rag_pipeline.py)

Implements a retrieval system to find relevant document chunks
Uses keyword-based matching and scoring
Generates responses based on the retrieved content


API Server (app.py)

Provides a RESTful API endpoint (/api/chat)
Initializes the RAG pipeline on startup
Processes queries and returns responses



.NET Web API
The .NET Web API provides:

API Controller (ChatController.cs)

Exposes a POST endpoint for receiving queries
Validates input
Handles errors gracefully


Service Layer (ChatbotService.cs)

Communicates with the Python backend
Formats requests and processes responses
Calls the repository for database logging


Repository Layer (ChatRepository.cs)

Handles database operations
Logs queries and responses
Provides methods to retrieve past interactions



SQL Database
The database schema consists of:

UserQueries Table

Stores user questions with timestamps


ChatbotResponses Table

Stores chatbot responses with timestamps
Links responses to queries via foreign key


ChatInteractions View

Joins the tables for easy querying of complete interactions



Challenges and Solutions
Challenge 1: Database Schema Mismatch
The Entity Framework model was initially looking for a table named ChatInteractions instead of the separate UserQueries and ChatbotResponses tables created by the SQL script. This was resolved by:

Creating proper entity models for UserQuery and ChatbotResponse
Updating the AppDbContext to correctly map these entities to the database tables
Modifying the ChatRepository to handle the two-table structure

Challenge 2: API Communication
There were initial issues with the HttpClient in the .NET API not having a BaseAddress set. This was fixed by explicitly setting the BaseAddress in Program.cs and adding a fallback in ChatbotService.cs.
Conclusion
This implementation satisfies all the requirements specified in the LDC Technical Assessment:

It successfully integrates a Python backend using a RAG approach for answering HR policy questions
It provides a .NET Web API that handles user queries and communicates with the Python backend
It logs all interactions in a SQL database for tracking and analysis

The system demonstrates a good understanding of RAG concepts, API development, and database integration, showcasing the ability to build robust AI-powered applications with proper architecture and design patterns.
