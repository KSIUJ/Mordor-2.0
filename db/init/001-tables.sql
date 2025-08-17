-- Table defining upload limits for different user roles
CREATE TABLE users_limits (
  user_role varchar PRIMARY KEY,  -- References user roles
  size_limit numeric DEFAULT 10000000,    -- Size limit in bytes (default 10MB)
  number_limit integer DEFAULT 20         -- Maximum number of files allowed
);

-- Basic users information table
CREATE TABLE users (
  id integer PRIMARY KEY AUTOINCREMENT,
  username varchar(50) UNIQUE NOT NULL,  -- Unique username for each user
  role varchar NOT NULL references users_limits(user_role),   -- User role for permissions
  email varchar(100) UNIQUE               -- Unique email for each user
);

-- Files storage information
CREATE TABLE files (
  id integer PRIMARY KEY AUTOINCREMENT,
  name varchar(100) NOT NULL,          -- Display name of the file
  filepath varchar NOT NULL CHECK (name <> ''),     -- Physical path to the file
  status varchar DEFAULT 'pending',    -- File status: pending/accepted/rejected
  size integer NOT NULL,               -- File size in bytes
  uploaded_at timestamp DEFAULT CURRENT_TIMESTAMP,               -- Timestamp of upload
  uploaded_by integer REFERENCES users(id)  -- User who uploaded the file
);

-- Files recently opened by users
CREATE TABLE recently_opened (
  user_id integer REFERENCES users(id),    -- Which user opened the file
  file_id integer REFERENCES files(id),    -- Which file was opened
  opened_at timestamp,                     -- When the file was opened
  UNIQUE (user_id, file_id)                -- Each user-file pair is unique
);

-- Tags information
CREATE TABLE tags (
  id integer PRIMARY KEY AUTOINCREMENT,
  name varchar(50) UNIQUE NOT NULL  -- Unique tag name
);

-- Junction table connecting files and tags
CREATE TABLE tag_file (
  file_id integer REFERENCES files(id),   -- Reference to file
  tag_id integer REFERENCES tags(id),     -- Reference to tag
  UNIQUE (file_id, tag_id)                -- Each file-tag combination is unique
);

-- Index on file status for faster filtering
CREATE INDEX idx_files_status ON files (status);