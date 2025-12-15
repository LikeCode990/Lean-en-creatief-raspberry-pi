// Automatisch sensor data verversen
let autoRefreshInterval;

// Start auto-refresh bij laden pagina
window.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard geladen');
    refreshSensorData();
    startAutoRefresh();
    updateLEDStatus();
});

// Sensor data ophalen en tonen
function refreshSensorData() {
    fetch('/api/sensor')
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperature').textContent = data.temperature.toFixed(1);
            document.getElementById('humidity').textContent = data.humidity.toFixed(1);
            document.getElementById('timestamp').textContent = data.timestamp;
            
            // Status indicator
            const statusEl = document.getElementById('status');
            if (data.status === 'demo') {
                statusEl.textContent = '⚠️ Demo modus - Geen sensor aangesloten';
                statusEl.className = 'sensor-status demo';
            } else {
                statusEl.textContent = '✅ Sensor actief';
                statusEl.className = 'sensor-status success';
            }
            
            console.log('Sensor data bijgewerkt:', data);
        })
        .catch(error => {
            console.error('Fout bij ophalen sensor data:', error);
            document.getElementById('status').textContent = '❌ Verbindingsfout';
            document.getElementById('status').className = 'sensor-status demo';
        });
}

// Auto-refresh starten
function startAutoRefresh() {
    // Ververs elke 5 seconden
    autoRefreshInterval = setInterval(refreshSensorData, 5000);
    console.log('Auto-refresh gestart (elke 5 seconden)');
}

// Auto-refresh stoppen
function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        console.log('Auto-refresh gestopt');
    }
}

// LED toggle
function toggleLED(ledNum) {
    fetch(`/api/led/${ledNum}/toggle`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(`LED ${ledNum} toggled:`, data);
        updateLEDIndicator(ledNum, data.state);
    })
    .catch(error => {
        console.error(`Fout bij toggle LED ${ledNum}:`, error);
        alert('Fout bij bedienen LED');
    });
}

// LED naar specifieke state zetten
function setLED(ledNum, state) {
    fetch(`/api/led/${ledNum}/state`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ state: state })
    })
    .then(response => response.json())
    .then(data => {
        console.log(`LED ${ledNum} set to ${state}:`, data);
        updateLEDIndicator(ledNum, data.state);
    })
    .catch(error => {
        console.error(`Fout bij zetten LED ${ledNum}:`, error);
        alert('Fout bij bedienen LED');
    });
}

// LED indicator bijwerken
function updateLEDIndicator(ledNum, state) {
    const indicator = document.getElementById(`led${ledNum}-indicator`);
    if (state) {
        indicator.classList.add('on');
    } else {
        indicator.classList.remove('on');
    }
}

// Status van alle LEDs ophalen
function updateLEDStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            updateLEDIndicator(1, data.led1);
            updateLEDIndicator(2, data.led2);
            console.log('LED status bijgewerkt:', data);
        })
        .catch(error => {
            console.error('Fout bij ophalen LED status:', error);
        });
}

// Keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // Spatiebalk = refresh sensor data
    if (event.code === 'Space' && event.target === document.body) {
        event.preventDefault();
        refreshSensorData();
        console.log('Sensor data handmatig vernieuwd (spatiebalk)');
    }
    
    // 1 = toggle LED 1
    if (event.key === '1') {
        toggleLED(1);
    }
    
    // 2 = toggle LED 2
    if (event.key === '2') {
        toggleLED(2);
    }
});

// Console melding
console.log('Raspberry Pi Dashboard JavaScript geladen');
console.log('Toetsenbord shortcuts:');
console.log('- Spatiebalk: Ververs sensor data');
console.log('- 1: Toggle LED 1');
console.log('- 2: Toggle LED 2');
