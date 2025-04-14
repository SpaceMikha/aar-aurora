#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <chrono>
#include <sstream>

#ifdef _WIN32
#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")
#else
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#endif

void initSockets()
{
#ifdef _WIN32
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);
#endif
}

void cleanupSockets()
{
#ifdef _WIN32
    WSACleanup();
#endif
}

std::string sendCommand(int sock, const std::string &cmd)
{
    send(sock, cmd.c_str(), cmd.size(), 0);
    std::this_thread::sleep_for(std::chrono::milliseconds(200)); // slight delay for response

    char buffer[1024];
    int bytesReceived = recv(sock, buffer, sizeof(buffer) - 1, 0);
    if (bytesReceived <= 0)
        return "";

    buffer[bytesReceived] = '\0';
    return std::string(buffer);
}

struct Aircraft
{
    std::string callsign;
    std::string type;
    std::string dep;
    std::string arr;
    std::string flightlevel;
};

int main()
{
    initSockets();

    const char *aurora_ip = "127.0.0.1";
    int port = 1130;

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)
    {
        std::cerr << "Failed to create socket.\n";
        return 1;
    }

    sockaddr_in server{};
    server.sin_family = AF_INET;
    server.sin_port = htons(port);
    server.sin_addr.s_addr = inet_addr(aurora_ip);

    if (connect(sock, (sockaddr *)&server, sizeof(server)) < 0)
    {
        std::cerr << "Connection to Aurora failed.\n";
        return 1;
    }

    std::string response = sendCommand(sock, "#TR\n");
    std::cout << "\nRAW RESPONSE FROM AURORA:\n"
              << response << "\n\n";

    std::istringstream stream(response);
    std::string line;
    std::cout << "Received Traffic Data:\n";

    std::vector<Aircraft> aircraftList;
    while (std::getline(stream, line))
    {
        if (!line.empty() &&
            line.find("#TR") == std::string::npos &&
            line.find("Welcome") == std::string::npos &&
            line[0] != '[')
        {
            std::istringstream lineStream(line);
            Aircraft ac;
            lineStream >> ac.callsign >> ac.type >> ac.dep >> ac.arr >> ac.flightlevel;

            aircraftList.push_back(ac);

            std::cout << "* " << ac.callsign << " " << ac.type << " " << ac.dep << " -> " << ac.arr
                      << " FL" << ac.flightlevel;

            std::string typeUpper;
            for (char c : ac.type)
            {
                typeUpper += std::toupper(c);
            }
            std::cout << "   [DEBUG] Normalized type: '" << typeUpper << "'\n";

            if (typeUpper.find("KC") != std::string::npos || typeUpper.find("MRTT") != std::string::npos)
            {
                std::cout << "  <- TANKER";
            }

            std::string fpCmd = "#FP " + ac.callsign + "\n";
            std::string fpResponse = sendCommand(sock, fpCmd);

            if (!fpResponse.empty())
            {
                std::cout << "   [FP] " << fpResponse;
                // check if 'AAR' is mentioned in the flight plan
                if (fpResponse.find("AAR") != std::string::npos || fpResponse.find("TANKER") != std::string::npos)
                {
                    std::cout << "   => AAR-RELATED FLIGHT\n";
                }
            }
            std::cout << '\n';
        }
    }

    std::string input;
    while (true)
    {
        std::cout << "Enter Aurora command (or 'exit'): ";
        std::getline(std::cin, input);
        if (input == "exit")
            break;

        std::string response = sendCommand(sock, input + "\n");
        std::cout << response << "\n";
    }

#ifdef _WIN32
    closesocket(sock);
#else
    close(sock);
#endif
    cleanupSockets();

    return 0;
}
