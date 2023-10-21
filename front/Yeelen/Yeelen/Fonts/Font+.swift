//
//  Font+.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import SwiftUI

/*
 New York
 == NewYork-Regular
 == NewYork-Medium
 == NewYork-Semibold
 == NewYork-Bold
 == NewYork-Heavy
 == NewYork-Black
 */

public enum YeelenFont: String {
    case regular = "NewYork-Regular"
    case medium = "NewYork-Medium"
    case semibold = "NewYork-Semibold"
    case bold = "NewYork-Bold"
    case heavy = "NewYork-Heavy"
    case black = "NewYork-Black"
}

public struct YeelenFontModifier: ViewModifier {
    let type: YeelenFont
    let size: Int

    public func body(content: Content) -> some View {
        content
            .font(.custom(type.rawValue, size: CGFloat(size)))
    }
}

public extension View {
    func yFont(_ type: YeelenFont, size: Int) -> some View {
        self
            .modifier(YeelenFontModifier(type: type, size: size))
    }
}
