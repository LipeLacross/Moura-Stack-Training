namespace ProcessAutomation.Api.Models;

public class ProcessModel
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string Status { get; set; } = "pending";
    public string? Owner { get; set; }
    public int Priority { get; set; } = 0;
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public DateTime? CompletedAt { get; set; }
}

public class ProcessStep
{
    public int Id { get; set; }
    public int ProcessId { get; set; }
    public string Name { get; set; } = string.Empty;
    public int Order { get; set; }
    public string? AssignedTo { get; set; }
    public string Status { get; set; } = "pending";
    public int DurationMinutes { get; set; }
}

public class CreateProcessRequest
{
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? Owner { get; set; }
    public int Priority { get; set; }
}

public class ProcessDashboard
{
    public int TotalProcesses { get; set; }
    public int CompletedProcesses { get; set; }
    public int PendingProcesses { get; set; }
    public int InProgressProcesses { get; set; }
    public double AverageCompletionTimeHours { get; set; }
}
