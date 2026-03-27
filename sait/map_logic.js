// --- CALIBRATION ---
const METERS_PER_SECOND = 0.25; 
const DEGREES_PER_SECOND = 45;   

const map = L.map('map').setView([42.6977, 23.3219], 18);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 21 }).addTo(map);

let points = [];
let markers = []; // За да можем да ги трием
let lines = [];   // За да можем да ги трием
let lastPoint = null;
let currentHeading = 0; 

// Свързване на бутоните от HTML
document.getElementById('sendBtn').onclick = processAndSendPath;
document.getElementById('eraseBtn').onclick = clearMap;

function getBearing(p1, p2) {
    const lat1 = p1.lat * Math.PI / 180;
    const lat2 = p2.lat * Math.PI / 180;
    const lon1 = p1.lng * Math.PI / 180;
    const lon2 = p2.lng * Math.PI / 180;
    const y = Math.sin(lon2 - lon1) * Math.cos(lat2);
    const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(lon2 - lon1);
    return (Math.atan2(y, x) * 180 / Math.PI + 360) % 360;
}

map.on("click", function(e) {
    const latlng = e.latlng;
    
    if (lastPoint) {
        const dist = latlng.distanceTo(lastPoint);
        let line = L.polyline([lastPoint, latlng], {color: '#f44336', weight: 5}).addTo(map)
                    .bindTooltip(`${dist.toFixed(1)}m`, {permanent: true, direction: 'center'});
        lines.push(line);
    }
    
    let marker = L.circleMarker(latlng, {radius: 6, color: '#4CAF50', fillOpacity: 1}).addTo(map);
    markers.push(marker);
    
    points.push(latlng);
    lastPoint = latlng;
    updateStats();
});

function updateStats() {
    document.getElementById('stats').innerText = `Точки: ${points.length}`;
}

// ФУНКЦИЯ ЗА ПРАЩАНЕ
async function processAndSendPath() {
    if (points.length < 2) return alert("Първо начертайте път!");

    let commands = [];
    let tempHeading = currentHeading;

    for (let i = 0; i < points.length - 1; i++) {
        const p1 = points[i];
        const p2 = points[i+1];

        const distance = p1.distanceTo(p2);
        const targetHeading = getBearing(p1, p2);

        let turnAngle = targetHeading - tempHeading;
        if (turnAngle > 180) turnAngle -= 360;
        if (turnAngle < -180) turnAngle += 360;

        const turnTime = Math.abs(turnAngle) / DEGREES_PER_SECOND;
        const driveTime = distance / METERS_PER_SECOND;

        if (Math.abs(turnAngle) > 5) {
            commands.push({ action: turnAngle > 0 ? "right" : "left", time: turnTime });
        }
        commands.push({ action: "forward", time: driveTime });
        tempHeading = targetHeading;
    }

    // Изпращане към Flask сървъра
    try {
        const response = await fetch('http://localhost:5000/save-path', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(commands)
        });
        
        if (response.ok) {
            alert("Маршрутът е изпратен успешно!");
        } else {
            alert("Сървърна грешка!");
        }
    } catch (e) {
        console.error(e);
        alert("Няма връзка със сървъра (map.py работи ли?)");
    }
}

// ФУНКЦИЯ ЗА ИЗТРИВАНЕ
function clearMap() {
    points = [];
    lastPoint = null;
    markers.forEach(m => map.removeLayer(m));
    lines.forEach(l => map.removeLayer(l));
    markers = [];
    lines = [];
    updateStats();
}