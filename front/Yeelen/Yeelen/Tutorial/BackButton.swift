//
//  BackButton.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import SwiftUI

struct BackButton: View {
    @Environment(\.dismiss) var dismiss
    var body: some View {
        Button {
            dismiss()
        } label: {
            Rectangle()
                .frame(width: 66, height: 34)
                .foregroundColor(Color(red: 0.15, green: 0.15, blue: 0.15))
                .cornerRadius(10)
                .overlay(
                    RoundedRectangle(cornerRadius: 10)
                        .inset(by: 0.50)
                        .stroke(Color(red: 0.20, green: 0.20, blue: 0.20), lineWidth: 1)
                )
                .overlay {
                    Text("Back")
                        .yFont(.semibold, size: 15)
                        .foregroundStyle(.white)
                        .opacity(0.8)
                }
        }
    }
}

#Preview {
    BackButton()
}
