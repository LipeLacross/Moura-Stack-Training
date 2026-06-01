const api = new MouraApiClient('http://localhost:8000');
let chartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    loadProcesses();
    setupForms();
});

async function loadDashboard() {
    try {
        const processes = await api.getProcesses();
        const total = processes.length;
        const concluidos = processes.filter(p => p.status === 'completed' || p.description?.includes('conclu')).length;
        const pendentes = processes.filter(p => p.status === 'pending' || p.description?.includes('pendente')).length;
        const andamento = total - concluidos - pendentes;

        document.getElementById('total-processos').textContent = total;
        document.getElementById('concluidos').textContent = concluidos;
        document.getElementById('pendentes').textContent = pendentes;
        document.getElementById('andamento').textContent = andamento;

        renderChart([concluidos, pendentes, andamento]);
    } catch (err) {
        console.warn('Dashboard offline, usando dados mock');
        document.querySelectorAll('#kpi-container h3').forEach(el => el.textContent = '--');
    }
}

function renderChart(data) {
    const ctx = document.getElementById('chart-processos').getContext('2d');
    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Concluídos', 'Pendentes', 'Em Andamento'],
            datasets: [{
                data: data,
                backgroundColor: ['#22c55e', '#f59e0b', '#3b82f6'],
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } }
        }
    });
}

async function loadProcesses() {
    try {
        const processes = await api.getProcesses();
        const tbody = document.getElementById('processos-body');
        tbody.innerHTML = '';

        processes.forEach(p => {
            const tr = document.createElement('tr');
            const statusClass = p.status === 'completed' || p.description?.includes('conclu') ? 'concluido'
                : p.status === 'pending' || p.description?.includes('pendente') ? 'pendente' : 'andamento';
            tr.innerHTML = `
                <td>${p.id || '-'}</td>
                <td>${p.name}</td>
                <td><span class="status-badge ${statusClass}">${p.status || 'pending'}</span></td>
                <td>${p.description || '-'}</td>
                <td>${p.created_at ? new Date(p.created_at).toLocaleDateString() : '-'}</td>
                <td><button class="outline" onclick="deleteProcess(${p.id})">Excluir</button></td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        document.getElementById('processos-body').innerHTML =
            '<tr><td colspan="6">API indisponível. Inicie o servidor com: uvicorn src.python.api.main:app --reload</td></tr>';
    }
}

function setupForms() {
    document.getElementById('form-processo').addEventListener('submit', async (e) => {
        e.preventDefault();
        const nome = document.getElementById('nome-processo').value;
        const desc = document.getElementById('descricao-processo').value;
        const resp = document.getElementById('responsavel-processo').value;
        try {
            await api.createProcess({ name: nome, description: desc, owner: resp });
            e.target.reset();
            loadProcesses();
            loadDashboard();
        } catch (err) {
            alert('Erro ao criar processo: ' + err.message);
        }
    });

    document.getElementById('form-integracao').addEventListener('submit', async (e) => {
        e.preventDefault();
        const origem = document.getElementById('origem').value;
        const destino = document.getElementById('destino').value;
        const payloadRaw = document.getElementById('payload-integracao').value || '{"items":[]}';
        try {
            const payload = JSON.parse(payloadRaw);
            const result = await api.syncSystems(origem, destino, payload);
            document.getElementById('resultado-integracao').textContent =
                JSON.stringify(result, null, 2);
        } catch (err) {
            document.getElementById('resultado-integracao').textContent =
                `Erro: ${err.message}`;
        }
    });
}

async function deleteProcess(id) {
    if (!confirm('Excluir processo?')) return;
    try {
        await api.deleteProcess(id);
        loadProcesses();
        loadDashboard();
    } catch (err) {
        alert('Erro ao excluir: ' + err.message);
    }
}
