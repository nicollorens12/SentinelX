import SwiftUI

struct CleanButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .padding(.horizontal, 20)
            .frame(maxWidth: 370) // Ancho flexible
            .padding()
            .background(Color(.blue))
            .foregroundColor(.white)
            .cornerRadius(8)
            .shadow(color: .black.opacity(0.2), radius: 10, x:5, y: 10)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.black.opacity(0.3), lineWidth: 1)
            )
    }
}

struct CustomTextField: View {
    var placeholder: String
    @Binding var text: String
    var body: some View {
        TextField(placeholder, text: $text)
            .textFieldStyle(PlainTextFieldStyle())
            .padding()
            .background(Color(.black).opacity(0.2))
            .foregroundColor(.white)
            .cornerRadius(8)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.black.opacity(0.2), lineWidth: 1)
            )
            .frame(height: 45)
            .frame(maxWidth: 400) // Ancho flexible
    }
}

struct CustomSecureField: View {
    var placeholder: String
    @Binding var text: String
    var body: some View {
        SecureField(placeholder, text: $text)
            .textFieldStyle(PlainTextFieldStyle())
            .padding()
            .background(Color(.black).opacity(0.2))
            .foregroundColor(.white)
            .cornerRadius(8)
            .overlay(
                RoundedRectangle(cornerRadius: 8)
                    .stroke(Color.black.opacity(0.2), lineWidth: 1)
            )
            .shadow(radius: 2)
            .frame(height: 45)
            .frame(maxWidth: 400) // Ancho flexible
    }
}

struct Login: View {
    @State private var username: String = ""
    @State private var password: String = ""
    @State private var isShowingAlert = false
    @Binding var isLoggedIn: Bool
    private var mongoDBService = MongoDBService()
    
    init(isLoggedIn: Binding<Bool>) {
        self._isLoggedIn = isLoggedIn
    }

    struct SmoothWaveBackground: View {
        @State private var animate = false
        
        var body: some View {
            ZStack {
                AngularGradient(
                    gradient: Gradient(colors: [
                        Color.white.opacity(0.5),
                        Color.white.opacity(0.5),
                        Color.white.opacity(0.1),
                        Color.white.opacity(0.8),
                        Color.white.opacity(1),
                        Color.white.opacity(0.6)
                    ]),
                    center: .center,
                    startAngle: .degrees(0),
                    endAngle: .degrees(360)
                )
                .blur(radius: 50)
                .scaleEffect(6)
                .rotationEffect(.degrees(animate ? 360 : 0))
                .animation(
                    Animation.linear(duration: 30)
                        .repeatForever(autoreverses: false),
                    value: animate
                )
                .onAppear {
                    animate = true
                }
                .background(BlurWindow())
            }
            .ignoresSafeArea()
        }
    }
    
    var body: some View {
        GeometryReader { geometry in
            ZStack {
                SmoothWaveBackground()
                
                VStack(spacing: 10) {
                    Image("logo")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(width: 300, height: 200)
                        .shadow(color: .black.opacity(0.5), radius: 10, x:5, y: 10)
                    
                    VStack(spacing: 20) {
                        CustomTextField(placeholder: "Username", text: $username)
                        
                        CustomSecureField(placeholder: "Password", text: $password)
                    }
                    .padding(.horizontal, 20)
                    
                    Button("Log In", action: loginAction)
                        .buttonStyle(CleanButtonStyle())
                    
                    Text("Forgot Password?")
                        .foregroundColor(Color(.black))
                        .font(.footnote)
                        .underline()
                        .padding(.top, 10)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .padding()
                .alert(isPresented: $isShowingAlert) {
                    Alert(title: Text("Login Failed"), message: Text("Incorrect username or password"), dismissButton: .default(Text("OK")))
                }
            }
        }
    }

    private func loginAction() {
        guard !username.isEmpty, !password.isEmpty else {
            isShowingAlert = true
            return
        }
        mongoDBService.findUser(username: username, password: password) { success in
            DispatchQueue.main.async {
                if success {
                    self.isLoggedIn = true
                    mongoDBService.writeLog(message: "User \(username) has logged in.")
                } else {
                    self.isShowingAlert = true
                }
            }
        }
    }
}

struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        Login(isLoggedIn: .constant(false))
            .preferredColorScheme(.dark)
    }
}
