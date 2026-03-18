import React, { useState } from 'react';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [gameState, setGameState] = useState(null);
  const [mode, setMode] = useState(null); // null, 'demo', 'intro'
  const [retailerOrder, setRetailerOrder] = useState('4');
  const [gameOver, setGameOver] = useState(false);

  // Run demo: auto-play
  const startDemo = async () => {
    setMode('demo');
    setDemoRunning(true);
    setGameOver(false);
    
    try {
      const res = await fetch(`${API_URL}/api/demo`, { method: 'POST' });
      const data = await res.json();
      setGameState(data);
    } catch (err) {
      console.error('Demo error:', err);
      alert('Error connecting to backend. Is the server running?');
    }
    
    setDemoRunning(false);
  };

  // Start intro: new interactive game
  const startIntro = async () => {
    setMode('intro');
    setGameOver(false);
    
    try {
      const res = await fetch(`${API_URL}/api/new-game`, { method: 'POST' });
      const data = await res.json();
      
      // Fetch initial state
      const stateRes = await fetch(`${API_URL}/api/state`);
      const stateData = await stateRes.json();
      setGameState(stateData);
    } catch (err) {
      console.error('New game error:', err);
      alert('Error connecting to backend. Is the server running?');
    }
  };

  // Player places order
  const placeOrder = async () => {
    try {
      const order = parseInt(retailerOrder);
      const res = await fetch(`${API_URL}/api/place-order?retailer_order=${order}`, {
        method: 'POST',
      });
      const data = await res.json();
      
      if (data.error) {
        setGameOver(true);
      } else {
        setGameState(data);
        // Reset input for next week
        setRetailerOrder('4');
      }
    } catch (err) {
      console.error('Order error:', err);
    }
  };

  // Reset to main menu
  const reset = () => {
    setMode(null);
    setGameState(null);
    setGameOver(false);
    setRetailerOrder('4');
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🍺 Bullwhip Effect Simulator</h1>
        <p>See how small demand changes ripple through a supply chain</p>
      </header>

      {!mode && (
        <div className="menu">
          <h2>Choose a Mode</h2>
          <button className="btn btn-primary" onClick={startDemo}>
            📊 Demo Mode (2-3 min)
          </button>
          <p>Watch the bullwhip effect in action</p>

          <button className="btn btn-primary" onClick={startIntro}>
            🎮 Try It Yourself (15 min)
          </button>
          <p>Control retail orders, see what happens</p>
        </div>
      )}

      {mode && gameState && (
        <div className="game-container">
          <div className="game-header">
            <h2>{mode === 'demo' ? 'Demo Mode' : 'Intro Simulation'}</h2>
            <p>Week {gameState.week} / {gameState.customer_demand.length}</p>
            <button className="btn btn-reset" onClick={reset}>← Back</button>
          </div>

          {/* Supply Chain Display */}
          <div className="supply-chain">
            <div className="tier manufacturer">
              <h3>Manufacturer</h3>
              <p>Inventory: <strong>{gameState.manufacturer.inventory}</strong></p>
              <p>Orders Placed: {gameState.manufacturer.orders_placed.length}</p>
              <p>Cost: ${gameState.manufacturer.costs}</p>
            </div>

            <div className="arrow">→</div>

            <div className="tier distributor">
              <h3>Distributor</h3>
              <p>Inventory: <strong>{gameState.distributor.inventory}</strong></p>
              <p>Orders Placed: {gameState.distributor.orders_placed.length}</p>
              <p>Cost: ${gameState.distributor.costs}</p>
            </div>

            <div className="arrow">→</div>

            <div className="tier wholesaler">
              <h3>Wholesaler</h3>
              <p>Inventory: <strong>{gameState.wholesaler.inventory}</strong></p>
              <p>Orders Placed: {gameState.wholesaler.orders_placed.length}</p>
              <p>Cost: ${gameState.wholesaler.costs}</p>
            </div>

            <div className="arrow">→</div>

            <div className="tier retailer">
              <h3>Retailer</h3>
              <p>Inventory: <strong>{gameState.retailer.inventory}</strong></p>
              <p>Orders Placed: {gameState.retailer.orders_placed.length}</p>
              <p>Cost: ${gameState.retailer.costs}</p>
            </div>
          </div>

          {/* Demand & Orders Chart */}
          <div className="chart-section">
            <h3>Demand vs Orders (The Bullwhip Effect)</h3>
            <div className="chart">
              <table>
                <thead>
                  <tr>
                    <th>Week</th>
                    <th>Customer Demand</th>
                    <th>Retailer Orders</th>
                    <th>Wholesaler Orders</th>
                    <th>Distributor Orders</th>
                    <th>Manufacturer Orders</th>
                  </tr>
                </thead>
                <tbody>
                  {gameState.customer_demand.map((demand, week) => (
                    <tr key={week}>
                      <td>{week + 1}</td>
                      <td>{demand}</td>
                      <td>{gameState.retailer.orders_placed[week] || '-'}</td>
                      <td>{gameState.wholesaler.orders_placed[week] || '-'}</td>
                      <td>{gameState.distributor.orders_placed[week] || '-'}</td>
                      <td>{gameState.manufacturer.orders_placed[week] || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Player Input (Intro Mode) */}
          {mode === 'intro' && !gameOver && (
            <div className="player-input">
              <h3>Your Turn (Week {gameState.week + 1})</h3>
              <p>Customer demand this week: <strong>{gameState.customer_demand[gameState.week]}</strong></p>
              <p>Current retailer inventory: <strong>{gameState.retailer.inventory}</strong></p>
              
              <div className="input-group">
                <label>How many units will you order from the wholesaler?</label>
                <input
                  type="number"
                  value={retailerOrder}
                  onChange={(e) => setRetailerOrder(e.target.value)}
                  min="0"
                  max="20"
                />
                <button className="btn btn-submit" onClick={placeOrder}>
                  Place Order
                </button>
              </div>

              <p className="hint">
                💡 Tip: Think about what the retailer needs. Will you order exactly what customers demand, or more/less?
              </p>
            </div>
          )}

          {/* Game Over (Intro Mode) */}
          {mode === 'intro' && gameOver && (
            <div className="game-over">
              <h2>Simulation Complete!</h2>
              <p>Total Retail Cost: ${gameState.retailer.costs}</p>
              <p>Total Supply Chain Cost: ${(gameState.retailer.costs + gameState.wholesaler.costs + gameState.distributor.costs + gameState.manufacturer.costs).toFixed(2)}</p>
              <p className="reflection">
                <strong>Reflection:</strong> Did your orders match customer demand, or did you order more/less? 
                How did that affect inventory levels upstream? That's the bullwhip effect!
              </p>
              <button className="btn btn-primary" onClick={reset}>Play Again</button>
            </div>
          )}

          {mode === 'demo' && (
            <div className="demo-complete">
              <h2>Demo Complete</h2>
              <p className="insight">
                <strong>The Bullwhip Effect:</strong> Notice how customer demand only went from 4 → 8 → 4.
                But look at the manufacturer's orders—they swung much more dramatically! 
                This is the bullwhip effect: small changes in retail demand cause huge swings upstream.
              </p>
              <button className="btn btn-primary" onClick={reset}>Back to Menu</button>
            </div>
          )}
        </div>
      )}

      <footer className="footer">
        <p>Supply Chain Management - Bullwhip Effect Learning Simulator</p>
      </footer>
    </div>
  );
}

export default App;
