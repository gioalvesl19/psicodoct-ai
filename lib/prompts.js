const SYSTEM_PROMPT =
  'Você é um assistente especializado em psicologia clínica. ' +
  'Gere documentos clínicos profissionais, objetivos e tecnicamente precisos em português brasileiro. ' +
  'Use linguagem clínica formal. Baseie-se apenas nas informações da transcrição fornecida. ' +
  "Para dados não mencionados, indique 'Não referido na sessão'.";

const TEMPLATES = {
  anamnese: `Com base na transcrição, elabore uma ANAMNESE PSICOLÓGICA completa.

Paciente: {patient_name} | Data: {session_date} | Psicólogo(a): {psychologist_name}
{extra}

Seções obrigatórias:
1. IDENTIFICAÇÃO
2. QUEIXA PRINCIPAL E DEMANDA
3. HISTÓRIA DO PROBLEMA ATUAL (início, evolução, fatores)
4. HISTÓRICO PESSOAL (infância, desenvolvimento, marcos)
5. HISTÓRICO FAMILIAR (dinâmica, figuras significativas)
6. SAÚDE FÍSICA E MEDICAMENTOS
7. VIDA SOCIAL, OCUPACIONAL E AFETIVA
8. SONO, APETITE E ROTINA
9. OBSERVAÇÕES CLÍNICAS INICIAIS

TRANSCRIÇÃO:
{transcript}`,

  evolucao: `Com base na transcrição, elabore uma EVOLUÇÃO DE SESSÃO.

Paciente: {patient_name} | Data: {session_date} | Psicólogo(a): {psychologist_name}
{extra}

Inclua: estado inicial do paciente, conteúdos trabalhados, intervenções realizadas,
resposta às intervenções, material emergente (defesas, emoções, insights),
encerramento e estado final, observações para próxima sessão.

TRANSCRIÇÃO:
{transcript}`,

  soap: `Com base na transcrição, elabore nota no formato SOAP.

Paciente: {patient_name} | Data: {session_date} | Psicólogo(a): {psychologist_name}
{extra}

S – SUBJETIVO (relatos, queixas, sentimentos verbalizados)
O – OBJETIVO (comportamentos observáveis, apresentação, afeto, estado mental)
A – AVALIAÇÃO (impressão clínica, hipóteses, análise da evolução)
P – PLANO (intervenções, estratégias, próximos passos, encaminhamentos)

TRANSCRIÇÃO:
{transcript}`,

  relatorio: `Com base na transcrição, elabore um RELATÓRIO PSICOLÓGICO.

Paciente: {patient_name} | Data: {session_date} | Psicólogo(a): {psychologist_name}
{extra}

1. IDENTIFICAÇÃO DO PACIENTE
2. MOTIVO DO ENCAMINHAMENTO / OBJETIVO
3. PROCEDIMENTOS UTILIZADOS
4. DADOS COLETADOS E ANÁLISE CLÍNICA
5. SÍNTESE PSICODIAGNÓSTICA
6. CONCLUSÃO E RECOMENDAÇÕES
7. (Espaço para assinatura e CRP)

TRANSCRIÇÃO / DADOS:
{transcript}`,

  declaracao: `Elabore uma DECLARAÇÃO DE COMPARECIMENTO formal.

Paciente: {patient_name} | Data: {session_date} | Psicólogo(a): {psychologist_name}
{extra}

A declaração deve confirmar comparecimento à consulta psicológica, indicar data e horário se mencionados,
ser formal e adequada para apresentação institucional, e ter espaço para assinatura e CRP.

INFORMAÇÕES DA SESSÃO:
{transcript}`,

  resumo: `Com base na transcrição, elabore um RESUMO DA SESSÃO conciso (máx. 400 palavras).

Paciente: {patient_name} | Data: {session_date}
{extra}

Capture: principais temas, questões centrais, intervenções e técnicas usadas,
insights ou mudanças percebidas, pontos de atenção para próxima sessão.

TRANSCRIÇÃO:
{transcript}`,

  hipoteses: `Com base na transcrição, elabore HIPÓTESES CLÍNICAS E TEMAS CENTRAIS.

Paciente: {patient_name} | Data: {session_date} | Psicólogo(a): {psychologist_name}
{extra}

TEMAS CENTRAIS OBSERVADOS
HIPÓTESES CLÍNICAS (CID-11 ou DSM-5 se aplicável — apresentar como hipóteses de trabalho)
MECANISMOS DE DEFESA IDENTIFICADOS
RECURSOS E POTENCIALIDADES DO PACIENTE
ÁREAS DE INVESTIGAÇÃO FUTURA

TRANSCRIÇÃO:
{transcript}`,

  plano_terapeutico: `Com base na transcrição, elabore um PLANO TERAPÊUTICO.

Paciente: {patient_name} | Data: {session_date} | Psicólogo(a): {psychologist_name}
{extra}

OBJETIVOS TERAPÊUTICOS (gerais e específicos, curto e médio prazo)
ABORDAGEM E ESTRATÉGIAS (linha teórica, técnicas previstas)
TEMAS PRIORITÁRIOS PARA TRABALHO
FREQUÊNCIA E MODALIDADE PROPOSTAS
INDICADORES DE PROGRESSO
PRÓXIMOS PASSOS IMEDIATOS

TRANSCRIÇÃO:
{transcript}`,
};

function buildPrompt(type, { transcript, patient_name, session_date, psychologist_name, additional_context }) {
  const tmpl = TEMPLATES[type];
  if (!tmpl) throw new Error(`Tipo inválido: ${type}`);
  return tmpl
    .replace('{transcript}', transcript)
    .replace('{patient_name}', patient_name || 'Não informado')
    .replace('{session_date}', session_date || 'Não informado')
    .replace('{psychologist_name}', psychologist_name || 'Não informado')
    .replace('{extra}', additional_context ? `Contexto adicional: ${additional_context}` : '');
}

module.exports = { SYSTEM_PROMPT, TEMPLATES, buildPrompt };
