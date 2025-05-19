using ChatbotAPI.Models;
using Microsoft.EntityFrameworkCore;

namespace ChatbotAPI.Repositories
{
    public class ChatRepository : IChatRepository
    {
        private readonly AppDbContext _context;
        private readonly ILogger<ChatRepository> _logger;

        public ChatRepository(AppDbContext context, ILogger<ChatRepository> logger)
        {
            _context = context;
            _logger = logger;
        }

        public async Task LogInteractionAsync(ChatInteraction interaction)
        {
            try
            {
                _logger.LogInformation("Logging interaction to database...");
                
                // Create and save the UserQuery
                var userQuery = new UserQuery
                {
                    QueryText = interaction.Query,
                    Timestamp = interaction.Timestamp
                };
                
                _context.UserQueries.Add(userQuery);
                await _context.SaveChangesAsync();
                
                _logger.LogInformation("User query saved with ID: {QueryID}", userQuery.QueryID);
                
                // Create and save the ChatbotResponse
                var chatbotResponse = new ChatbotResponse
                {
                    QueryID = userQuery.QueryID,
                    ResponseText = interaction.Response,
                    Timestamp = interaction.Timestamp
                };
                
                _context.ChatbotResponses.Add(chatbotResponse);
                await _context.SaveChangesAsync();
                
                _logger.LogInformation("Chatbot response saved with ID: {ResponseID}", chatbotResponse.ResponseID);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error logging interaction");
                throw;
            }
        }

        public async Task<IEnumerable<ChatInteraction>> GetInteractionsAsync()
        {
            // Join UserQueries and ChatbotResponses to create ChatInteraction objects
            var interactions = await (from q in _context.UserQueries
                                     join r in _context.ChatbotResponses
                                     on q.QueryID equals r.QueryID
                                     select new ChatInteraction
                                     {
                                         Id = q.QueryID,
                                         Query = q.QueryText,
                                         Response = r.ResponseText,
                                         Timestamp = q.Timestamp
                                     }).OrderByDescending(i => i.Timestamp).ToListAsync();
            
            return interactions;
        }
    }
}