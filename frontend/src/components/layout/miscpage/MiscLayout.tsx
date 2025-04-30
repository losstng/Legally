export default function MiscLayout({ children }: { children: React.ReactNode }) {
    return (
      <div className="flex flex-col min-h-screen bg-gray-50">
        <header className="h-16 flex items-center justify-center bg-white shadow">
          <div className="text-xl font-bold">Legally - Settings</div>
        </header>
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    );
  }