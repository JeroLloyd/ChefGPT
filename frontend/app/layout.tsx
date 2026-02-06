import './globals.css'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-950 text-white">
        <main className="h-screen flex flex-col">
          {children}
        </main>
      </body>
    </html>
  )
}