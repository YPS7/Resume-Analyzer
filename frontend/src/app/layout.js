import "./globals.css";
import Header from "@/components/Header";

export const metadata = {
  title: "Resume Analyzerr | AI-Powered Resume Scoring",
  description: "Analyze your resume against job descriptions using advanced AI.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main className="main-content">
          {children}
        </main>
      </body>
    </html>
  );
}
