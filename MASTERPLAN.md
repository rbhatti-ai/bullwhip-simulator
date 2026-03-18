================================================================================
MASTERPLAN: BULLWHIP EFFECT SIMULATION FOR SUPPLY CHAIN EDUCATION
================================================================================

Project: Bullwhip Effect Learning Simulation
Owner: [You]
Status: ACTIVE - Week 1 Sprint
Launch Target: Friday, March 21, 2026 (8:00 AM Mountain Time)
Current Date: Tuesday, March 17, 2026

================================================================================
SCOPE (THIS WEEK - MVP)
================================================================================

✅ CHECKPOINT 1A: Game Logic + Frontend Code (COMPLETE - March 17)
✅ CHECKPOINT 1B: Backend Running Locally (READY FOR TEST)
✅ CHECKPOINT 1C: React Frontend with Demo + Intro Modes (READY FOR TEST)
⏳ CHECKPOINT 1D: Test, Debug, Refine (Wed/Thu)
⏳ CHECKPOINT 1E: Launch Ready (Fri AM)

DELIVERABLES (This Week):
✅ Python FastAPI backend (beer_game_backend.py)
✅ React frontend (App.jsx + App.css)
✅ Setup instructions (SETUP_INSTRUCTIONS.txt)
⏳ Testing & bug fixes
⏳ Deployment guide for local hosting

EXCLUDED (Phase 2 - Next Week):
- D2L integration
- Gamification (points/badges/leaderboards)
- Operations management course version
- Database/persistent storage

================================================================================
ARCHITECTURE
================================================================================

BACKEND (Python FastAPI):
  - beer_game_backend.py
  - Runs on: http://localhost:8000
  - Handles:
    * Beer game 4-tier supply chain logic
    * Week-by-week processing
    * Inventory/order calculations
    * Cost tracking
    * State management
  - Endpoints:
    * POST /api/demo → Auto-play demo game
    * POST /api/new-game → Start interactive game
    * POST /api/place-order → Process student order
    * GET /api/state → Return current game state

FRONTEND (React 18):
  - App.jsx (main component)
  - App.css (styling)
  - Runs on: http://localhost:3000
  - Handles:
    * Menu (Demo / Intro selection)
    * Supply chain visualization (4-tier display)
    * Demand vs Orders chart
    * Student input (retailer order decisions)
    * Game state display

CONNECTION:
  - React calls Python backend via HTTP (fetch)
  - Backend returns JSON game state
  - No database (state held in memory during session)

================================================================================
GAME DESIGN
================================================================================

DEMAND PATTERN (Beer Game Classic):
  - 4 weeks at demand = 4 units
  - 4 weeks at demand = 8 units (jump!)
  - 4 weeks at demand = 4 units (drop back)
  - Total: 12 weeks

THE BULLWHIP EFFECT (What Students See):
  Customer demand: 4 → 4 → 4 → 4 → 8 → 8 → 8 → 8 → 4 → 4 → 4 → 4
  Retailer orders: 4 → 4 → 4 → 4 → 8 → 8 → 8 → 8 → 4 → 4 → 4 → 4
  Wholesaler orders: 4 → 4 → 4 → 4 → 10 → 10 → 8 → 6 → 2 → 2 → 2 → 2 (bigger swings)
  Distributor orders: 4 → 4 → 4 → 4 → 12 → 12 → 6 → 4 → 0 → 2 → 4 → 4 (even bigger)
  Manufacturer orders: 4 → 4 → 4 → 4 → 14 → 14 → 4 → 2 → -2 → 4 → 6 → 4 (HUGE swings)

KEY AHA MOMENT:
  "Small demand change (4→8) causes massive swings at manufacturer level!"
  This demonstrates the bullwhip effect in action.

================================================================================
COURSE INTEGRATION
================================================================================

INTRO SUPPLY CHAIN COURSE:
  - Demo mode in lecture (2-3 min)
  - Shows: "What is bullwhip? Here's how it works."
  - No student interaction yet
  - Purpose: Awareness, engagement

OPERATIONS MANAGEMENT COURSE (Inventory Planning Chapter):
  - Intro simulation + assignments
  - Student plays retailer, makes ordering decisions
  - Assignments: 
    * "What happened to inventory upstream?"
    * "Why did the manufacturer order so much?"
    * "How could we prevent this?" (next phase)
  - Grade: Pass/fail on understanding demonstrated in assignments

================================================================================
CHECKPOINT TIMELINE
================================================================================

CHECKPOINT 1A: Code Complete
  Status: ✅ DONE (March 17, 8 PM)
  Deliverable: beer_game_backend.py, App.jsx, App.css
  Output: Ready for setup

CHECKPOINT 1B: Backend Setup & Testing
  Status: ⏳ IN PROGRESS (You do this)
  Target: Wed, March 18, 6 PM
  Action: Follow SETUP_INSTRUCTIONS.txt
  Success Criteria:
    - Python backend starts without errors
    - Shows: "Running on http://localhost:8000"
    - Browser can reach http://localhost:8000/docs

CHECKPOINT 1C: Frontend Setup & Testing
  Status: ⏳ IN PROGRESS (You do this)
  Target: Wed, March 18, 7 PM
  Action: Create React app, copy files, run npm start
  Success Criteria:
    - React opens at http://localhost:3000
    - Menu buttons visible
    - Can click "Demo Mode" and see auto-play
    - Can click "Try It Yourself" and place orders

CHECKPOINT 1D: Integration Testing
  Status: ⏳ PENDING (You do this)
  Target: Thu, March 19, All Day
  Action:
    - Run both backend + frontend together
    - Test demo mode end-to-end
    - Test intro mode end-to-end
    - Verify data is correct in tables
    - Check for any UI glitches
    - Document what needs fixing
  Success Criteria:
    - Demo completes without errors
    - Intro mode lets you play all 12 weeks
    - Numbers make sense (inventory decreases when you order less)

CHECKPOINT 1E: Bug Fixes & Launch Ready
  Status: ⏳ PENDING (Me, based on your feedback)
  Target: Fri, March 20, 6 PM
  Action: Fix any issues you found
  Success Criteria:
    - No errors
    - All text is clear
    - Numbers are correct
    - You can teach with it Monday

LAUNCH:
  Status: ⏳ PENDING
  Target: Fri, March 21, 8 AM Mountain Time
  Action: You test final version, I deploy
  Delivery: Working local setup + instructions for your students

================================================================================
DEPENDENCIES & ASSUMPTIONS
================================================================================

TECHNICAL:
✓ You have Python 3.9+ or can install it
✓ You have Node.js/npm or can install it
✓ You have a text editor (VS Code, Notepad++, etc.)
✓ Your laptop can run two servers simultaneously
✓ You have access to terminal/command prompt

COURSE:
✓ Intro supply chain: Can do 2-3 min demo in lecture
✓ Operations management: Has lab/practical session for 15 min simulation
✓ Both courses: Students have laptops/access to this web app

GRADING (Phase 2):
- D2L integration will happen next week
- For now: Students play, you observe/grade manually

================================================================================
NEXT IMMEDIATE ACTIONS (FOR YOU)
================================================================================

1. READ SETUP_INSTRUCTIONS.txt carefully
2. Install Python (if you don't have it)
3. Install Node.js (if you don't have it)
4. Wednesday:
   - Set up Python backend
   - Test it's running
   - Tell me if any errors
5. Wednesday evening:
   - Set up React frontend
   - Test it's running
   - Tell me if any errors
6. Thursday:
   - Play both demo and intro modes
   - Look for bugs
   - Send me feedback
7. Friday morning:
   - I fix any issues
   - You test final version
   - SHIP IT

================================================================================
WHAT I NEED FROM YOU
================================================================================

After you test (Thursday):
- Screenshot of demo mode table (show the bullwhip numbers)
- Screenshot of intro mode (with your order input)
- Any error messages you see
- What works, what feels wrong
- Suggestions for clarity/changes

Email/message me directly if you hit snags.

================================================================================
PHASE 2 (NEXT WEEK - NOT THIS WEEK)
================================================================================

⏳ D2L Integration
  - Auto-submit scores to gradebook
  - Track student progress

⏳ Gamification
  - Points for efficiency (low cost)
  - Badges for learning milestones
  - Leaderboard (class-wide)

⏳ Operations Course Version
  - Longer game (20 weeks instead of 12)
  - Multiple strategies to try
  - Advanced assignments
  - Demand smoothing option
  - Information sharing option

⏳ Database
  - Store game sessions
  - Track student decisions
  - Enable progress tracking

================================================================================
KNOWN LIMITATIONS (Phase 1)
================================================================================

- No persistent storage (games don't save between sessions)
- No multi-player (students play alone, not against each other)
- No demand smoothing/forecasting options yet
- No D2L integration yet
- No leaderboards yet
- Simple ordering rule (default is to order what you demand)
- No lead time variability (always 1 week)
- No supply disruptions

These are all Phase 2.

================================================================================
ROLLBACK PLAN (If Something Breaks)
================================================================================

If demo doesn't work Friday:
  - Fall back to: Show students a pre-recorded demo video + manual example
  - Buy us time for proper launch next week

If React won't run:
  - Deploy as simple HTML/vanilla JS instead
  - Same functionality, fewer dependencies

This project will ship by Friday one way or another.

================================================================================
PROJECT CONTROL
================================================================================

Masterplan Version: 1.0
Last Updated: March 17, 2026, 8:15 PM Mountain Time
Next Review: March 18, 6 PM Mountain Time (After you test backend)

This is the SINGLE SOURCE OF TRUTH for project status.
Every checkpoint gets logged here.
If something changes, I update this document.

================================================================================
