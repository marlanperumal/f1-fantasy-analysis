import React from "react";

export default function AnalysisPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">F1 Fantasy Analysis</h1>
        <p className="text-gray-600">
          Advanced analysis tools to optimize your F1 Fantasy team
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Price-Points Correlation</h2>
          <div className="h-64 bg-gray-100 flex items-center justify-center">
            <p className="text-gray-500">Price-Points scatter plot visualization</p>
          </div>
          <p className="mt-4 text-sm text-gray-600">
            This chart shows the correlation between driver/team price and points scored.
            Points above the trend line represent better value.
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Form Trends</h2>
          <div className="h-64 bg-gray-100 flex items-center justify-center">
            <p className="text-gray-500">Form trends line chart visualization</p>
          </div>
          <p className="mt-4 text-sm text-gray-600">
            This chart shows how driver/team performance has changed over recent races.
            Upward trends may indicate good future performance.
          </p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-xl font-bold mb-4">Optimal Team Selection</h2>
        <div className="mb-6">
          <h3 className="font-semibold mb-2">Budget Constraints</h3>
          <div className="flex items-center">
            <input
              type="range"
              min="80"
              max="120"
              defaultValue="100"
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <span className="ml-4 font-medium">$100M</span>
          </div>
        </div>

        <div className="mb-6">
          <h3 className="font-semibold mb-2">Optimization Strategy</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="flex items-center">
              <input
                type="radio"
                id="maxPoints"
                name="strategy"
                defaultChecked
                className="mr-2"
              />
              <label htmlFor="maxPoints">Maximize Points</label>
            </div>
            <div className="flex items-center">
              <input
                type="radio"
                id="valueRatio"
                name="strategy"
                className="mr-2"
              />
              <label htmlFor="valueRatio">Best Value</label>
            </div>
            <div className="flex items-center">
              <input
                type="radio"
                id="balanced"
                name="strategy"
                className="mr-2"
              />
              <label htmlFor="balanced">Balanced Approach</label>
            </div>
          </div>
        </div>

        <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Generate Optimal Team
        </button>

        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold mb-4">Recommended Team</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-2">Drivers</h4>
              <ul className="space-y-2">
                <li className="flex justify-between">
                  <span>Max Verstappen (RBR)</span>
                  <span className="font-medium">$30.5M</span>
                </li>
                <li className="flex justify-between">
                  <span>Charles Leclerc (FER)</span>
                  <span className="font-medium">$25.8M</span>
                </li>
                <li className="flex justify-between">
                  <span>Sergio Perez (RBR)</span>
                  <span className="font-medium">$20.2M</span>
                </li>
                <li className="flex justify-between">
                  <span>Lando Norris (MCL)</span>
                  <span className="font-medium">$18.5M</span>
                </li>
                <li className="flex justify-between">
                  <span>Oscar Piastri (MCL)</span>
                  <span className="font-medium">$15.0M</span>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-2">Teams</h4>
              <ul className="space-y-2">
                <li className="flex justify-between">
                  <span>Red Bull Racing</span>
                  <span className="font-medium">$32.5M</span>
                </li>
                <li className="flex justify-between">
                  <span>Ferrari</span>
                  <span className="font-medium">$30.0M</span>
                </li>
              </ul>
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-gray-200 flex justify-between">
            <span>Total Budget:</span>
            <span className="font-bold">$172.5M / $100.0M</span>
          </div>
          <div className="mt-2 flex justify-between text-green-600">
            <span>Projected Points:</span>
            <span className="font-bold">325 pts</span>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-4">Advanced Analysis Tools</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer">
            <h3 className="font-semibold mb-2">Undervalued Drivers</h3>
            <p className="text-sm text-gray-600">
              Find drivers who are performing better than their price suggests.
            </p>
          </div>
          <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer">
            <h3 className="font-semibold mb-2">Team Performance</h3>
            <p className="text-sm text-gray-600">
              Analyze team performance metrics across different track types.
            </p>
          </div>
          <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer">
            <h3 className="font-semibold mb-2">Points Prediction</h3>
            <p className="text-sm text-gray-600">
              Predict future points based on historical performance and upcoming tracks.
            </p>
          </div>
          <div className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer">
            <h3 className="font-semibold mb-2">Price Trend Analysis</h3>
            <p className="text-sm text-gray-600">
              Track price changes and predict future price movements.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
} 