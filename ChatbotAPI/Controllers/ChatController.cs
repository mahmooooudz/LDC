// ChatbotAPI/Controllers/ChatController.cs
using ChatbotAPI.Models;
using ChatbotAPI.Services;
using Microsoft.AspNetCore.Mvc;

namespace ChatbotAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ChatController : ControllerBase
    {
        private readonly IChatbotService _chatbotService;
        private readonly ILogger<ChatController> _logger;

        public ChatController(IChatbotService chatbotService, ILogger<ChatController> logger)
        {
            _chatbotService = chatbotService;
            _logger = logger;
        }

        [HttpPost]
        public async Task<ActionResult<ChatResponse>> Post([FromBody] ChatQuery query)
        {
            if (string.IsNullOrWhiteSpace(query.Query))
            {
                return BadRequest("Query cannot be empty");
            }

            try
            {
                var response = await _chatbotService.GetChatResponseAsync(query);
                return Ok(response);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing chat query");
                return StatusCode(500, "An error occurred while processing your request");
            }
        }
    }
}