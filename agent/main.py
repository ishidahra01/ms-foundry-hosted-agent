# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os

from azure.ai.agentserver.agentframework import from_agent_framework

from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential, DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

"""
Hello Agent — Simplest possible agent

This sample creates a minimal agent using AzureOpenAIResponsesClient via an
Azure AI Foundry project endpoint, and runs it in both non-streaming and streaming modes.

There are XML tags in all of the get started samples, those are used to display the same code in the docs repo.

Environment variables:
  AZURE_AI_PROJECT_ENDPOINT        — Your Azure AI Foundry project endpoint
  AZURE_OPENAI_CHAT_DEPLOYMENT_NAME — Model deployment name (e.g. gpt-4o)
"""


def main() -> None:
    # <create_agent>
    credential = DefaultAzureCredential()
    client = AzureOpenAIResponsesClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        credential=credential,
    )

    agent = client.as_agent(
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )
    hosted_agent = from_agent_framework(agent)
    hosted_agent.run()


if __name__ == "__main__":
    main()