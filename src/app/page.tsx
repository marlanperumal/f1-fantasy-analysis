import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-4">F1 Fantasy Dashboard</h1>
        <p className="text-gray-600 mb-8">
          Analyze Formula 1 fantasy data and optimize your team selection
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Quick stats cards */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-2">Current Season</h3>
          <p className="text-3xl font-bold">2024</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-2">Next Race</h3>
          <p className="text-3xl font-bold">Australian GP</p>
          <p className="text-gray-500">March 24, 2024</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-2">Budget</h3>
          <p className="text-3xl font-bold">$100M</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-2">Optimal Team Score</h3>
          <p className="text-3xl font-bold">325 pts</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Recent performance */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Top Performing Drivers</h2>
          <div className="space-y-4">
            {[
              { name: "Max Verstappen", team: "Red Bull Racing", points: 51 },
              { name: "Charles Leclerc", team: "Ferrari", points: 47 },
              { name: "Sergio Perez", team: "Red Bull Racing", points: 36 },
              { name: "Carlos Sainz", team: "Ferrari", points: 33 },
              { name: "Lewis Hamilton", team: "Mercedes", points: 19 },
            ].map((driver, index) => (
              <div key={index} className="flex justify-between items-center border-b pb-2">
                <div>
                  <p className="font-medium">{driver.name}</p>
                  <p className="text-sm text-gray-500">{driver.team}</p>
                </div>
                <p className="font-bold">{driver.points} pts</p>
              </div>
            ))}
          </div>
          <div className="mt-4">
            <Link href="/drivers" className="text-blue-600 hover:underline">
              View all drivers →
            </Link>
          </div>
        </div>

        {/* Team performance */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Top Performing Teams</h2>
          <div className="space-y-4">
            {[
              { name: "Red Bull Racing", points: 87 },
              { name: "Ferrari", points: 80 },
              { name: "Mercedes", points: 38 },
              { name: "McLaren", points: 28 },
              { name: "Aston Martin", points: 20 },
            ].map((team, index) => (
              <div key={index} className="flex justify-between items-center border-b pb-2">
                <p className="font-medium">{team.name}</p>
                <p className="font-bold">{team.points} pts</p>
              </div>
            ))}
          </div>
          <div className="mt-4">
            <Link href="/teams" className="text-blue-600 hover:underline">
              View all teams →
            </Link>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Analysis tools */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Analysis Tools</h2>
          <p className="mb-4">
            Use our advanced analysis tools to optimize your F1 Fantasy team selection.
          </p>
          <Link 
            href="/analysis" 
            className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Go to Analysis
          </Link>
        </div>

        {/* Simulator */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Race Simulator</h2>
          <p className="mb-4">
            Simulate race outcomes and predict fantasy points for different scenarios.
          </p>
          <Link 
            href="/simulator" 
            className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Go to Simulator
          </Link>
        </div>
      </div>
    </div>
  );
}
