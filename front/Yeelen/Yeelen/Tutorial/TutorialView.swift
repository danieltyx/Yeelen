//
//  TutorialView.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import SwiftUI
import SwiftUIX
@_spi(Advanced) import SwiftUIIntrospect
import ReplayKit

struct TutorialView: View {
    let text: String

    @State var read = false

    @State var holder = Holder()

    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Spacer()

                Text("Tutorial")
                    .yFont(.bold, size: 28)

                Spacer()
            }
            .overlay {
                HStack {
                    BackButton()

                    Spacer()
                }
            }
            .padding(.top, 80)
            .padding(.horizontal, 30)

            ScrollView(showsIndicators: false) {
                VStack(spacing: 30) {
                    HStack {
                        TextStepView(index: 1, content: "Tap the “Start Broadcast” button below.")

                        Spacer()
                    }
                    .padding(.horizontal, 30)

                    HStack {
                        TextStepView(index: 2, content: "Yeelen will should a broadcast choosing picker. You just need to tap the “Start Broadcast” button below the picker.")

                        Spacer()
                    }
                    .padding(.horizontal, 30)

                    Image("screen1")
                        .resizable()
                        .scaledToFit()
                        .padding(.horizontal, 50)

                    HStack {
                        TextStepView(index: 3, content: "Then you should open the app that you are asking for help.")

                        Spacer()
                    }
                    .padding(.horizontal, 30)

                    HStack {
                        TextStepView(index: 4, content: "Wait a moment; you will receive a notification with instructions.")

                        Spacer()
                    }
                    .padding(.horizontal, 30)

                    Image("screen2")
                        .resizable()
                        .scaledToFit()
                        .padding(.horizontal, 50)

                    HStack {
                        TextStepView(index: 5, content: "Follow the instructions, and once you finish this step, instructions for the next step will be sent.")

                        Spacer()
                    }
                    .padding(.horizontal, 30)

                    HStack {
                        TextStepView(index: 6, content: "After you solve the problem, Yeelen will stop the broadcast.")

                        Spacer()
                    }
                    .padding(.horizontal, 30)
                }
                .padding(.top, 20)
                .padding(.bottom, 180)
                .measureScroll { offset in
                    if offset.y <= 20 && offset.y > -200 {
                        read = read || true
                    }
                }
            }
            .padding(.top, 20)
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

                Button {
                    UserDefaults(suiteName: "group.zhuhaoyu.yeelen")?.set(text, forKey: "question")
                    holder.button?.sendActions(for: .allEvents)
                } label: {
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
                            Text("Start Broadcast")
                                .foregroundStyle(.black)
                                .yFont(.bold, size: 16)
                        }
                        .overlay {
                            RoundedRectangle(cornerRadius: 19.88)
                                .foregroundStyle(.black.opacity(0.3))
                                .opacity(!read ? 1 : 0)
                                .animation(.easeInOut, value: read)
                        }
                }
                .disabled(!read)
                .padding(.horizontal, 30)
                .padding(.bottom, 70)
            }
        }
        .introspect(.viewController, on: .iOS(.v13...)) { controller in
            let broadcastPicker = RPSystemBroadcastPickerView(frame: CGRect(x: 100, y: 100, width: 100, height: 100))
            broadcastPicker.preferredExtension = "com.zhuhaoyu.Yeelen.Broadcast"

            controller.view.addSubview(broadcastPicker)

            broadcastPicker.alpha = 0

            for view in broadcastPicker.subviews {
                if let button = view as? UIButton {
                    holder.button = button
                }
            }
        }
        .navigationBarBackButtonHidden(true)
        .background(Color(hexadecimal: "1A1A1A"))
        .ignoresSafeArea(.all)
    }
}

#Preview {
    TutorialView(text: "")
}
