using ProcessAutomation.Api.Models;

namespace ProcessAutomation.Api.Services;

public class ProcessService
{
    private readonly List<ProcessModel> _processes = new();
    private readonly List<ProcessStep> _steps = new();
    private int _nextProcessId = 1;
    private int _nextStepId = 1;

    public ProcessModel Create(CreateProcessRequest request)
    {
        var process = new ProcessModel
        {
            Id = _nextProcessId++,
            Name = request.Name,
            Description = request.Description,
            Owner = request.Owner,
            Priority = request.Priority,
            Status = "pending",
            CreatedAt = DateTime.UtcNow
        };
        _processes.Add(process);
        return process;
    }

    public ProcessModel? GetById(int id) => _processes.FirstOrDefault(p => p.Id == id);

    public List<ProcessModel> GetAll() => _processes;

    public ProcessModel? UpdateStatus(int id, string status)
    {
        var process = GetById(id);
        if (process == null) return null;

        process.Status = status;
        if (status == "completed")
            process.CompletedAt = DateTime.UtcNow;

        return process;
    }

    public ProcessModel? Delete(int id)
    {
        var process = GetById(id);
        if (process != null)
            _processes.Remove(process);
        return process;
    }

    public ProcessStep AddStep(int processId, string name, int order, int durationMinutes)
    {
        var step = new ProcessStep
        {
            Id = _nextStepId++,
            ProcessId = processId,
            Name = name,
            Order = order,
            DurationMinutes = durationMinutes,
            Status = "pending"
        };
        _steps.Add(step);
        return step;
    }

    public List<ProcessStep> GetSteps(int processId) =>
        _steps.Where(s => s.ProcessId == processId).OrderBy(s => s.Order).ToList();

    public ProcessDashboard GetDashboard()
    {
        var completed = _processes.Where(p => p.Status == "completed").ToList();
        var avgHours = completed.Any()
            ? completed.Average(p => (p.CompletedAt!.Value - p.CreatedAt).TotalHours)
            : 0;

        return new ProcessDashboard
        {
            TotalProcesses = _processes.Count,
            CompletedProcesses = completed.Count,
            PendingProcesses = _processes.Count(p => p.Status == "pending"),
            InProgressProcesses = _processes.Count(p => p.Status == "in_progress"),
            AverageCompletionTimeHours = Math.Round(avgHours, 2)
        };
    }
}
