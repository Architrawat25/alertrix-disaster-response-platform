# alertrix-disaster-response-platform
Alertrix is an AI-driven disaster response and coordination platform designed to help communities respond to natural disasters and emergencies. Core idea is that people can report disaster incidents through a web interface, and the system automatically analyzes these reports using AI to generate actionable alerts for emergency responders and the public.

# Functionality
The system works like this: when someone reports a disaster (like a flood, earthquake, or fire), the system uses AI to understand what type of disaster it is, how severe it is, where exactly it's happening, and creates an organized alert. These alerts are then displayed on a map and in a list so that emergency services and people in the area can see what's happening in real-time.

# System Architecture
The project is built as a full-stack application with a clear separation between frontend and backend:
## Backend: 
I have uilt a FastAPI (Python) server that handles all the business logic, AI processing, and data storage. Deployed on Render
## Frontend: 
Built this using Firebase Studio - it's the user interface where people view alerts on a map and submit new disaster reports. 
Framework: Next.js 14+ with TypeScript 
Styling: Tailwind CSS 
Mapping: Leaflet.js with OpenStreetMap
Deployed on vercel
## Database: 
SQLite, a simple file-based database that works well for this scale.
## AI Services: 
The system can integrate with real AI services like OpenAI and Hugging Face, but by default runs in "mock mode" so it works without any API keys or internet connection.


## Main Application (app/main.py) 
This is the entry point that starts the FastAPI server. It sets up CORS (Cross-Origin Resource Sharing) so the frontend can communicate with the backend, and it initializes the database when the server starts.
API Routes
* /health - Simple endpoint that just returns "ok" to check if the server is running
* /report - Accepts new disaster reports and stores them in the database
* /analyze - Can manually trigger analysis of a specific report
* /alerts - Returns all the generated alerts, with filtering options

# Work is still in progress
