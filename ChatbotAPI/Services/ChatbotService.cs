using ChatbotAPI.Models;
using ChatbotAPI.Repositories;
using System.Net.Http.Json;
using System.Text.Json;

namespace ChatbotAPI.Services
{
    public class ChatbotService : IChatbotService
    {
        private readonly HttpClient _httpClient;
        private readonly IChatRepository _chatRepository;
        private readonly ILogger<ChatbotService> _logger;

        public ChatbotService(HttpClient httpClient, IChatRepository chatRepository, ILogger<ChatbotService> logger)
        {
            _httpClient = httpClient;
            _chatRepository = chatRepository;
            _logger = logger;
        }

        public async Task<ChatResponse> GetChatResponseAsync(ChatQuery query)
        {
            try
            {
                _logger.LogInformation("Processing query: {Query}", query.Query);
                
                // Verify that the BaseAddress is set
                if (_httpClient.BaseAddress == null)
                {
                    _logger.LogWarning("HttpClient BaseAddress is not set. Setting it to default: http://localhost:8000");
                    _httpClient.BaseAddress = new Uri("http://localhost:8000");
                }

                // Send the query to the Python backend
                var response = await _httpClient.PostAsJsonAsync("api/chat", query);
                response.EnsureSuccessStatusCode();
                
                var chatResponse = await response.Content.ReadFromJsonAsync<ChatResponse>();
                
                if (chatResponse == null)
                {
                    _logger.LogError("Received null response from Python backend");
                    throw new Exception("Received null response from Python backend");
                }
                
                // Log the interaction to the database
                await _chatRepository.LogInteractionAsync(
                    new ChatInteraction 
                    { 
                        Query = query.Query, 
                        Response = chatResponse.Response, 
                        Timestamp = DateTime.UtcNow 
                    });
                
                return chatResponse;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting chat response");
                throw;
            }
        }
    }
}