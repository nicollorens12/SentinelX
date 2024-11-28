import SwiftUI

struct ContentView: View {
    @Binding var isLoggedIn: Bool
    @State private var selected = "Inicio"

    var body: some View {
        GeometryReader { geometry in
            HStack {
                // Barra lateral de menú, ajustada al alto de la pantalla disponible
                SideMenu(isLoggedIn: $isLoggedIn, selected: $selected, width: Binding.constant(geometry.size.width*0.15), height: Binding.constant(geometry.size.height))
                
                // Contenido principal con barra de búsqueda y vista dinámica según selección
                ScrollView {
                    VStack(spacing: -25) {
                        SearchBar()
                        
                        // Vista dinámica según la selección en el menú
                        switch selected {
                        case "Inicio":
                            Home(width: Binding.constant(geometry.size.width*0.85), height: Binding.constant(geometry.size.height))
                        case "Análisis":
                            NetworkScanView()
                        case "Histórico":
                            AlertHistoryView()
                        default:
                            Text("Hola")
                        }
                    }
                }
            }
            .frame(width: geometry.size.width, height: geometry.size.height)
            .background(Color(.white))
            .background(BlurWindow())
        }
    }
}

#Preview {
    ContentView(isLoggedIn: Binding.constant(true))
}
