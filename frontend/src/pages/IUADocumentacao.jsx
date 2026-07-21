const COR = {
  indigo: "#5B52C7",
  verde:  "#1D9E75",
  amber:  "#BA7517",
};

const DOCS = [
  {
    key: "iua",
    label: "IUA — Índice Urbano Aberto",
    cor: COR.indigo,
    icone: "ti-chart-histogram",
    descricao: "Índice experimental de qualidade urbana intraurbana para Maringá-PR, calculado por setor censitário a partir de dados públicos do Censo 2022 (IBGE). Inspirado na metodologia do IBEU (Índice de Bem-Estar Urbano) do Observatório das Metrópoles — não é uma implementação oficial dela.",
    formula: "IUA(s) = (D3(s) + D4(s)) / 2 — média simples das duas dimensões do IBEU disponíveis no nível de setor censitário para o Censo 2022.",
    escala: "0 a 1 — quanto maior, melhor a condição urbana relativa do setor dentro do universo de comparação (setores de Maringá).",
    fonte: "IBGE — Censo 2022, Agregados por Setores Censitários (Resultados do Universo).",
    notas: "O IBEU original combina 5 dimensões (D1 Mobilidade, D2 Condições Ambientais, D3 Habitacionais, D4 Serviços Coletivos, D5 Infraestrutura). Só D3 e D4 estão disponíveis no nível de setor censitário no Censo 2022 — os microdados da amostra (base de D1) e a pesquisa do entorno (base de D2 e D5) foram adiados pelo IBGE para 2026. A arquitetura está preparada para incorporar as demais dimensões quando forem liberadas.",
  },
  {
    key: "d3",
    label: "D3 — Condições Habitacionais",
    cor: COR.verde,
    icone: "ti-home",
    descricao: "Mede a adequação das condições físicas dos domicílios do setor: tipo de construção (espécie do domicílio), densidade de moradores por banheiro e ausência de aglomerado subnormal (favela) no setor.",
    formula: "D3(s) = (espécie_adequada + densidade_banheiro_aprox + não_aglomerado_subnormal) / 3 — o IBEU original também usa material de parede e densidade morador/dormitório, variáveis inexistentes no Censo 2022; peso redistribuído entre os 3 indicadores disponíveis.",
    escala: "0 a 1, normalizado de forma relacional (min-max) dentro do universo de comparação.",
    fonte: "Variáveis V00047–V00052 (espécie do domicílio), V00232–V00238 + V00552–V00558 (banheiro/moradores) e CD_FCU (aglomerado subnormal) — Censo 2022.",
    notas: "Densidade morador/banheiro é uma aproximação por faixa agregada, já que o Censo não divulga o par moradores/banheiros por domicílio individual. Em Maringá, nenhum setor tem aglomerado subnormal delimitado pelo IBGE em 2022 — esse indicador é constante (100%) na cidade.",
  },
  {
    key: "d4",
    label: "D4 — Serviços Coletivos Urbanos",
    cor: COR.amber,
    icone: "ti-droplet",
    descricao: "Mede o acesso dos domicílios a infraestrutura básica: abastecimento de água por rede geral, esgotamento sanitário adequado e coleta de lixo.",
    formula: "D4(s) = água·1/4 + esgoto·1/2 + lixo·1/4 — o IBEU original também usa energia elétrica adequada, variável inexistente no Censo 2022; peso redistribuído entre os 3 indicadores disponíveis.",
    escala: "0 a 1, normalizado de forma relacional (min-max) dentro do universo de comparação.",
    fonte: "Variáveis V00111–V00118 (água), V00309 (esgoto) e V00397–V00398 (lixo) — Censo 2022.",
    notas: "Energia elétrica adequada não é medida por não existir variável equivalente no Censo 2022.",
  },
];

const LIMITACOES = [
  "Índice experimental — inspirado no IBEU, mas não é a implementação oficial do Observatório das Metrópoles (que usa dados de 2010 nas 5 dimensões completas).",
  "Só 2 das 5 dimensões do IBEU (D3 + D4): D1 (Mobilidade), D2 (Ambientais) e D5 (Infraestrutura) dependem de bases do Censo 2022 ainda não liberadas em nível intraurbano.",
  "Unidade dos indicadores é domicílios, não pessoas.",
  "Sigilo estatístico: células suprimidas pelo IBGE (marcador \"X\", sempre um valor de 1 ou 2 domicílios) são tratadas como 0 — erro máximo de 1 a 2 domicílios por célula.",
  "Setores com menos de 5 domicílios particulares permanentes são marcados como \"sem dado\" e excluídos do cálculo — limiar oficial do IBGE para omissão de variáveis.",
  "Densidade morador/banheiro é uma aproximação por faixa agregada de domicílios, não o cálculo domicílio a domicílio do IBEU original.",
  "Granularidade limitada ao setor censitário — nível mais fino de divulgação pública do Censo. Não é possível descer a quadra ou lote com esta fonte.",
];

const REFERENCIAS = [
  "Ribeiro, L. C. Q.; Ribeiro, M. G. Índice de Bem-Estar Urbano (IBEU) — Procedimentos Metodológicos. Observatório das Metrópoles.",
  "Observatório das Metrópoles — IBEU Local / IBEU Maringá.",
  "IBGE — Censo 2022: Agregados por Setores Censitários (Resultados do Universo).",
  "IBGE — Agregados por Setores Censitários: Resultados do universo (apresentação institucional, tratamento de sigilo estatístico).",
  "IBGE — Malha de setores censitários (Censo 2022).",
];

export default function IUADocumentacao() {
  return (
    <div style={{ padding: "1.5rem", maxWidth: 860 }}>

      <h1 style={{ fontSize: 20, fontWeight: 500, color: "#1a1a1a", marginBottom: 4 }}>
        Documentação do IUA
      </h1>
      <p style={{ fontSize: 13, color: "#666", marginBottom: "2rem", lineHeight: 1.6 }}>
        Metodologia, fontes de dados e limitações do Índice Urbano Aberto (IUA), calculado a partir
        de dados públicos do Censo 2022 (IBGE) para os setores censitários de Maringá-PR — linha
        independente da base da prefeitura (Track B do projeto).
      </p>

      <div style={{ display: "flex", flexDirection: "column", gap: 16, marginBottom: "2rem" }}>
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
              <div style={{ gridColumn: "1 / -1" }}>
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

      {/* Limitações */}
      <div style={{
        background: "#fff",
        border: "0.5px solid #e0e0e0",
        borderLeft: "4px solid #D85A30",
        borderRadius: 10,
        padding: "1.25rem 1.5rem",
        marginBottom: "1.5rem",
      }}>
        <p style={{ margin: "0 0 10px", fontSize: 14, fontWeight: 500, color: "#1a1a1a" }}>
          <i className="ti ti-alert-triangle" style={{ color: "#D85A30", marginRight: 6 }} aria-hidden="true" />
          Limitações e desvios metodológicos
        </p>
        <ul style={{ margin: 0, paddingLeft: 20, color: "#333", fontSize: 13, lineHeight: 1.8 }}>
          {LIMITACOES.map((item, i) => <li key={i}>{item}</li>)}
        </ul>
      </div>

      {/* Referências */}
      <div style={{
        background: "#fff",
        border: "0.5px solid #e0e0e0",
        borderRadius: 10,
        padding: "1.25rem 1.5rem",
      }}>
        <p style={{ margin: "0 0 10px", fontSize: 14, fontWeight: 500, color: "#1a1a1a" }}>
          <i className="ti ti-books" style={{ color: "#888", marginRight: 6 }} aria-hidden="true" />
          Referências
        </p>
        <ul style={{ margin: 0, paddingLeft: 20, color: "#555", fontSize: 12, lineHeight: 1.9 }}>
          {REFERENCIAS.map((item, i) => <li key={i}>{item}</li>)}
        </ul>
      </div>
    </div>
  );
}
