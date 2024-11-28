import SwiftUI

struct SearchBar: View {
    @State private var search = ""
    @State private var response = "" // Para mostrar la respuesta de ChatGPT
    @FocusState private var isTextFieldFocused: Bool // Para detectar el Enter
    
    
    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            // Barra de búsqueda
            HStack(spacing: 12) {
                HStack(spacing: 15) {
                    Image(systemName: "magnifyingglass")
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                    
                    TextField("Escribe tu pregunta...", text: $search, onCommit: fetchResponse)
                        .fontWeight(.semibold)
                        .textFieldStyle(PlainTextFieldStyle())
                        .foregroundColor(.white)
                        .cornerRadius(8)
                        .focused($isTextFieldFocused)
                }
                .padding(.vertical, 10)
                .padding(.horizontal)
                .background(Color.gray)
                .cornerRadius(10)
                .frame(maxWidth: 1250) // Ancho máximo para la barra de búsqueda
            }
            
            // Cuadro de respuesta
            if !response.isEmpty {
                ZStack(alignment: .topTrailing) {
                    // Fondo del cuadro de respuesta
                    RoundedRectangle(cornerRadius: 10)
                        .fill(Color.gray.opacity(0.8)) // Fondo gris claro
                        .frame(maxWidth: 1250)
                    HStack(alignment: .top, spacing: 0){
                        ScrollView {
                            Text(response)
                                .font(.body)
                                .foregroundColor(.white)
                                .padding()
                                .frame(maxWidth: .infinity, alignment: .leading) // Alinear el texto a la izquierda
                        }
                        .frame(minHeight: 50)
                        .frame(maxWidth: 1250, maxHeight: 200)
                        Button(action: {
                            response = "" // Cierra la respuesta al hacer clic en "X"
                        }) {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundColor(.white)
                                .font(.system(size: 16, weight: .bold))
                                .padding(8)
                        }
                        .padding(.top, 8) // Alineación para que no se sobreponga
                        .padding(.trailing, 8)
                        .buttonStyle(.borderless)
                    }
                }
                .fixedSize(horizontal: false, vertical: true) // Ajuste dinámico del alto
                
            }
            
            Spacer()
        }
        .padding()
    }
    
    // Función para hacer la llamada a la API de ChatGPT
    private func fetchResponse() {
        guard !search.isEmpty else { return }
        
        let apiKey = "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" // Reemplaza con tu clave API de OpenAI
        let url = URL(string: "https://api.openai.com/v1/chat/completions")!
        let headers = [
            "Authorization": "Bearer \(apiKey)",
            "Content-Type": "application/json"
        ]
        
        let requestData: [String: Any] = [
            "model": "gpt-3.5-turbo",
            "messages": [
                ["role": "user", "content": search]
            ]
        ]
        
        do {
            let data = try JSONSerialization.data(withJSONObject: requestData)
            
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.allHTTPHeaderFields = headers
            request.httpBody = data
            
            // Realiza la solicitud a la API de OpenAI
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error en la solicitud: \(error.localizedDescription)")
                    return
                }
                
                guard let data = data else {
                    print("No se recibieron datos de la API.")
                    return
                }
                
                do {
                    // Procesa la respuesta JSON de la API de OpenAI
                    if let json = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any],
                       let choices = json["choices"] as? [[String: Any]],
                       let message = choices.first?["message"] as? [String: Any],
                       let content = message["content"] as? String {
                        DispatchQueue.main.async {
                            self.response = content // Actualiza la respuesta en la interfaz
                            self.search = "" // Limpia el campo de búsqueda después de enviar la consulta
                            self.isTextFieldFocused = false // Cierra el teclado
                        }
                    }
                } catch {
                    print("Error al procesar la respuesta de la API: \(error.localizedDescription)")
                }
            }.resume()
            
        } catch {
            print("Error al preparar los datos de la solicitud: \(error.localizedDescription)")
        }
    }
}

#Preview {
    SearchBar()
}
