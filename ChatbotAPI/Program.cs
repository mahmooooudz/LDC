using ChatbotAPI.Repositories;
using ChatbotAPI.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Configure database
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Configure HTTP client for Python backend
builder.Services.AddHttpClient<IChatbotService, ChatbotService>(client =>
{
    // Explicitly set the base address to the Python backend URL
    client.BaseAddress = new Uri("http://localhost:8000");
});

// Register repositories and services
builder.Services.AddScoped<IChatRepository, ChatRepository>();
builder.Services.AddScoped<IChatbotService, ChatbotService>();

// Add CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll",
        builder => builder.AllowAnyOrigin()
            .AllowAnyMethod()
            .AllowAnyHeader());
});

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors("AllowAll");
app.UseAuthorization();
app.MapControllers();

app.Run();