const $ = (id) => document.getElementById(id);

async function refresh() {
  try {
    const response = await fetch('/api/stats');
    if (!response.ok) throw new Error('Server error');
    const data = await response.json();
    $('cpu').textContent = `${data.cpu.toFixed(1)}%`;
    $('ram').textContent = `${data.ram.toFixed(1)}%`;
    $('ram-detail').textContent = `${data.ram_used_gb} GB of ${data.ram_total_gb} GB`;
    $('cpu-bar').style.width = `${data.cpu}%`;
    $('ram-bar').style.width = `${data.ram}%`;
    $('chart').replaceChildren(...data.history.map((sample) => {
      const column = document.createElement('div');
      column.className = 'column';
      column.title = `${new Date(sample.time * 1000).toLocaleTimeString()} · CPU ${sample.cpu}% · RAM ${sample.ram}%`;
      column.innerHTML = `<div class="cpu-line" style="height:${sample.cpu}%"></div><div class="ram-line" style="height:${sample.ram}%"></div>`;
      return column;
    }));
    $('status').textContent = `Live · ${new Date().toLocaleTimeString()}`;
    $('status').className = 'live';
  } catch (error) {
    $('status').textContent = 'Disconnected · retrying';
    $('status').className = 'offline';
  }
}

refresh();
setInterval(refresh, 5000);
