//
//  SideMenu.swift
//  sentinelX
//
//  Created by Daniel Sánchez on 11/11/24.
//

import SwiftUI

struct SideMenu: View {
    @Binding var isLoggedIn: Bool
    @Binding var selected: String
    @Namespace var animation
    @Binding var width: CGFloat
    @Binding var height: CGFloat
    var body: some View {
        HStack(spacing:0){
            HStack(spacing:0){
                VStack(alignment: .leading, spacing: 25) {
                    Image("logo")
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                        .frame(width: 100, height: 100)
                        .padding(.leading)
                    
                    VStack(spacing: 25){
                        TapButton(image: "house.fill", title: "Inicio", selected: $selected,
                                  animation: animation)
                        TapButton(image: "gauge.with.needle.fill", title: "Análisis", selected: $selected,
                                  animation: animation)
                        TapButton(image: "list.dash", title: "Histórico", selected: $selected,
                                  animation: animation)
                    }
                    // Tap button with binding

                    
                    HStack {
                        Text("Últimas alertas")
                            .fontWeight(.semibold)
                            .foregroundColor(Color(.gray))
                    }
                    .padding()

                    HStack (spacing: 10){
                        Image("profile")
                            .resizable()
                            .aspectRatio(contentMode: .fill)
                            .frame(width: 35, height: 35)
                            .clipShape(Circle())
                        VStack(alignment: .leading, spacing: 8, content: {
                            Text("Daniel Sánchez")
                                .fontWeight(.semibold)
                                .foregroundColor(Color(.black))
                            
                        })
                    }
                    .padding(.leading)
                    Button(action: {isLoggedIn = false}) {
                        HStack{
                            Text("Log Out")
                            Image(systemName: "power")
                                .frame(width: 10)
                        }
                    }
                    .background(.black.opacity(0.5))
                    .cornerRadius(10)
                    .padding()

                }
            }
            Divider()
                .overlay(.blue)
                .offset(x: -17)
        }
        .frame(width: width, alignment: .topLeading)

    }
}

#Preview {
    SideMenu(isLoggedIn: Binding.constant(true), selected: Binding.constant("Inicio"), width: Binding.constant(1000), height: Binding.constant(1000)
             )
}
