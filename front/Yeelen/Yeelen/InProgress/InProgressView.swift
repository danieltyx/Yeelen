//
//  InProgressView.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/22.
//

import SwiftUI

struct InProgressView: View {
    var body: some View {
        VStack(spacing: 0) {
            HStack {
                Spacer()

                Text("In Progress")
                    .yFont(.bold, size: 28)

                Spacer()
            }
            .padding(.top, 80)
            .padding(.horizontal, 30)

            Image("progress")
                .resizable()
                .scaledToFit()
                .frame(width: 220, height: 220)
                .clipShape(Circle())
                .padding(.top, 80)

            Text("Yeelen is currently helping you solve your problems with the specific app.\n\nPlease return to that app so we can continue providing you with instructions.")
                .multilineTextAlignment(.center)
                .yFont(.semibold, size: 20)
                .padding(.horizontal, 30)
                .padding(.top, 60)

            Spacer()

            Button {
                UserDefaults(suiteName: "group.zhuhaoyu.yeelen")?.set(true, forKey: "shouldClose")
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
                        Text("End the Session")
                            .foregroundStyle(.black)
                            .yFont(.bold, size: 16)
                    }
            }
            .padding(.horizontal, 30)
            .padding(.bottom, 70)
        }
        .ignoresSafeArea(.all)
    }
}

#Preview {
    InProgressView()
}
