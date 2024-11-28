import SwiftUI

@main
struct sentinelXApp: App {
    @State private var isLoggedIn = true // Track login status
    var body: some Scene {
        WindowGroup {
            if isLoggedIn {
                ContentView(isLoggedIn: $isLoggedIn) // Show MainView when logged in
            } else {
                Login(isLoggedIn: $isLoggedIn)
            }
        }
    }
}
