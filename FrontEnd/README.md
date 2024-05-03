# Confluent Current Gen AI

## Realtime Chat Application

The realtime chat application is a monorepo that consists two projects: frontend application, and a socket server. Both of these must be running for the chat application to work.

### Socket Server

- All code for the socket server is located in `FrontEnd` folder.

- Built using NodeJS.

- Responsible for generating socket sessions to maintain with the frontend as well as producing and consuming messages from Confluent Kafka.

- We create a custom partitioner while producing messages to a Kafka topic so that we have better control over which message lands in which partition. We do this to preserve the order of messages, and to make sure all messages from a specific socket session are all located in a single partition and in order.

- Server produces messages to a Kafka topic called `Questions` and consumes messages from a topic called `Answers`.

- Pre-requisites to running the server:
    - For local deployment, create a file called `.env.local` and copy the contents of `.env.example`. Also fill in the appropriate values for all the variables. (You can find these values in Confluent Cloud)
    - For cloud deployment, make sure all the environment variables in `.env.example` are being provided to the application.

### FrontEnd Application

- All code for the frontend application is located in `FrontEnd` folder.

- Built using React and NodeJS.

- Majority of the logic is located in `src/Components/ChatBody.js`. This is where we initiate a socket connection to the socket server and read/write to the connection.

- Running the application:
    - Run `sh run_local.sh`
