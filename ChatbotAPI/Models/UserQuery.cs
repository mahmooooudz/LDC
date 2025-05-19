namespace ChatbotAPI.Models
{
    public class UserQuery
    {
        public int QueryID { get; set; }
        public string? QueryText { get; set; }
        public DateTime Timestamp { get; set; }
    }
}