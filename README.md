# GPS Server Teltonika

This project is a GPS server written in Python that uses sockets and threading to receive GPS data from GPS devices and decode it using various codecs.

## Features

- Receives GPS data from GPS devices using sockets
- Decodes GPS data using various codecs (Codec8, Codec16, Codec8Ex)
- Supports multiple client connections using threading
- Uses Teltonika protocols for communication with GPS devices
- Simple and easy to use

## Installation

1. Clone this repository to your local machine using the following command:

git clone https://github.com/qontrastss/GPS-Server-Teltonika.git

2. Install the required dependencies


## Usage

1. Connect your GPS devices to the server's IP address and port number.
2. Run the server using the following command:

python server.py


3. The server will start listening for incoming GPS data from the connected GPS devices.
4. The decoded GPS data will be displayed on the console.

## Configuration

You can configure the server by modifying the following parameters:

- `HOST`: The IP address of the server.
- `PORT`: The port number to listen on.
- `MAX_CLIENTS`: The maximum number of concurrent client connections.
- `CODECS`: The list of codecs to use for decoding GPS data.
- `TELTONIKA_PROTOCOL`: The Teltonika protocol to use for communication with GPS devices.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions to this project are welcome. To contribute, please fork the repository, make your changes, and submit a pull request.

## Contact

If you have any questions or comments about this project, please contact the author at [aslan.abulai2003@gmail.com].
