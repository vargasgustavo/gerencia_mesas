import threading
try:
self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
self.running = True
self.listener_thread = threading.Thread(target=self._listen, daemon=True)
self.listener_thread.start()
self.state.update({'state':'IDLE','is_connected':True, 'last_update': time.strftime('%Y-%m-%dT%H:%M:%S')})
return True, 'connected'
except Exception as e:
return False, str(e)


def disconnect(self):
self.running = False
if self.ser and self.ser.is_open:
self.ser.close()
self.state.update({'state':'DISCONNECTED','is_connected':False})


def _listen(self):
while self.running and self.ser and self.ser.is_open:
try:
line = self.ser.readline().decode('utf-8').strip()
if line:
# handle messages
print('arduino->', line)
# simple parser
parts = line.split(':')
if parts[0] == 'STATUS':
# STATUS:IDLE:BASE
_, st, cur = parts[:3]
self.state.update({'state': st, 'current_table': cur, 'last_update': time.strftime('%Y-%m-%dT%H:%M:%S')})
except Exception as e:
print('robot listen error', e)
time.sleep(0.5)


def _send(self, cmd: str):
with self.lock:
if not self.ser or not self.ser.is_open:
return False, 'not connected'
try:
self.ser.write((cmd + '\n').encode('utf-8'))
return True, None
except Exception as e:
return False, str(e)


def send_move(self, table_id):
return self._send(f'MOVE:T{int(table_id):02d}')


def send_clean(self, table_id):
return self._send(f'CLEAN:T{int(table_id):02d}')


def send_check(self, table_id):
return self._send(f'CHECK:T{int(table_id):02d}')


def send_return(self):
return self._send('RETURN')


def send_stop(self):
return self._send('STOP')


def get_status(self):
return self.state