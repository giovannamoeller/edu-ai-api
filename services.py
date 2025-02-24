from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from models import CompetencyDetails, CompetencyFeedback, EssayResponse, EssayScores
from prompts import PREPROCESSING_PROMPT
from datetime import datetime

class EssayAnalysisService:
    def __init__(self, openai_api_key: str, model_name: str = "gpt-4"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            openai_api_key=openai_api_key
        )
        
        # Initialize output parsers
        self.feedback_parser = PydanticOutputParser(pydantic_object=CompetencyFeedback)
        self.scores_parser = PydanticOutputParser(pydantic_object=EssayScores)
        
    async def preprocess_essay(self, text: str) -> str:
        prompt = ChatPromptTemplate.from_template(PREPROCESSING_PROMPT)
        chain = prompt | self.llm
        result = await chain.ainvoke({"text": text})
        return result.content.strip()
    
    async def analyze_essay(self, text: str, subject: str) -> EssayResponse:
      # First clean the text
      cleaned_text = await self.preprocess_essay(text)
      
      # Create the format instructions
      format_instructions = f"""
      You must format your output as a JSON object with two main sections: 'scores' and 'feedback'.

      The 'scores' section should contain:
      - competency1: integer (0, 40, 80, 120, 160, or 200)
      - competency2: integer (0, 40, 80, 120, 160, or 200)
      - competency3: integer (0, 40, 80, 120, 160, or 200)
      - competency4: integer (0, 40, 80, 120, 160, or 200)
      - competency5: integer (0, 40, 80, 120, 160, or 200)

      The 'feedback' section should contain for each competency (1-5):
      - score: integer matching the score above
      - justification: string explaining the score and improvement suggestions. be very specific and provide examples on how to improve. for example, if you mention 'However, the argument could be more complex and nuanced.'
      """
      
      # Create the complete prompt
      complete_prompt = f"""
      Analyze the following ENEM essay according to the official evaluation criteria:

      Subject: {{subject}}

      Essay Text:
      {{text}}

      {format_instructions}
      """
      
      prompt = ChatPromptTemplate.from_template(complete_prompt)
      chain = prompt | self.llm
      
      # Get the analysis
      result = await chain.ainvoke({
          "text": cleaned_text,
          "subject": subject
      })
      
      try:
          # Parse the JSON response
          import json
          parsed_json = json.loads(result.content)
          
          # Extract scores and feedback separately
          scores = EssayScores(**parsed_json["scores"])
          feedback = CompetencyFeedback(**parsed_json["feedback"])
          
          # Create the response
          return EssayResponse(
              text=cleaned_text,
              subject=subject,
              scores=scores,
              feedback=feedback
          )
          
      except Exception as e:
          # If parsing fails, provide detailed error
          raise ValueError(f"Failed to parse LLM output: {str(e)}\nOutput was: {result.content}")