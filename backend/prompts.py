SYSTEM_PROMPT = (
    "Você é um assistente especializado em psicologia clínica. "
    "Gere documentos clínicos profissionais, objetivos e tecnicamente precisos em português brasileiro. "
    "Use linguagem clínica formal. Baseie-se apenas nas informações da transcrição fornecida. "
    "Para dados não mencionados, indique 'Não referido na sessão'."
)

DOCUMENT_PROMPTS = {
    "anamnese": """Com base na transcrição da sessão abaixo, elabore uma ANAMNESE PSICOLÓGICA completa e estruturada.

**Paciente:** {patient_name}
**Data da sessão:** {session_date}
**Psicólogo(a):** {psychologist_name}

Organize em seções:
1. IDENTIFICAÇÃO
2. QUEIXA PRINCIPAL E DEMANDA
3. HISTÓRIA DO PROBLEMA ATUAL (início, evolução, fatores desencadeantes)
4. HISTÓRICO PESSOAL (infância, desenvolvimento, marcos)
5. HISTÓRICO FAMILIAR (dinâmica, figuras significativas, padrões)
6. SAÚDE FÍSICA E MEDICAMENTOS
7. VIDA SOCIAL, OCUPACIONAL E AFETIVA
8. SONO, APETITE E ROTINA
9. OBSERVAÇÕES CLÍNICAS INICIAIS

{additional_context}

TRANSCRIÇÃO DA SESSÃO:
{transcript}""",

    "evolucao": """Com base na transcrição abaixo, elabore uma EVOLUÇÃO DE SESSÃO (nota de evolução psicológica).

**Paciente:** {patient_name}
**Data:** {session_date}
**Psicólogo(a):** {psychologist_name}

Inclua:
- Estado geral do paciente no início da sessão
- Conteúdos e temas trabalhados
- Intervenções realizadas pelo psicólogo
- Resposta do paciente às intervenções
- Material emergente (defesas, emoções, insights)
- Encerramento da sessão e estado final
- Observações para próxima sessão

{additional_context}

TRANSCRIÇÃO:
{transcript}""",

    "soap": """Com base na transcrição abaixo, elabore uma nota no formato SOAP.

**Paciente:** {patient_name}
**Data:** {session_date}
**Psicólogo(a):** {psychologist_name}

**S – SUBJETIVO**
(Relatos do paciente, queixas verbalizadas, sentimentos expressos, perspectiva do paciente)

**O – OBJETIVO**
(Comportamentos observáveis durante a sessão, apresentação, afeto, estado mental, dados objetivos)

**A – AVALIAÇÃO**
(Impressão clínica, hipóteses diagnósticas, análise da evolução, nível de funcionamento)

**P – PLANO**
(Intervenções realizadas, estratégias terapêuticas, próximos passos, encaminhamentos se houver)

{additional_context}

TRANSCRIÇÃO:
{transcript}""",

    "relatorio": """Com base na transcrição abaixo, elabore um RELATÓRIO PSICOLÓGICO estruturado.

**Paciente:** {patient_name}
**Data da avaliação:** {session_date}
**Psicólogo(a) responsável:** {psychologist_name}

O relatório deve conter:
1. IDENTIFICAÇÃO DO PACIENTE
2. MOTIVO DO ENCAMINHAMENTO / OBJETIVO DA AVALIAÇÃO
3. PROCEDIMENTOS UTILIZADOS
4. DADOS COLETADOS E ANÁLISE CLÍNICA
5. SÍNTESE PSICODIAGNÓSTICA
6. CONCLUSÃO E RECOMENDAÇÕES
7. ASSINATURA E CRP

Use linguagem técnica, objetiva e fundamentada. Evite julgamentos de valor.

{additional_context}

TRANSCRIÇÃO / DADOS DA SESSÃO:
{transcript}""",

    "declaracao": """Elabore uma DECLARAÇÃO DE COMPARECIMENTO formal para:

**Paciente:** {patient_name}
**Data da sessão:** {session_date}
**Psicólogo(a):** {psychologist_name}

A declaração deve:
- Confirmar que o paciente compareceu à consulta psicológica
- Indicar data, horário (se mencionado na transcrição) e duração
- Ser formal e adequada para apresentação profissional ou institucional
- Conter espaço para assinatura e CRP

{additional_context}

INFORMAÇÕES DA SESSÃO:
{transcript}""",

    "resumo": """Com base na transcrição abaixo, elabore um RESUMO DA SESSÃO conciso e claro.

**Paciente:** {patient_name}
**Data:** {session_date}

O resumo deve capturar:
- Principais temas abordados
- Questões centrais trazidas pelo paciente
- Intervenções e técnicas utilizadas
- Insights ou mudanças percebidas
- Pontos de atenção para próxima sessão

Seja direto e claro. Máximo de 400 palavras.

{additional_context}

TRANSCRIÇÃO:
{transcript}""",

    "hipoteses": """Com base na transcrição abaixo, elabore um documento de HIPÓTESES CLÍNICAS E TEMAS CENTRAIS.

**Paciente:** {patient_name}
**Data:** {session_date}
**Psicólogo(a):** {psychologist_name}

Inclua:

**TEMAS CENTRAIS OBSERVADOS**
(Padrões recorrentes, conflitos nucleares, demandas implícitas)

**HIPÓTESES CLÍNICAS**
(Hipóteses diagnósticas possíveis, com base em CID-11 ou DSM-5 se aplicável)

**MECANISMOS DE DEFESA IDENTIFICADOS**
(Se observáveis na transcrição)

**RECURSOS E POTENCIALIDADES DO PACIENTE**
(Fatores protetivos identificados)

**ÁREAS DE INVESTIGAÇÃO FUTURA**
(O que precisa ser aprofundado nas próximas sessões)

Apresente como hipóteses de trabalho, não como diagnóstico definitivo.

{additional_context}

TRANSCRIÇÃO:
{transcript}""",

    "plano_terapeutico": """Com base na transcrição abaixo, elabore um PLANO TERAPÊUTICO INICIAL ou de PRÓXIMOS PASSOS.

**Paciente:** {patient_name}
**Data:** {session_date}
**Psicólogo(a):** {psychologist_name}

Estruture em:

**OBJETIVOS TERAPÊUTICOS**
(Gerais e específicos, a curto e médio prazo)

**ABORDAGEM E ESTRATÉGIAS**
(Linha teórica, técnicas previstas, recursos terapêuticos)

**TEMAS PRIORITÁRIOS PARA TRABALHO**
(Ordenados por urgência/relevância clínica)

**FREQUÊNCIA E MODALIDADE**
(Proposta de atendimento)

**INDICADORES DE PROGRESSO**
(Como avaliar evolução)

**PRÓXIMOS PASSOS IMEDIATOS**
(O que será trabalhado nas próximas sessões)

{additional_context}

TRANSCRIÇÃO:
{transcript}""",
}
