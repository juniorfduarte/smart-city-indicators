import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Indicadores from "./pages/Indicadores";
import IUA from "./pages/IUA";
import IUADocumentacao from "./pages/IUADocumentacao";

export default function App() {
  const [pagina, setPagina]           = useState("dashboard");
  const [aberta, setAberta]           = useState(true);
  const [menuMobileAberto, setMenuMobileAberto] = useState(false);

  const fecharMenuMobile = () => setMenuMobileAberto(false);

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
      {/* Barra superior visível apenas em telas pequenas */}
      <div className="mobile-topbar" style={{ position: "fixed", top: 0, left: 0, right: 0, height: 48, background: "#0a5c47", alignItems: "center", gap: 10, padding: "0 14px", zIndex: 900 }}>
        <button
          onClick={() => setMenuMobileAberto(true)}
          aria-label="Abrir menu"
          style={{ background: "none", border: "none", cursor: "pointer", padding: 0, color: "#fff", fontSize: 22, display: "flex", alignItems: "center" }}
        >
          <i className="ti ti-menu-2" aria-hidden="true" />
        </button>
        <span style={{ color: "#fff", fontSize: 13, fontWeight: 500 }}>Smart City</span>
      </div>

      <div className={`sidebar-backdrop${menuMobileAberto ? " is-open" : ""}`} onClick={fecharMenuMobile} />

      <Sidebar
        paginaAtiva={pagina}
        setPagina={setPagina}
        aberta={aberta}
        setAberta={setAberta}
        menuMobileAberto={menuMobileAberto}
        fecharMenuMobile={fecharMenuMobile}
      />
      <main className="app-main" style={{ flex: 1, overflow: "auto", minWidth: 0 }}>
        {renderPagina()}
      </main>
    </div>
  );
}