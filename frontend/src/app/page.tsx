import Chat from "@/app/components/Chat";
import EmergencyBanner from "@/app/components/EmergencyBanner";

export default function Home() {
  return (
    <div className="flex flex-col h-screen bg-white dark:bg-black text-black dark:text-white font-sans">
      <EmergencyBanner />
      <main className="flex-grow flex flex-col items-center justify-center">
        <Chat />
      </main>
    </div>
  );
}
