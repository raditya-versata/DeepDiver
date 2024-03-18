# Deploy with SAM using environment variables
sam build
sam deploy --guided --parameter-overrides AgentName=%AGENT_NAME% OpenAIKey=%OPENAI_API_KEY% CoachingKey=%COACHING_API_KEY% AcademicKey=%ACADEMIC_API_KEY%