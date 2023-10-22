//
//  Firebase.swift
//  Broadcast
//
//  Created by 朱浩宇 on 2023/10/21.
//

import Foundation
import FirebaseApp
import Firestore

class FirebaseManager {
    static let shared = FirebaseManager()

    let json = #"""
{
  "type": "service_account",
  "project_id": "yeelen-165b8",
  "private_key_id": "37ee1b173c298881a6e31f5b3d9533aaf46c7fd1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDvt6sovZWWW1hT\nV5Pwl71U2224nXMWSZgBGAn2wkTKkNIjg3OPOaS9lz0lEBafzEkDl3QtYo8La9aX\n/YvhKLEKFq2jYy89+Z+aiIx+l36QZNiZhUefVVJvmuhz4vQZgjfh4Az9PgKqHHzQ\ne6flWSA0tA32l4h1FnCq7gj3cWtTPplsj24vLpMQVwrPU1mo2WL1iTp3lB49SHiP\nYinMq0vthNWItfb+LEaFYAy6hC22bdePoeDnmRZGdryWuAEQwJ6B4jjtXIvQwZSu\n3Squ6Hl+v/AxdMDLJRW2JIdqQ2cIF6C5UgfP3DgRs6PpIAHZ2JIEFBzJ58Tipr5R\nXH//YMVdAgMBAAECggEAEYckhL4YCf5z3uQwdQ8jUOkahL0+hQqsiqfvUpOx4/3i\n36Xk9TwJx7MfTW53uQd+7zxLymXCf9tKvaJUcApBp7MwzxmZgraV7P6/ByKcpoI5\nNECClCvw8ygohxC5OIRFAccYLAw0tauPlM7139c8e54Ox1EdMTKK2nS9QxqP9m4h\nHw4KPt24kP6T/aETM8m+T4fiPHxp7To8hFYJyAUZ4vqSrSb7SVHW1UqL+j9vSZYq\nFN2KAnTvchr0odAsGpdVgMlhKTZXVLAZjReiJJnHlOXWYdPBRwNoEQhTjVr1yoyF\nrdZtGI9p1CiQqggNfp2D7XBOPp7kIbAZPhBW2+7VIQKBgQD6W5974FPLs1A8G1st\nybJhzjs+5qdKNtGn/Y7queJIpbEZDlsIg379XEverPFIjKb0QBC3Yt67MuPsQyaQ\nHTBcRYmp6FK6c6Qk1TeaSCXiwz27AqgSl+zqSwjTyB+qIGRXUqkdpbMrfguFdhed\noF8yhdt92/yz8ZnvgtwwumAH8wKBgQD1HqiBN8cmT2VrU4nc+WK5tpKyQDj8id/b\nVJLQDv+dj2N1+aAkvYBnH5pPIefcj6EVJvx+kS2lfdzRWpOwe7a3wizcqgiBtZzj\n0eQAk2zjuzgYkPuGu7r/KUVXBBa/mjid5V8/sdNyGic4YXjRRv1MGmptaSgIylwk\nztgWMy0hbwKBgGmNnaUNxGaauFZPNlcMtc+0spfniVqp2CUaq1nde0Ej0pH80na5\nch4B/t7oTWZIHs/V/vZCkiOc5imjeivCkrQkgVEIaXDA9tCssJ+0kXyU0n75NMF6\nGmIBtrwLoQYKWCPU7wZX6T2KC/N+AaDsj5Zuh0b+LAH19+/aXVmSCpDvAoGBALnp\nre6MCr1w3MCBlQAIGqw24J7X/SD1xdcKF2w84/1yIwL4+VDEdl5A5v37/msYeRmc\n/0dT/6YUh2Y2Z+wkeRp46SPYxyjyQXO930vchWtYtZxUYqH3Q0aC2/e6vzJF24lO\nzmZ2DqTtVy/5JfS8/iM5qd0gM+Au86JrTBPSbvl7AoGAKReA58NdujBJuQ0CnisT\nfZisLTQbrUzg50jFyTOiwsXOkIy0nuCg0ebHVaOtDcj/TxLfPlmd1tsS70mNud1Y\nbJzqEdK8lq1zXdIrZWGQMjBD0aCTIu6/QeR+Xjj1Q9k9rA1aS4mZ3G75kAHKjgLX\nbDzds4TWQQqaythGk+gyXFc=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-15xnw@yeelen-165b8.iam.gserviceaccount.com",
  "client_id": "114770100509248330579",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-15xnw%40yeelen-165b8.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""#

    init() {
        func loadServiceAccount(from jsonFile: String) throws -> ServiceAccount {
            do {
                let data = json.data(using: .utf8)!
                let decoder = JSONDecoder()
                let serviceAccount = try decoder.decode(ServiceAccount.self, from: data)
                return serviceAccount
            } catch {
                throw NSError(domain: "JSONParsingError", code: 400, userInfo: [NSLocalizedDescriptionKey: "Error parsing JSON file: \(error)"])
            }
        }

        let serviceAccount = try! loadServiceAccount(from: "ServiceAccount")
        FirebaseApp.initialize(serviceAccount: serviceAccount)
    }

    func read() async throws -> String {
        let ref = Firestore
            .firestore()
            .collection("links")
            .document("cloudflared")

        let readData = try await ref.getDocument(type: Object.self)

        return readData?.url ?? ""
    }
}


struct Object: Codable, Equatable {
    var url: String
}
