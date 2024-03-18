#!/bin/bash

# Path to the .env file
ENV_FILE=".env"

# Check if .env file exists
if [ -f "$ENV_FILE" ]; then
  # Load environment variables from .env file
  export $(cat $ENV_FILE | xargs)
else
  # Prompt the user for input and create the .env file
  echo "No .env file detected. Let's create one."

  # Prompt for AGENT_NAME
  read -p "Enter your AGENT_NAME (like JamesMiller): " AGENT_NAME
  echo "AGENT_NAME=${AGENT_NAME}" > $ENV_FILE

  # Prompt for OPENAI_API_KEY
  read -p "Enter your OPENAI_API_KEY: " OPENAI_API_KEY
  echo "TICKET_TOKEN=${OPENAI_API_KEY}" >> $ENV_FILE

  # Prompt for COACHING_API_KEY
  read -p "Enter your COACHING_API_KEY : " COACHING_API_KEY
  echo "TICKET_TOKEN=${COACHING_API_KEY}" >> $ENV_FILE

  # Prompt for COACHING_API_KEY
  read -p "Enter your COACHING_API_KEY : " ACADEMIC_API_KEY
  echo "TICKET_TOKEN=${ACADEMIC_API_KEY}" >> $ENV_FILE

  # Export the newly entered variables
  export AGENT_NAME OPENAI_API_KEY COACHING_API_KEY ACADEMIC_API_KEY
fi

# Deploy with SAM using environment variables
sam build
sam deploy --guided --profile=saml --parameter-overrides AgentName=$AGENT_NAME OpenAIKey=$OPENAI_API_KEY CoachingKey=$COACHING_API_KEY AcademicKey=$ACADEMIC_API_KEY