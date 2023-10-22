//
//  RankBadge.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import SwiftUI

struct RankBadge: View {
    let rank: Int

    var body: some View {
        if rank == 1 {
            Image("first")
                .resizable()
                .scaledToFit()
                .frame(width: 26, height: 26)
                .clipShape(RoundedRectangle(cornerRadius: 8))
                .overlay {
                    Text("#1")
                        .yFont(.bold, size: 13)
                        .multilineTextAlignment(.center)
                        .foregroundStyle(.white)
                        .opacity(0.8)
                }
        } else {
            Rectangle()
                .foregroundColor(.clear)
                .frame(width: 26, height: 26)
                .cornerRadius(8)
                .overlay(
                    RoundedRectangle(cornerRadius: 7.69)
                        .inset(by: 0.50)
                        .stroke(Color(red: 0.25, green: 0.25, blue: 0.25), lineWidth: 1)
                )
                .overlay {
                    Text("#\(rank)")
                        .yFont(.bold, size: 13)
                        .multilineTextAlignment(.center)
                        .foregroundStyle(.white)
                        .opacity(0.8)
                }
        }
    }
}

#Preview {
    VStack {
        RankBadge(rank: 1)
        RankBadge(rank: 2)
    }
}
