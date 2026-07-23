import { useState, useEffect, useCallback } from "react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  ScatterChart, Scatter, CartesianGrid
} from "recharts";

const API = import.meta.env.VITE_API_URL || "https://smart-city-indicators-api.onrender.com";

const COR = {
  verde:  "#1D9E75",
  azul:   "#378ADD",
  coral:  "#D85A30",
  amber:  "#BA7517",
  roxo:   "#7F77DD",
  cinza:  "#888780",
};

const INDICADORES = [
  { key: "smart_city_score",              label: "Smart City Score",      cor: COR.verde },
  { key: "indice_qualidade_urbana",       label: "Qualidade Urbana",      cor: COR.azul  },
  { key: "indice_infraestrutura_urbana",  label: "Infraestrutura Urbana", cor: COR.roxo  },
  { key: "indice_adensamento_inteligente",label: "Adensamento Inteligente",cor: COR.amber },
];

const fmt = v => (typeof v === "number" ? v.toFixed(3) : "—");

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: 8, padding: "8px 12px", fontSize: 12 }}>
      <p style={{ margin: 0, color: "var(--color-text-secondary)" }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ margin: 0, fontWeight: 500, color: p.color || "var(--color-text-primary)" }}>
          {p.name}: {typeof p.value === "number" ? p.value.toFixed(3) : p.value}
        </p>
      ))}
    </div>
  );
};

export default function Dashboard() {
  const [dados, setDados]         = useState([]);
  const [porBairro, setPorBairro] = useState([]);
  const [loading, setLoading]     = useState(true);
  const [erro, setErro]           = useState(null);
  const [filtroBairro, setFiltroBairro] = useState("");
  const [filtroZona, setFiltroZona]     = useState("");
  const [inputBairro, setInputBairro]   = useState("");
  const [inputZona, setInputZona]       = useState("");
  const [indicadorAtivo, setIndicadorAtivo] = useState("smart_city_score");
  const [pagina, setPagina]       = useState(0);
  const POR_PAG = 10;

  const buscarDados = useCallback(async () => {
    setLoading(true);
    setErro(null);
    try {
      const params = new URLSearchParams();
      if (filtroBairro) params.append("bairro", filtroBairro);
      if (filtroZona)   params.append("zona",   filtroZona);

      const [r1, r2] = await Promise.all([
        fetch(`${API}/maringa/indicadores?${params}`),
        fetch(`${API}/maringa/indicadores/bairro`)
      ]);
      if (!r1.ok || !r2.ok) throw new Error("Erro na API");
      const [d1, d2] = await Promise.all([r1.json(), r2.json()]);
      setDados(d1);
      setPorBairro(d2);
      setPagina(0);
    } catch (e) {
      setErro(e.message);
    } finally {
      setLoading(false);
    }
  }, [filtroBairro, filtroZona]);

  useEffect(() => { buscarDados(); }, [buscarDados]);

  const media = key => dados.length ? dados.reduce((s, r) => s + (r[key] || 0), 0) / dados.length : 0;

  const dfSorted = [...dados].sort((a, b) => b[indicadorAtivo] - a[indicadorAtivo]);
  const pagTotal = Math.ceil(dfSorted.length / POR_PAG);
  const pagDados = dfSorted.slice(pagina * POR_PAG, (pagina + 1) * POR_PAG);

  const radarData = INDICADORES.map(ind => ({
    indicador: ind.label.split(" ")[0],
    valor: parseFloat((media(ind.key) * 100).toFixed(1))
  }));

  const bairrosUnicos = [...new Set(dados.map(d => d.bairro).filter(Boolean))].sort();
  const zonasUnicas   = [...new Set(dados.map(d => d.zona).filter(Boolean))].sort();

  return (
    <div style={{ fontFamily: "var(--font-sans)", paddingBottom: "2rem" }}>

      {/* Header */}
      <div style={{ background: "#0F6E56", padding: "1rem 1.5rem", display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 8, background: "rgba(255,255,255,0.15)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <i className="ti ti-building-community" style={{ fontSize: 20, color: "#fff" }} aria-hidden="true" />
          </div>
          <div>
            <p style={{ margin: 0, fontSize: 15, fontWeight: 500, color: "#fff" }}>Smart City Dashboard — Maringá</p>
            <p style={{ margin: 0, fontSize: 11, color: "rgba(255,255,255,0.7)" }}>UEM · Prefeitura de Maringá · Indicadores Urbanos</p>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ width: 8, height: 8, borderRadius: "50%", background: loading ? COR.amber : erro ? COR.coral : COR.verde, display: "inline-block" }} />
          <span style={{ fontSize: 11, color: "rgba(255,255,255,0.8)" }}>
            {loading ? "Carregando..." : erro ? "Erro na API" : `${dados.length} lotes carregados`}
          </span>
        </div>
      </div>

      <div style={{ padding: "1.25rem" }}>

        {/* Filtros */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10, marginBottom: "1.25rem", alignItems: "end" }}>
          <div style={{ flex: "1 1 160px" }}>
            <label style={{ fontSize: 11, color: "var(--color-text-secondary)", display: "block", marginBottom: 4 }}>Bairro</label>
            <input
              list="bairros-list"
              value={inputBairro}
              onChange={e => setInputBairro(e.target.value)}
              placeholder="ex: Centro"
              style={{ width: "100%", boxSizing: "border-box" }}
            />
            <datalist id="bairros-list">
              {bairrosUnicos.map(b => <option key={b} value={b} />)}
            </datalist>
          </div>
          <div style={{ flex: "1 1 160px" }}>
            <label style={{ fontSize: 11, color: "var(--color-text-secondary)", display: "block", marginBottom: 4 }}>Zona</label>
            <input
              list="zonas-list"
              value={inputZona}
              onChange={e => setInputZona(e.target.value)}
              placeholder="ex: Zona 01"
              style={{ width: "100%", boxSizing: "border-box" }}
            />
            <datalist id="zonas-list">
              {zonasUnicas.map(z => <option key={z} value={z} />)}
            </datalist>
          </div>
          <button onClick={() => { setFiltroBairro(inputBairro); setFiltroZona(inputZona); }}
            style={{ flex: "0 0 auto", padding: "0 20px", height: 36, cursor: "pointer" }}>
            <i className="ti ti-search" aria-hidden="true" /> Filtrar
          </button>
          <button onClick={() => { setInputBairro(""); setInputZona(""); setFiltroBairro(""); setFiltroZona(""); }}
            style={{ flex: "0 0 auto", padding: "0 16px", height: 36, cursor: "pointer" }}>
            <i className="ti ti-x" aria-hidden="true" /> Limpar
          </button>
        </div>

        {erro && (
          <div style={{ background: "var(--color-background-danger)", border: "0.5px solid var(--color-border-danger)", borderRadius: 8, padding: "12px 16px", marginBottom: "1rem", fontSize: 13, color: "var(--color-text-danger)" }}>
            <i className="ti ti-alert-circle" aria-hidden="true" /> Não foi possível conectar à API. Verifique se o serviço está ativo.
          </div>
        )}

        {/* KPI cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))", gap: 10, marginBottom: "1.25rem" }}>
          {INDICADORES.map(ind => (
            <div key={ind.key} style={{ background: "var(--color-background-secondary)", borderRadius: 8, padding: "0.875rem 1rem" }}>
              <p style={{ margin: "0 0 6px", fontSize: 11, color: "var(--color-text-secondary)" }}>{ind.label}</p>
              <p style={{ margin: 0, fontSize: 22, fontWeight: 500, color: ind.cor }}>{fmt(media(ind.key))}</p>
              <p style={{ margin: "4px 0 0", fontSize: 10, color: "var(--color-text-secondary)" }}>média dos lotes</p>
            </div>
          ))}
        </div>

        {/* Gráficos row 1 */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: 12, marginBottom: 12 }}>

          {/* Score por bairro */}
          <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: 12, padding: "1rem 1.25rem" }}>
            <p style={{ margin: "0 0 4px", fontSize: 13, fontWeight: 500, color: "var(--color-text-primary)" }}>Score médio por bairro</p>
            <p style={{ margin: "0 0 12px", fontSize: 11, color: "var(--color-text-secondary)" }}>Smart City Score — fonte: API /maringa/indicadores/bairro</p>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={porBairro.slice(0, 8)} layout="vertical" margin={{ left: 8, right: 16 }}>
                <XAxis type="number" domain={[0, 1]} tick={{ fontSize: 10, fill: "#888" }} tickFormatter={v => v.toFixed(1)} />
                <YAxis type="category" dataKey="bairro" tick={{ fontSize: 10, fill: "var(--color-text-secondary)" }} width={80} />
                <Tooltip content={<CustomTooltip />} />
                <Bar dataKey="smart_city_score" name="Score" fill={COR.verde} radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Radar perfil */}
          <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: 12, padding: "1rem 1.25rem" }}>
            <p style={{ margin: "0 0 4px", fontSize: 13, fontWeight: 500, color: "var(--color-text-primary)" }}>Perfil de indicadores</p>
            <p style={{ margin: "0 0 12px", fontSize: 11, color: "var(--color-text-secondary)" }}>Média geral dos lotes filtrados (escala 0–100)</p>
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="var(--color-border-tertiary)" />
                <PolarAngleAxis dataKey="indicador" tick={{ fontSize: 11, fill: "var(--color-text-secondary)" }} />
                <Radar dataKey="valor" name="Média" stroke={COR.azul} fill={COR.azul} fillOpacity={0.2} />
                <Tooltip content={<CustomTooltip />} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Comparativo por bairro */}
        <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: 12, padding: "1rem 1.25rem", marginBottom: 12 }}>
          <p style={{ margin: "0 0 4px", fontSize: 13, fontWeight: 500, color: "var(--color-text-primary)" }}>Comparativo de indicadores por bairro</p>
          <p style={{ margin: "0 0 12px", fontSize: 11, color: "var(--color-text-secondary)" }}>Todos os índices lado a lado</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={porBairro.slice(0, 8)} margin={{ left: 0, right: 16 }}>
              <XAxis dataKey="bairro" tick={{ fontSize: 10, fill: "var(--color-text-secondary)" }} />
              <YAxis domain={[0, 1]} tick={{ fontSize: 10, fill: "#888" }} tickFormatter={v => v.toFixed(1)} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="smart_city_score"              name="Smart City"      fill={COR.verde} />
              <Bar dataKey="indice_qualidade_urbana"       name="Qualidade"       fill={COR.azul}  />
              <Bar dataKey="indice_infraestrutura_urbana"  name="Infraestrutura"  fill={COR.roxo}  />
              <Bar dataKey="indice_adensamento_inteligente"name="Adensamento"     fill={COR.amber} />
            </BarChart>
          </ResponsiveContainer>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "6px 16px", marginTop: 8 }}>
            {[["Smart City", COR.verde], ["Qualidade", COR.azul], ["Infraestrutura", COR.roxo], ["Adensamento", COR.amber]].map(([l, c]) => (
              <span key={l} style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 11, color: "var(--color-text-secondary)" }}>
                <span style={{ width: 10, height: 10, borderRadius: 2, background: c }} />{l}
              </span>
            ))}
          </div>
        </div>

        {/* Ranking de lotes */}
        <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: 12, padding: "1rem 1.25rem", marginBottom: 12 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem", flexWrap: "wrap", gap: 8 }}>
            <div>
              <p style={{ margin: 0, fontSize: 13, fontWeight: 500, color: "var(--color-text-primary)" }}>Ranking de lotes</p>
              <p style={{ margin: 0, fontSize: 11, color: "var(--color-text-secondary)" }}>Ordenado por indicador selecionado</p>
            </div>
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
              {INDICADORES.map(ind => (
                <button key={ind.key} onClick={() => { setIndicadorAtivo(ind.key); setPagina(0); }}
                  style={{ fontSize: 11, padding: "4px 10px", borderRadius: 20, cursor: "pointer",
                    background: indicadorAtivo === ind.key ? ind.cor : "transparent",
                    color: indicadorAtivo === ind.key ? "#fff" : "var(--color-text-secondary)",
                    border: `0.5px solid ${indicadorAtivo === ind.key ? ind.cor : "var(--color-border-tertiary)"}` }}>
                  {ind.label.split(" ")[0]}
                </button>
              ))}
            </div>
          </div>

          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12, tableLayout: "fixed" }}>
              <thead>
                <tr style={{ borderBottom: "0.5px solid var(--color-border-tertiary)" }}>
                  {["#", "ID Lote", "Bairro", "Zona", "Smart City Score", "Qualidade Urbana"].map(h => (
                    <th key={h} style={{ padding: "6px 8px", textAlign: "left", fontWeight: 500, fontSize: 11, color: "var(--color-text-secondary)" }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {pagDados.map((row, i) => (
                  <tr key={row.id_lote} style={{ borderBottom: "0.5px solid var(--color-border-tertiary)", background: i % 2 === 0 ? "transparent" : "var(--color-background-secondary)" }}>
                    <td style={{ padding: "6px 8px", color: i + pagina * POR_PAG < 3 ? COR.verde : "var(--color-text-secondary)", fontWeight: 500 }}>{i + pagina * POR_PAG + 1}</td>
                    <td style={{ padding: "6px 8px", color: "var(--color-text-secondary)", fontFamily: "var(--font-mono)", fontSize: 11 }}>{row.id_lote}</td>
                    <td style={{ padding: "6px 8px", color: "var(--color-text-primary)" }}>{row.bairro || "—"}</td>
                    <td style={{ padding: "6px 8px", color: "var(--color-text-secondary)" }}>{row.zona || "—"}</td>
                    <td style={{ padding: "6px 8px", fontWeight: 500, color: COR.verde }}>{fmt(row.smart_city_score)}</td>
                    <td style={{ padding: "6px 8px", color: COR.azul }}>{fmt(row.indice_qualidade_urbana)}</td>
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
              <span style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>Página {pagina + 1} de {pagTotal}</span>
              <button onClick={() => setPagina(p => Math.min(pagTotal - 1, p + 1))} disabled={pagina === pagTotal - 1} style={{ padding: "4px 12px", cursor: "pointer" }}>
                <i className="ti ti-chevron-right" aria-hidden="true" />
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ borderTop: "0.5px solid var(--color-border-tertiary)", paddingTop: "0.875rem", display: "flex", justifyContent: "space-between", flexWrap: "wrap", gap: 8 }}>
          <span style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>
            Dados mockados
          </span>
          <span style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>
            API: smart-city-indicators.onrender.com
          </span>
        </div>
      </div>
    </div>
  );
}