# SentinelX

## Folder Structure 

- `api`: Contains the API that saves and gets information from the mongoDB database. Also, the api loads the trained models and encodings to make predictions.

- `frontend`: Contains the frontend of the project. It's a macOS made with Swift that has a simple interface that shows real time traffic and the attacks detected.

- `models`: Contains the traning dataset, the trained models and the notebooks used to train the models. More info on the [README](https://github.com/nicollorens12/SentinelX/tree/main/models) 

- `trafficGenerator`: Contains the traffic generator that simulates the network traffic. It generates benign and malign traffic. The malign traffic is generated with the attacks that the models were trained to detect.