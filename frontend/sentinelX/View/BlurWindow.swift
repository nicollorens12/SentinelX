import SwiftUI

struct BlurWindow: NSViewRepresentable {
    func makeNSView(context: Context) -> NSVisualEffectView {
        let view = NSVisualEffectView()
        view.blendingMode = .behindWindow
        return view
    }
    func updateNSView(_ nsView: NSVisualEffectView, context: Context) {
        
    }
}

#Preview {
    BlurWindow()
}
