# AAR Aurora – Air-to-Air Refueling Coordinator for IVAO Aurora

**AAR Aurora** is a desktop application developed in C++ to support **IVAO Special Operations** in managing **Air-to-Air Refueling (AAR)** procedures within the Aurora radar system.

This tool connects with Aurora via TCP and enhances operational efficiency by providing real-time data visualization and coordination features between tanker and receiver aircraft.

---

## Features

- Live tanker and receiver pairing with real-time session updates
- TCP-based integration with Aurora over port 1130 using the 3rd-party API
- Visual indication of tanker status, position, and assigned receivers
- Easy-to-use interface tailored for IVAO ATC controllers involved in special ops
- Logs and monitors refueling session durations and statuses

---

## Getting Started

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/SpaceMikha/aar-aurora.git
   ```
2. Open the project in your C++ IDE (e.g., Visual Studio or VS Code)
3. Configure CMake if needed and build the project
4. Run the application while Aurora is running

---

## Usage

1. Launch **AAR Aurora** while connected to Aurora.
2. Monitor live aircraft relevant to AAR operations.
3. Assign receivers to tankers using the UI.
4. The tool will handle and monitor sessions automatically.

---

## Architecture Overview

- Language: C++
- Framework: Qt (planned/optional for UI)
- Communication: TCP client to Aurora's 3rd party API
- Aurora Commands Used: `#TR`, `#FP`, `#MSGFR`, `#MSGPM`, `#LBALT`, `#LBSQK`

---

## Contribution

Contributions are welcome. Please open an issue or submit a pull request.

---

## Author

Developed by Mikhael da Silva.