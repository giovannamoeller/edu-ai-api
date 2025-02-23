from models import CompetencyDetails, CompetencyFeedback
from typing import Dict

BASE_SYSTEM_PROMPT = """You are an expert ENEM essay evaluator. Your task is to evaluate essays following the official ENEM scoring criteria.
Key evaluation principles:
1. Focus on helping students improve their writing
2. Provide specific, actionable and very detailed feedback
3. Consider the context and development of ideas
4. Balance critique with constructive suggestions
5. Be thorough but not overly rigid in scoring
"""

PREPROCESSING_PROMPT = """You are an expert at formatting and cleaning ENEM essays. Your task is to process the following raw text from an OCR system and extract only the essay content, properly formatted with paragraphs.

Raw OCR Text:
{text}

Requirements:
1. Remove any personal information (names, CPF numbers, RG numbers, emails, etc.)
2. Remove any header or footer information
3. Remove any registration numbers or candidate IDs
4. Remove any page numbers or markers
5. Remove any teacher notes or grades
6. Fix any obvious OCR errors in Portuguese words
7. Properly separate paragraphs with line breaks
8. Maintain only the actual essay content
9. Ensure proper capitalization and basic punctuation
10. Remove any excessive spaces or line breaks

Return only the cleaned essay text, properly formatted with paragraphs. Do not add any comments, explanations, or additional text. The essay should be ready for evaluation. The essays are in Portuguese, so keep this language. 
"""

COMPETENCY_RULES = {
    "competency1": """
Competency 1 - Command of formal written Portuguese:
- Evaluate proper use of grammar, spelling, and punctuation
- Check agreement, verb tense, and sentence structure
- Consider paragraph organization and text cohesion
- Look for appropriate vocabulary and register

Scoring criteria (0-200):
0: Complete lack of formal writing command
40: Poor command with frequent errors
80: Insufficient command with many errors
120: Average command with some errors
160: Good command with few errors
200: Excellent command with minimal errors
""",
    "competency2": """
Competency 2 - Understanding and development of the topic:
- Evaluate comprehension of the essay prompt
- Check use of interdisciplinary knowledge
- Assess adherence to argumentative essay structure
- Consider depth of topic exploration

Scoring criteria (0-200):
0: Off-topic or wrong text structure
40: Tangential approach to topic
80: Limited development with heavy reliance on prompt materials
120: Average development with predictable arguments
160: Good development with consistent argumentation
200: Excellent development with productive sociocultural repertoire
""",
    "competency3": """
Competency 3 - Organizing and interpreting information:
- Evaluate selection and use of arguments
- Check logical connection between ideas
- Assess coherence of viewpoint defense
- Consider quality of supporting evidence

Scoring criteria (0-200):
0: Unrelated or incoherent information
40: Poorly related information without clear viewpoint
80: Basic information with limited organization
120: Average organization with some limitations
160: Good organization with clear viewpoint
200: Excellent organization with consistent authorial voice
""",
    "competency4": """
Competency 4 - Argumentative construction:
- Evaluate use of cohesive devices
- Check logical progression of ideas
- Assess paragraph transitions
- Consider argument structure and development

Scoring criteria (0-200):
0: No textual articulation
40: Poor articulation of ideas
80: Insufficient articulation with limited resources
120: Average articulation with some inadequacies
160: Good articulation with minor issues
200: Excellent articulation with diverse resources
""",
    "competency5": """
Competency 5 - Solution proposal:
- Evaluate intervention proposal practicality
- Check respect for human rights
- Assess solution relevance to the problem
- Consider proposal detail and articulation

Scoring criteria (0-200):
0: No proposal or unrelated proposal
40: Vague or inadequate proposal
80: Insufficient proposal with limited connection
120: Average proposal with basic articulation
160: Good proposal with clear connection
200: Excellent detailed proposal with strong articulation
"""
}

ANALYSIS_PROMPT = """Analyze the following ENEM essay according to the official evaluation criteria:

Subject: {subject}

Essay Text:
{text}

Evaluate the essay for each competency with:
1. A score (must be exactly 0, 40, 80, 120, 160, or 200)
2. Detailed justification for the score
3. Concrete improvement suggestions

Your output should include:
1. Scores for each competency
2. Very detailed feedback for each competency, explain on which parts the user could improve and how

Remember:
- Focus on content over formatting
- Provide actionable feedback
- Look for strengths while noting areas for improvement
- Be specific in your examples and suggestions

The essay should be zeroed if it:
- Completely deviates from the topic
- Has inappropriate text structure
- Is shorter than 7 lines
- Disrespects human rights
"""
