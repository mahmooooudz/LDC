// ChatbotAPI/Services/IChatbotService.cs
using ChatbotAPI.Models;

namespace ChatbotAPI.Services
{
    public interface IChatbotService
    {
        Task<ChatResponse> GetChatResponseAsync(ChatQuery query);
    }
}