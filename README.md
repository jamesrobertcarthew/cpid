cpid
====

A Cloud Based PID Controller intended to demonstrate the possibilities of applying web-based services to robotics. A PID controller is to be designed to operate on a host server and provide control data to a client via the Internet. As the controller will have to operate in real time, packet loss and network latency will have to be accounted for. A client account will allow developers to choose gain values for the PID controller. The server and the client will have different data communication responsibilities during operation.

Error is calculated on the client side of the Internet to minimise latency and allow the client to dynamically change set point. A server based PID controller will be complemented with a simple linear predictor that utilises the current latency value in an attempt to time the arrival of a control effort data packet at the client in such a way that minimises error. Both the Control Effort and Error data will be sent accompanied by a time code and sequence number to allow for packet confirmation.
