# Bullwhip Effect Simulator

Supply chain simulation for university courses demonstrating how small demand changes at the retail level amplify into large order swings upstream — the **bullwhip effect**.

## Modes

- **Demo Mode** (2-3 min): Auto-plays a 12-week simulation showing the bullwhip effect in a 4-tier supply chain
- **Intro Mode** (15 min): Students play as the retailer, making ordering decisions and observing upstream impact

## Quick Start

### Backend (Terminal 1)
```bash
cd backend
pip install fastapi uvicorn python-multipart
python3 beer_game_backend.py
```
API docs at http://localhost:8000/docs

### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm start
```
Opens at http://localhost:3000

## Architecture

React (port 3000) → HTTP fetch → FastAPI (port 8000) → JSON game state

- **Backend**: Single-file Python FastAPI server. In-memory game state, no database.
- **Frontend**: React 18 single-component app. No routing or state library.
- **Supply Chain**: 4 tiers (Retailer → Wholesaler → Distributor → Manufacturer), 1-week lead time, $0.50/unit holding cost, $1.00/unit backorder cost.

## Deployment

- **Frontend**: Vercel
- **Backend**: Railway

## License

MIT
