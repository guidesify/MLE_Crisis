import { createClient } from '@supabase/supabase-js'

// This is exposed to public but it is okay due to row level security.
export const supabase = createClient('https://gshpvsjdvqzajoicqjbq.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdzaHB2c2pkdnF6YWpvaWNxamJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODYzNzUwNzIsImV4cCI6MjAwMTk1MTA3Mn0.Mi8imeBUZgJITjkxjSDuFjNqaUhWmBc08RJSZiVGJFg', {
      auth: {
        persistSession: false,
      },
    })