// // RobotController.h
// #ifndef ROBOT_CONTROLLER_H
// #define ROBOT_CONTROLLER_H

// #include <Arduino.h>

// class RobotController
// {
// public:
//     enum RobotState
//     {
//         ST_IDLE,
//         ST_MOVING,
//         ST_CLEANING,
//         ST_CHECKING,
//         ST_RETURNING,
//         ST_STOPPED
//     };

//     RobotController(uint8_t ledPin = 13);

//     // Inicializa (chamar em setup())
//     void begin(unsigned long baud = 9600);

//     // Atualiza o controlador (chamar repetidamente em loop())
//     void update();

//     // Envia atualmente não exposto: todas as entradas são lidas internamente

// private:
//     // Temporizações (ms)
//     static const unsigned long MOVE_TIME_PER_TABLE;
//     static const unsigned long MIN_MOVE_TIME;
//     static const unsigned long CLEAN_DURATION;
//     static const unsigned long CHECK_DURATION;
//     static const unsigned long HEARTBEAT_INTERVAL;

//     RobotState state;
//     int current_table;
//     int target_table;

//     unsigned long action_start;
//     unsigned long action_duration;
//     unsigned long last_heartbeat;

//     String incomingLine;
//     // flag para ação após chegada: '\0' = nenhuma, 'C' = CLEAN, 'K' = CHECK
//     char next_action_after_arrival;

//     uint8_t ledPin;

//     // helpers
//     const char *stateToString(RobotState s);
//     String locationToString(int t);
//     int parseTableId(const String &s);
//     void sendStatus();
//     void handleSerialInput();
//     void handleCommand(const String &cmd);
//     void startMoveToTarget();
//     void startCleaning();
//     void startChecking();
//     void processState();
// };

// #endif // ROBOT_CONTROLLER_H
