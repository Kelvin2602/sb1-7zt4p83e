/*
  # Chat Application Schema

  1. New Tables
    - `rooms`
      - `id` (uuid, primary key)
      - `name` (text, required)
      - `description` (text)
      - `created_at` (timestamp)
      - `created_by` (uuid, references auth.users)

    - `room_members`
      - `room_id` (uuid, references rooms)
      - `user_id` (uuid, references auth.users)
      - `joined_at` (timestamp)

  2. Security
    - Enable RLS on all tables
    - Add policies for room access and message management
*/

-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    description text,
    created_at timestamptz DEFAULT now(),
    created_by uuid REFERENCES auth.users(id)
);

-- Room members table
CREATE TABLE IF NOT EXISTS room_members (
    room_id uuid REFERENCES rooms(id) ON DELETE CASCADE,
    user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
    joined_at timestamptz DEFAULT now(),
    PRIMARY KEY (room_id, user_id)
);

-- Enable RLS
ALTER TABLE rooms ENABLE ROW LEVEL SECURITY;
ALTER TABLE room_members ENABLE ROW LEVEL SECURITY;

-- Policies for rooms
CREATE POLICY "Users can view rooms they are members of"
    ON rooms FOR SELECT
    USING (
        id IN (
            SELECT room_id 
            FROM room_members 
            WHERE user_id = auth.uid()
        )
    );

CREATE POLICY "Users can create rooms"
    ON rooms FOR INSERT
    WITH CHECK (auth.uid() = created_by);

-- Policies for room members
CREATE POLICY "Users can view room members"
    ON room_members FOR SELECT
    USING (true);

CREATE POLICY "Users can join rooms"
    ON room_members FOR INSERT
    WITH CHECK (auth.uid() = user_id);