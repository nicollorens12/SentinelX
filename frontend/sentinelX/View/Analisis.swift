import SwiftUI
import Charts

struct NetworkScanView: View {
    @State private var isScanning = false
    @State private var scanStartTime: Date? = nil
    @State private var scanEndTime: Date? = nil
    @State private var scanDuration: TimeInterval = 10 // Duración predeterminada de 10 segundos
    @State private var trafficData: [TrafficData] = [] // Datos del tráfico de red
    @State private var scanProgress = "Escaneo inactivo"
    @State private var tableData: [ScanData] = [] // Datos de la tabla
    @State private var timer: Timer?
    
    var body: some View {
        VStack(spacing: 20) {
            // Sección de Botones
            HStack(spacing: 20) {
                // Botón de Iniciar Escaneo
                Button(action: startScan) {
                    Label("Iniciar", systemImage: "play.circle.fill")
                        .font(.title3)
                        .foregroundColor(.white)
                        .padding()
                        .background(isScanning ? Color.gray : Color.blue)
                        .cornerRadius(10)
                        .animation(.easeInOut, value: isScanning)
                }
                .buttonStyle(PlainButtonStyle())
                
                
                // Botón de Finalizar Escaneo
                Button(action: stopScan) {
                    Label("Finalizar", systemImage: "stop.circle.fill")
                        .font(.title3)
                        .foregroundColor(.white)
                        .padding()
                        .background(isScanning ? Color.red : Color.gray)
                        .cornerRadius(10)
                        .animation(.easeInOut, value: isScanning)
                }
                .buttonStyle(PlainButtonStyle())
                
                Button(action: {
                    stopScan()// Cierra la respuesta al hacer clic en "X"
                }) {
                    Image(systemName: "gearshape.fill")
                        .foregroundColor(.white)
                        .font(.system(size: 16, weight: .bold))
                        .padding(8)
                }
                .padding(.top, 8) // Alineación para que no se sobreponga
                .padding(.trailing, 8)
                
                // Botón de Configuración
                Menu {
                    Button(action: { scanDuration = 5 }) { Text("Duración: 5 seg") }
                    Button(action: { scanDuration = 10 }) { Text("Duración: 10 seg") }
                    Button(action: { scanDuration = 20 }) { Text("Duración: 20 seg") }
                } label: {
                    Image(systemName: "gearshape.fill")
                        .font(.title)
                        .foregroundColor(.gray)
                        .padding()
                        .background(Color(.gray))
                        .clipShape(Circle())
                }
                .frame(minWidth: 0, maxWidth: 50)
            }
            
            // Gráfico de Tráfico de Red en Tiempo Real
            ScrollView(.horizontal) {
                ZStack(alignment: .bottomLeading) {
                    Chart(trafficData) { data in
                        LineMark(
                            x: .value("Tiempo", data.timestamp),
                            y: .value("Tráfico", data.traffic)
                        )
                        .foregroundStyle(Color.blue.gradient)
                    }
                    .chartXAxis {
                        AxisMarks(values: .stride(by: .second))
                    }
                    .chartYScale(domain: 0...150)
                    .frame(height: 200)
                    
                    // Marcadores de Inicio y Fin de Escaneo
                    if let start = scanStartTime {
                        Text("Inicio")
                            .font(.caption)
                            .foregroundColor(.blue)
                            .position(x: 20, y: 20)
                            .transition(.opacity)
                    }
                    if let end = scanEndTime {
                        Text("Fin")
                            .font(.caption)
                            .foregroundColor(.red)
                            .position(x: 200, y: 20)
                            .transition(.opacity)
                    }
                }
            }
            .frame(height: 200)
            .background(Color(.gray))
            .cornerRadius(10)
            .shadow(radius: 5)
            
            // Estado de Escaneo
            HStack {
                Text("Estado: \(scanProgress)")
                    .foregroundColor(.gray)
                    .font(.headline)
                Spacer()
                if isScanning {
                    Text("Tiempo restante: \(Int(scanDuration))s")
                        .foregroundColor(.gray)
                        .font(.subheadline)
                        .transition(.opacity)
                }
            }
            .padding()
            
            // Tabla de Datos Obtenidos
            VStack(alignment: .leading) {
                Text("Datos Obtenidos del Escaneo")
                    .font(.headline)
                    .padding(.bottom, 5)
                
                /*
                List($tableData) { entry in
                    HStack {
                        Text(Date(), style: .time) // Formato de tiempo corregido
                        Spacer()
                        Text("IP Origen: \(entry.sourceIP)")
                        Spacer()
                        Text("IP Destino: \(entry.destinationIP)")
                        Spacer()
                        Text("Protocolo: \(entry.protocol)")
                        Spacer()
                        Text("Puerto: \(entry.port)")
                        Spacer()
                        Text("\(entry.traffic, specifier: "%.2f") Mbps")
                    }
                }
                .frame(height: 250) // Limita la altura de la tabla
                 */
            }
            .padding()
            
            Spacer()
        }
        .padding()
    }
    
    // Función para iniciar el escaneo
    private func startScan() {
        isScanning = true
        scanStartTime = Date()
        scanProgress = "Escaneo en progreso"
        trafficData.removeAll()
        tableData.removeAll()
        
        // Simula datos en tiempo real
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { timer in
            let currentTime = Date()
            let trafficValue = Double.random(in: 50...100)
            let trafficDataPoint = TrafficData(timestamp: currentTime, traffic: trafficValue)
            trafficData.append(trafficDataPoint)
            tableData.append(
                ScanData(
                    timestamp: currentTime,
                    traffic: trafficValue,
                    sourceIP: "192.168.1.\(Int.random(in: 1...255))",
                    destinationIP: "10.0.0.\(Int.random(in: 1...255))",
                    protocol2: ["TCP", "UDP"].randomElement()!,
                    port: Int.random(in: 1024...65535)
                )
            )
            
            if currentTime.timeIntervalSince(scanStartTime!) >= scanDuration {
                stopScan()
                timer.invalidate()
            }
        }
    }
    
    // Función para finalizar el escaneo
    private func stopScan() {
        isScanning = false
        scanEndTime = Date()
        scanProgress = "Escaneo completado"
    }
}

// Datos simulados de tráfico de red
struct TrafficData: Identifiable {
    let id = UUID()
    let timestamp: Date
    let traffic: Double
}

// Datos de la tabla con más detalles
struct ScanData: Identifiable {
    let id = UUID()
    var timestamp: Date
    let traffic: Double
    var sourceIP: String
    var destinationIP: String
    let protocol2: String
    let port: Int
}

#Preview {
    NetworkScanView()
}
