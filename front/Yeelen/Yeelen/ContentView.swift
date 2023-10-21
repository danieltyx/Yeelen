//
//  ContentView.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import SwiftUI
@_spi(Advanced) import SwiftUIIntrospect
import SwiftUIX
import UserNotifications

struct ContentView: View {
    @State var text = ""
    @FocusState var focus: Bool

    var body: some View {
        VStack(spacing: 0) {
            Text("Yeelen")
                .yFont(.bold, size: 28)
                .padding(.top, 80)
            

            RoundedRectangle(cornerRadius: 24)
                .frame(height: 160)
                .foregroundColor(Color(red: 0.15, green: 0.15, blue: 0.15))
                .overlay(
                    RoundedRectangle(cornerRadius: 23.86)
                        .inset(by: 1)
                        .stroke(Color(red: 0.20, green: 0.20, blue: 0.20), lineWidth: 2)
                )
                .overlay {
                    VStack {
                        HStack {
                            Text("Enter your question about using the app on your phone...")
                                .padding(20)
                                .yFont(.medium, size: 16)
                                .foregroundStyle(Color(hexadecimal: "B3B3B3"))

                            Spacer()
                        }
                        Spacer()
                    }
                    .opacity(focus || !text.isEmpty ? 0 : 1)
                }
                .overlay {
                    TextEditor(text: $text)
                        .focused($focus)
                        .padding(20)
                        .scrollContentBackground(.hidden)
                        .yFont(.medium, size: 16)
                        .introspect(.textEditor, on: .iOS(.v17...)) { textEditor in
                            textEditor.textContainerInset = UIEdgeInsets.zero
                            textEditor.textContainer.lineFragmentPadding = 0
                        }
                }
                .shadow(
                    color: Color(red: 0, green: 0, blue: 0, opacity: 0.15), radius: 15
                )

                .padding(.top, 40)
                .padding(.horizontal, 30)

            ScrollView(showsIndicators: false) {
                VStack(spacing: 30) {
                    ForEach(TopHitManager.shared.topHits) { item in
                        TopHitCard(image: item.appName, appName: item.appName, rank: item.rank, content: item.content)
                            .padding(.horizontal, 30)
                    }
                }
                .padding(.bottom, 180)
            }
            .padding(.top, 40)

            Spacer()
        }
        .overlay {
            VStack {
                Spacer()

                Rectangle()
                    .frame(width: 393, height: 200)
                    .foregroundColor(Color(red: 0.10, green: 0.10, blue: 0.10))
                    .blur(radius: 60)
            }
            .frame(height: Screen.main.height + 200)
        }
        .overlay {
            VStack {
                Spacer()

                Image("buttonGrad")
                    .resizable()
                    .scaledToFit()
                    .contentShape(RoundedRectangle(cornerRadius: 20))
                    .cornerRadius(20)
                    .clipped()
                    .overlay {
                        RoundedRectangle(cornerRadius: 19.88)
                            .foregroundStyle(.black.opacity(0.15))
                    }
                    .overlay {
                        RoundedRectangle(cornerRadius: 19.88)
                            .inset(by: 1)
                            .stroke(Color(red: 1, green: 1, blue: 1).opacity(0.40), lineWidth: 2)
                    }
                    .overlay {
                        Text("Get Instructions")
                            .foregroundStyle(.black)
                            .yFont(.bold, size: 16)
                    }
                    .overlay {
                        RoundedRectangle(cornerRadius: 19.88)
                            .foregroundStyle(.black.opacity(0.3))
                            .opacity(text.isEmpty ? 1 : 0)
                            .animation(.easeInOut, value: text)
                    }
                    .padding(.horizontal, 30)
                    .padding(.bottom, 70)
            }
        }
        .background(Color(hexadecimal: "1A1A1A").onTapGesture(perform: {
            focus = false
        }))
        .ignoresSafeArea(.all)
    }
}

#Preview {
    ContentView()
}
