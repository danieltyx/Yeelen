//
//  TopHitManager.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/21.
//

import Foundation

class TopHitManager {
    static let shared = TopHitManager()

    let topHits = [
        TopHit(appName: "Facebook", content: "How can I change my profile image in the Facebook?", rank: 1),
        TopHit(appName: "Settings", content: "How can I turn down Twitter’s notification in the Settings App?", rank: 2),
        TopHit(appName: "Settings", content: "How can I add a Japanese Alphabet keyboard in the Settings App?", rank: 3),
        TopHit(appName: "Canva", content: "How can I add a new page in the Canvas?", rank: 4),
        TopHit(appName: "Facebook", content: "How can I add bio in the Facebook?", rank: 5),
    ]
}
