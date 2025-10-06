// // RobotController.cpp
// #include "RobotController.h"

// // Define constantes
// const unsigned long RobotController::MOVE_TIME_PER_TABLE = 2000UL; // 2s por "unidade"
// const unsigned long RobotController::MIN_MOVE_TIME = 1000UL;       // tempo mínimo de movimento
// const unsigned long RobotController::CLEAN_DURATION = 5000UL;      // 5s para limpeza
// const unsigned long RobotController::CHECK_DURATION = 2000UL;      // 2s para checagem
// const unsigned long RobotController::HEARTBEAT_INTERVAL = 10000UL; // 10s

// RobotController::RobotController(uint8_t ledPin_)
//     : state(ST_IDLE),
//       current_table(0),
//       target_table(0),
//       action_start(0),
//       action_duration(0),
//       last_heartbeat(0),
//       incomingLine(""),
//       next_action_after_arrival(0),
//       ledPin(ledPin_)
// {
// }

// void RobotController::begin(unsigned long baud)
// {
//     pinMode(ledPin, OUTPUT);
//     digitalWrite(ledPin, LOW);

//     Serial.begin(baud);
//     delay(50);
//     sendStatus();
//     last_heartbeat = millis();
// }

// void RobotController::update()
// {
//     handleSerialInput();
//     processState();

//     if (millis() - last_heartbeat >= HEARTBEAT_INTERVAL)
//     {
//         sendStatus();
//         last_heartbeat = millis();
//     }
// }

// void RobotController::handleSerialInput()
// {
//     if (Serial.available())
//     {
//         incomingLine = Serial.readStringUntil('\n');
//         incomingLine.trim();
//         if (incomingLine.length() > 0)
//         {
//             Serial.print("COMMAND_RECEIVED:");
//             Serial.println(incomingLine);
//             handleCommand(incomingLine);
//         }
//     }
// }

// const char *RobotController::stateToString(RobotState s)
// {
//     switch (s)
//     {
//     case ST_IDLE:
//         return "IDLE";
//     case ST_MOVING:
//         return "MOVING";
//     case ST_CLEANING:
//         return "CLEANING";
//     case ST_CHECKING:
//         return "CHECKING";
//     case ST_RETURNING:
//         return "RETURNING";
//     case ST_STOPPED:
//         return "STOPPED";
//     default:
//         return "UNKNOWN";
//     }
// }

// String RobotController::locationToString(int t)
// {
//     if (t <= 0)
//         return "BASE";
//     char buf[8];
//     snprintf(buf, sizeof(buf), "T%02d", t);
//     return String(buf);
// }

// int RobotController::parseTableId(const String &s)
// {
//     String tmp = s;
//     tmp.trim();
//     if (tmp.length() == 0)
//         return -1;
//     if (tmp.startsWith("T") || tmp.startsWith("t"))
//         tmp = tmp.substring(1);
//     tmp.trim();
//     if (tmp.length() == 0)
//         return -1;
//     int val = tmp.toInt();
//     if (val < 0)
//         return -1;
//     return val; // 0 é BASE
// }

// void RobotController::sendStatus()
// {
//     Serial.print("STATUS:");
//     Serial.print(stateToString(state));
//     Serial.print(':');
//     Serial.println(locationToString(current_table));
// }

// void RobotController::handleCommand(const String &cmd)
// {
//     String c = cmd;
//     c.trim();
//     String u = c;
//     u.toUpperCase();

//     if (u == "RETURN")
//     {
//         target_table = 0;
//         startMoveToTarget();
//         return;
//     }

//     if (u == "STOP")
//     {
//         state = ST_STOPPED;
//         action_duration = 0;
//         digitalWrite(ledPin, LOW);
//         sendStatus();
//         return;
//     }

//     if (u.startsWith("MOVE:"))
//     {
//         int p = c.indexOf(':');
//         String arg = (p >= 0) ? c.substring(p + 1) : String("");
//         int tid = parseTableId(arg);
//         if (tid < 0)
//         {
//             Serial.println("ERROR:INVALID_TABLE_ID");
//             return;
//         }
//         target_table = tid;
//         startMoveToTarget();
//         return;
//     }

//     if (u.startsWith("CLEAN:"))
//     {
//         int p = c.indexOf(':');
//         String arg = (p >= 0) ? c.substring(p + 1) : String("");
//         int tid = parseTableId(arg);
//         if (tid < 0)
//         {
//             Serial.println("ERROR:INVALID_TABLE_ID");
//             return;
//         }
//         if (current_table != tid)
//         {
//             target_table = tid;
//             next_action_after_arrival = 'C';
//             startMoveToTarget();
//         }
//         else
//         {
//             startCleaning();
//         }
//         return;
//     }

//     if (u.startsWith("CHECK:"))
//     {
//         int p = c.indexOf(':');
//         String arg = (p >= 0) ? c.substring(p + 1) : String("");
//         int tid = parseTableId(arg);
//         if (tid < 0)
//         {
//             Serial.println("ERROR:INVALID_TABLE_ID");
//             return;
//         }
//         if (current_table != tid)
//         {
//             target_table = tid;
//             next_action_after_arrival = 'K';
//             startMoveToTarget();
//         }
//         else
//         {
//             startChecking();
//         }
//         return;
//     }

//     Serial.println("ERROR:UNKNOWN_COMMAND");
// }

// void RobotController::startMoveToTarget()
// {
//     if (state == ST_STOPPED)
//     {
//         Serial.println("ERROR:STOPPED_STATE");
//         sendStatus();
//         return;
//     }
//     int distance = abs(target_table - current_table);
//     unsigned long units = (distance > 0) ? (unsigned long)distance : 1UL;
//     unsigned long dur = MOVE_TIME_PER_TABLE * units;
//     if (dur < MIN_MOVE_TIME)
//         dur = MIN_MOVE_TIME;

//     action_start = millis();
//     action_duration = dur;
//     state = (target_table == 0 ? ST_RETURNING : ST_MOVING);
//     digitalWrite(ledPin, HIGH);
//     sendStatus();
// }

// void RobotController::startCleaning()
// {
//     action_start = millis();
//     action_duration = CLEAN_DURATION;
//     state = ST_CLEANING;
//     digitalWrite(ledPin, HIGH);
//     sendStatus();
// }

// void RobotController::startChecking()
// {
//     action_start = millis();
//     action_duration = CHECK_DURATION;
//     state = ST_CHECKING;
//     digitalWrite(ledPin, HIGH);
//     sendStatus();
// }

// void RobotController::processState()
// {
//     if (state == ST_STOPPED)
//         return;

//     if (action_duration > 0)
//     {
//         unsigned long now = millis();
//         if (now - action_start >= action_duration)
//         {
//             // ação finalizou
//             if (state == ST_MOVING || state == ST_RETURNING)
//             {
//                 current_table = target_table;
//                 action_duration = 0;
//                 digitalWrite(ledPin, LOW);
//                 state = ST_IDLE;
//                 sendStatus();

//                 // ações pendentes
//                 if (next_action_after_arrival == 'C')
//                 {
//                     next_action_after_arrival = 0;
//                     startCleaning();
//                 }
//                 else if (next_action_after_arrival == 'K')
//                 {
//                     next_action_after_arrival = 0;
//                     startChecking();
//                 }
//             }
//             else if (state == ST_CLEANING)
//             {
//                 action_duration = 0;
//                 digitalWrite(ledPin, LOW);
//                 state = ST_IDLE;
//                 Serial.println("CLEANING_COMPLETED:OK");
//                 sendStatus();
//             }
//             else if (state == ST_CHECKING)
//             {
//                 action_duration = 0;
//                 digitalWrite(ledPin, LOW);
//                 state = ST_IDLE;
//                 Serial.print("CHECK_RESULT:");
//                 Serial.print(locationToString(current_table));
//                 Serial.println(":OK");
//                 sendStatus();
//             }
//         }
//     }
// }
