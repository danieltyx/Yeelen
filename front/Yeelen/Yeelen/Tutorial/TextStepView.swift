//
//  TextStepView.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import SwiftUI

struct TextStepView: View {
    let index: Int
    let content: String

    var body: some View {
        HStack(alignment: .top, spacing: 20) {
            Image("first")
                .resizable()
                .scaledToFit()
                .frame(width: 36, height: 36)
                .clipShape(Circle())
                .overlay {
                    Text("\(index).")
                        .foregroundStyle(.white.opacity(0.8))
                        .yFont(.semibold, size: 18)
                }

            Text(content)
                .yFont(.semibold, size: 16)
        }
    }
}

#Preview {
    TextStepView(index: 1, content: "Tap the “Start Broadcast” button below.")
}
