//
//  SampleHandler.swift
//  Broadcast
//
//  Created by 朱浩宇 on 2023/10/21.
//

import ReplayKit
import Starscream

class SampleHandler: RPBroadcastSampleHandler, WebSocketDelegate {
    func didReceive(event: Starscream.WebSocketEvent, client: Starscream.WebSocketClient) {
        switch event {
        case .connected(_):
            let bodyObject: [String : Any] = [
                "type": "event",
                "message": "start",
                "identifier": identifier.uuidString,
                "apnsDeviceToken": UserDefaults(suiteName: "group.zhuhaoyu.yeelen")?.string(forKey: "pushNotificationToken") ?? "Error",
                "question": UserDefaults(suiteName: "group.zhuhaoyu.yeelen")?.string(forKey: "question") ?? "Error",
            ]

            send(bodyObject: bodyObject)
            started = true
        default:
            break
        }
    }

    var socket: WebSocket!
    var counter = 0
    var started = false

    let identifier = UUID()

    override func broadcastStarted(withSetupInfo setupInfo: [String : NSObject]?) {
        Task {
            let urlString = try await FirebaseManager.shared.read()
            print(urlString)

            let request = URLRequest(url: URL(string: urlString)!)
            socket = WebSocket(request: request)
            socket.delegate = self
            socket.connect()
        }

        Task {
            while !(UserDefaults(suiteName: "group.zhuhaoyu.yeelen")?.bool(forKey: "shouldClose") ?? false) {
                try? await Task.sleep(for: .seconds(1))
            }
            self.finishBroadcastWithError(Finish.finish)
        }

        UserDefaults(suiteName: "group.zhuhaoyu.yeelen")?.set(true, forKey: "status")
    }
    
    override func broadcastPaused() {
        // User has requested to pause the broadcast. Samples will stop being delivered.
    }
    
    override func broadcastResumed() {
        // User has requested to resume the broadcast. Samples delivery will resume.
    }
    
    override func broadcastFinished() {
        // User has requested to finish the broadcast.
        UserDefaults(suiteName: "group.zhuhaoyu.yeelen")?.set(false, forKey: "status")
        socket.disconnect(closeCode: 1000)
    }

    deinit {
        UserDefaults(suiteName: "group.zhuhaoyu.yeelen")?.set(false, forKey: "status")
        socket.disconnect(closeCode: 1000)
    }

    override func processSampleBuffer(_ sampleBuffer: CMSampleBuffer, with sampleBufferType: RPSampleBufferType) {
        switch sampleBufferType {
        case RPSampleBufferType.video:
            // Handle video sample buffer
            guard started else { return }

            autoreleasepool {
                if let image = imageFromSampleBuffer(sampleBuffer: sampleBuffer),
                   let data = image.jpegData(compressionQuality: 0.3) {
                    let timestamp = CMSampleBufferGetPresentationTimeStamp(sampleBuffer)

                    let bodyObject: [String : Any] = [
                        "type": "video",
                        "identifier": identifier.uuidString,
                        "data": data.base64EncodedString(),
                        "timestamp": timestamp.seconds
                    ]

                    send(bodyObject: bodyObject)
                }
            }

            break
        case RPSampleBufferType.audioApp:
            // Handle audio sample buffer for app audio
            break
        case RPSampleBufferType.audioMic:
            // Handle audio sample buffer for mic audio
            break
        @unknown default:
            // Handle other sample buffer types
            fatalError("Unknown type of sample buffer")
        }
    }

    func send(bodyObject: [String : Any]) {
        if let jsonData = try? JSONSerialization.data(withJSONObject: bodyObject, options: []) {
            print("send data")
            socket.write(data: jsonData)
        }
    }

    func imageFromSampleBuffer(sampleBuffer: CMSampleBuffer) -> UIImage? {
        if let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) {
            let ciImage = CIImage(cvPixelBuffer: pixelBuffer)
            let temporaryContext = CIContext(options: nil)
            if let temporaryImage = temporaryContext.createCGImage(ciImage, from: CGRect(x: 0, y: 0, width: CVPixelBufferGetWidth(pixelBuffer), height: CVPixelBufferGetHeight(pixelBuffer))) {
                return UIImage(cgImage: temporaryImage)
            }
        }

        return nil
    }
}

enum Finish: String, Error {
    case finish = "Amazing! You have done this! You have caught up!"
}
