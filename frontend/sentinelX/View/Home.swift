import SwiftUI

struct Home: View {
    @Binding var width: CGFloat
    @Binding var height: CGFloat
    var body: some View {
        // Safely unwrap the window frame
        HStack(alignment: .top, spacing:-20){
            VStack(spacing:10){
                SecurityCardView()
                    .frame(maxWidth: width*0.4, maxHeight: height*0.5)
                ActiveAlertsCardView()
                    .frame(maxWidth: width*0.4, maxHeight: height*0.5)
            }
            VStack(alignment: .leading, spacing:-5){
                NetworkTrafficCardView()
                    .frame(maxWidth: width*0.6, maxHeight: height*0.55)
                HStack(alignment: .top){
                    SOCResponseTimesCardView()
                    LogsPanelCardView()
                }
                .frame(maxWidth: width*0.6, maxHeight: height*0.45)
                .padding()
            }
        }
    }
}

// Preview provider
#Preview {
    Home(width: Binding.constant(1000), height: Binding.constant(1000))
}

struct SecurityCardView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            
            Text("Estado general del sistema")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.black)
                .padding(.bottom, 10)
            
            SectionView(icon: "shield.lefthalf.filled.trianglebadge.exclamationmark",
                        title: "Amenazas activas",
                        color: .red,
                        value: "3",
                        subtitle: "Críticas y urgentes")
            SectionView(icon: "flag.badge.ellipsis",
                        title: "Amenazas pendientes de acción",
                        color: .orange,
                        value: "5",
                        subtitle: "En proceso de análisis")
            SectionView(icon: "checkmark.rectangle.stack.fill",
                        title: "Amenazas resueltas",
                        color: .green,
                        value: "25",
                        subtitle: "Última en menos de 1h")
            
            SectionView(icon: "timer",
                        title: "Última actualización",
                        color: .purple,
                        value: "10:45 AM",
                        subtitle: "Hace 5 minutos")
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(Color.white)
                .shadow(color: Color.black.opacity(0.1), radius: 10, x: 0, y: 5)
        )
        .padding(.horizontal)
    }
}

struct SectionView: View {
    var icon: String
    var title: String
    var color: Color
    var value: String
    var subtitle: String
    
    var body: some View {
        HStack(spacing: 15) {
            Image(systemName: icon)
                .foregroundColor(color)
                .font(.system(size: 24))
                .frame(width: 40, height: 40)
                .background(color.opacity(0.2))
                .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 5) {
                HStack {
                    Text(title)
                        .foregroundColor(.black)
                        .font(.body)
                        .fontWeight(.semibold)
                    
                    Spacer()
                }
                
                Text(subtitle)
                    .foregroundColor(.gray)
                    .font(.footnote)
            }
            Text(value)
                .font(title == "Última actualización" ? .body : .title)
                .fontWeight(.bold)
                .foregroundColor(color)
                .padding(.leading)
            Spacer()
        }
    }
}

struct NetworkTrafficCardView: View {
    @State private var trafficData: [CGFloat] = Array(repeating: 0, count: 30) // Datos simulados
    @State private var maxTraffic: CGFloat = 100 // Máximo del gráfico

    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Tráfico de Red")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.black)
                .padding(.bottom, 10)
            
            LineGraph(data: trafficData, maxDataValue: maxTraffic)
                .stroke(
                    LinearGradient(gradient: Gradient(colors: [Color.blue, Color.cyan]), startPoint: .leading, endPoint: .trailing),
                    lineWidth: 2
                )
                .frame(height: 200)
                .padding(.vertical, 10)
            
            HStack {
                Text("Máximo: \(Int(maxTraffic)) Mbps")
                    .font(.footnote)
                    .foregroundColor(.gray)
                Spacer()
                Text("Actual: \(Int(trafficData.last ?? 0)) Mbps")
                    .font(.footnote)
                    .foregroundColor(.gray)
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(Color.white)
                .shadow(color: Color.black.opacity(0.1), radius: 10, x: 0, y: 5)
        )
        .padding(.horizontal)
        .onAppear {
            // Simular actualización de tráfico de red
            Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
                updateTrafficData()
            }
        }
    }
    
    private func updateTrafficData() {
        // Generar un valor aleatorio para simular el tráfico de red
        let newTrafficValue = CGFloat.random(in: 20...100)
        trafficData.append(newTrafficValue)
        
        // Limitar el número de datos para que el gráfico no crezca indefinidamente
        if trafficData.count > 30 {
            trafficData.removeFirst()
        }
        
        // Actualizar el máximo del tráfico si es necesario
        if newTrafficValue > maxTraffic {
            maxTraffic = newTrafficValue
        }
    }
}

struct LineGraph: Shape {
    var data: [CGFloat]
    var maxDataValue: CGFloat

    func path(in rect: CGRect) -> Path {
        var path = Path()
        
        guard data.count > 1 else { return path }
        
        let step = rect.width / CGFloat(data.count - 1)
        let scale = rect.height / maxDataValue
        
        let points = data.enumerated().map { index, value in
            CGPoint(x: CGFloat(index) * step, y: rect.height - value * scale)
        }
        
        path.move(to: points[0])
        for point in points.dropFirst() {
            path.addLine(to: point)
        }
        
        return path
    }
}

struct ActiveAlertsCardView: View {
    @State private var activeAlerts: [AlertItem] = [
        AlertItem(title: "Amenaza crítica detectada", description: "IP sospechosa detectada en la red", timestamp: "Hace 5 min", level: .critical),
        AlertItem(title: "Intento de acceso no autorizado", description: "Intento de acceso en servidor principal", timestamp: "Hace 10 min", level: .high),
        AlertItem(title: "Escaneo de puertos detectado", description: "Se detectaron múltiples escaneos de puertos", timestamp: "Hace 15 min", level: .medium)
    ]
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Últimas Alertas Activas")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.black)
                .padding(.bottom, 10)
            
            ForEach(activeAlerts) { alert in
                Button(action: {
                    // Acción al hacer clic en la alerta
                    print("Alerta seleccionada: \(alert.title)")
                }) {
                    AlertRow(alert: alert)
                }
                .buttonStyle(PlainButtonStyle()) // Estilo sin resaltar el botón
            }
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(Color.white)
                .shadow(color: Color.black.opacity(0.1), radius: 10, x: 0, y: 5)
        )
        .padding(.horizontal)
    }
}

struct AlertItem: Identifiable {
    let id = UUID()
    var title: String
    var description: String
    var timestamp: String
    var level: AlertLevel
}

enum AlertLevel {
    case critical, high, medium, low

    var color: Color {
        switch self {
        case .critical:
            return Color.red
        case .high:
            return Color.orange
        case .medium:
            return Color.yellow
        case .low:
            return Color.green
        }
    }
    
    var icon: String {
        switch self {
        case .critical:
            return "exclamationmark.shield.fill"
        case .high:
            return "questionmark.diamond"
        case .medium:
            return "exclamationmark.icloud.fill"
        case .low:
            return "checkmark.seal.fill"
        }
    }
}

struct AlertRow: View {
    var alert: AlertItem
    
    var body: some View {
        HStack(spacing: 15) {
            // Icono de nivel de alerta con color específico
            Image(systemName: alert.level.icon)
                .foregroundColor(alert.level.color)
                .font(.system(size: 24))
                .frame(width: 40, height: 40)
                .background(alert.level.color.opacity(0.2))
                .clipShape(Circle())
            
            VStack(alignment: .leading, spacing: 5) {
                HStack {
                    Text(alert.title)
                        .font(.headline)
                        .fontWeight(.semibold)
                        .foregroundColor(.black)
                    Spacer()
                }
                Text(alert.description)
                    .font(.subheadline)
                    .foregroundColor(.gray)
                Text(alert.timestamp)
                    .font(.footnote)
                    .foregroundColor(.gray)
            }
            Image(systemName: "chevron.right")
                .foregroundColor(.gray.opacity(0.3))
                .font(.system(size: 24))
                .frame(width: 40, height: 40)
                .background(Color.clear)
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 15)
                .fill(Color.white.opacity(0.9))
                .shadow(color: Color.black.opacity(0.3), radius: 5, x: 0, y: 5)
        )
    }
}

struct SOCResponseTimesCardView: View {
    @State private var responseTimes: [ResponseTime] = [
        ResponseTime(name: "Detección de Amenazas", time: "500 ms"),
        ResponseTime(name: "Análisis de Incidentes", time: "1.2 s"),
        ResponseTime(name: "Resolución Automática", time: "800 ms"),
        ResponseTime(name: "Notificación al Usuario", time: "200 ms"),
        ResponseTime(name: "Acceso a la base de datos", time: "90 ms")
    ]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Tiempos de Respuesta del SOC")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.black)
                .padding(.bottom, 10)
            
            ForEach(responseTimes) { response in
                HStack {
                    Text(response.name)
                        .font(.subheadline)
                        .foregroundColor(.black)
                    
                    Spacer()
                    
                    Text(response.time)
                        .font(.subheadline)
                        .fontWeight(.bold)
                        .foregroundColor(.blue)
                }
                .padding(.vertical, 8)
                .padding(.horizontal)
                Divider()
                    .overlay(.blue.opacity(0.1))
            }
        }
        .frame(maxHeight: 300) // Limitar la altura del panel de logs
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(Color.white)
                .shadow(color: Color.black.opacity(0.1), radius: 10, x: 0, y: 5)
        )
    }
}

struct ResponseTime: Identifiable {
    let id = UUID()
    var name: String
    var time: String
}

struct LogsPanelCardView: View {
    @State private var logs: [LogEntry] = [
        LogEntry(message: "Inicio del sistema de seguridad.", timestamp: "00:00:00"),
        LogEntry(message: "Detección de escaneo de puertos.", timestamp: "00:01:15"),
        LogEntry(message: "Intento de acceso no autorizado bloqueado.", timestamp: "00:02:30")
    ]
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            Text("Panel de Logs")
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.black)
                .padding(.bottom, 10)
            
            ScrollView {
                VStack(alignment: .leading, spacing: 5) {
                    ForEach(logs) { log in
                        HStack(alignment: .top) {
                            Text(log.timestamp)
                                .font(.footnote)
                                .foregroundColor(.gray)
                            
                            Text(log.message)
                                .font(.subheadline)
                                .foregroundColor(.black)
                        }
                        .padding()
                        .background(
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color.white.opacity(0.9))
                                .shadow(color: Color.black.opacity(0.05), radius: 5, x: 0, y: 2)
                        )
                    }
                }
                .padding(.horizontal)
            }
            .frame(maxHeight: 250) // Limitar la altura del panel de logs
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(Color.white)
                .shadow(color: Color.black.opacity(0.1), radius: 10, x: 0, y: 5)
        )
        .onAppear {
            // Simula la llegada de nuevos logs cada 2 segundos
            Timer.scheduledTimer(withTimeInterval: 2.0, repeats: true) { _ in
                addNewLogEntry()
            }
        }
    }
    
    private func addNewLogEntry() {
        let newLog = LogEntry(message: "Nuevo evento detectado en la red.", timestamp: Date().formatted(.dateTime.hour().minute().second()))
        logs.insert(newLog, at: 0) // Agrega el log en la parte superior
        if logs.count > 20 { // Limita la cantidad de logs visibles
            logs.removeLast()
        }
    }
}

struct LogEntry: Identifiable {
    let id = UUID()
    var message: String
    var timestamp: String
}
