namespace ChatbotAPI.Models
{
    public class ChatbotResponse
    {
        public int ResponseID { get; set; }
        public int QueryID { get; set; }
        public string? ResponseText { get; set; }
        public DateTime Timestamp { get; set; }
    }
}