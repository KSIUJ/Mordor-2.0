-- Basic users information table
CREATE TABLE users (
  id serial PRIMARY KEY,
  username varchar UNIQUE NOT NULL,  -- Unique username for each user
  password varchar NOT NULL,         -- Hashed password storage
  role varchar NOT NULL              -- User role for permissions
);

-- Additional information about users (may need improvement)
CREATE TABLE users_info (
  id integer REFERENCES users.id,  -- References users table
  email varchar UNIQUE              -- Unique email for each user
);

-- Table defining upload limits for different user roles
CREATE TABLE users_limits (
  user_role varchar PRIMARY KEY REFERENCES users.role,  -- References user roles
  size_limit numeric DEFAULT 10000000,    -- Size limit in bytes (default 10MB)
  number_limit integer DEFAULT 20         -- Maximum number of files allowed
);

-- Files recently opened by users
CREATE TABLE recently_opened (
  user_id integer REFERENCES users.id,    -- Which user opened the file
  file_id integer REFERENCES files.id,    -- Which file was opened
  opened_at timestamp,                     -- When the file was opened
  UNIQUE (user_id, file_id)                -- Each user-file pair is unique
);

-- Files storage information
CREATE TABLE files (
  id serial PRIMARY KEY,
  name varchar NOT NULL,               -- Display name of the file
  filepath varchar NOT NULL,           -- Physical path to the file
  status varchar DEFAULT 'pending',    -- File status: pending/accepted/rejected
  size integer NOT NULL,               -- File size in bytes
  uploaded_at timestamp,               -- Timestamp of upload
  uploaded_by integer REFERENCES users.id  -- User who uploaded the file
);

-- Tags information
CREATE TABLE tags (
  id serial PRIMARY KEY,
  name varchar UNIQUE NOT NULL  -- Unique tag name
);

-- Junction table connecting files and tags
CREATE TABLE tag_file (
  file_id integer REFERENCES files.id,   -- Reference to file
  tag_id integer REFERENCES tags.id,     -- Reference to tag
  UNIQUE (file_id, tag_id)               -- Each file-tag combination is unique
);

-- Index on file status for faster filtering
CREATE INDEX ON files (status);