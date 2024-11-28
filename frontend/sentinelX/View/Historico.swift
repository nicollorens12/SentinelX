import SwiftUI

struct AlertHistoryView: View {
    // Lista simulada de 45 alertas
    @State private var alerts: [AlertItem2] = (1...45).map { index in
        AlertItem2(
            level: AlertLevel2.allCases.randomElement()!,
            title: "Alerta \(index)",
            description: "Descripción detallada de la alerta \(index).",
            timestamp: "\(Int.random(in: 1...59)) min atrás",
            sourceIP: "192.168.1.\(Int.random(in: 1...255))",
            destinationIP: "10.0.0.\(Int.random(in: 1...255))",
            protocolType: ["TCP", "UDP"].randomElement()!,
            sourcePort: Int.random(in: 1024...65535),
            destinationPort: Int.random(in: 1024...65535),
            location: "Madrid, España",
            priority: ["Alta", "Media", "Baja"].randomElement()!
        )
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            Text("Histórico de Alertas del Sistema")
                .font(.title)
                .fontWeight(.bold)
                .padding(.horizontal)
            
            ScrollView {
                LazyVStack(spacing: 15) {
                    ForEach(alerts) { alert in
                        AlertCard(alert: alert)
                    }
                }
                .padding(.horizontal)
            }
        }
        .padding()
    }
}

// Vista de Tarjeta para cada Alerta
struct AlertCard: View {
    var alert: AlertItem2
    
    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            // Título y Nivel de Alerta
            HStack {
                Image(systemName: alert.level.icon)
                    .foregroundColor(.white)
                    .background(alert.level.color)
                    .clipShape(Circle())
                    .frame(width: 40, height: 40)
                
                VStack(alignment: .leading, spacing: 5) {
                    Text(alert.title)
                        .font(.headline)
                        .foregroundColor(alert.level.color)
                    Text(alert.timestamp)
                        .font(.footnote)
                        .foregroundColor(.gray)
                }
                Spacer()
                Text(alert.priority)
                    .font(.subheadline)
                    .padding(6)
                    .background(alert.level.color.opacity(0.2))
                    .foregroundColor(alert.level.color)
                    .cornerRadius(5)
            }
            
            // Descripción
            Text(alert.description)
                .font(.subheadline)
                .foregroundColor(.gray)
            
            Divider()
            
            // Información detallada de la alerta
            HStack(spacing: 10) {
                VStack(alignment: .leading) {
                    Text("IP Origen: \(alert.sourceIP)")
                        .font(.caption)
                        .foregroundColor(.primary)
                    Text("Puerto Origen: \(alert.sourcePort)")
                        .font(.caption)
                        .foregroundColor(.primary)
                }
                
                Spacer()
                
                VStack(alignment: .leading) {
                    Text("IP Destino: \(alert.destinationIP)")
                        .font(.caption)
                        .foregroundColor(.primary)
                    Text("Puerto Destino: \(alert.destinationPort)")
                        .font(.caption)
                        .foregroundColor(.primary)
                }
                
                Spacer()
                
                VStack(alignment: .leading) {
                    Text("Protocolo: \(alert.protocolType)")
                        .font(.caption)
                        .foregroundColor(.primary)
                    Text("Ubicación: \(alert.location)")
                        .font(.caption)
                        .foregroundColor(.primary)
                }
            }
            .padding(.top, 5)
        }
        .padding()
        .background(Color(.gray))
        .cornerRadius(12)
        .shadow(color: Color.black.opacity(0.05), radius: 4, x: 0, y: 2)
    }
}

// Modelo de datos de alerta
struct AlertItem2: Identifiable {
    let id = UUID()
    var level: AlertLevel2
    var title: String
    var description: String
    var timestamp: String
    var sourceIP: String
    var destinationIP: String
    var protocolType: String
    var sourcePort: Int
    var destinationPort: Int
    var location: String
    var priority: String
}

// Enum para los niveles de alerta con colores e iconos
enum AlertLevel2: CaseIterable {
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
            return "exclamationmark.octagon.fill"
        case .high:
            return "exclamationmark.triangle.fill"
        case .medium:
            return "info.circle.fill"
        case .low:
            return "checkmark.seal.fill"
        }
    }
}

#Preview {
    AlertHistoryView()
}
