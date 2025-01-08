# SentinelX

This is the code repository for the course Applied Engenieering Project (PAE) at Universitat Politècnica de Catalunya. The objective of this course was to take a challenge from a company and solve it with the knowledge acquired during the degree. The company that proposed the challenge was [Hypergraph AI](https://hypergraphai.tech/). The challenge was to create a model that could detect malign traffic on a network and create an AI assistant to help the network administrator to solve the detected attacks. 

Our solution was called SentinelX. And eventhough Hypergraph AI are using much complex models like GNNs, that understand the context of the network where the traffic comes thanks to the Graph component of the NN we didn't want to copy their recipy and we wanted to explore other options. They were really happy that we tried a different approach. We used a simple 3-layer model that could detect malign traffic and we created a macOS app that showed the real time traffic and the attacks detected.


## Folder Structure 

- `api`: Contains the API that saves and gets information from the mongoDB database. Also, the api loads the trained models and encodings to make predictions.

- `frontend`: Contains the frontend of the project. It's a macOS made with Swift that has a simple interface that shows real time traffic and the attacks detected.

- `models`: Contains the traning dataset, the trained models and the notebooks used to train the models. More info on the [README](https://github.com/nicollorens12/SentinelX/tree/main/models) 

- `trafficGenerator`: Contains the traffic generator that simulates the network traffic. It generates benign and malign traffic. The malign traffic is generated with the attacks that the models were trained to detect.

## Future Work

This a study and working version of a simple model that can detect malign traffic. The next steps would be to improve the model and the interface. The model could be improved by adding more data and more types of attacks. Also, other kinds of models like GNN's it's probably a much better option as for one big trained GNN could work with precisition for all kinds of networks as shown on this [study](https://upcommons.upc.edu/handle/2117/417495). The interface should be improved by adding more information about the traffic and the attacks detected, also, not all information on the UI is real, some is made up for presentation purposes.

