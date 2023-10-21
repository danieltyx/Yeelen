//
//  TopHit.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import Foundation

struct TopHit: Identifiable {
    let id = UUID()
    let appName: String
    let content: String
    let rank: Int
}
