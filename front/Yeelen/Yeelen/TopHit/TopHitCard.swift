//
//  TopHitCard.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import SwiftUI

struct TopHitCard: View {
    let image: String
    let appName: String
    let rank: Int
    let content: String

    var body: some View {
        VStack(spacing: 16) {
            HStack {
                HStack(spacing: 12) {
                    Image(image)
                        .resizable()
                        .scaledToFit()
                        .frame(width: 26, height: 26)
                        .clipShape(RoundedRectangle(cornerRadius: 8))


                    Text(appName)
                        .yFont(.semibold, size: 16)
                        .foregroundStyle(.white)
                }

                Spacer()

                if rank <= 3 {
                    RankBadge(rank: rank)
                }
            }
            .padding(.horizontal, 20)
            .padding(.top, 20)

            HStack {
                Text(content)
                    .yFont(.medium, size: 14)
                    .foregroundStyle(Color(hexadecimal: "CCCCCC"))
                    .multilineTextAlignment(.leading)

                Spacer()
            }
            .padding(.horizontal, 20)
            .padding(.bottom, 20)
        }
        .background(Color(hexadecimal: "262626"))
        .cornerRadius(24)
        .overlay {
            RoundedRectangle(cornerRadius: 23.86)
                .inset(by: 0.5)
                .stroke(Color(red: 0.20, green: 0.20, blue: 0.20), lineWidth: 1)
        }
    }
}
