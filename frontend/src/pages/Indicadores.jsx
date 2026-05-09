const DOCS = [
  {
    key: "smart_city_score",
    label: "Smart City Score",
    cor: "#1D9E75",
    icone: "ti-award",
    descricao: "Índice composto que representa o nível geral de inteligência urbana do lote, combinando infraestrutura, qualidade e adensamento.",
    formula: "Média ponderada dos demais índices urbanos do lote.",
    fonte: "Prefeitura de Maringá — dados mockados (MVP)",
    escala: "0 a 1 — quanto maior, melhor o desempenho urbano geral.",
    notas: "Este indicador será recalculado com dados reais assim que a API da prefeitura estiver disponível.",
  },
  {
    key: "indice_qualidade_urbana",
    label: "Índice de Qualidade Urbana (IQU)",
    cor: "#378ADD",
    icone: "ti-building",
    descricao: "Mede a qualidade do ambiente urbano do lote considerando aspectos como acesso a serviços, mobilidade, saneamento e áreas verdes.",
    formula: "Composição de sub-indicadores de serviços urbanos disponíveis na região do lote.",
    fonte: "Prefeitura de Maringá — dados mockados (MVP)",
    escala: "0 a 1 — quanto maior, melhor a qualidade urbana percebida.",
    notas: "Futuramente integrará dados do IBGE e da prefeitura para cálculo real.",
  },
  {
    key: "indice_infraestrutura_urbana",
    label: "Índice de Infraestrutura Urbana (IIU)",
    cor: "#7F77DD",
    icone: "ti-road",
    descricao: "Avalia a disponibilidade e qualidade de infraestrutura física no entorno do lote: vias, calçadas, iluminação, redes de água e esgoto.",
    formula: "Pontuação baseada na presença e estado de conservação dos elementos de infraestrutura.",
    fonte: "Prefeitura de Maringá — dados mockados (MVP)",
    escala: "0 a 1 — quanto maior, melhor a infraestrutura disponível.",
    notas: "Indicador prioritário para decisões de investimento público.",
  },
  {
    key: "indice_adensamento_inteligente",
    label: "Índice de Adensamento Inteligente (IAI)",
    cor: "#BA7517",
    icone: "ti-building-skyscraper",
    descricao: "Representa o grau de verticalização e uso eficiente do solo urbano, considerando o potencial construtivo do lote em relação ao seu uso atual.",
    formula: "Relação entre a área construída, gabarito e o potencial máximo permitido pela legislação urbanística.",
    fonte: "Prefeitura de Maringá — dados mockados (MVP)",
    escala: "0 a 1 — valores próximos a 1 indicam uso intensivo e eficiente do solo.",
    notas: "Essencial para análise de verticalização e planejamento de zoneamento.",
  },
];

export default function Indicadores() {
  return (
    <div style={{ padding: "1.5rem", maxWidth: 860 }}>

      <h1 style={{ fontSize: 20, fontWeight: 500, color: "#1a1a1a", marginBottom: 4 }}>
        Documentação dos Indicadores
      </h1>
      <p style={{ fontSize: 13, color: "#666", marginBottom: "2rem", lineHeight: 1.6 }}>
        Descrição metodológica dos índices utilizados na plataforma Smart City Maringá.
        Os dados são atualmente mockados para fins de desenvolvimento do MVP.
      </p>

      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {DOCS.map(ind => (
          <div key={ind.key} style={{
            background: "#fff",
            border: "0.5px solid #e0e0e0",
            borderLeft: `4px solid ${ind.cor}`,
            borderRadius: 10,
            padding: "1.25rem 1.5rem",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
              <div style={{ width: 36, height: 36, borderRadius: 8, background: `${ind.cor}18`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <i className={`ti ${ind.icone}`} style={{ fontSize: 18, color: ind.cor }} aria-hidden="true" />
              </div>
              <div>
                <p style={{ margin: 0, fontSize: 14, fontWeight: 500, color: "#1a1a1a" }}>{ind.label}</p>
                <code style={{ fontSize: 10, color: "#888", background: "#f5f5f5", padding: "1px 6px", borderRadius: 4 }}>{ind.key}</code>
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px 24px", fontSize: 13 }}>
              <div style={{ gridColumn: "1 / -1" }}>
                <span style={{ fontSize: 11, fontWeight: 500, color: "#888", textTransform: "uppercase", letterSpacing: "0.05em" }}>Descrição</span>
                <p style={{ margin: "4px 0 0", color: "#333", lineHeight: 1.6 }}>{ind.descricao}</p>
              </div>
              <div>
                <span style={{ fontSize: 11, fontWeight: 500, color: "#888", textTransform: "uppercase", letterSpacing: "0.05em" }}>Fórmula / Metodologia</span>
                <p style={{ margin: "4px 0 0", color: "#333", lineHeight: 1.6 }}>{ind.formula}</p>
              </div>
              <div>
                <span style={{ fontSize: 11, fontWeight: 500, color: "#888", textTransform: "uppercase", letterSpacing: "0.05em" }}>Escala</span>
                <p style={{ margin: "4px 0 0", color: "#333", lineHeight: 1.6 }}>{ind.escala}</p>
              </div>
              <div>
                <span style={{ fontSize: 11, fontWeight: 500, color: "#888", textTransform: "uppercase", letterSpacing: "0.05em" }}>Fonte</span>
                <p style={{ margin: "4px 0 0", color: "#333", lineHeight: 1.6 }}>{ind.fonte}</p>
              </div>
              <div style={{ gridColumn: "1 / -1", background: "#fffbf0", border: "0.5px solid #f0e0b0", borderRadius: 6, padding: "8px 12px" }}>
                <span style={{ fontSize: 11, fontWeight: 500, color: "#a06000" }}>Observação</span>
                <p style={{ margin: "2px 0 0", color: "#7a4f00", fontSize: 12, lineHeight: 1.5 }}>{ind.notas}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}