// ChatbotAPI/Repositories/IChatRepository.cs
using ChatbotAPI.Models;

namespace ChatbotAPI.Repositories
{
    public interface IChatRepository
    {
        Task LogInteractionAsync(ChatInteraction interaction);
        Task<IEnumerable<ChatInteraction>> GetInteractionsAsync();
    }
}