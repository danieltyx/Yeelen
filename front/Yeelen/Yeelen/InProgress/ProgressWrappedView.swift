//
//  ProgressWrappedView.swift
//  Yeelen
//
//  Created by 朱浩宇 on 2023/10/22.
//

import SwiftUI

struct ProgressWrappedView: View {
    let text: String

    @Environment(\.dismiss) var dismiss

    @AppStorage("status", store: UserDefaults(suiteName: "group.zhuhaoyu.yeelen")) var status = false

    var body: some View {
        if status {
            InProgressView()
                .onDisappear {
                    dismiss()
                }
                .navigationBarBackButtonHidden(true)
        } else {
            TutorialView(text: text)
                .navigationBarBackButtonHidden(true)
        }
    }
}
