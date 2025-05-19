-- SQL Database Schema for Chatbot System

-- Create the database
CREATE DATABASE ChatbotDB;
GO

USE ChatbotDB;
GO

-- Create the UserQueries table to store user questions
CREATE TABLE UserQueries (
    QueryID INT IDENTITY(1,1) PRIMARY KEY,
    QueryText NVARCHAR(MAX) NOT NULL,
    Timestamp DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);

-- Create the ChatbotResponses table to store chatbot responses
CREATE TABLE ChatbotResponses (
    ResponseID INT IDENTITY(1,1) PRIMARY KEY,
    QueryID INT NOT NULL,
    ResponseText NVARCHAR(MAX) NOT NULL,
    Timestamp DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FOREIGN KEY (QueryID) REFERENCES UserQueries(QueryID)
);

-- Create a view for easy querying of complete interactions
CREATE VIEW ChatInteractions AS
SELECT 
    q.QueryID,
    q.QueryText,
    q.Timestamp AS QueryTimestamp,
    r.ResponseID,
    r.ResponseText,
    r.Timestamp AS ResponseTimestamp
FROM 
    UserQueries q
JOIN 
    ChatbotResponses r ON q.QueryID = r.QueryID;

-- Create a stored procedure for logging a complete interaction
CREATE PROCEDURE LogChatInteraction
    @QueryText NVARCHAR(MAX),
    @ResponseText NVARCHAR(MAX)
AS
BEGIN
    DECLARE @QueryID INT;
    
    -- Insert the query
    INSERT INTO UserQueries (QueryText, Timestamp)
    VALUES (@QueryText, GETUTCDATE());
    
    -- Get the inserted query ID
    SET @QueryID = SCOPE_IDENTITY();
    
    -- Insert the response
    INSERT INTO ChatbotResponses (QueryID, ResponseText, Timestamp)
    VALUES (@QueryID, @ResponseText, GETUTCDATE());
    
    -- Return the IDs
    SELECT @QueryID AS QueryID, SCOPE_IDENTITY() AS ResponseID;
END;
GO

-- Create indexes for better performance
CREATE INDEX IX_UserQueries_Timestamp ON UserQueries(Timestamp);
CREATE INDEX IX_ChatbotResponses_Timestamp ON ChatbotResponses(Timestamp);
CREATE INDEX IX_ChatbotResponses_QueryID ON ChatbotResponses(QueryID);