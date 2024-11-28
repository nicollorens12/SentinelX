import SwiftUI

struct TapButton: View {
    var image: String
    var title: String
    @Binding var selected: String
    var animation : Namespace.ID
    var body: some View {
        Button(action: {
            withAnimation(.easeInOut(duration: 0.3)){
                selected = title
            }
        }, label:{
            HStack{
                Image(systemName: image)
                    .font(.title2)
                    .foregroundColor(selected == title ? Color.blue : black)
                Text(title)
                    .fontWeight(selected == title ? .bold : .none)
                    .foregroundColor(selected == title ? Color.blue : black)
                    .animation(.none)
                Spacer()
                // Capsule
                
                ZStack{
                    Capsule()
                        .fill(Color.clear)
                        .frame(width: 3, height: 18)
                    if selected == title{
                        Capsule()
                            .fill(Color.blue)
                            .frame(width: 3, height: 20)
                            .matchedGeometryEffect(id: "Tab", in: animation)
                    }
                }
            }
            .padding(.horizontal)
        })
        .buttonStyle(PlainButtonStyle())
    }
}

var black = Color.black.opacity(0.5)
