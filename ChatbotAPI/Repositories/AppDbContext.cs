using ChatbotAPI.Models;
using Microsoft.EntityFrameworkCore;

namespace ChatbotAPI.Repositories
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        public DbSet<UserQuery> UserQueries { get; set; }
        public DbSet<ChatbotResponse> ChatbotResponses { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Configure UserQueries entity
            modelBuilder.Entity<UserQuery>()
                .ToTable("UserQueries")
                .HasKey(q => q.QueryID);
            
            modelBuilder.Entity<UserQuery>()
                .Property(q => q.QueryText)
                .IsRequired();
            
            modelBuilder.Entity<UserQuery>()
                .Property(q => q.Timestamp)
                .IsRequired();
            
            // Configure ChatbotResponses entity
            modelBuilder.Entity<ChatbotResponse>()
                .ToTable("ChatbotResponses")
                .HasKey(r => r.ResponseID);
            
            modelBuilder.Entity<ChatbotResponse>()
                .Property(r => r.ResponseText)
                .IsRequired();
            
            modelBuilder.Entity<ChatbotResponse>()
                .Property(r => r.Timestamp)
                .IsRequired();
            
            modelBuilder.Entity<ChatbotResponse>()
                .HasOne<UserQuery>()
                .WithMany()
                .HasForeignKey(r => r.QueryID)
                .IsRequired();
        }
    }
}