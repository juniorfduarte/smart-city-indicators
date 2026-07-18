import { useState, useEffect, useCallback, useMemo } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from "recharts";

const API = import.meta.env.VITE_API_URL || "https://smart-city-indicators-api.onrender.com";

const COR = {
  indigo: "#5B52C7",
  verde:  "#1D9E75",
  coral:  "#D85A30",
  amber:  "#BA7517",
  cinza:  "#888780",
};

const fmt = v => (typeof v === "number" ? v.toFixed(3) : "—");

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 8, padding: "8px 12px", fontSize: 12 }}>
      <p style={{ margin: 0, color: "#666" }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ margin: 0, fontWeight: 500, color: p.color || "#1a1a1a" }}>
          {p.name}: {p.value}
        </p>
      ))}
    </div>
  );
};

function construirHistograma(setores) {
  const bins = Array.from({ length: 10 }, (_, i) => ({
    faixa: `${(i / 10).toFixed(1)}–${((i + 1) / 10).toFixed(1)}`,
    setores: 0,
  }));
  setores.forEach(s => {
    if (typeof s.iua !== "number") return;
    const idx = Math.min(9, Math.floor(s.iua * 10));
    bins[idx].setores += 1;
  });
  return bins;
}

export default function IUA() {
  const [setores, setSetores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro]       = useState(null);
  const [pagina, setPagina]   = useState(0);
  const POR_PAG = 10;

  const buscarDados = useCallback(async () => {
    setLoading(true);
    setErro(null);
    try {
      const r = await fetch(`${API}/iua/setores`);
      if (!r.ok) throw new Error("Erro na API");
      setSetores(await r.json());
      setPagina(0);
    } catch (e) {
      setErro(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { buscarDados(); }, [buscarDados]);

  const comDado = useMemo(() => setores.filter(s => !s.sem_dado), [setores]);
  const media = key => comDado.length ? comDado.reduce((s, r) => s + (r[key] || 0), 0) / comDado.length : 0;
  const semDadoCount = setores.length - comDado.length;
  const histograma = useMemo(() => construirHistograma(setores), [setores]);

  const dfSorted = [...setores].sort((a, b) => (b.iua ?? -1) - (a.iua ?? -1));
  const pagTotal = Math.ceil(dfSorted.length / POR_PAG);
  const pagDados = dfSorted.slice(pagina * POR_PAG, (pagina + 1) * POR_PAG);

  return (
    <div style={{ paddingBottom: "2rem" }}>

      {/* Header */}
      <div style={{ background: "#3B2F7A", padding: "1rem 1.5rem", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 8, background: "rgba(255,255,255,0.15)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <i className="ti ti-chart-histogram" style={{ fontSize: 20, color: "#fff" }} aria-hidden="true" />
          </div>
          <div>
            <p style={{ margin: 0, fontSize: 15, fontWeight: 500, color: "#fff" }}>IUA — Índice Urbano Aberto</p>
            <p style={{ margin: 0, fontSize: 11, color: "rgba(255,255,255,0.7)" }}>Dados Abertos · Censo 2022 (IBGE) · Setores censitários de Maringá</p>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: loading ? COR.amber : erro ? COR.coral : COR.verde, display: "inline-block" }} />
          <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)" }}>
            {loading ? "Carregando..." : erro ? "Erro na API" : `${setores.length} setores carregados`}
          </span>
        </div>
      </div>

      <div style={{ padding: "1.25rem" }}>

        {/* Nota metodológica */}
        <div style={{ background: "#f0eefc", border: "0.5px solid #d8d3f5", borderRadius: 10, padding: "0.875rem 1.25rem", marginBottom: "1.25rem", fontSize: 12, color: "#332a66", lineHeight: 1.6 }}>
          <i className="ti ti-info-circle" aria-hidden="true" /> O IUA é um índice experimental inspirado na metodologia do <strong>IBEU</strong> (Observatório das Metrópoles) — <strong>não é uma implementação oficial dela</strong>. Calculado a partir de dados públicos do Censo 2022 (IBGE), em uma linha independente da base da prefeitura. Setores com menos de 5 domicílios ("sem dado") são excluídos do cálculo por sigilo estatístico do IBGE.
        </div>

        {erro && (
          <div style={{ background: "#fdecea", border: "0.5px solid #f3c6c2", borderRadius: 8, padding: "12px 16px", marginBottom: "1rem", fontSize: 13, color: "#a03327" }}>
            <i className="ti ti-alert-circle" aria-hidden="true" /> Não foi possível conectar à API. Verifique se o serviço está ativo.
          </div>
        )}

        {/* KPI cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 10, marginBottom: "1.25rem" }}>
          <div style={{ background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 8, padding: "0.875rem 1rem" }}>
            <p style={{ margin: "0 0 6px", fontSize: 11, color: "#888" }}>IUA médio</p>
            <p style={{ margin: 0, fontSize: 22, fontWeight: 500, color: COR.indigo }}>{fmt(media("iua"))}</p>
            <p style={{ margin: "4px 0 0", fontSize: 10, color: "#888" }}>setores com dado</p>
          </div>
          <div style={{ background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 8, padding: "0.875rem 1rem" }}>
            <p style={{ margin: "0 0 6px", fontSize: 11, color: "#888" }}>D3 — Condições habitacionais</p>
            <p style={{ margin: 0, fontSize: 22, fontWeight: 500, color: COR.verde }}>{fmt(media("d3"))}</p>
            <p style={{ margin: "4px 0 0", fontSize: 10, color: "#888" }}>média dos setores</p>
          </div>
          <div style={{ background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 8, padding: "0.875rem 1rem" }}>
            <p style={{ margin: "0 0 6px", fontSize: 11, color: "#888" }}>D4 — Infraestrutura urbana</p>
            <p style={{ margin: 0, fontSize: 22, fontWeight: 500, color: COR.amber }}>{fmt(media("d4"))}</p>
            <p style={{ margin: "4px 0 0", fontSize: 10, color: "#888" }}>média dos setores</p>
          </div>
          <div style={{ background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 8, padding: "0.875rem 1rem" }}>
            <p style={{ margin: "0 0 6px", fontSize: 11, color: "#888" }}>Setores sem dado</p>
            <p style={{ margin: 0, fontSize: 22, fontWeight: 500, color: COR.cinza }}>{semDadoCount}</p>
            <p style={{ margin: "4px 0 0", fontSize: 10, color: "#888" }}>&lt; 5 domicílios (sigilo IBGE)</p>
          </div>
        </div>

        {/* Histograma */}
        <div style={{ background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 12, padding: "1rem 1.25rem", marginBottom: 12 }}>
          <p style={{ margin: "0 0 4px", fontSize: 13, fontWeight: 500, color: "#1a1a1a" }}>Distribuição do IUA</p>
          <p style={{ margin: "0 0 12px", fontSize: 11, color: "#888" }}>Número de setores por faixa de índice (0 a 1)</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={histograma} margin={{ left: 0, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#eee" vertical={false} />
              <XAxis dataKey="faixa" tick={{ fontSize: 10, fill: "#888" }} />
              <YAxis tick={{ fontSize: 10, fill: "#888" }} allowDecimals={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="setores" name="Setores" fill={COR.indigo} radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Tabela de setores */}
        <div style={{ background: "#fff", border: "0.5px solid #e0e0e0", borderRadius: 12, padding: "1rem 1.25rem", marginBottom: 12 }}>
          <div style={{ marginBottom: "0.75rem" }}>
            <p style={{ margin: 0, fontSize: 13, fontWeight: 500, color: "#1a1a1a" }}>Setores censitários</p>
            <p style={{ margin: 0, fontSize: 11, color: "#888" }}>Ordenado por IUA (maior para menor)</p>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, tableLayout: "fixed" }}>
              <thead>
                <tr style={{ borderBottom: "0.5px solid #e0e0e0" }}>
                  {["#", "Código do setor", "D3", "D4", "IUA", "Status"].map(h => (
                    <th key={h} style={{ padding: "6px 8px", textAlign: "left", fontWeight: 500, fontSize: 11, color: "#888" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pagDados.map((row, i) => (
                  <tr key={row.cd_setor} style={{ borderBottom: "0.5px solid #e0e0e0", background: i % 2 === 0 ? "transparent" : "#f8f8f8" }}>
                    <td style={{ padding: "6px 8px", color: "#888", fontWeight: 500 }}>{i + pagina * POR_PAG + 1}</td>
                    <td style={{ padding: "6px 8px", color: "#333", fontFamily: "monospace", fontSize: 11 }}>{row.cd_setor}</td>
                    <td style={{ padding: "6px 8px", color: COR.verde }}>{fmt(row.d3)}</td>
                    <td style={{ padding: "6px 8px", color: COR.amber }}>{fmt(row.d4)}</td>
                    <td style={{ padding: "6px 8px", fontWeight: 500, color: COR.indigo }}>{fmt(row.iua)}</td>
                    <td style={{ padding: "6px 8px" }}>
                      {row.sem_dado ? (
                        <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 20, background: "#f0f0f0", color: "#888" }}>sem dado</span>
                      ) : (
                        <span style={{ fontSize: 10, padding: "2px 8px", borderRadius: 20, background: "#e6f6ef", color: COR.verde }}>ok</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {pagTotal > 1 && (
            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: 12, marginTop: "0.875rem" }}>
              <button onClick={() => setPagina(p => Math.max(0, p - 1))} disabled={pagina === 0} style={{ padding: "4px 12px", cursor: "pointer" }}>
                <i className="ti ti-chevron-left" aria-hidden="true" />
              </button>
              <span style={{ fontSize: 12, color: "#888" }}>Página {pagina + 1} de {pagTotal}</span>
              <button onClick={() => setPagina(p => Math.min(pagTotal - 1, p + 1))} disabled={pagina === pagTotal - 1} style={{ padding: "4px 12px", cursor: "pointer" }}>
                <i className="ti ti-chevron-right" aria-hidden="true" />
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ borderTop: "0.5px solid #e0e0e0", paddingTop: "0.875rem", display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: 8 }}>
          <span style={{ fontSize: 11, color: "#888" }}>Fonte: Censo 2022 (IBGE) — Agregados por Setores Censitários</span>
          <span style={{ fontSize: 11, color: "#888" }}>API: /iua/setores</span>
        </div>
      </div>
    </div>
  );
}
