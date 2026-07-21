import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Indicadores from "./pages/Indicadores";
import IUA from "./pages/IUA";
import IUADocumentacao from "./pages/IUADocumentacao";

export default function App() {
  const [pagina, setPagina]   = useState("dashboard");
  const [aberta, setAberta]   = useState(true);

  const renderPagina = () => {
    switch (pagina) {
      case "dashboard":   return <Dashboard />;
      case "indicadores": return <Indicadores />;
      case "iua":          return <IUA />;
      case "iua-doc":      return <IUADocumentacao />;
      default:            return <Dashboard />;
    }
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#f5f5f3" }}>
      <Sidebar
        paginaAtiva={pagina}
        setPagina={setPagina}
        aberta={aberta}
        setAberta={setAberta}
      />
      <main style={{ flex: 1, overflow: "auto" }}>
        {renderPagina()}
      </main>
    </div>
  );
}