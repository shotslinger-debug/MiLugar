// Referencia al contenedor principal de HTML
const appContainer = document.getElementById('app-container');

// DATOS SIMULADOS
const rutasDisponibles = [
    { id: 1, nombre: "Tuxtla vía JOBO", proxima_salida: "10:15 AM", unidad: "12" },
    { id: 2, nombre: "Tuxtla vía TERÁN", proxima_salida: "10:30 AM", unidad: "05" }
];

// VISTA 1: Lista de Rutas
function renderRutas() {
    let html = `
        <h2 class="rutas-title">Selecciona tu ruta</h2>
        <div>
    `;
    
    rutasDisponibles.forEach(ruta => {
        html += `
            <div class="ruta-card" onclick="renderAsientos(${ruta.id})">
                <h3 class="ruta-card-title">${ruta.nombre}</h3>
                <div class="ruta-info">
                    <span>Unidad: <span class="highlight-dark">#${ruta.unidad}</span></span>
                    <span>Salida: <span class="highlight-red">${ruta.proxima_salida}</span></span>
                </div>
            </div>
        `;
    });
    
    html += `
        </div>
        
        <!-- Publicidad central para rellenar espacio vacío -->
        <div class="inline-ad" onclick="alert('Visita a nuestro patrocinador')">
            <span class="inline-ad-tag">Cafetería Local</span>
            <div style="display:flex; justify-content:center;">
                <img src="assets/cafe.png" alt="Promo Café" width="55">
            </div>
            <h3 class="inline-ad-title">¿Café para el camino?</h3>
            <p class="inline-ad-text">Pasa por tu americano caliente. Muestra esta app y te regalamos un pan dulce para tu viaje.</p>
        </div>
    `;
    
    appContainer.innerHTML = html;
}

// VISTA 2: Croquis de Asientos
function renderAsientos(rutaId) {
    const ruta = rutasDisponibles.find(r => r.id === rutaId);
    
    // Simulación de asientos ocupados
    const asientosOcupados = [1, 5, 21, 19]; 
    
    // Matriz del croquis. "null" representa el pasillo vacío.
    const layout = [
        ['Driver', 21, null, 1],
        [4, 3, null, 2],
        [7, 6, null, 5],
        [10, 9, null, 8],
        [13, 12, null, 11],
        [16, 15, null, 14],
        [20, 19, 18, 17] // Última fila completa
    ];
    
    let asientosHtml = '';
    
    layout.forEach(fila => {
        fila.forEach(asiento => {
            if (asiento === null) {
                // Espacio vacío para el pasillo
                asientosHtml += `<div class="seat empty"></div>`;
            } else if (asiento === 'Driver') {
                // Volante del chofer
                asientosHtml += `
                    <div class="seat driver">
                        <img src="assets/volante.png" alt="Volante" width="22" style="opacity: 0.7;">
                    </div>
                `;
            } else {
                // Asientos de pasajeros
                const estaOcupado = asientosOcupados.includes(asiento);
                const claseEstado = estaOcupado ? 'occupied' : 'available';
                const accionClick = !estaOcupado 
                    ? `onclick="mostrarFormulario('${asiento}', ${ruta.id})"` 
                    : '';
                    
                asientosHtml += `
                    <div class="seat ${claseEstado}" ${accionClick}>
                        ${asiento}
                    </div>
                `;
            }
        });
    });

    appContainer.innerHTML = `
        <button onclick="renderRutas()" class="btn-back" style="display:flex; align-items:center; gap:6px;">
            <img src="assets/flecha-izquierda.png" alt="Atrás" width="14"> Volver a rutas
        </button>
        
        <div class="croquis-container">
            <h2 class="croquis-title">${ruta.nombre}</h2>
            
            <div class="van-body">
                <div class="van-front-label">FRENTE</div>
                
                <div class="seat-grid">
                    ${asientosHtml}
                </div>
            </div>
            
            <div class="legend">
                <div class="legend-item"><div class="box-green"></div> Libre</div>
                <div class="legend-item"><div class="box-red"></div> Ocupado</div>
            </div>
        </div>
    `;
}

// VISTA 2.5: Formulario de Reserva
function mostrarFormulario(numAsiento, rutaId) {
    const ruta = rutasDisponibles.find(r => r.id === rutaId);
    
    appContainer.innerHTML = `
        <button onclick="renderAsientos(${rutaId})" class="btn-back" style="display:flex; align-items:center; gap:6px;">
            <img src="assets/flecha-izquierda.png" alt="Atrás" width="14"> Cancelar y volver al croquis
        </button>
        
        <div class="form-container">
            <h2 class="croquis-title">Confirmar Asiento ${numAsiento}</h2>
            <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 1rem;">
                Ingresa tu nombre para apartar tu lugar en la unidad <strong>#${ruta.unidad}</strong> de la ruta <strong>${ruta.nombre}</strong>.
            </p>
            
            <input type="text" id="nombrePasajero" class="form-input" placeholder="Ej. Juan Pérez" autocomplete="off">
            
            <button onclick="generarBoleto('${numAsiento}', ${rutaId})" class="btn-primary">Apartar Asiento</button>
        </div>
    `;
    
    // Auto-enfocar el input para mayor agilidad
    document.getElementById('nombrePasajero').focus();
}

// VISTA 3: Boleto Digital (Confirmación)
function generarBoleto(numAsiento, rutaId) {
    const inputNombre = document.getElementById('nombrePasajero');
    const nombre = inputNombre.value.trim();
    
    if (!nombre) {
        alert("Por favor, ingresa tu nombre para poder apartar el asiento.");
        return;
    }

    const ruta = rutasDisponibles.find(r => r.id === rutaId);
    
    appContainer.innerHTML = `
        <button onclick="renderRutas()" class="btn-back" style="display:flex; align-items:center; gap:6px;">
            <img src="assets/flecha-izquierda.png" alt="Atrás" width="14"> Volver al inicio
        </button>
        
        <div class="ticket">
            <div class="ticket-header" style="display:flex; flex-direction:column; align-items:center;">
                <img src="assets/check_verde.png" alt="Éxito" width="48" style="margin-bottom:8px;">
                <h2>¡Asiento Apartado!</h2>
                <p>Tu lugar está asegurado</p>
            </div>
            
            <div class="ticket-body">
                <div class="ticket-row">
                    <span class="ticket-label">Pasajero:</span>
                    <span class="ticket-value">${nombre}</span>
                </div>
                <div class="ticket-row">
                    <span class="ticket-label">Ruta:</span>
                    <span class="ticket-value">${ruta.nombre}</span>
                </div>
                <div class="ticket-row">
                    <span class="ticket-label">Unidad / Asiento:</span>
                    <span class="ticket-value">#${ruta.unidad} - Lugar ${numAsiento}</span>
                </div>
                <div class="ticket-row">
                    <span class="ticket-label">Salida Estimada:</span>
                    <span class="ticket-value highlight-red">${ruta.proxima_salida}</span>
                </div>
            </div>
            
            <!-- Publicidad de Alto Impacto -->
            <div class="ticket-ad">
                <h3 class="ticket-ad-title" style="display:flex; justify-content:center; align-items:center; gap:8px;">
                    <img src="assets/confeti.png" alt="Felicidades" width="24"> ¡Felicidades!
                </h3>
                <p class="ticket-ad-text">Muestra este boleto en <strong>Cafetería La Base</strong> y obtén un 2x1 en tu bebida mientras esperas tu salida.</p>
                <div class="ad-tag">Anuncio Patrocinado</div>
            </div>
        </div>
    `;
}

// Inicializar la aplicación
renderRutas();
