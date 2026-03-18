"""
Beer Game Supply Chain Simulation - Backend Logic
Demonstrates the Bullwhip Effect in a 4-tier supply chain

Tiers: Retailer -> Wholesaler -> Distributor -> Manufacturer
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import math

app = FastAPI()

# Allow React frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== GAME STATE ====================

class Tier:
    """Represents one tier in the supply chain"""
    def __init__(self, name: str, initial_inventory: int = 12):
        self.name = name
        self.inventory = initial_inventory
        self.orders_placed = []  # Orders sent to supplier each week
        self.orders_received = []  # Orders received from customer each week
        self.costs = 0  # Cumulative holding + backorder costs
        self.backorder = 0  # Unfulfilled demand
        
    def receive_order(self, amount: int):
        """Customer places an order"""
        self.orders_received.append(amount)
        
    def place_order(self, amount: int):
        """Place order to supplier"""
        self.orders_placed.append(amount)
        
    def fulfill_demand(self, demand: int) -> int:
        """Fulfill what we can from inventory"""
        fulfilled = min(demand, self.inventory)
        self.inventory -= fulfilled
        
        # Handle backorder
        unfulfilled = demand - fulfilled
        if unfulfilled > 0:
            self.backorder += unfulfilled
        
        return fulfilled

class BeerGame:
    """Main beer game simulation engine"""
    def __init__(self):
        # Initialize tiers
        self.retailer = Tier("Retailer")
        self.wholesaler = Tier("Wholesaler")
        self.distributor = Tier("Distributor")
        self.manufacturer = Tier("Manufacturer")
        
        self.tiers = [self.retailer, self.wholesaler, self.distributor, self.manufacturer]
        
        # Game state
        self.current_week = 0
        self.max_weeks = 0
        self.customer_demand = []  # Exogenous demand at retail
        
        # Inventory in transit (lead time = 1 week)
        self.retailer_inbound = 0
        self.wholesaler_inbound = 0
        self.distributor_inbound = 0
        self.manufacturer_inbound = 0
        
    def set_demand_pattern(self, pattern: List[int]):
        """Set the demand pattern for the game"""
        self.customer_demand = pattern
        self.max_weeks = len(pattern)
        
    def process_week(self, retailer_order: int = None):
        """
        Process one week of the game.
        
        Flow:
        1. Customer demand arrives at retailer
        2. Retailer fulfills from inventory
        3. Each tier receives goods from supplier
        4. Each tier places orders based on decision rule
        5. Calculate costs
        """
        
        # Get customer demand for this week
        if self.current_week >= len(self.customer_demand):
            return False
            
        demand = self.customer_demand[self.current_week]
        
        # --- WEEK STARTS ---
        
        # Retailer decides what to order
        # If player controls retailer, use retailer_order param
        # Otherwise use simple rule (order = demand)
        if retailer_order is None:
            retailer_order = demand
        
        # Step 1: Goods arrive from inbound pipelines
        self.retailer.inventory += self.retailer_inbound
        self.wholesaler.inventory += self.wholesaler_inbound
        self.distributor.inventory += self.distributor_inbound
        self.manufacturer.inventory += self.manufacturer_inbound
        
        # Reset pipelines
        self.retailer_inbound = 0
        self.wholesaler_inbound = 0
        self.distributor_inbound = 0
        self.manufacturer_inbound = 0
        
        # Step 2: Retailer receives customer demand
        self.retailer.receive_order(demand)
        fulfilled = self.retailer.fulfill_demand(demand)
        
        # Step 3: Wholesaler receives retailer's order
        self.wholesaler.receive_order(retailer_order)
        fulfilled_w = self.wholesaler.fulfill_demand(retailer_order)
        self.retailer_inbound = fulfilled_w  # Goods in transit to retailer
        
        # Step 4: Distributor receives wholesaler's order
        # Wholesaler orders what they couldn't fulfill
        wholesaler_order = retailer_order  # Simple rule: order = demand
        self.distributor.receive_order(wholesaler_order)
        fulfilled_d = self.distributor.fulfill_demand(wholesaler_order)
        self.wholesaler_inbound = fulfilled_d
        
        # Step 5: Manufacturer receives distributor's order
        distributor_order = wholesaler_order  # Simple rule
        self.manufacturer.receive_order(distributor_order)
        fulfilled_m = self.manufacturer.fulfill_demand(distributor_order)
        self.distributor_inbound = fulfilled_m
        
        # Manufacturer always produces (unlimited capacity)
        # Order to manufacturer goes to "supplier" (outside system)
        manufacturer_order = distributor_order
        self.manufacturer_inbound = distributor_order  # They produce
        
        # Step 6: Calculate costs (inventory holding + backorder penalties)
        for tier in self.tiers:
            holding_cost = tier.inventory * 0.5  # $0.50 per unit per week
            backorder_cost = tier.backorder * 1.0  # $1.00 per unit per week
            tier.costs += holding_cost + backorder_cost
        
        # Record orders
        self.retailer.place_order(retailer_order)
        self.wholesaler.place_order(wholesaler_order)
        self.distributor.place_order(distributor_order)
        self.manufacturer.place_order(manufacturer_order)
        
        self.current_week += 1
        return True
    
    def auto_play(self, demand_pattern: List[int]):
        """Auto-play entire game with default rules"""
        self.set_demand_pattern(demand_pattern)
        
        while self.current_week < len(self.customer_demand):
            self.process_week()  # Use default ordering rule
    
    def get_state(self) -> Dict:
        """Return current game state as JSON"""
        return {
            "week": self.current_week,
            "retailer": {
                "name": "Retailer",
                "inventory": self.retailer.inventory,
                "orders_placed": self.retailer.orders_placed,
                "orders_received": self.retailer.orders_received,
                "costs": round(self.retailer.costs, 2),
            },
            "wholesaler": {
                "name": "Wholesaler",
                "inventory": self.wholesaler.inventory,
                "orders_placed": self.wholesaler.orders_placed,
                "orders_received": self.wholesaler.orders_received,
                "costs": round(self.wholesaler.costs, 2),
            },
            "distributor": {
                "name": "Distributor",
                "inventory": self.distributor.inventory,
                "orders_placed": self.distributor.orders_placed,
                "orders_received": self.distributor.orders_received,
                "costs": round(self.distributor.costs, 2),
            },
            "manufacturer": {
                "name": "Manufacturer",
                "inventory": self.manufacturer.inventory,
                "orders_placed": self.manufacturer.orders_placed,
                "orders_received": self.manufacturer.orders_received,
                "costs": round(self.manufacturer.costs, 2),
            },
            "customer_demand": self.customer_demand,
        }

# ==================== GLOBAL GAME INSTANCE ====================
game = BeerGame()

# ==================== API ENDPOINTS ====================

@app.post("/api/demo")
def run_demo():
    """Run auto-play demo: small demand increase, watch bullwhip"""
    global game
    game = BeerGame()
    
    # Demand pattern: stable at 4, then jump to 8, then drop back to 4
    demand = [4, 4, 4, 4, 8, 8, 8, 8, 4, 4, 4, 4]
    game.auto_play(demand)
    
    return game.get_state()

@app.post("/api/new-game")
def new_game():
    """Start a new interactive game"""
    global game
    game = BeerGame()
    
    # Intro mode: stable demand for 12 weeks
    demand = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    game.set_demand_pattern(demand)
    
    return {"status": "Game started", "max_weeks": game.max_weeks}

@app.post("/api/place-order")
def place_order(retailer_order: int):
    """Player places an order as retailer"""
    global game
    
    if game.current_week >= game.max_weeks:
        return {"error": "Game over"}
    
    game.process_week(retailer_order)
    return game.get_state()

@app.get("/api/state")
def get_game_state():
    """Get current game state"""
    return game.get_state()

# ==================== ENTRY POINT ====================

if __name__ == "__main__":
    import uvicorn
    print("\n🍺 BEER GAME BACKEND STARTING...")
    print("Running on http://localhost:8000")
    print("Docs: http://localhost:8000/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
