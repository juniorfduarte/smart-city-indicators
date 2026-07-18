const MENU = [
  { id: "dashboard",   label: "Dashboard",    icon: "ti-layout-dashboard" },
  { id: "indicadores", label: "Indicadores",  icon: "ti-file-description" },
  { id: "iua",         label: "IUA",          icon: "ti-chart-histogram" },
];

export default function Sidebar({ paginaAtiva, setPagina, aberta, setAberta }) {
  return (
    <aside style={{
      width: aberta ? 220 : 56,
      minHeight: "100vh",
      background: "#0a5c47",
      transition: "width 0.25s ease",
      display: "flex",
      flexDirection: "column",
      overflow: "hidden",
      flexShrink: 0,
    }}>

      {/* Toggle + logo */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, padding: "1rem 14px", borderBottom: "0.5px solid rgba(255,255,255,0.1)" }}>
        <button
          onClick={() => setAberta(a => !a)}
          aria-label={aberta ? "Recolher menu" : "Expandir menu"}
          style={{ background: "none", border: "none", cursor: "pointer", padding: 0, color: "#fff", fontSize: 20, display: "flex", alignItems: "center" }}
        >
          <i className={`ti ${aberta ? "ti-layout-sidebar-left-collapse" : "ti-layout-sidebar-left-expand"}`} />
        </button>
        {aberta && (
          <span style={{ color: "#fff", fontSize: 13, fontWeight: 500, whiteSpace: "nowrap", overflow: "hidden" }}>
            Smart City
          </span>
        )}
      </div>

      {/* Itens de navegação */}
      <nav style={{ flex: 1, paddingTop: 8 }}>
        {MENU.map(item => {
          const ativo = paginaAtiva === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setPagina(item.id)}
              title={!aberta ? item.label : undefined}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: 12,
                padding: "10px 16px",
                background: ativo ? "rgba(255,255,255,0.15)" : "transparent",
                border: "none",
                borderLeft: ativo ? "3px solid #fff" : "3px solid transparent",
                cursor: "pointer",
                color: ativo ? "#fff" : "rgba(255,255,255,0.65)",
                fontSize: 13,
                textAlign: "left",
                whiteSpace: "nowrap",
                transition: "background 0.15s",
              }}
            >
              <i className={`ti ${item.icon}`} style={{ fontSize: 18, flexShrink: 0 }} aria-hidden="true" />
              {aberta && <span>{item.label}</span>}
            </button>
          );
        })}
      </nav>

      {/* Rodapé da sidebar */}
      {aberta && (
        <div style={{ padding: "12px 16px", borderTop: "0.5px solid rgba(255,255,255,0.1)" }}>
          <p style={{ margin: 0, fontSize: 10, color: "rgba(255,255,255,0.4)", lineHeight: 1.6 }}>
            Desenvolvido por:<br />
            Francisco Junior<br />
            Maringá - PR, 2026.
          </p>
        </div>
      )}
    </aside>
  );
}