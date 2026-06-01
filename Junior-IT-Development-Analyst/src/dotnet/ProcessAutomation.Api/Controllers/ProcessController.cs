using Microsoft.AspNetCore.Mvc;
using ProcessAutomation.Api.Models;
using ProcessAutomation.Api.Services;

namespace ProcessAutomation.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProcessController : ControllerBase
{
    private readonly ProcessService _service;

    public ProcessController()
    {
        _service = new ProcessService();
    }

    [HttpGet]
    public ActionResult<List<ProcessModel>> GetAll()
    {
        return Ok(_service.GetAll());
    }

    [HttpGet("{id}")]
    public ActionResult<ProcessModel> GetById(int id)
    {
        var process = _service.GetById(id);
        if (process == null)
            return NotFound(new { message = $"Processo {id} não encontrado" });
        return Ok(process);
    }

    [HttpPost]
    public ActionResult<ProcessModel> Create([FromBody] CreateProcessRequest request)
    {
        var process = _service.Create(request);
        return CreatedAtAction(nameof(GetById), new { id = process.Id }, process);
    }

    [HttpPatch("{id}/status")]
    public ActionResult<ProcessModel> UpdateStatus(int id, [FromBody] string status)
    {
        var validStatuses = new[] { "pending", "in_progress", "completed", "cancelled" };
        if (!validStatuses.Contains(status))
            return BadRequest(new { message = $"Status inválido: {status}" });

        var process = _service.UpdateStatus(id, status);
        if (process == null)
            return NotFound(new { message = $"Processo {id} não encontrado" });
        return Ok(process);
    }

    [HttpDelete("{id}")]
    public ActionResult Delete(int id)
    {
        var process = _service.Delete(id);
        if (process == null)
            return NotFound(new { message = $"Processo {id} não encontrado" });
        return NoContent();
    }

    [HttpGet("{id}/steps")]
    public ActionResult<List<ProcessStep>> GetSteps(int id)
    {
        if (_service.GetById(id) == null)
            return NotFound(new { message = $"Processo {id} não encontrado" });
        return Ok(_service.GetSteps(id));
    }

    [HttpPost("{id}/steps")]
    public ActionResult<ProcessStep> AddStep(int id, [FromBody] ProcessStep step)
    {
        if (_service.GetById(id) == null)
            return NotFound(new { message = $"Processo {id} não encontrado" });

        var created = _service.AddStep(id, step.Name, step.Order, step.DurationMinutes);
        return CreatedAtAction(nameof(GetSteps), new { id }, created);
    }

    [HttpGet("dashboard")]
    public ActionResult<ProcessDashboard> GetDashboard()
    {
        return Ok(_service.GetDashboard());
    }
}
