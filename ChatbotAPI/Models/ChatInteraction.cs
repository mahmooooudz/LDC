// ChatbotAPI/Models/ChatInteraction.cs
namespace ChatbotAPI.Models
{
    public class ChatInteraction
    {
        public int Id { get; set; }
        public string? Query { get; set; }
        public string? Response { get; set; }
        public DateTime Timestamp { get; set; }
    }
}