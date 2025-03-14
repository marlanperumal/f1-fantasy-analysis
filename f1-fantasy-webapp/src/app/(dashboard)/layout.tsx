import Link from "next/link";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white p-4">
        <div className="mb-8">
          <h1 className="text-2xl font-bold">F1 Fantasy Analysis</h1>
        </div>
        <nav className="space-y-2">
          <Link 
            href="/" 
            className="block py-2 px-4 rounded hover:bg-gray-800"
          >
            Dashboard
          </Link>
          <Link 
            href="/drivers" 
            className="block py-2 px-4 rounded hover:bg-gray-800"
          >
            Drivers
          </Link>
          <Link 
            href="/teams" 
            className="block py-2 px-4 rounded hover:bg-gray-800"
          >
            Teams
          </Link>
          <Link 
            href="/analysis" 
            className="block py-2 px-4 rounded hover:bg-gray-800"
          >
            Analysis
          </Link>
          <Link 
            href="/simulator" 
            className="block py-2 px-4 rounded hover:bg-gray-800"
          >
            Simulator
          </Link>
        </nav>
      </div>
      
      {/* Main content */}
      <div className="flex-1 p-8">
        {children}
      </div>
    </div>
  );
} 