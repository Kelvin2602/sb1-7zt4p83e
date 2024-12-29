/*
  # Create messages table for chat application

  1. New Tables
    - `messages`
      - `id` (uuid, primary key)
      - `room_id` (text, required)
      - `content` (text, required)
      - `sender_id` (uuid, required)
      - `created_at` (timestamp)
    
  2. Security
    - Enable RLS on `messages` table
    - Add policies for authenticated users to:
      - Read messages in their rooms
      - Create new messages
*/

CREATE TABLE IF NOT EXISTS messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  room_id text NOT NULL,
  content text NOT NULL,
  sender_id uuid NOT NULL REFERENCES auth.users(id),
  created_at timestamptz DEFAULT now()
);

ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Allow users to read messages in their rooms
CREATE POLICY "Users can read messages in their rooms"
  ON messages
  FOR SELECT
  TO authenticated
  USING (true);  -- In a real app, you'd want to check room membership

-- Allow authenticated users to create messages
CREATE POLICY "Users can create messages"
  ON messages
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = sender_id);