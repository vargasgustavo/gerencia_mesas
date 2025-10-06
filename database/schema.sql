-- users
CREATE TABLE
    IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

CREATE TABLE
    IF NOT EXISTS auth_tokens (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        token VARCHAR(255) UNIQUE NOT NULL,
        expires_at TIMESTAMP NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS tables (
        id INT AUTO_INCREMENT PRIMARY KEY,
        table_number VARCHAR(10) UNIQUE NOT NULL,
        capacity INT NOT NULL DEFAULT 4,
        x_position FLOAT DEFAULT 0,
        y_position FLOAT DEFAULT 0,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

CREATE TABLE
    IF NOT EXISTS table_status (
        id INT AUTO_INCREMENT PRIMARY KEY,
        table_id INT NOT NULL,
        status ENUM ('empty', 'occupied', 'reserved', 'cleaning') DEFAULT 'empty',
        detected_by ENUM ('manual', 'camera', 'robot') DEFAULT 'manual',
        confidence_score FLOAT DEFAULT 1.0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (table_id) REFERENCES tables (id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS reservations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        table_id INT NOT NULL,
        customer_name VARCHAR(100) NOT NULL,
        customer_phone VARCHAR(20),
        reservation_time TIMESTAMP NOT NULL,
        party_size INT NOT NULL,
        status ENUM (
            'pending',
            'confirmed',
            'seated',
            'completed',
            'cancelled'
        ) DEFAULT 'pending',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (table_id) REFERENCES tables (id) ON DELETE CASCADE
    );

CREATE TABLE
    IF NOT EXISTS robot_commands (
        id INT AUTO_INCREMENT PRIMARY KEY,
        command_type ENUM ('move', 'clean', 'check', 'return') NOT NULL,
        table_id INT,
        status ENUM ('pending', 'executing', 'completed', 'failed') DEFAULT 'pending',
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP NULL,
        response TEXT,
        FOREIGN KEY (table_id) REFERENCES tables (id) ON DELETE SET NULL
    );

CREATE TABLE
    IF NOT EXISTS system_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        log_level ENUM ('info', 'warning', 'error', 'debug') DEFAULT 'info',
        module VARCHAR(50) NOT NULL,
        message TEXT NOT NULL,
        details JSON,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

-- indices
CREATE INDEX IF NOT EXISTS idx_table_status_table_id ON table_status (table_id);

CREATE INDEX IF NOT EXISTS idx_table_status_created_at ON table_status (created_at);

CREATE INDEX IF NOT EXISTS idx_reservations_table_id ON reservations (table_id);

CREATE INDEX IF NOT EXISTS idx_reservations_time ON reservations (reservation_time);

CREATE INDEX IF NOT EXISTS idx_robot_commands_status ON robot_commands (status);

CREATE INDEX IF NOT EXISTS idx_auth_tokens_token ON auth_tokens (token);

CREATE INDEX IF NOT EXISTS idx_auth_tokens_expires ON auth_tokens (expires_at);