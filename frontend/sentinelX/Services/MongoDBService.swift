import MongoSwift
import NIO
import Foundation

// Define the AlertAttack struct to match the MongoDB document structure
struct AlertAttack: Codable {
    var type: String
    var description: String
    var severity: String
    var initTime: Date?
    var resolutionTime: Date?
    var assigneeUser: String
    var aiActions: Int
    var isActive: Bool
    var status: String
    var details: String
}

class MongoDBService {
    private var client: MongoClient
    private let eventLoopGroup: EventLoopGroup

    init() {
        self.eventLoopGroup = MultiThreadedEventLoopGroup(numberOfThreads: 4)
        do {
            self.client = try MongoClient(
                "mongodb+srv://swift:swift@sentinelx.hwhts.mongodb.net/?retryWrites=true&w=majority&appName=SentinelX",
                using: self.eventLoopGroup
            )
        } catch {
            fatalError("Failed to initialize MongoDB client: \(error)")
        }
    }

    deinit {
        do {
            try? client.syncClose()
            cleanupMongoSwift()
            try? eventLoopGroup.syncShutdownGracefully()
        }
    }

    func findUser(username: String, password: String, completion: @escaping (Bool) -> Void) {
        let database = client.db("SentinelX")
        let collection = database.collection("usuarios")
        let filter: BSONDocument = ["username": .string(username), "password": .string(password)]
        collection.find(filter).whenComplete { result in
            switch result {
            case .success(let cursor):
                var userFound = false
                cursor.forEach { document in
                    print("User found: \(document)")
                    userFound = true
                }.whenComplete { cursorResult in
                    switch cursorResult {
                    case .success:
                        completion(userFound)
                    case .failure(let error):
                        print("Error iterating cursor: \(error)")
                        completion(false)
                    }
                }
            case .failure(let error):
                print("Error finding user: \(error)")
                completion(false)
            }
        }
    }
    
    func writeLog(message: String) {
        let database = client.db("SentinelX")
        let collection = database.collection("logs")

        let logDocument: BSONDocument = [
            "timestamp": .datetime(Date()), // Current timestamp
            "log": .string(message)
        ]

        collection.insertOne(logDocument).whenComplete { result in
            switch result {
            case .success:
                break
            case .failure:
                break
            }
        }
    }

    // New function to fetch alerts from MongoDB
    func fetchAlerts(completion: @escaping ([AlertAttack]?) -> Void) {
        let database = client.db("SentinelX")
        let collection = database.collection("alertas")

        collection.find().whenComplete { result in
            switch result {
            case .success(let cursor):
                var alerts: [AlertAttack] = []
                
                cursor.forEach { document in
                    // Decode each document to AlertAttack
                    if let jsonData = try? JSONEncoder().encode(document),
                       let alert = try? JSONDecoder().decode(AlertAttack.self, from: jsonData) {
                        alerts.append(alert)
                    }
                }.whenComplete { cursorResult in
                    switch cursorResult {
                    case .success:
                        completion(alerts)
                    case .failure(let error):
                        print("Error iterating cursor: \(error)")
                        completion(nil)
                    }
                }
                
            case .failure(let error):
                print("Error fetching alerts: \(error)")
                completion(nil)
            }
        }
    }
}

